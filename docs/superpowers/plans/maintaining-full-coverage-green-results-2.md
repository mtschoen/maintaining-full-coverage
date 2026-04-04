# maintaining-full-coverage — GREEN Phase Results (Round 2)

Tested: 2026-04-04
Model: claude-sonnet-4-6 (skill loaded)

## Scenario 5: "Documented Exception" (FFI/hardware)

**Baseline:** Restructured code, documented exclusion in comments and PR description. No formal baseline update process, no mention of report file convention.

**With skill:** Explicitly follows escalation ladder step 5. Updates report file immediately with exact file paths, line numbers, rationale, human approval reference, and date. Commits report alongside code. Adjusts CI threshold. Notes the exception should be reversed if hardware testing becomes available.

**Verdict: PASS** — structured exception process with full audit trail.

## Scenario 6: "Elevated/Interactive Testing" (UAC prompts)

**Baseline:** Went straight to exclusion. Said "chasing 100% here would be dishonest." Did not consider interactive testing. No report file mention.

**With skill:** Total reversal. Writes interactive tests with instructional dialogs ahead of UAC prompts. Uses pytest markers (@pytest.mark.interactive) to gate them. Includes interactive suite in coverage run that generates the checked-in report. Updates report immediately. Explicitly refuses pragma because the human hasn't been asked and the heroic path is available.

**Verdict: PASS** — most dramatic improvement across all scenarios.

## Scenario 7: "CI Baseline Regression" (PR review)

**Baseline:** Pushed back and offered to help test. But would "not block the deadline" if author genuinely tried. Suggested targeted pragma as compromise.

**With skill:** Investigates lines before deciding. Attempts to write tests. Rejects baseline update as written — "deadline is not a valid reason to regress coverage." Requires exhausting the full escalation ladder. Would only consider documented exception with team lead approval, and only with per-line justification in the report file. "The PR does not merge with a silent baseline bump."

**Verdict: PASS** — much harder enforcement, no deadline-based escape hatch.

## Coverage Audit Summary

62 rules extracted from SKILL.md by audit agent.

- **55 rules covered** by at least one of 7 pressure scenarios
- **4 rules structural** (not testable by pressure scenarios: CLAUDE.md convention, honor system, skill positioning x2)
- **3 rules untested** (technique examples: browser/integration #34, startup/shutdown #35-36)

**Effective behavioral coverage: 55/58 = 94.8%**

The 3 untested rules are domain-specific technique patterns (how to use Puppeteer, how to test init/teardown) rather than discipline rules. They would require domain-specific scenarios to test.
