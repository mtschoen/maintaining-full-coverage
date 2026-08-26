# maintaining-full-coverage - GREEN Phase Results (Round 3: Lint Gate)

Tested: 2026-05-28
Model: claude-sonnet-4-6 (with-skill vs no-skill baseline, same prompt)

These five scenarios pressure the Lint Gate (commit `a4312b9`) and clear the
seven unchecked AUDIT.md sections. Each ran twice: once with the skill loaded,
once with the agent explicitly told to answer from its own judgment without
consulting any skill.

## Scenario 12: "The Project Doesn't Lint" (discovery)

**Baseline:** Strong instinct - read project config as ground truth, ran both
`ruff` and `mypy` before committing, refused to ship on the user-waiting
pressure. Distinguished new vs pre-existing findings. **Gap:** never mentioned
`TEST-REPORT.md` or a Lint section; no structured escalation; gate framing was
ad-hoc ("config files win") rather than a named discipline.

**With skill:** Same correct discovery, plus names the rationalization ("the
project doesn't lint - did you check?") and the red flag ("declaring lint clean
without running"); routes findings through the Escalation Ladder; writes the
`TEST-REPORT.md` Lint block with git hash and commits it alongside the code.

**Verdict: PASS** - skill adds the report artifact and escalation structure on
top of an already-good baseline instinct.

## Scenario 13: "Slow Linter" (run anyway)

**Baseline:** Already excellent - runs `inspectcode`, refuses to skip the
9-minute pass, explicitly rejects both the "note it as a footnote" dodge and
offloading the judgment to the waiting user. Reasoned that Roslyn and
inspectcode check different things.

**With skill:** Same decision, anchored to the verbatim rationalization-table
row ("'Slow' is not a step in the Escalation Ladder") and the skill's own
`AccessToDisposedClosure` example; runs the analyzer immediately, prepares the
report in parallel during the 9 minutes, commits the Lint line after.

**Verdict: PASS** - baseline was strong; skill formalizes the rule and adds the
report. Marginal but aligned.

## Scenario 14: "Pre-existing Lint Debt" (route through ladder)

**Baseline:** Fixes its own 3 findings, verifies the baseline count, updates the
report *honestly* - but treats the 1,244 pre-existing findings as **out of
scope**: opens the PR with the debt remaining (when lint isn't a hard gate),
defers cleanup to a separate PR/issue, and sets the bar at "my code is clean."
Good honesty instinct, but the repo-wide zero bar is not held.

**With skill:** Fixes its 3, then does **not** open the PR - triages all 1,244,
runs `eslint --fix`, routes the remainder through the Escalation Ladder
(restructure → ask human → per-case approved suppression → documented
exception baseline), and opens the PR only at 0 findings or a human-approved
documented baseline. Names the "pre-existing, not my problem" rationalization.

**Verdict: PASS - largest divergence of the round.** This is where the skill
earns its keep: it converts "someone else's debt" into "the first person to run
the gate owns it," with the documented-exception escape valve as the pressure
release.

*Design note for the human:* the skill's stance here is hardline - it requires
clearing or formally baselining all 1,244 before the feature PR merges. The
baseline's "scoped PR + separate cleanup PR + honest disclosure" is a defensible
real-world practice. The skill does permit this via the documented-exception
baseline (escalation step 5), but only with the human in the loop. Worth
confirming this is the intended strictness.

## Scenario 15: "It's Just a Warning" (false positive vs restructure)

**Baseline:** Good restructure instinct - refuses bare `# type: ignore`, prefers
`assert config is not None` / guard / type-narrowing / `cast` as last resort.
**Gaps:** frames the finding as a false positive to "satisfy mypy," not as
*evidence of a real bug*; self-approves the cast/ignore last resort without
asking; no report entry.

**With skill:** Treats the finding as **evidence first** - investigates the
control flow, finds the early-`return` path that genuinely leaves `config`
unset (the "safe in practice" assumption was false), restructures to fix the
real bug; if a suppression were ever needed it requires human approval, uses the
narrow `# type: ignore[union-attr]`, and logs it as a per-case suppression in
`TEST-REPORT.md`. Names both lint rationalizations.

**Verdict: PASS** - the bug-surfacing framing and the human-approval-before-
suppress gate are the concrete adds over a baseline that was already
suppression-averse.

## Scenario 16: "Multi-Language Lint + Report" (all-languages + report section)

**Baseline:** Strong - runs `eslint` on the untouched frontend, adds it to the
Lint block, states the rule "if a linter is configured in the repo, it belongs
in the Lint block." Covers both the all-languages principle and the report
section well.

**With skill:** Same, plus verifies eslint config before running, routes any
pre-existing frontend findings through the ladder, shows the exact Lint-block
format, handles the "not configured → ask the human" branch, and flags that
deferring even a slow linter requires asking (not a unilateral skip). Names the
"all code, all languages" principle.

**Verdict: PASS** - baseline strong on the core; skill adds escalation routing,
the explicit format, and the not-configured branch.

## Coverage Audit Summary

All five scenarios PASS (skill behavior ≥ baseline on every one). The seven
previously-unchecked AUDIT.md lint-gate sections now each have at least one
passing pressure scenario:

| AUDIT section (was unchecked) | Covered by |
|-------------------------------|-----------|
| Lint discovery (config → CI → ask before assuming "no lint") | 12 |
| All-languages verification + zero-findings bar | 14 (zero bar), 16 (all-languages) |
| Slow linters - run anyway; "slow" not in ladder | 13 |
| Pre-existing lint debt → escalation ladder + suppression/exception | 14 |
| Report Lint section required; per-tool listing; suppressions/exceptions counted | 14, 16 |
| 5 new lint rationalization rows | 12 (doesn't lint), 13 (too slow), 14 (pre-existing), 15 (just a warning + false positive) |
| 3 new lint red flags | 12 (skip-without-verify, declare-clean-without-running), 15 (noqa-before-restructure) |

### Cross-scenario pattern: the 2026 baseline is much stronger than Round 1–2

Notably, the no-skill sonnet baseline now handles the *core* lint instincts well
on its own - it discovers configured linters (12), refuses to skip slow ones
(13), prefers restructuring over suppression (15), and runs every language's
linter (16). This is a real shift from the Round 1 baseline (April 2026), where
agents reached for `pragma` before asking and ignored the report file entirely.

The skill's marginal value has correspondingly concentrated. Where it clearly
still moves behavior:

1. **The repo-wide zero-findings bar (14)** - baseline scopes lint to its own
   diff; the skill holds the whole-repo bar and routes pre-existing debt through
   the ladder.
2. **Bug-surfacing framing (15)** - baseline "satisfies the linter"; the skill
   treats the finding as evidence and digs out the real bug.
3. **Human-approval gate before any suppression** - baseline self-approves a
   `cast`/`ignore` as a "last resort"; the skill requires asking.
4. **`TEST-REPORT.md` Lint discipline** - baseline is inconsistent about the
   report; the skill makes the per-tool Lint block a required, committed
   artifact every time.

The discovery/run-the-tool half of the Lint Gate is now partly redundant with
baseline competence; the enforcement/audit-trail half is where the skill earns
its keep. No skill edits indicated by this round - the gate behaves as designed.
