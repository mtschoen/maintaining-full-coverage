# maintaining-full-coverage — GREEN Phase Results

Tested: 2026-04-04
Model: claude-sonnet-4-6 (skill loaded)

## Scenario 1: "Close Enough" (98.6%)

**Baseline:** Would try to test, but pragma was option B. No human escalation. No report file mention.

**With skill:** Follows escalation ladder explicitly — writes test first, if block is unreachable asks the human (not pragma). Notes that pragma requires human approval. States "if the report does not say 100%, I am not done." Report file mentioned as part of completion.

**Verdict: PASS** — all baseline gaps addressed.

## Scenario 2: "Platform Code"

**Baseline:** Would mock platform check (good). Report file treated as afterthought. No human escalation path.

**With skill:** Mocks `platform.system()` and `os.execv()`. Explicitly references the Rationalization Table entry about platform-specific code. Updates test-report.txt "immediately — not later, not as a follow-up." Report committed alongside bugfix and test.

**Verdict: PASS** — report file elevated from afterthought to first-class.

## Scenario 3: "Pragma Shortcut"

**Baseline:** Would write the test (good), but explicitly said would NOT ask human. Pragma with TODO as fallback.

**With skill:** Writes the test. "The pragma path is off the table" — explicitly references that exclusions require human approval and the escalation ladder hasn't been exhausted. Report updated as part of the same change.

**Verdict: PASS** — pragma blocked, human escalation path acknowledged.

## Scenario 4: "Batch Testing"

**Baseline:** Would pause to write tests (good). Report file mentioned but as "pending regeneration."

**With skill:** Stops coding immediately. Writes tests branch-by-branch — "each if/else, every try/except, every early return." Report file is "not paperwork after the real work — it is the proof that the work is actually done." Updated and committed together with tests.

**Verdict: PASS** — branch awareness added, report file elevated.

## Summary

All 4 baseline gaps were addressed by the skill:

1. **Escalation ladder followed in order** — no skipping to pragma
2. **Report file treated as first-class** — committed alongside changes, not deferred
3. **Human escalation acknowledged** — before pragma, not instead of it
4. **Dead code awareness** — agents consider deletion as an option
5. **Branch coverage awareness** — both sides of conditionals mentioned

**No new rationalizations or loopholes identified.** The skill is effective as written.
