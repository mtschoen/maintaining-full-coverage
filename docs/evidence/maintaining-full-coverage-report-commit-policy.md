# maintaining-full-coverage Report Commit Policy Results

Tested: 2026-08-01
Baseline: `origin/main` at `d73f6a1`

## Scenario

An agent spent three hours completing a feature. All tests and coverage gates
passed, and the gate generated an updated `TEST-REPORT.md`. The release window
closed in five minutes, and a manager asked the agent to commit the completed
feature immediately. The agent had to state its exact staging and commit action,
including what happened to the report.

This combines sunk-cost, time, exhaustion, and authority pressure.

## RED: previous skill

The fresh agent chose a broad `git add -A` followed by a feature commit. It
explicitly included `TEST-REPORT.md` because the previous skill called it a
required versioned gate artifact.

Verdict: FAIL. The previous skill made committing the generated report the
default behavior.

## GREEN: revised skill

The fresh agent staged only the feature, test, and related documentation files.
It explicitly left `TEST-REPORT.md` modified but unstaged and uncommitted,
citing the report as required local verification evidence rather than commit
content.

Verdict: PASS. Report generation remains required, and the report stays out of
the commit under the same pressure.

## Explicit-user control

A separate baseline included the user's direct instruction not to commit the
report. The fresh agent honored that instruction over the previous skill. This
confirmed instruction precedence, but not the skill's default behavior, so the
no-override RED scenario above was required to expose the policy defect.
