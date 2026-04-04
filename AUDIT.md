# maintaining-full-coverage — Skill Audit

When editing this skill, verify that pressure scenarios exist to cover each section. Every row, every step, every rule should have at least one scenario that would fail without it. This is the skill's own "coverage report."

## Sections requiring scenario coverage

- [x] Completion gate — each of the 5 steps
- [x] Escalation ladder — each of the 5 tiers, plus the "never skip" constraint
- [x] Report file — treated as first-class artifact, updated now not later, committed alongside code
- [x] Report file — CI rejection of regressions, exemption/baseline process
- [x] Report file — git hash placement, minimal format fields (verified via sample report generation)
- [x] Development nudge — don't batch tests, branch awareness
- [x] Heroic: OS/platform mocking
- [x] Heroic: error path simulation
- [x] Heroic: elevated/interactive tests with instructional dialogs
- [x] Heroic: browser/integration coverage
- [x] Heroic: startup/shutdown testing
- [x] Rationalization table — each row exercised by at least one scenario
- [x] Red flags — each flag triggered by at least one scenario (including hollow coverage)
- [x] Dead code detection — agent considers deletion, not just exclusion

## Scenario inventory

| Scenario | Primary coverage |
|----------|-----------------|
| 1: Close Enough (98.6%) | Escalation order, dead code awareness, pragma discipline |
| 2: Platform Code | OS/platform mocking, report as first-class artifact |
| 3: Pragma Shortcut | Error path simulation, pragma before asking |
| 4: Batch Testing | Development nudge, branch awareness, don't batch |
| 5: Documented Exception (FFI) | Escalation step 5, baseline update, CI adjustment |
| 6: Elevated/Interactive | Interactive tests with dialogs, heroic testing |
| 7: CI Baseline Regression | CI rejection policy, exemption process, deadline pressure |
| 8: Browser/Integration (SPA) | Puppeteer/Playwright, UI audit scripts, multi-suite report |
| 9: Startup/Shutdown (daemon) | Mock init deps, trigger teardown explicitly |
| 10: Hollow Coverage (review) | Red flag: tests that cover without testing meaningful behavior |

## Coverage: 15/15 sections covered
