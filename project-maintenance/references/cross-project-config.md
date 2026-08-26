# Cross-project configuration conventions

The canonical *target shapes* for the fleet-wide conventions project-maintenance checks. When a
project-tracker `get_maintenance_checklist` finding points here, use these as
the draft you bring to the user - never apply straight to disk.

This list grows. **When a new cross-project convention is adopted, add its
target shape here AND a detection check in project-tracker's checklist
scanner so project-maintenance surfaces drift automatically.**

---

## Agent-instruction file convention

**AGENTS.md is the single source of truth.** It is the cross-tool standard
(Linux Foundation / Agentic AI Foundation; read natively by Codex, Cursor,
Copilot, opencode, Amp, …). Tool-specific files are **thin import pointers**:

- `CLAUDE.md` and `GEMINI.md` contain the import directive **`@AGENTS.md`**.
- Claude Code and Gemini CLI **auto-expand `@`-imports into context** at launch
  (relative path, max 4 hops). A plain markdown link - `See [AGENTS.md](AGENTS.md)`
  - does **not** load; the guidance is then silently absent from most sessions.
  That is why a linked pointer is flagged (`agents_pointer_weak_link`) for upgrade.
- A symlink (`ln -s AGENTS.md CLAUDE.md`) is the upstream recommendation but is
  sketchy on Windows - prefer the `@AGENTS.md` text pointer, which is
  git-portable and cross-platform.

### Target shapes

Bare pointer (the common case - nothing tool-specific):

```text
@AGENTS.md
```

Pointer **with a platform-specific addendum** (the allowed exception). The
import line comes first; genuinely tool-specific rules follow below it:

```text
@AGENTS.md

## Common configurations
- Worktrees live under `.worktrees/`; reserve with a self-documenting `.worktree-reserved` marker (contents: `reserved-by`, `reserved-at`, `stale-after`), not a bare touch file.
- The on-save linter hook is configured in project settings, e.g. `.agents/settings.json`.
```

`reserved-by` is any harness name plus its session/instance id, or `user@host` for a
manual reservation; `reserved-at` is ISO 8601 UTC (`YYYY-MM-DDTHH:MM:SSZ`). Filled-in
example (full field spec lives in fleet-orchestration's warm worktree pool section):

```text
worktree pool-slot reservation
reserved-by: opencode session 7f3a9c12
reserved-at: 2026-08-04T21:40:00Z
branch: fix/worktree-reserved-marker
task: finalize .worktree-reserved marker spec across three PRs
stale-after: 24h - safe to delete if reserved-at is older and the owning session is gone
```

### What counts as "platform-specific" (stays in CLAUDE.md / GEMINI.md)

Keep below the import line ONLY content that is meaningless to other agents:
Claude Code hooks/settings paths, the `Skill` tool, `claude -p`, subagent
`model:` routing, `~/.claude/...` locations. **Everything else is shared and
belongs in AGENTS.md** - including quality-gate docs (aislop), build/test
commands, architecture notes, and coding conventions. A frequent mistake is
leaving the aislop section in CLAUDE.md; it is not Claude-specific - move it.

---

## On-save linter hook

A `PostToolUse` Write|Edit hook that lints each file as it is written. This is
not supported in all agent harnesses. For claude code, add the following to
 `.claude/settings.json`. Canonical ruff + shellcheck form:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "f=$(jq -r '.tool_input.file_path // .tool_response.filePath // empty'); case \"$f\" in *.py) o=$(ruff check -q \"$f\" 2>/dev/null); [ -n \"$o\" ] && jq -n --arg c \"ruff:\\n$o\" '{hookSpecificOutput:{hookEventName:\"PostToolUse\",additionalContext:$c}}';; *.sh) o=$(shellcheck \"$f\" 2>/dev/null); [ -n \"$o\" ] && jq -n --arg c \"shellcheck:\\n$o\" '{hookSpecificOutput:{hookEventName:\"PostToolUse\",additionalContext:$c}}';; esac; exit 0"
          }
        ]
      }
    ]
  }
}
```

Repos with an aislop gate add a second hook entry of the same shape that runs
the pinned aislop binary. **Pin the aislop binary version in a hook - never
`@latest`** (a hook runs on every edit and `@latest` does a network check each
time). Tailor the `case` arms to the repo's actual languages.

---

## CI (`.gitea/workflows/` - Gitea Actions)

Automates the validate tier (lint + format check + tests) so regressions block
at merge. Minimal lint skeleton:

```yaml
name: lint
on: [push, pull_request]
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.12" }
      - run: pip install ruff
      - run: ruff check . && ruff format --check .
```

Scope paths explicitly (or rely on a root `pyproject.toml` `exclude`) so CI does
not run on generated/fixture trees. GitHub-mirrored repos use `.github/workflows/`.

---

## aislop quality gate (`.aislop/config.yml`)

Language-agnostic AI-slop gate (deterministic, scored 0–100). Per-edit hook +
PR/CI gate. Target config:

```yaml
ci:
  failBelow: 80          # tune to the repo's current pass rate
exclude:
  - "*/workspace/**"     # generated / fixture trees
```

CI step (pin a version, NOT `@latest`): `npx --yes aislop@<ver> ci .` - use the
CLI on Gitea Actions, not the GitHub composite action. Known Python false
positive: `ai-slop/unused-import` fires on `from __future__ import annotations`
(do NOT remove that line). aislop scores the **whole repo** - there is no
diff-only mode.

---

## Local settings tracking convention

Most harnesses split config into two files. For example, Claude Code does this:

- **`.claude/settings.json`** - shared, **committed**. Plugins, hooks, shared
  permissions: anything the whole team/fleet should get.
- **`.claude/settings.local.json`** - per-machine **local override**, must
  **never** be tracked. The permission-approval flow writes to it every session
  (each approved command becomes an `allow` entry), so a tracked copy churns on
  every run and can smuggle in an over-broad grant like `PowerShell(curl *)`.

The convention ignores the whole `.claude/` tree and re-includes only the shared
settings, so any local file (settings.local.json, state, scratch) is
auto-ignored:

```gitignore
.claude/*
!.claude/settings.json
```

Two distinct findings draw from this section, using Claude Code as an example:

- **`agents_settings_local_tracked`** (high, `recommendation: untrack`) -
  `.claude/settings.local.json` is tracked. The fix is **`git rm --cached
  .claude/settings.local.json`** then commit; the working copy stays on disk and
  is caught by the ignore rule going forward. `action_on_approval` is exactly
  that `git rm --cached` (do **not** delete the working file). Critically, a
  `.gitignore` rule added *after* the file was committed does NOT retroactively
  untrack it - git keeps tracking an already-tracked path regardless of a later
  ignore rule, so "the ignore line exists" does not clear this finding. The only
  fix is to untrack.
- **`missing_agents_settings_ignore`** (low, `recommendation:
  setup:agents_ignore`) - the repo tracks `.claude/settings.json` (so it is
  Claude-configured) but `.gitignore` lacks the two-line convention above. Draft
  is to append those two lines. Tolerate leading slashes (`/.claude/*`,
  `!/.claude/settings.json`). Note: a repo may also *intentionally* track other
  `.claude/` files (CLAUDE.md, AISLOP.md, notes/) as force-added-despite-ignore;
  that is fine and this check does not flag it - it only validates the gitignore
  shape, never the other tracked files.

---

## Safe git clean + post-clean init

**The invariant:** `git clean -ffxd` must always be safe to run. Safety comes
from an invariant, not a wrapper or exclude list: nothing unrecoverable lives
in the working tree. Every file is either tracked and pushed, or reproducible
by re-running a tool. Git offers no way to protect a file from `clean`
(aliases cannot shadow built-in commands, there is no pre-clean hook, and `-x`
overrides `.git/info/exclude`), so the invariant is the whole mechanism. A
compliant repo therefore has no load-bearing untracked files: anything under
`.claude/scripts/` (gitignored via `.claude/*`) that other tracked files
reference moves to a tracked `scripts/` directory, with every reference
updated; spent one-off scripts are deleted instead.

### `.gitignore` blocks

The Claude Code block ignores everything under `.claude/` except the shared,
tracked settings file, with a comment explaining why the generated files stay
untracked:

```gitignore
# Claude Code
# .claude/AISLOP.md and .claude/CLAUDE.md are generated boilerplate written by
# `aislop hook install claude --project` (a sentinel-fenced block that the
# installer rewrites on upgrade), so they stay ignored - see AGENTS.md for the
# restore command. settings.json is tracked because it carries the aislop hook
# registration. Hand-written tooling belongs in scripts/, not here.
.claude/*
!.claude/settings.json
```

`.maintenance.json` is tracked, not gitignored: it records which maintenance
findings were actioned and which were deliberately rejected, and nothing
regenerates that. The machine-wide excludes file ignores it, so the
repo-level `.gitignore` needs an explicit negation:

```gitignore
# .maintenance.json is tracked here: it records which maintenance findings
# were actioned and which were deliberately rejected, and nothing regenerates
# that. The negation is needed because the machine-wide excludes file ignores
# it, and a repository .gitignore takes precedence over that.
!.maintenance.json
```

The aislop block ignores runtime artifacts (session/history logs, caches,
baselines) but keeps the checked-in gate config, unanchored so nested project
directories are covered too:

```gitignore
# aislop runtime artifacts (session/history logs, caches, baselines).
# Unanchored so nested project directories are covered too.
**/.aislop/*
!**/.aislop/config.yml
```

A repo that carries the fork-commit pin file also negates it:
`!**/.aislop/fork-commit`.

### `.gitattributes` rules

Shell scripts must check out with LF on every platform, and batch files must
check out with CRLF, each with a comment explaining the failure mode a
missing rule produces:

```gitattributes
# Shell scripts must check out with LF on every platform. With CRLF endings a
# script fails on Linux at the shebang: "bad interpreter: /usr/bin/env bash^M".
*.sh text eol=lf

# Batch files must check out with CRLF. cmd.exe tolerates LF for simple
# line-by-line scripts, but mis-parses labels, goto targets, and multi-line
# blocks, so an LF-only .bat works until someone adds one and then fails in a
# way that reads as a logic bug rather than a line-ending problem.
*.bat text eol=crlf
*.cmd text eol=crlf
```

The init scripts below depend on these rules: a CRLF `.sh` fails at the
shebang on Linux, and an LF `.bat` mis-parses on Windows.

### `init.ps1` / `init.bat` / `init.sh`

Three idempotent scripts at the repository root restore a checkout to a
working state after `git clean -ffxd`, since two things do not come back on
their own: package restore, and the agent instruction files the aislop
installer generates. The reference implementation is the `MFTLib` repo's
`init.ps1`, `init.bat`, and `init.sh` - copy their structure, adapt only the
build-system specifics (which prerequisites are checked, what "restore"
means, what an optional build flag runs) from the target repo's own
`AGENTS.md` build section and CI workflow. Required steps, in order:

1. **Prerequisite check.** Report what is missing; do not install anything.
   Include the package manager / SDK, any platform-specific build tooling,
   and `aislop` (report its version if present, a missing-tool hint if not).
2. **Package restore.** Whatever the stack's dependency-restore step is.
3. **`aislop hook install claude --project`**, skipped with a hint when
   `aislop` is not on PATH. This regenerates `.claude/AISLOP.md` and
   `.claude/CLAUDE.md`.
4. **Settings line-ending normalization guard.** The installer rewrites the
   tracked `.claude/settings.json` with LF endings, which can leave
   `git status` reporting it modified with no content diff. Restore the file
   only in that exact case - both ordinary `git diff --quiet -- .claude/settings.json`
   and staged `git diff --cached --quiet -- .claude/settings.json` clean
   (exit code 0) but `git status --porcelain -- .claude/settings.json` non-empty
   - never when there is a real content change (staged or unstaged). All
   commands must be scoped to `-- .claude/settings.json` so that unrelated
   dirty or staged files elsewhere in the checkout do not suppress or
   mis-trigger the restore.
5. **Optional provisioner call.** If a settings-provisioning tool is on
   PATH, ask it to re-apply the project-scope settings it owns (a clean
   removes `.claude/settings.local.json`). Call it by a feature name (for
   example `apply auto-memory`), never the bare pipeline command, and try
   `schoen-lab-onboard` before the `schoen-lab` fallback name - never the
   bare `onboard` name, which collides with an unrelated GUI binary on some
   Linux distributions. Skip entirely, without error, when the tool is
   absent.
6. **Optional build.** `-Build` (PowerShell) / `--build` (bash), off by
   default to keep the script fast.
7. **Completed/missing summary.** Print what ran and what prerequisites are
   still missing.

`init.bat` is a thin forwarder: it resolves `pwsh` (falling back to Windows
PowerShell), forwards every argument to `init.ps1`, and propagates the exit
code. This is required, not optional - `init.ps1` cannot be invoked directly
from `cmd.exe`, so without a forwarder the documented post-clean sequence
silently does nothing under `cmd.exe`: it reports the file "not recognized"
and the shell moves on, and no restore step ever runs.

### `AGENTS.md` "Cleaning the working tree" section

Shape, modelled on the reference implementation:

1. **The invariant paragraph** - `git clean -ffxd` must always be safe to
   run, stated as the check that a checkout still matches a fresh clone, plus
   the "why no exclude list" explanation (an exclude list leaves the tree
   unequal to a fresh clone, defeating the reason for cleaning, and git has
   no mechanism to protect a file from `clean` regardless).
2. **A Removed / Restored-by table**, filled in from a real
   `git clean -n -ffxd` listing of the target repo - not copied from another
   repo's table, since build output directories and generated-file names
   differ by stack.
3. **"Getting back to work after a clean"** - the `init.ps1` / `init.bat`
   invocation from PowerShell, the `init.bat` invocation from `cmd.exe` (note
   the `.\` prefix: a machine with `NoDefaultCurrentDirectoryInExePath=1` set
   does not search the working directory, so a bare `init.bat` fails as "not
   recognized"), and the `./init.sh` invocation from bash.
4. **The provisioner paragraph** - what the optional settings-provisioning
   call does and why it is safe to skip when the tool is absent.
5. **The prerequisites line** - what each script checks for but does not
   install, per platform.

### Verification (mandatory, and how to do it without destroying anything)

- **Never run a real `git clean -ffxd` in the repo owner's main checkout** -
  it would wipe `.claude/settings.local.json` permission grants and local
  hook wiring that a real session depends on.
- **Dry-run first**: `git clean -n -ffxd` in the main checkout enumerates
  what a real clean would remove. Every entry must map to a row of the
  AGENTS.md restore table, or be a spent one-off file that should be deleted
  outright instead.
- **Real run in a worktree OUTSIDE the repository**, which starts with no
  untracked files - exactly the post-clean state - without touching the
  owner's checkout. A path relative to the repo's own directory without a
  leading `../` resolves *inside* the repo tree, and `git clean -ffxd` would
  then remove the worktree it was meant to verify: confirmed empirically by
  running `git worktree add --detach myrepo-worktrees/init-verify mybranch` from
  inside `myrepo`, which lands the worktree at
  `myrepo/myrepo-worktrees/init-verify`, and `git clean -n -ffxd` in `myrepo`
  then reports `Would remove myrepo-worktrees/`. Create the worktree as a
  sibling outside the repo instead - one level up with `../`, or at an absolute
  path such as `~/<repo>-worktrees/init-verify` - never under the repo's own
  working tree: `git worktree add --detach ../<repo>-worktrees/init-verify <branch>`
  run from the repository root (a branch cannot be checked out in two
  worktrees, hence `--detach`). Then, from that worktree, run the init script
  for every platform the repo targets:
  - PowerShell: `./init.ps1`
  - `cmd.exe`: `init.bat` (proves the forwarder)
  - bash (Linux/macOS): `./init.sh`

  Confirm the generated agent files appear, `git status` is clean
  afterward, and a second run is idempotent. Remove the worktree when done
  (`git worktree remove`); keep the branch.
- Confirm line endings took effect: `git ls-files --eol init.sh init.bat
  init.ps1` should show `w/lf` for `.sh` and `w/crlf` for `.bat` (the index side
  is always `i/lf` because `text=auto` normalizes what git stores).

---

## Full detail

- A repo's own `LINTER-SETUP.md` - the per-repo survey output, when present.
- The aislop section of the user's global `AGENTS.md` - install rules and the
  pinned version.
