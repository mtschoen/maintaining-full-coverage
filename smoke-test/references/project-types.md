# Smoke tests by project type

Fallback catalog for projects with no `SMOKE.md`. Each entry gives the floor (does it build/run?) and the bar (does it do what was asked?). Use the most specific approach that applies to what you changed.

## Compiled projects (.NET, C++, Java, Go, Rust)

**Floor:** Build the project. The full solution, not just the file you changed - dependency errors hide in other projects.

```text
dotnet build                    # .NET
msbuild /p:Configuration=Debug  # C++/MSBuild
go build ./...                  # Go
cargo build                     # Rust
mvn compile                     # Java/Maven
```

**Bar:** If the change affects runtime behavior, run the application and exercise the changed code path. For a CLI tool, run it with arguments that hit the new/changed functionality. For a library, run the tests that cover the changed code, or write a quick test if none exist.

## Web frontend (React, Vue, Svelte, etc.)

**Floor:** Make sure the dev server starts without errors.

```text
npm run dev    # or yarn dev, pnpm dev
```

**Bar:** Open the browser and check that the change works visually. If you can't open a browser, check the dev server console for runtime errors and verify the component renders by checking the dev server output. Be explicit about what you checked and what you couldn't check - say "I verified the server starts and there are no console errors, but I can't visually confirm the layout change; please check in the browser."

## Web backend (Node, Python, .NET API, etc.)

**Floor:** Start the server. Watch for startup errors, missing env vars, failed DB connections.

**Bar:** Hit the endpoint you changed. Use `curl`, `wget`, or the project's existing HTTP test client. Verify the response is what you expect - status code, response body, not just "no error."

```text
curl -s http://localhost:3000/api/your-endpoint | head -20
```

## Unity projects

**Floor:** Run a batch-mode compile. This catches script errors without needing the Editor open.

```text
Unity -batchmode -nographics -projectPath . -logFile - -quit
```

**Bar:** If the change affects gameplay or scene behavior, note what needs manual testing in the Editor and tell the user what to check. Don't claim the behavior works if you can only verify compilation.

## Scripts and CLI tools

**Floor:** Run the script with valid input. Check exit code.

**Bar:** Verify the output matches expectations. If it writes a file, check the file exists and has reasonable content. If it transforms data, spot-check the result.

## Configuration changes (CI, Docker, Terraform, etc.)

**Floor:** Validate the config syntax.

```text
docker compose config           # Docker Compose
terraform validate              # Terraform
yamllint .github/workflows/     # GitHub Actions
```

**Bar:** If possible, do a dry run. `terraform plan`, `docker compose build`, etc. If not possible, say what you validated and what needs to be tested in the real environment.

## Test-only changes

**Floor and bar are the same:** Run the tests. All of them, not just the one you changed - you might have broken a shared fixture.

```text
dotnet test
npm test
pytest
```
