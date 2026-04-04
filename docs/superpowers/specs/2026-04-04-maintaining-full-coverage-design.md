# maintaining-full-coverage — Design Spec

## Purpose

A discipline skill that gates task completion on 100% test coverage, with a checked-in report file for regression tracking. This is the final layer in a three-skill stack:

1. `test-driven-development` — writes tests before code
2. `verification-before-completion` — proves tests pass with evidence
3. `maintaining-full-coverage` — proves every line is covered and the report is updated

The skill fires primarily at completion time but also nudges throughout development to prevent batching all test-writing to the end.

## Trigger

Use when completing any feature, bugfix, or refactor in a project that tracks test coverage. Also applies when establishing coverage tracking for the first time — creating the initial report file and baseline. The skill is project-agnostic — it enforces discipline around the coverage number, not specific tooling. Each project declares its own coverage commands and conventions in CLAUDE.md.

## Escalation Ladder

When coverage is below 100%, follow this order strictly. Never skip steps.

1. **Write tests** — the default. Most uncovered lines are straightforwardly testable.
2. **Heroic testing** — mock OS paths, simulate error conditions, use framework features creatively. 100% is almost always achievable.
3. **Ask the human** — if you genuinely cannot figure out how to cover a line, ask. Two likely outcomes:
   - The code is unreachable/dead — delete it
   - The human knows a testing trick you don't — apply it
4. **Framework exclusions** — `# pragma: no cover`, `/* istanbul ignore */`, etc. Only with human approval. These produce a synthetic 100% in the report.
5. **Documented exceptions** — absolute last resort. The report file explicitly lists what's uncovered and why. This becomes the new baseline.

Key discipline: never skip to step 4 or 5 without going through 1-3. The temptation to slap `pragma: no cover` on a tricky line is the primary rationalization this skill must block.

## Report File Convention

Every project maintains a checked-in coverage report file. Minimal required format:

```
<project> test report — <ISO 8601 timestamp>
═══════════════════════════════════════════

Status:   PASS | FAIL
Tests:    <total> total
Git:      <short commit hash> (<branch or commit message>)
Coverage: <covered>/<total> statements (<pct>%)
          <N> lines uncovered
          <N> exclusion annotations
```

Beyond the minimum, projects add whatever is useful — per-suite breakdowns, branch coverage, UI audit stats, timing, etc.

### Report file rules

- Checked into the repo, tracked in git history
- Updated whenever tests or coverage change
- Commit hash ties the report to exact code state — placed above coverage results so it establishes what code the numbers describe
- The project's CLAUDE.md documents the command that generates this file and where it lives
- **With CI:** PRs that regress coverage are rejected unless an exemption is granted, which updates the baseline. Other PRs must then meet that new baseline.
- **Without CI:** honor system, but git history still shows regressions via `git diff` on the report file

## Development Nudge

While developing, periodically ask: "If I ran coverage right now, would the code I just wrote be covered? Did I cover both branches of that `if`?"

This is not a second TDD skill. If TDD is active, it handles test-first discipline. The nudge catches what TDD might miss — code added in templates, config paths, integration glue, or conditional branches that weren't explicitly targeted.

Every `if` has at least two paths. Every `try` has an `except`. Every early `return` has a condition that triggers it. Are they all tested?

## Completion Gate

Before claiming work is done:

1. **Find** the project's coverage command (CLAUDE.md, scripts, etc.)
2. **Run** it — fresh, full, no cache
3. **Read** the output — actual percentage, uncovered lines
4. **Is it 100%?**
   - **Yes** → update the report file, commit it
   - **No** → enter the escalation ladder. Do not claim completion. Do not skip to exclusions.
5. **Only** after the report says 100% (or baseline-approved exceptions): done

### Relationship to other skills

- `verification-before-completion` says "evidence before claims." This skill defines what counts as evidence for coverage specifically. They stack.
- `test-driven-development` ensures tests exist before code. This skill catches what TDD missed. TDD is the upstream discipline; this is the downstream audit.

## Heroic Coverage Scenarios

Concrete patterns demonstrating that 100% is almost always achievable:

### OS/platform-specific code
Mock `platform.system()`, `Path.read_text()` with `PurePosixPath` comparison, `os.execv()`. Test both branches even if you can only run on one OS.

### Error paths requiring external failures
Mock the dependency — database connection errors, network timeouts, file permission denied. The error handler exists because it can happen, so simulate it.

### Elevated/admin-only code paths
Mock the privilege check to test both elevated and non-elevated paths. For things that genuinely cannot be mocked (e.g., UAC prompts), interactive tests are an option: show an instructional dialog ahead of the system prompt ("you should say yes to this one" / "you should say no to the next one") so the human knows what to do.

### Browser/integration coverage
Puppeteer/Playwright tests hitting every route, testing every button handler. UI audit scripts tracking which pages, functions, and handlers are exercised.

### Startup/shutdown code
Test initialization sequences with mocked dependencies. Test cleanup and teardown paths by triggering them explicitly.

### The message
If you think a line is untestable, you are probably wrong. Mock harder, simulate the condition, or ask the human — they may know a trick, or the code might be dead and should be deleted.

## Rationalization Table

| Excuse | Reality |
|--------|---------|
| "That line is unreachable" | Then delete it. Dead code is a bug, not an exception. |
| "It's just error handling" | Error handlers exist because errors happen. Mock the error. |
| "I can't test platform-specific code" | Mock the platform check. Test both branches. |
| "Coverage is 98%, close enough" | 98% means uncovered lines. Find them. Test them. |
| "I'll add tests later" | Later never comes. The gate is now. |
| "This is just config/glue code" | Config can break. Glue can fail. Test it. |
| "The framework makes this untestable" | Ask the human. They may know a trick, or the code should be restructured. |
| "Adding `pragma: no cover` is faster" | Exclusions require human approval. Try testing first. |

## Red Flags

Stop and reconsider if you catch yourself:

- Reaching for `pragma: no cover` before attempting to test the line
- Claiming completion with uncovered lines you haven't investigated
- Assuming code is unreachable without verifying
- Batching all test-writing to the end
- Skipping straight to step 4 or 5 of the escalation ladder
