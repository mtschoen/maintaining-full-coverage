# Handoff: make the TEST-REPORT.md template render-safe markdown

**Raised:** 2026-06-02 (during schoen-claude-status PR #9).
**Status:** open / future work. Not yet applied to this skill.

## Problem

The skill's `SKILL.md` "Report File Convention" -> "Minimal required format"
example is written in a plaintext-block style:

- a box-drawing horizontal rule (`═══...`, U+2550) directly under the title
- field lines with no blank-line separation
- indented sub-blocks (coverage / lint breakdowns)

Markdown renderers (gitea, GitHub, VS Code preview) collapse that: consecutive
non-blank lines merge into one run-on paragraph, the `═══` line glues to the
title, and the indentation does not reliably become a code block. When a
repository commits `TEST-REPORT.md`, the report is read on the forge during
review, so it needs to render cleanly there, not just in a terminal. The old
template's title line also used an em-dash (`-` rule violation per the user's
global no-em-dash rule).

User report, verbatim: "the test report template doesn't render very nicely on
gitea (or anywhere else for that matter). The newlines around the ==== are
collapsed, and a bunch of others."

## Proposed fix

Rewrite the "Minimal required format" block (and any other plaintext-block
example in `SKILL.md`) as render-safe markdown, keeping the SAME required fields
(Status, Mode, Tests, Git, Coverage, Lint) and the same Three-Modes semantics:

- `#` / `##` headers instead of the `═══` rule.
- A markdown table for the status fields (Status / Mode / Tests / Git) and for
  the lint-tool and per-module coverage breakdowns.
- Fenced ```` ```bash ```` blocks for the gate/coverage commands.
- Blank line between every section/paragraph.
- ASCII only: no `═`/box-drawing, no em-dashes.
- Escape literal pipes inside table cells (e.g. a `|| true` CI note becomes
  `\|\| true`) or they break the table.

## Reference implementation (copy from here)

A fully reformatted, render-safe version already exists and renders correctly on
gitea. Use it as the template to backport into `SKILL.md`:

- Repo: `schoen-claude-status`
- File: `TEST-REPORT.md` at `main` (commit `38be07e`; reformat landed on the
  feature branch as `c416d67` "docs: reformat TEST-REPORT.md as render-safe
  markdown").

It uses headers + tables + a bash code fence and carries all the required
fields, so it doubles as the new minimal-format example.

## Scope note

This is a docs/template change to `SKILL.md` only - no behavioral change to the
coverage/lint gate logic. After editing, re-run `install-skills.sh` (or the
project's deploy step) so the deployed copy under `~/.claude/skills/` matches.
