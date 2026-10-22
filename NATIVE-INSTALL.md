# Native installation and validation

This is the complete Solaris Dev Shop native source plugin for OpenClaw2026.10.5:61 specialist workflows plus a chief-of-staff coordinator, with actual deterministic intake through the native CLI.

```sh
openclaw plugins install git:github.com/Shaisolaris/solaris-dev-shop-openclaw@4c74fbeb48f7356af8bf510918bb0684cb4b9c31
openclaw plugins enable solaris-dev-shop
openclaw solaris intake 'review this code' --json
```

Review the source and declared skill/CLI surfaces in OpenClaw's normal install prompt. Python3.10+ must be available as `python3` onPATH. Intake returns a bounded assignment and does not execute specialist work. The native adapter uses argument separation, no shell, a32KiB input cap,20second timeout and a minimal child environment. There are no MCP servers, hooks, schedules, credential sources or model calls. Host permissions and role prerequisites apply.

The immutable source is [reviewed distributionc69fbcf](https://github.com/Shaisolaris/solaris-dev-shop-plugins/commit/c69fbcf49e46da3837fcf75420b9914705b2eab7), profile `harnesses/openclaw`. All1196 canonical files are preserved. Both independent source review and [exact-revision Linux CI](https://github.com/Shaisolaris/solaris-dev-shop-plugins/actions/runs/39783696949) pass, including actual OpenClaw install, command invocation and62 visible skills; separate macOS native checks cover shell-text/option-like-input handling, oversized refusal and complete installed source/modes. These checks are not a claim of vulnerability-free code or model quality.

This Git distribution is public. ClawHub registry publication/review is separate and remains pending publisher authentication. No version was bumped for this distribution work; existing tags/releases are preserved. MIT licensed. Solaris Technologies, https://solaristek.com.
