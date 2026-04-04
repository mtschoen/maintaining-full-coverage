# maintaining-full-coverage — RED Phase Baseline Results

Tested: 2026-04-04
Model: claude-sonnet-4-6 (no skill loaded)

## Scenario 1: "Close Enough" (98.6%)

**Behavior:** Would read the uncovered code first, then try to write a test. If the code is "genuinely untestable boilerplate," would add `pragma: no cover` with an inline explanation.

**Gaps identified:**
- Jumped to `pragma: no cover` as option B — no "ask the human" step
- Did not consider the code might be unreachable/dead and should be deleted
- No mention of the report file at all
- No structured escalation — ad-hoc judgment

## Scenario 2: "Platform Code" (Linux block on Windows)

**Behavior:** Would mock `platform.system()` and `os.execv()` to test the Linux branch. Would update test-report.txt after confirming coverage.

**Gaps identified:**
- Report file treated as afterthought ("then I would update it")
- No escalation to human if mocking didn't work
- No mention of interactive testing as an option

## Scenario 3: "Pragma Shortcut" (DB error handler)

**Behavior:** Would write the test to mock the database error. Strong instinct against pragma. Would only escalate if the DB layer is "unusually hard to mock."

**Gaps identified:**
- Explicitly said would NOT ask the human first — "takes less time than composing a question"
- Pragma with TODO mentioned as fallback — no structured escalation
- No mention of report file
- No consideration of whether the error handler is even correct/reachable

## Scenario 4: "Batch Testing" (no tests at 80%)

**Behavior:** Would pause implementation to write tests now. Good instinct about not deferring. Would not update report until all tests pass.

**Gaps identified:**
- Report file mentioned but only as "pending regeneration" — not a first-class step
- No mention of branch coverage specifically
- No structured process — just "override the inclination deliberately"

## Cross-Scenario Patterns

### The skill must fix these (consistent failures):

1. **Report file is an afterthought** — no agent treated it as a mandatory, first-class artifact
2. **No escalation to human** — agents prefer autonomy over asking; "ask the human" never appeared as an explicit step
3. **Pragma before asking** — pragma is reached for before human escalation
4. **No escalation ladder** — agents use ad-hoc judgment, not a structured sequence
5. **Dead code not considered** — uncovered code assumed to be live; nobody asked "should this be deleted?"
6. **Branch coverage not mentioned** — no general awareness of covering both sides of conditionals

### Surprisingly good baseline (skill can build on these):

1. Would actually try to write tests first (all 4 scenarios)
2. Would mock platform-specific code rather than skip it
3. Would pause batched coding to write tests when reminded of coverage target
4. Treated 100% as a real target, not aspirational
