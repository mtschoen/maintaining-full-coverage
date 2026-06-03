# smoke-test

A Claude Code skill that makes the agent run a smoke test after every change, before declaring work complete — so the user is never the first person to discover that a change doesn't work.

## When it fires

Before saying "done", "complete", "finished", "all set", or "ready to commit" — every time you finish implementing a feature, fixing a bug, refactoring, or changing configuration. The only exception is changes with no runtime effect (comments, docs, .gitignore).

## What it does

Answers two questions in order: (1) does it build and run? (the floor) and (2) does it do what was asked? (the bar). The skill body gives the right smoke test per project type — compiled, web frontend/backend, Unity, scripts/CLI, config, and test-only changes — plus a fix-and-retry sequence and a "report with evidence" close.

## Project-advertised smoke tests (SMOKE.md)

A project can ship a `SMOKE.md` in its root describing exactly how to smoke test it — the floor command, the bar command that exercises real behavior, plus any setup and cleanup. When present, it's authoritative: the agent follows it instead of guessing from the project type. Run `smoke-test --init` in a project to have the agent inspect it and author a `SMOKE.md` from a template.

The authoritative spec is [`SKILL.md`](SKILL.md).

**Repo:** <https://github.com/mtschoen/skills-smoke-test>
