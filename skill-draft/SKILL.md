---
name: maintaining-full-coverage
description: "Use when: user mentions coverage, 100% coverage, coverage gate, test report, or TEST-REPORT.md; BEFORE declaring work done, summarizing what you built, or saying 'all passing/working/done'; BEFORE committing or pushing; completing any feature/bugfix/refactor in a project that tracks test coverage; establishing coverage tracking for a new project. If you wrote or changed production code, this skill applies — no exceptions."
---

# Maintaining Full Coverage

## Overview

If the coverage report doesn't say 100%, you're not done.

**Core principle:** Every line of production code must be exercised by a test. Uncovered lines are either untested (write a test) or unreachable (delete them).

**This means ALL code, in ALL languages, in the ENTIRE repo.** A C# project with a C++ native library needs 100% coverage in both C# and C++. A Python backend with a JavaScript frontend needs 100% coverage in both Python and JavaScript. If production code exists in the repo and it's in a language you can compile/run, it needs coverage tooling and tests. No language gets a pass.

**Violating the letter of this rule is violating the spirit of this rule.**

This skill is the final layer in a three-skill stack:
1. `test-driven-development` — writes tests before code
2. `verification-before-completion` — proves tests pass with evidence
3. `maintaining-full-coverage` — proves every line is covered and the report is updated

TDD is upstream discipline. Verification is evidence. This skill is the metric gate.

## When to Use

**Before you declare anything "done":**
- You wrote or changed production code → this skill applies
- You're about to say "all passing", "here's what changed", or summarize your work → STOP, run coverage first
- You're about to commit or push → STOP, run coverage first
- User asks you to commit → this is a completion event, run coverage before the commit

**Always:**
- Completing a feature, bugfix, or refactor
- Setting up coverage tracking for a new project
- Reviewing whether work is ready to commit

**The test you wrote passing is not the finish line. 100% suite-wide coverage is the finish line.**

**Throughout development (the nudge):**
While coding, periodically ask yourself: "If I ran coverage right now, would the code I just wrote be covered?" Every `if` has at least two paths. Every `try` has an `except`. Every early `return` has a condition that triggers it. Are both branches tested?

Don't batch all test-writing to the end. Write tests alongside code. Coverage debt compounds.

## The Completion Gate

```
BEFORE claiming completion:

1. FIND the repo's coverage command. Check in this order:
   a. CLAUDE.md — look for a documented coverage command
   b. Scripts directory — look for run-coverage, coverage, or test scripts
      (e.g., scripts/run-coverage.ps1, scripts/coverage.sh)
   c. CI config — .github/workflows, Makefile, etc.
   d. If none found, construct one that covers ALL test projects in the repo
      (not just one — search for all *.csproj with test references,
       all test directories, etc.)
   IMPORTANT: Coverage must include the ENTIRE repo, not a single project.
2. VERIFY the command covers all production code IN EVERY LANGUAGE.
   Do NOT trust CLAUDE.md or existing scripts blindly — they may be incomplete.
   a. Scan the repo for ALL production code across ALL languages
      (e.g., *.cs, *.cpp, *.h, *.js, *.ts, *.py, *.go, *.rs, etc.)
   b. For EACH language with production code, identify the coverage tool
      (e.g., dotnet-coverage for C#, gcov/llvm-cov for C++, istanbul/c8
      for JS/TS, coverage.py for Python, go cover for Go)
   c. Check which assemblies/packages/modules the coverage commands
      actually instrument
   d. If any production code in any language is excluded, fix it before running
   Example: a repo has C# managed code and a C++ native library — you need
   BOTH dotnet-coverage AND gcov/llvm-cov. One coverage tool is not enough.
   Example: a repo has a Python API and a React frontend — you need BOTH
   coverage.py AND istanbul/c8. The frontend JS is not optional.
3. RUN it — fresh, full, no cache
4. READ the output — actual percentage, uncovered lines
5. Is it 100%?
   - YES → continue to step 6
   - NO  → enter the Escalation Ladder below
           Do NOT claim completion. Do NOT skip to exclusions.
6. WRITE or UPDATE `TEST-REPORT.md` at the repo root
   - Use the format from the Report File Convention section
   - Include the current git hash, test count, and coverage numbers
   - This file is a REQUIRED artifact — do not skip this step
7. COMMIT `TEST-REPORT.md` alongside your other changes
8. ONLY after the report file is written and committed: done
```

The report file is a first-class artifact. It is not an afterthought. Write it and commit it as part of your work, not as a cleanup step later.

## The Escalation Ladder

When coverage is below 100%, follow this order. **Never skip steps.**

```dot
digraph escalation {
    "Coverage < 100%" [shape=diamond];
    "1. Write tests" [shape=box];
    "Covered?" [shape=diamond];
    "2. Heroic testing\n(mock, simulate, get creative)" [shape=box];
    "Covered now?" [shape=diamond];
    "3. Ask the human\n(may reveal dead code to delete)" [shape=box];
    "Human says testable?" [shape=diamond];
    "Apply human's approach" [shape=box];
    "Delete dead code" [shape=box];
    "4. Framework exclusions\n(pragma, istanbul-ignore)\nONLY with human approval" [shape=box];
    "5. Documented exceptions\n(update report baseline)\nAbsolute last resort" [shape=box];
    "Update report file → done" [shape=doublecircle];

    "Coverage < 100%" -> "1. Write tests";
    "1. Write tests" -> "Covered?";
    "Covered?" -> "Update report file → done" [label="yes"];
    "Covered?" -> "2. Heroic testing\n(mock, simulate, get creative)" [label="no"];
    "2. Heroic testing\n(mock, simulate, get creative)" -> "Covered now?";
    "Covered now?" -> "Update report file → done" [label="yes"];
    "Covered now?" -> "3. Ask the human\n(may reveal dead code to delete)" [label="no"];
    "3. Ask the human\n(may reveal dead code to delete)" -> "Human says testable?";
    "Human says testable?" -> "Apply human's approach" [label="yes, here's how"];
    "Human says testable?" -> "Delete dead code" [label="it's dead code"];
    "Human says testable?" -> "4. Framework exclusions\n(pragma, istanbul-ignore)\nONLY with human approval" [label="exclude it"];
    "Apply human's approach" -> "Update report file → done";
    "Delete dead code" -> "Update report file → done";
    "4. Framework exclusions\n(pragma, istanbul-ignore)\nONLY with human approval" -> "Update report file → done";
    "Human says testable?" -> "5. Documented exceptions\n(update report baseline)\nAbsolute last resort" [label="can't exclude either"];
    "5. Documented exceptions\n(update report baseline)\nAbsolute last resort" -> "Update report file → done";
}
```

**Step 1 — Write tests.** Most uncovered lines are straightforwardly testable. Just write the test.

**Step 2 — Heroic testing.** Mock OS calls, simulate errors, use framework features creatively. See Heroic Coverage Scenarios below. 100% is almost always achievable.

**Step 3 — Ask the human.** If you genuinely cannot figure out how to cover a line, ask. Do not guess. Do not skip this step. Two likely outcomes:
- The code is unreachable/dead → **delete it.** Dead code is a bug, not an exception.
- The human knows a testing trick you don't → apply it.

**Step 4 — Framework exclusions.** `# pragma: no cover`, `/* istanbul ignore */`, etc. **Only with explicit human approval.** These produce a synthetic 100% in the report. Never apply these silently.

**Step 5 — Documented exceptions.** Absolute last resort. The report file explicitly lists what's uncovered and why. This becomes the new baseline that other work must meet.

## Report File Convention

Every project maintains a checked-in coverage report at the **repo root** named `TEST-REPORT.md`. If a project already has a report file under a different name, use that. Otherwise, create `TEST-REPORT.md`.

### Creating or updating the report

After running coverage, **you must** write or overwrite `TEST-REPORT.md` with the results. This is not optional — it is a required artifact of every coverage run.

1. Get the current git short hash: `git rev-parse --short HEAD`
2. Get the total test count from the test runner output
3. Get line/branch/method coverage from the coverage tool output
4. Write `TEST-REPORT.md` at the repo root using the format below
5. Stage and commit it alongside your other changes

### Minimal required format

```
<project> test report — <ISO 8601 timestamp>
═══════════════════════════════════════════

Status:   PASS | FAIL
Tests:    <total> total
Git:      <short hash> (<branch or commit message>)
Coverage: <covered>/<total> statements (<pct>%)
          <N> lines uncovered
          <N> exclusion annotations
```

Beyond the minimum, projects add whatever is useful — per-suite breakdowns, branch coverage, UI audit stats, timing.

### Report file rules

- **Lives at repo root as `TEST-REPORT.md`** unless the project already has a report file elsewhere.
- **Checked into the repo.** Tracked in git history. `git diff` on the report instantly shows regressions.
- **Updated whenever tests or coverage change.** Not "later" — now, as part of the work.
- **Git hash above coverage results.** It establishes what code the numbers describe.
- **CLAUDE.md documents the coverage command** and references `TEST-REPORT.md`.
- **With CI:** PRs that regress coverage are rejected unless an exemption grants a new baseline.
- **Without CI:** Honor system, but git history still catches regressions.

## Heroic Coverage Scenarios

100% is almost always achievable. These patterns prove it.

### OS/platform-specific code
Mock `platform.system()`, `Path.read_text()` with `PurePosixPath` comparison, `os.execv()`. Test both branches even on one OS.

### Error paths requiring external failures
Mock the dependency — database errors, network timeouts, permission denied. The error handler exists because it can happen. Simulate it.

### Elevated/admin-only code paths
Mock the privilege check to test both paths. For things that genuinely cannot be mocked (e.g., UAC prompts), interactive tests are an option: show an instructional dialog ahead of the system prompt ("you should say yes to this one" / "you should say no to the next one") so the human knows what to do during the test run.

### Browser/integration coverage
Puppeteer/Playwright tests hitting every route and handler. UI audit scripts tracking which pages, functions, and handlers are exercised.

### Startup/shutdown code
Test initialization with mocked dependencies. Trigger cleanup/teardown paths explicitly.

### The bottom line
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
| "Asking the human takes longer than just fixing it" | If you can fix it, fix it. If you can't, ask. Don't reach for pragma instead of asking. |
| "I'll update the report file after" | The report is a first-class artifact. Update it now, commit it with your changes. |
| "Both branches do the same thing, testing one is enough" | The coverage tool disagrees. Test both. |
| "The C++/JS/other-language code is a separate concern" | If it's in the repo and it's production code, it needs 100% coverage. Set up the coverage tool for that language. |
| "I got 100% on the C# / Python / main language" | That's 100% of ONE language. Check ALL languages in the repo. Every language needs its own coverage tooling. |

## Red Flags — STOP and Reconsider

- Reaching for `pragma: no cover` before attempting to test the line
- Reaching for `pragma: no cover` before asking the human
- Claiming completion with uncovered lines you haven't investigated
- Assuming code is unreachable without verifying (it might be dead — delete it)
- Batching all test-writing to the end
- Treating `TEST-REPORT.md` as optional or "I'll do it later"
- Claiming completion without writing or updating `TEST-REPORT.md`
- Skipping straight to step 4 or 5 of the escalation ladder
- Writing tests that cover the line but don't test meaningful behavior
- Forgetting to test both branches of a conditional
- Declaring 100% coverage when you only checked one language in a multi-language repo
- Ignoring C++, JavaScript, or other secondary languages because the "main" language has full coverage
