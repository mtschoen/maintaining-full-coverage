# maintaining-full-coverage

An agent skill that gates task completion on test coverage and lint cleanliness, with a report file for verification evidence. Written for [Claude Code](https://docs.anthropic.com/en/docs/claude-code) as one example install target, but not specific to it - any agent or model can use this skill.

This skill is part of the completion suite: `maintaining-full-coverage`, `smoke-test`, `docs-update`, `escalate-over-shortcut`, and `wrap`. Suite skills install separately (each lives in its own repo) but are designed to be installed together, and they reference each other directly. Each works standalone; treat cross-references to missing suite members as optional.

## What it does

When loaded, this skill enforces a completion gate on production code:

1. **A Coverage Gate and a Lint Gate, run together.** Every line of production code must be exercised by a test AND be clean against every linter/analyzer the project has configured. No rounding, no "close enough," no checking only one of the two.
2. **Three Modes calibrate what "done" means**, since not every project starts at 100% / 0 findings:
   - **Maintain** - the project is already clean; hold the bar, no regressions allowed.
   - **Close the gap** - reaching 100% coverage and 0 findings IS the task; the same strict bar applies to every uncovered line and every finding.
   - **Best effort** - the project is dirty and the task is a feature, bugfix, or refactor elsewhere. The bar becomes a ratchet: cover and clean what you touch, don't let coverage fall or findings rise versus the prior report, and surface pre-existing debt instead of silently inheriting it.
3. **A required report file** records verification evidence only - status, mode, counts, coverage, lint findings, exclusions; explicit current-task user instructions, then repository policy, decide whether it is tracked, staged, or committed.
4. **A strict escalation ladder** when either gate fails: write tests / fix findings, heroic testing / restructuring, ask the human, framework exclusions (with approval), documented exceptions (last resort).

The skill layers on top of `test-driven-development` (write tests first) and `verification-before-completion` (prove tests pass). This skill closes the loop on the metric.

## Install

Copy `SKILL.md` to your Claude Code skills directory:

```bash
mkdir -p ~/.claude/skills/maintaining-full-coverage
cp SKILL.md ~/.claude/skills/maintaining-full-coverage/SKILL.md
```

The skill will appear in your `/skills` list and trigger automatically when completing work in projects that track coverage.

## Report file format

The skill expects projects to maintain an up-to-date coverage and lint report. Generate or update it for each gate run, then follow explicit current-task user instructions and repository policy for tracking, staging, and commits. The report records verification evidence only - status, mode, counts, coverage, lint findings, exclusions - never a narrative of what was implemented. Minimal format:

```text
myproject test report - 2026-04-04T12:00:00-07:00
===================================================

Status:   PASS
Mode:     maintain
Tests:    365 total
Git:      a4f2c91 (add-webhook-support)
Coverage: 1203/1203 statements (100%)
          0 lines uncovered
          1 exclusion annotation
Lint:     eslint: 0 findings (0 errors, 0 warnings)
          0 per-case suppressions
          0 documented exceptions
```

Projects declare the command that generates this file and its location in their `AGENTS.md`.

## The escalation ladder

When coverage is below 100% or a linter has findings:

1. **Write tests / fix findings** -- most uncovered lines and findings are straightforwardly resolvable
2. **Heroic testing / restructuring** -- mock OS calls, simulate errors, interactive tests for UAC prompts; restructure code so an analyzer's premise no longer holds
3. **Ask the human** -- they may know a trick, or the code is dead and should be deleted
4. **Framework exclusions** -- `pragma: no cover`, `istanbul ignore`, `[SuppressMessage]` -- only with human approval
5. **Documented exceptions** -- absolute last resort, becomes the new baseline

## How it was tested

This skill was developed using the [TDD-for-skills](https://github.com/anthropics/superpowers) methodology: write pressure scenarios, observe baseline agent behavior without the skill, write the skill to fix the gaps, verify compliance.

**10 pressure scenarios** covering:

| Scenario | Tests |
|----------|-------|
| Close Enough (98.6%) | Escalation order, dead code awareness |
| Platform Code (Linux on Windows) | OS mocking, report as first-class artifact |
| Pragma Shortcut (DB error) | Error path simulation, pragma discipline |
| Batch Testing (no tests at 80%) | Development nudge, branch awareness |
| Documented Exception (FFI) | Baseline update, CI adjustment |
| Elevated/Interactive (UAC) | Interactive tests with instructional dialogs |
| CI Baseline Regression (PR review) | CI rejection policy, deadline pressure |
| Browser/Integration (SPA) | Puppeteer, UI audit scripts, multi-suite report |
| Startup/Shutdown (daemon) | Mock init deps, trigger teardown explicitly |
| Hollow Coverage (code review) | Tests that cover without testing behavior |

**15/15 skill sections covered** by at least one scenario. See [AUDIT.md](AUDIT.md) for the full coverage matrix.

All RED-GREEN comparisons are in `docs/evidence/`.

## Repo structure

```text
SKILL.md                -- the skill (copy this to install)
AUDIT.md                -- skill coverage audit (15/15 sections)
docs/evidence/          -- pressure scenarios, baseline and GREEN-phase results
```

## License

MIT
