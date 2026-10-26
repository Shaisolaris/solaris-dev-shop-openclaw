#!/usr/bin/env python3
"""Normal OpenClaw installation and refusal recovery in a new private profile.

Answers only the exact first-party local-source prompt once. Security-policy
warnings and other prompts receive no automatic answer. No force flags.
"""
import argparse
import errno
import json
import os
from pathlib import Path
import pty
import select
import subprocess
import sys
import time

CORE = 'c7c9b395795f488dd3c48122ff916970438b67e6'

def inventory(root):
    result = {}
    for path in root.rglob('*'):
        if path.is_symlink():
            raise ValueError('Symlink in product tree')
        if path.is_file():
            result[path.relative_to(root).as_posix()] = (path.read_bytes(),bool(path.stat().st_mode & 0o111))
    return result

def install(command, work, env):
    master, slave = pty.openpty()
    process = subprocess.Popen(command,stdin=slave,stdout=slave,stderr=slave,cwd=work,env=env)
    os.close(slave)
    output = bytearray()
    answered = False
    prompt = b'Install this non-ClawHub plugin source?'
    deadline = time.monotonic()+180
    try:
        while True:
            if time.monotonic() > deadline:
                raise TimeoutError('Normal source installation did not complete')
            readable,_,_ = select.select([master],[],[],0.2)
            if readable:
                try:
                    chunk = os.read(master,65536)
                except OSError as error:
                    if error.errno == errno.EIO:
                        break
                    raise
                if not chunk:
                    break
                output.extend(chunk)
                if not answered and prompt in output:
                    os.write(master,b'y\n')
                    answered = True
            elif process.poll() is not None:
                break
        assert process.wait(timeout=10) == 0, 'Normal install failed; inspect preserved log'
        assert answered, 'Expected explicit local-source consent was not observed'
        assert output.count(prompt) == 1, 'Unexpected repeated confirmation prompt'
    finally:
        if process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=5)
        os.close(master)
        (work/'install.log').write_bytes(output)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ['node','cli','profile','work']:
        parser.add_argument('--'+name,type=Path,required=True)
    args = parser.parse_args()
    node,cli,profile,work = (getattr(args,name).resolve() for name in ['node','cli','profile','work'])
    expected = inventory(profile)
    assert len(expected) == 1335
    assert json.loads((profile/'SOLARIS-BUILD-SOURCE.json').read_text())['source_commit'] == CORE
    manifest = json.loads((profile/'openclaw.plugin.json').read_text())
    assert manifest['version'] == '0.68.0' and manifest['id'] == 'solaris-dev-shop'
    assert not manifest.get('capabilities')
    work.mkdir(parents=True,exist_ok=False)
    home = work/'home'
    home.mkdir()
    env = {k:os.environ[k] for k in ['PATH','TMPDIR','TEMP','TMP','SSL_CERT_FILE','SSL_CERT_DIR','LANG','LC_ALL'] if k in os.environ}
    env.update(HOME=str(home),OPENCLAW_STATE_DIR=str(work/'state'),
               OPENCLAW_CONFIG_PATH=str(work/'state/openclaw.json'),DO_NOT_TRACK='1',
               PYTHONDONTWRITEBYTECODE='1',NO_COLOR='1')
    for name in ['CONFIG','DATA','CACHE','STATE']:
        env['XDG_'+name+'_HOME'] = str(work/name.lower())
    command = [str(node),str(cli)]
    def run(arguments,label,success=True):
        result = subprocess.run(command+arguments,cwd=work,env=env,capture_output=True,text=True,timeout=60)
        (work/(label+'.stdout')).write_text(result.stdout)
        (work/(label+'.stderr')).write_text(result.stderr)
        assert (result.returncode == 0) is success, label
        return result.stdout
    assert run(['--version'],'version').strip() == '2026.10.5'
    install(command+['plugins','install',str(profile)],work,env)
    run(['plugins','enable','solaris-dev-shop'],'enable')
    installed = work/'state/extensions/solaris-dev-shop'
    assert installed.is_dir() and inventory(installed) == expected, 'Installed files or modes differ'
    assignment = json.loads(run(['solaris','intake','review this code','--json'],'intake'))
    assert assignment['assignment']['primary_capability'] == 'solaris.code-reviewer'
    assert assignment['performed_work'] is False
    skills = json.loads(run(['skills','list','--json'],'skills'))['skills']
    names = {r['name'] for r in json.loads((profile/'native/skills.json').read_text())}
    rows = [r for r in skills if r['name'] in names]
    assert len(rows) == len({r['name'] for r in rows}) == len(names) == 62
    assert all(r['modelVisible'] for r in rows)
    marker = work/'must-not-exist'
    literal = 'review this code; $(touch '+str(marker)+')'
    response = json.loads(run(['solaris','intake',literal,'--json'],'literal'))
    assert response['performed_work'] is False and not marker.exists()
    run(['solaris','intake','x'*32769,'--json'],'oversize',success=False)
    recovered = json.loads(run(['solaris','intake','review this code','--json'],'after-refusal'))
    assert recovered['assignment']['primary_capability'] == 'solaris.code-reviewer' and recovered['performed_work'] is False
    assert inventory(installed) == expected, 'Product files changed during management checks'
    result = {'host':'OpenClaw2026.10.5','version':'0.68.0','sourceCore':CORE,
              'installedFilesAndModes':1335,'actualModelVisibleWorkflows':62,
              'normalSourcePromptAnsweredOnce':True,'forceUsed':False,'capabilityOverrideUsed':False,
              'shellLikeInputRemainedData':True,'oversizeRefused':True,'legitimateUseAfterRefusal':True,
              'modelCommandsIssued':0,'modelUsageMetered':False,'ownerProfileAccess':False,
              'marketplaceAdmission':False,'pass':True}
    (work/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__ == '__main__':
    main()
