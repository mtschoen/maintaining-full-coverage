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

## Review correction: neutral policy

The first revision removed the commit requirement by making the opposite rule
unconditional. Four of five fresh agents then excluded `TEST-REPORT.md` despite
explicit main, release, or CI policies requiring it in the commit. One followed
the repository rule, showing that the conflicting guidance also caused
inconsistent behavior.

Verdict: FAIL. Required generation had become required non-commitment.

The neutral revision separates two decisions:

1. Generate or update `TEST-REPORT.md` before completion.
2. Follow explicit current-task user instructions, then repository policy, for
   whether the report is tracked and whether the current update is staged or
   committed.

Five scenarios tested policies requiring the report in the commit, and five
tested policies requiring it left uncommitted. Across three agent contexts, all
ten scenarios followed the explicit policy while keeping report generation
required.

Additional cases verified the distinctions the main scenarios did not cover:

- A current-task user instruction to commit the report overrode a repository's
  usual no-commit feature-branch policy. The absent report was generated,
  tracked, staged, and committed.
- An absent report was generated but left untracked, unstaged, and uncommitted
  when repository policy required that PR behavior.
- An already tracked report stayed tracked while its current modification was
  left unstaged and uncommitted, without untracking the file.

Verdict: PASS. Generation is mandatory; Git disposition is neutral and follows
explicit current-task user and repository policy.
