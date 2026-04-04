# maintaining-full-coverage

A [Claude Code](https://docs.anthropic.com/en/docs/claude-code) skill that gates task completion on 100% test coverage, with a checked-in report file for regression tracking.

## What it does

When loaded, this skill enforces three things:

1. **Coverage must be 100% before you claim done.** No rounding, no "close enough."
2. **A checked-in report file** tracks coverage over time. `git diff test-report.txt` catches regressions instantly.
3. **A strict escalation ladder** when coverage drops: write tests, heroic testing, ask the human, framework exclusions (with approval), documented exceptions (last resort).

The skill layers on top of `test-driven-development` (write tests first) and `verification-before-completion` (prove tests pass). This skill closes the loop on the metric.

## Install

Copy `skill-draft/SKILL.md` to your Claude Code skills directory:

```bash
mkdir -p ~/.claude/skills/maintaining-full-coverage
cp skill-draft/SKILL.md ~/.claude/skills/maintaining-full-coverage/SKILL.md
```

The skill will appear in your `/skills` list and trigger automatically when completing work in projects that track coverage.

## Report file format

The skill expects projects to maintain a checked-in coverage report. Minimal format:

```
myproject test report — 2026-04-04T12:00:00-07:00
═══════════════════════════════════════════════════

Status:   PASS
Tests:    365 total
Git:      a4f2c91 (add-webhook-support)
Coverage: 1203/1203 statements (100%)
          0 lines uncovered
          1 exclusion annotation
```

Projects declare the command that generates this file and its location in their `CLAUDE.md`.

## The escalation ladder

When coverage is below 100%:

1. **Write tests** -- most uncovered lines are straightforwardly testable
2. **Heroic testing** -- mock OS calls, simulate errors, interactive tests for UAC prompts
3. **Ask the human** -- they may know a trick, or the code is dead and should be deleted
4. **Framework exclusions** -- `pragma: no cover`, `istanbul ignore` -- only with human approval
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

All RED-GREEN comparisons are in `docs/superpowers/plans/`.

## Repo structure

```
skill-draft/SKILL.md              -- the skill (copy this to install)
AUDIT.md                           -- skill coverage audit (15/15 sections)
docs/superpowers/
  specs/                           -- design spec
  plans/                           -- implementation plan, pressure scenarios,
                                      baseline results, GREEN phase results
```

## License

MIT
