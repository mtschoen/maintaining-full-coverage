# Completion discipline

Five skills that decide when an agent is allowed to say "done".

Coding agents are systematically overconfident about completion. They report
success from the absence of an error rather than the presence of evidence, they
declare a feature finished without running it, and they quietly lower a bar
rather than clear it. None of that is a knowledge gap: the agent usually knows
what it should have checked. It just stopped one step early, because stopping
felt like finishing.

These skills are the gates that make it stop later. Each one fires at the same
moment - the point where the agent is about to claim work is complete - and
each asks a different question that has to be answered before the claim is
allowed.

| Skill | The question it forces |
| --- | --- |
| [`smoke-test`](smoke-test/) | Did you actually run it? |
| [`maintaining-full-coverage`](maintaining-full-coverage/) | Did the coverage and lint bars hold, or did you move them? |
| [`docs-update`](docs-update/) | Did this change make any documentation lie? |
| [`escalate-over-shortcut`](escalate-over-shortcut/) | Is this a solution, or a suppression of the problem? |
| [`wrap`](wrap/) | Is the session actually closed out, or just abandoned? |

They compose deliberately. `smoke-test` proves the change runs,
`maintaining-full-coverage` proves it did not cost quality elsewhere,
`docs-update` catches the prose the change invalidated,
`escalate-over-shortcut` catches the case where the agent's own draft is a
dressed-up workaround, and `wrap` closes the session so nothing is left
stranded on an unpushed branch.

Most invocations end with nothing to report. That is the healthy case. The
value is the check, not the finding.

## Design notes

**Gates, not advice.** Each skill defines a concrete condition and a concrete
verification command, because a gate that can be satisfied by an agent's own
judgement is not a gate.

**No silent lowering.** Every one of these treats moving the bar as the failure
mode rather than the remedy. A red result is a worklist, not a verdict on
whether the bar was right.

**Portable.** These name actions, not tools. Where a specific tool would make a
step easier the agent will find it at runtime; the written instruction stays
tool-agnostic so the skill works on a machine that has none of it.

## Installing

These skills are distributed through the
[skills-dev](https://github.com/mtschoen/skills-dev) umbrella, which carries
the installer and can mirror them into Claude Code, Codex, opencode,
Antigravity, and Hermes. Each skill directory here is self-contained: `SKILL.md`
at its root plus optional `references/`, `scripts/`, and `assets/`.

## Related families

- [skills-working-method](https://github.com/mtschoen/skills-working-method) -
  habits applied while the work is happening, rather than gates at the end.
- [skills-orchestration](https://github.com/mtschoen/skills-orchestration) -
  what changes when work outgrows one agent, one machine, or one budget.
