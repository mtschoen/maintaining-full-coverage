---
name: smoke-test
description: "Run a smoke test after making changes, before declaring work complete. Use EVERY time you finish implementing a feature, fixing a bug, refactoring code, changing configuration, or modifying any file that affects runtime behavior. This skill applies before saying 'done', 'complete', 'finished', 'all set', 'ready to commit', or any variation — even if you're confident the change is correct. If you changed code, you smoke test it. No exceptions."
---

# Smoke Test

## The Problem This Solves

The user should never be the first person to discover that a change doesn't work. If they ask you to fix a bug and you say "done", then they try it and get a compile error — that's a failure of process, not just a failure of code. The smoke test catches these before the user ever sees them.

## What a Smoke Test Is

A smoke test answers two questions, in order:

1. **Does it build and run?** (the floor — compile errors, import failures, server crashes)
2. **Does it do what was asked?** (the actual bar — the feature works, the bug is fixed, the behavior changed)

Question 1 without question 2 is not a smoke test. Passing the build is necessary but not sufficient. If the user asked you to add a button that exports a CSV, and the project compiles, you still need to verify the button appears and the CSV downloads.

## When to Smoke Test

**Every time**, before you tell the user the work is done. This includes:

- Feature implementation
- Bug fixes
- Refactors (yes, even "safe" ones)
- Config changes
- Dependency updates
- Build script changes

The only exception is changes that have no runtime effect — like editing comments, documentation, or .gitignore.

## How to Smoke Test by Project Type

The right smoke test depends on what you changed and what kind of project it is. Use the most specific approach that applies.

### Compiled projects (.NET, C++, Java, Go, Rust)

**Floor:** Build the project. The full solution, not just the file you changed — dependency errors hide in other projects.

```text
dotnet build                    # .NET
msbuild /p:Configuration=Debug  # C++/MSBuild
go build ./...                  # Go
cargo build                     # Rust
mvn compile                     # Java/Maven
```

**Bar:** If the change affects runtime behavior, run the application and exercise the changed code path. For a CLI tool, run it with arguments that hit the new/changed functionality. For a library, run the tests that cover the changed code, or write a quick test if none exist.

### Web frontend (React, Vue, Svelte, etc.)

**Floor:** Make sure the dev server starts without errors.

```text
npm run dev    # or yarn dev, pnpm dev
```

**Bar:** Open the browser and check that the change works visually. If you can't open a browser, check the dev server console for runtime errors and verify the component renders by checking the dev server output. Be explicit about what you checked and what you couldn't check — say "I verified the server starts and there are no console errors, but I can't visually confirm the layout change; please check in the browser."

### Web backend (Node, Python, .NET API, etc.)

**Floor:** Start the server. Watch for startup errors, missing env vars, failed DB connections.

**Bar:** Hit the endpoint you changed. Use `curl`, `wget`, or the project's existing HTTP test client. Verify the response is what you expect — status code, response body, not just "no error."

```text
curl -s http://localhost:3000/api/your-endpoint | head -20
```

### Unity projects

**Floor:** Run a batch-mode compile. This catches script errors without needing the Editor open.

```text
Unity -batchmode -nographics -projectPath . -logFile - -quit
```

**Bar:** If the change affects gameplay or scene behavior, note what needs manual testing in the Editor and tell the user what to check. Don't claim the behavior works if you can only verify compilation.

### Scripts and CLI tools

**Floor:** Run the script with valid input. Check exit code.

**Bar:** Verify the output matches expectations. If it writes a file, check the file exists and has reasonable content. If it transforms data, spot-check the result.

### Configuration changes (CI, Docker, Terraform, etc.)

**Floor:** Validate the config syntax.

```text
docker compose config           # Docker Compose
terraform validate              # Terraform
yamllint .github/workflows/     # GitHub Actions
```

**Bar:** If possible, do a dry run. `terraform plan`, `docker compose build`, etc. If not possible, say what you validated and what needs to be tested in the real environment.

### Test-only changes

**Floor and bar are the same:** Run the tests. All of them, not just the one you changed — you might have broken a shared fixture.

```text
dotnet test
npm test
pytest
```

## The Smoke Test Sequence

After you finish the implementation but before you declare completion:

1. **Identify the project type and what changed.** This tells you which smoke test applies.
2. **Run the floor check** (build/compile/start). If it fails, fix it. Don't report the failure to the user — just fix it and retry.
3. **Run the bar check** (exercise the actual change). If it fails, fix it and retry.
4. **If you can't fix it after a thorough attempt** (3+ cycles of fix-and-retry, or you've hit something you genuinely don't understand), then report what you tried, what's still broken, and what you think the issue might be. The user should hear "I made the change but the server returns a 500 on the new endpoint — here's the stack trace, I tried X and Y but the issue seems to be Z" — not just "done."
5. **Report success with evidence.** Don't just say "done" — say what you verified. "Built the solution, ran the CLI with `--export csv`, confirmed the output file has the expected columns." Brief is fine, but concrete.

## What "Fix It" Means

When a smoke test fails, don't just retry the same thing. Diagnose:

- Read the error message carefully
- Check if your change introduced the issue or exposed a pre-existing one
- If it's your change, fix the root cause
- If it's pre-existing, note it but don't get sidetracked fixing unrelated issues — focus on verifying your change works

A "thorough attempt" means you've actually investigated, not just retried the build three times hoping it works. But also don't spend 30 minutes chasing a rabbit hole — if you're stuck after genuine investigation, say so.

## When You'll Be Tempted to Skip

The smoke test matters most in exactly the moments you'll want to skip it:

- **Late in a long session** when you've been working for a while and just want to wrap up. This is when you're most likely to make mistakes and least likely to catch them.
- **After a "trivially correct" change** — renaming a variable, fixing a typo, moving an import. These changes can have surprising knock-on effects (broken references, import cycles, case sensitivity issues).
- **When testing requires non-trivial setup** — starting a full stack, seeding test data, configuring environment variables. The effort of setting up the test is exactly why the user can't easily verify it themselves. If you skip it, you're pushing that cost onto them.
- **When you just finished a long debugging session** and finally found a fix. The temptation is to say "got it!" but the fix might have side effects, or might not actually work outside the narrow scenario you were debugging.
- **On step 3 of a 5-step task** where you want to keep moving. Test the intermediate state anyway — compounding untested changes is how you end up with a broken mess at the end that's hard to diagnose.

In all of these cases: run the smoke test. It takes 30 seconds. Debugging a broken change the user reports back to you takes much longer.

## Things That Are Not Smoke Tests

- "The linter passes" — linters don't run your code
- "The types check" — type checking doesn't catch runtime errors
- "I'm confident this is correct" — confidence is not evidence
- "The tests pass" (when you changed a feature, not a test) — tests might not cover what you changed
- "I reviewed the code and it looks right" — code review is not execution

These are all useful signals, but none of them substitute for actually running the changed code and seeing it work.

## When You Can't Fully Verify

Sometimes you genuinely can't complete the bar check — maybe you don't have browser access, or the change requires a running database you don't have, or it's a UI change in a native app. In these cases:

1. Do everything you can (build, start the server, run available tests)
2. Be explicit about what you verified and what you couldn't
3. Tell the user exactly what to check: "I verified it compiles and the unit tests pass. Please check in the browser that the modal closes after clicking Save — I couldn't test that from the CLI."

The user knowing what to test is far better than the user thinking everything was tested when it wasn't.

## After the Smoke Test Passes

Once the smoke test passes and you have no more changes to make, the change has settled. That is the moment to check whether it made any documentation lie. Use the **docs-update** skill - the sibling step to this one. It checks README, CLAUDE.md / AGENTS.md, other in-repo docs, and inline doc comments for drift your change introduced, and bundles any fixes into the same commit. Most of the time nothing needs updating; the value is the check.
