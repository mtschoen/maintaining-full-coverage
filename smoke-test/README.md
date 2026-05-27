# smoke-test

A Claude Code skill that makes the agent run a smoke test after every change, before declaring work complete — so the user is never the first person to discover that a change doesn't work.

## When it fires

Before saying "done", "complete", "finished", "all set", or "ready to commit" — every time you finish implementing a feature, fixing a bug, refactoring, or changing configuration. The only exception is changes with no runtime effect (comments, docs, .gitignore).

## What it does

Answers two questions in order: (1) does it build and run? (the floor) and (2) does it do what was asked? (the bar). The skill body gives the right smoke test per project type — compiled, web frontend/backend, Unity, scripts/CLI, config, and test-only changes — plus a fix-and-retry sequence and a "report with evidence" close.

The authoritative spec is [`SKILL.md`](SKILL.md).

**Repo:** <https://github.com/mtschoen/skills-smoke-test>
