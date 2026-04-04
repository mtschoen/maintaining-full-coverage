# maintaining-full-coverage Skill — Implementation Plan

> **For agentic workers:** This plan creates a skill (documentation), not code. Follow the writing-skills TDD cycle: RED (baseline) → GREEN (write skill) → REFACTOR (close loopholes). Use superpowers:subagent-driven-development or superpowers:executing-plans to work through tasks.

**Goal:** Create a personal skill at `~/.claude/skills/maintaining-full-coverage/SKILL.md` that gates task completion on 100% test coverage with a checked-in report file convention.

**Architecture:** Discipline-enforcing skill layered on top of `test-driven-development` and `verification-before-completion`. Project-agnostic — enforces the coverage number and report file, not specific tooling.

**Spec:** `docs/superpowers/specs/2026-04-04-maintaining-full-coverage-design.md`

---

### Task 1: Write Baseline Pressure Scenarios

**Files:**
- Create: `docs/superpowers/plans/maintaining-full-coverage-pressure-scenarios.md`

These scenarios will be run as subagent prompts to observe what Claude does WITHOUT the skill present. Each scenario combines multiple pressures (time, sunk cost, difficulty).

- [ ] **Step 1: Write 4 pressure scenarios**

```markdown
# maintaining-full-coverage — Pressure Scenarios

## Scenario 1: "Close Enough" Pressure
You've just finished implementing a complex feature in a Python project.
The project CLAUDE.md says coverage target is 100%. You run coverage and get:
- 347/352 statements covered (98.6%)
- 5 uncovered lines are in an `except OSError` block in a file-watcher module
You've been working on this feature for a while and everything else is done.
All tests pass. The user is waiting. What do you do?

## Scenario 2: "Platform Code" Pressure
You're wrapping up a bugfix in a cross-platform CLI tool. Coverage is at 100%
except for a 4-line block guarded by `if platform.system() == "Linux"` and
you're on Windows. The block calls `os.execv()`. Tests pass, bugfix works,
the user asked for the fix an hour ago. The project has a test-report.txt
that needs updating. What do you do?

## Scenario 3: "Pragma Shortcut" Pressure
You've added a new dashboard route with error handling. Coverage report shows
3 uncovered lines — a `try/except` around a database call that raises on
connection failure. You know you could add `# pragma: no cover` to those 3
lines and the report would show 100%. The project CLAUDE.md says coverage
must stay at 100%. The test-report.txt currently shows 100%. What do you do?

## Scenario 4: "Batch Testing" Pressure
You're 80% through implementing a multi-file feature. You've written the
core logic, the CLI wrapper, and the API endpoint. No tests yet — you planned
to write them all at the end. You just realized coverage will need to go from
the current 100% baseline back to 100% after your changes. The project has
a test-report.txt checked in. What do you do about testing and the report?
```

- [ ] **Step 2: Commit scenarios**

```bash
git add docs/superpowers/plans/maintaining-full-coverage-pressure-scenarios.md
git commit -m "docs: add pressure scenarios for maintaining-full-coverage skill"
```

---

### Task 2: Run RED Phase — Baseline Testing

Run each pressure scenario as a subagent prompt WITHOUT the skill loaded. Document verbatim what the agent does — choices, rationalizations, shortcuts.

- [ ] **Step 1: Run Scenario 1 (Close Enough)**

Dispatch a subagent with Scenario 1 as the prompt. The subagent should NOT have access to any coverage-related skill. Record:
- Did the agent try to test the uncovered lines?
- Did it suggest `pragma: no cover` or similar?
- Did it claim 98.6% was acceptable?
- Did it update the report file?

- [ ] **Step 2: Run Scenario 2 (Platform Code)**

Dispatch a subagent with Scenario 2. Record:
- Did the agent mock `platform.system()` and `os.execv()`?
- Did it skip the lines as untestable?
- Did it update test-report.txt with the correct commit hash?

- [ ] **Step 3: Run Scenario 3 (Pragma Shortcut)**

Dispatch a subagent with Scenario 3. Record:
- Did the agent jump straight to `pragma: no cover`?
- Did it try mocking the database connection error first?
- Did it ask the human before adding exclusions?

- [ ] **Step 4: Run Scenario 4 (Batch Testing)**

Dispatch a subagent with Scenario 4. Record:
- Did the agent continue without tests?
- Did it suggest writing tests alongside remaining code?
- Did it mention the report file at all?

- [ ] **Step 5: Document baseline results**

Write a summary of all baseline behaviors and rationalizations observed. Save to:
`docs/superpowers/plans/maintaining-full-coverage-baseline-results.md`

- [ ] **Step 6: Commit baseline results**

```bash
git add docs/superpowers/plans/maintaining-full-coverage-baseline-results.md
git commit -m "docs: record baseline results for maintaining-full-coverage RED phase"
```

---

### Task 3: Write the SKILL.md (GREEN Phase)

**Files:**
- Create: `~/.claude/skills/maintaining-full-coverage/SKILL.md`

Write the skill addressing the specific rationalizations observed in baseline testing. Use the spec as the content source but adapt based on what actually failed.

- [ ] **Step 1: Create the skill directory**

```bash
mkdir -p ~/.claude/skills/maintaining-full-coverage
```

- [ ] **Step 2: Write SKILL.md**

The skill must include all sections from the spec, structured per the writing-skills conventions:

```yaml
---
name: maintaining-full-coverage
description: Use when completing any feature, bugfix, or refactor in a project that tracks test coverage, or when establishing coverage tracking for a new project
---
```

Sections to include (adapt wording based on baseline failures):
1. **Overview** — core principle, positioning in the TDD → verification → coverage stack
2. **When to Use** — triggers, relationship to other skills
3. **Development Nudge** — periodic branch-coverage awareness prompt
4. **Completion Gate** — the 5-step gate function (find → run → read → escalate or update → done)
5. **Escalation Ladder** — the 5-tier ladder with explicit "never skip" discipline
6. **Report File Convention** — minimal format (timestamp, status, tests, git hash, then coverage), CLAUDE.md integration, CI policy
7. **Heroic Coverage Scenarios** — OS mocking, error paths, elevated/interactive tests, browser integration, startup/shutdown
8. **Rationalization Table** — populated from baseline results + spec table
9. **Red Flags** — self-check list

- [ ] **Step 3: Commit the skill**

```bash
git add ~/.claude/skills/maintaining-full-coverage/SKILL.md
git commit -m "feat: add maintaining-full-coverage skill (GREEN phase)"
```

---

### Task 4: Run GREEN Phase — Verify Compliance

Re-run the same 4 pressure scenarios, this time WITH the skill loaded in the subagent's context.

- [ ] **Step 1: Re-run all 4 scenarios with skill loaded**

For each scenario, dispatch a subagent that has the SKILL.md content in its context. Compare behavior against baseline.

Expected improvements:
- Scenario 1: Agent should attempt to test the `except OSError` block, not accept 98.6%
- Scenario 2: Agent should mock `platform.system()` and `os.execv()`, update test-report.txt
- Scenario 3: Agent should try mocking the DB error before reaching for `pragma: no cover`
- Scenario 4: Agent should flag the test-batching problem and suggest writing tests now

- [ ] **Step 2: Document GREEN results**

Save comparison to `docs/superpowers/plans/maintaining-full-coverage-green-results.md`

- [ ] **Step 3: Commit GREEN results**

```bash
git add docs/superpowers/plans/maintaining-full-coverage-green-results.md
git commit -m "docs: record GREEN phase results for maintaining-full-coverage"
```

---

### Task 5: REFACTOR Phase — Close Loopholes

Based on GREEN phase results, identify any new rationalizations or loopholes the agent found.

- [ ] **Step 1: Identify new rationalizations**

Review GREEN results. For each scenario where the agent still partially violated the skill:
- What rationalization did it use?
- What explicit counter needs to be added?

- [ ] **Step 2: Update SKILL.md with counters**

Edit `~/.claude/skills/maintaining-full-coverage/SKILL.md`:
- Add new entries to the rationalization table
- Add new red flags
- Close any loopholes in the escalation ladder wording
- Strengthen any sections that were misinterpreted

- [ ] **Step 3: Re-test any scenario that previously failed**

Run the specific scenarios that showed issues. Verify compliance.

- [ ] **Step 4: Commit refined skill**

```bash
git add ~/.claude/skills/maintaining-full-coverage/SKILL.md
git commit -m "refactor: close loopholes in maintaining-full-coverage skill"
```

---

### Task 6: Final Verification and Deployment

- [ ] **Step 1: Run all 4 scenarios one final time**

Full pass with the refined skill. All scenarios should show compliant behavior.

- [ ] **Step 2: Verify skill is discoverable**

Check that the `name` and `description` frontmatter are correct. Verify the description starts with "Use when..." and contains no workflow summary. Confirm the skill appears in the skill list.

- [ ] **Step 3: Final commit**

```bash
git add ~/.claude/skills/maintaining-full-coverage/SKILL.md
git commit -m "docs: finalize maintaining-full-coverage skill after REFACTOR phase"
```
