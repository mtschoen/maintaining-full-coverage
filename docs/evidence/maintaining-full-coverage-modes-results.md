# maintaining-full-coverage — Three-Modes Softening Results

Tested: 2026-05-28
Model: claude-sonnet-4-6
Baseline: **old skill** (pre-modes, git HEAD `a4312b9`) vs **new skill** (Three
Modes added). This is an improvement iteration, so the baseline is the previous
skill version, not no-skill.

## Why this change

Round-3 Scenario 14 surfaced a hardline stance: the skill demanded a dirty
project reach 100% / 0 findings (or a fully documented-exception baseline)
before an *unrelated* feature could be declared done. That blocks ordinary
feature work on inherited debt. The fix introduces three modes — **maintain**
(project already clean → hold the absolute bar), **close-the-gap** (reaching the
bar IS the task → insist on 100%), and **best-effort** (dirty project, unrelated
task → ratchet: cover what you touch, don't regress the baseline, surface the
debt). When the mode is ambiguous, ask.

## Scenario 14: Pre-existing eslint debt (now a best-effort case)

**Old skill:** Hardline. "Either I clear the debt, or I document it explicitly
with human buy-in — those are the only two paths to 'done.'" Refuses a PASS
while 1,244 inherited findings exist; routes all of them through the escalation
ladder. The 30-line feature is blocked on repo-wide cleanup.

**New skill:** Identifies Best-Effort mode. Fixes its own 3 findings, confirms
the count held at 1,244 (`+0`), writes `Mode: best-effort`, `Status: PASS`,
`Lint: eslint 1244 findings (pre-existing baseline, +0 this change)`, surfaces
the debt and suggests a cleanup task. Ships the feature without forcing repo
cleanup — while refusing to add debt or falsify the report.

**Verdict: SOFTENED correctly** — the headline change. Unrelated work is no
longer hostage to inherited debt.

## Scenario 17: Best-effort on a dirty Python project (new)

**Old skill:** "I do not declare done... 100% is the finish line." Works the
escalation ladder through all 22% uncovered lines AND all 1,244 ruff findings.
Explicitly: "The scope grew beyond what the user asked for. That is correct and
expected." A 40-line endpoint drags in whole-repo cleanup.

**New skill:** Best-Effort mode. New code covered + clean, baseline held, report
`Mode: best-effort` / `Status: PASS`, surfaces debt, offers a cleanup task.
Explicitly refuses to fix the 1,244 / the 22% as a side effect ("scope creep").

**Verdict: SOFTENED correctly** — clean separation of "my code" from "inherited
debt," with the ratchet (no regression, cover-what-you-touch) intact.

## Scenario 18: Ambiguous mode (new)

**Old skill:** Impressively still asks a disambiguating question on its own — but
frames both branches around the hardline bar ("I do not declare done at 82%
overall and call it 'close enough'"), so even after asking it leans strict.

**New skill:** "Step 0: Resolve the ambiguity before touching anything," citing
the skill's explicit "when mode is ambiguous, ask" rule. Names mode 2 vs mode 3,
asks one question, then applies the correct bar — best-effort holds the baseline
and does not clear inherited debt; close-the-gap insists on 100%. Records the
chosen mode in the report.

**Verdict: IMPROVED** — both ask (good latent instinct); the skill adds the
principled framework and the right post-disambiguation bar.

## Net assessment

The softening lands exactly as intended and introduces no new failure mode:

- **Best-effort no longer blocks unrelated work** on repo-wide debt (14, 17).
- **The ratchet still bites:** every new-skill run fixed its own findings,
  refused to let the count grow, and refused to write a false `0 findings` /
  `PASS`. Best-effort is a floor, not a free pass.
- **Maintain / close-the-gap keep the strict bar** — the round-1/2 strict
  scenarios (1–11) are unchanged maintain-mode cases and still hold.
- **Ambiguity routes to a question**, not a silent default in either direction.

No further skill edits indicated by this iteration. The report file now carries
a `Mode:` line so the baseline a number was measured against travels with it.
