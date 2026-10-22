# Native installation and validation

This is the complete Solaris Dev Shop native source plugin for OpenClaw2026.10.5:61 specialist workflows plus a chief-of-staff coordinator, with actual deterministic intake through the native CLI.

```sh
openclaw plugins install git:github.com/Shaisolaris/solaris-dev-shop-openclaw@841f59856d69f2196b35fe92e81a0be238ff8809
openclaw plugins enable solaris-dev-shop
openclaw solaris intake 'review this code' --json
```

Review the source and declared skill/CLI surfaces in OpenClaw's normal install prompt. Python3.10+ must be available as `python3` onPATH. Intake returns a bounded assignment and does not execute specialist work. The native adapter uses argument separation, no shell, a32KiB input cap,20second timeout and a minimal child environment. There are no MCP servers, hooks, schedules, credential sources or model calls. Host permissions and role prerequisites apply.

The immutable source is [reviewed distribution0dcda581](https://github.com/Shaisolaris/solaris-dev-shop-plugins/commit/0dcda5817286dcca4abd911a6d2b2292a17715cc), profile `harnesses/openclaw`. All1196 canonical files are preserved. Both independent source review and [exact-revision Linux CI](https://github.com/Shaisolaris/solaris-dev-shop-plugins/actions/runs/39783696949) pass, including actual OpenClaw install, command invocation and62 visible skills; separate macOS native checks cover shell-text/option-like-input handling, oversized refusal and complete installed source/modes. These checks are not a claim of vulnerability-free code or model quality.

This Git distribution is public. ClawHub registry publication/review is separate and remains pending publisher authentication. No version was bumped for this distribution work; existing tags/releases are preserved. MIT licensed. Solaris Technologies, https://solaristek.com.
