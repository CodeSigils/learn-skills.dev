---
name: powershell-safe-invocation
description: Use when writing or running PowerShell on Windows, especially native programs, quoted paths, escaping, pwsh vs powershell.exe, Start-Process, ProcessStartInfo, file operations, SSH/WSL/Bash calls, encoding, BOM, Chinese text, running exe locks, or shell troubleshooting.
---

# PowerShell Safe Invocation

Use this skill when PowerShell is the execution layer for Codex or automation. The main risk is losing argument boundaries by squeezing structured commands into nested quoted strings.

## Core Rule

Do not put complex commands inside one more layer of quotes.

Choose the simplest safe option:

1. PowerShell cmdlet.
2. Native command with `& $exe @args`.
3. Temporary `.ps1` file with `pwsh.exe -NoLogo -NoProfile -NonInteractive -File script.ps1`.
4. `ProcessStartInfo.ArgumentList`.
5. `Start-Process` only for elevation, new/hidden windows, detached launch, or shell behavior.
6. `cmd.exe /c` only when cmd semantics are required.
7. `Invoke-Expression` only as a tightly controlled last resort for trusted PowerShell source.

Read `reference.md` when the task involves SSH, WSL, Bash, JSON, regex, recursive filesystem mutation, encoding, stdout/stderr capture, or a failing shell invocation.

## Shell

Prefer PowerShell 7 through `pwsh.exe` unless Windows PowerShell 5.1 is explicitly required.

Verify when uncertain:

```powershell
$PSVersionTable.PSVersion
$PSNativeCommandArgumentPassing
Get-Command pwsh -ErrorAction SilentlyContinue
Get-Command powershell -ErrorAction SilentlyContinue
```

Do not assume installing PowerShell 7 makes `powershell.exe` use PowerShell 7:

- `pwsh.exe` = PowerShell 7
- `powershell.exe` = Windows PowerShell 5.1

Use this automation entry point for non-trivial scripts:

```text
pwsh.exe -NoLogo -NoProfile -NonInteractive -File script.ps1
```

Do not add `-ExecutionPolicy Bypass` by habit. Add it only when a trusted script is actually blocked and policy permits the override.

## Native Programs

Never construct one large command string when arguments can be passed separately.

```powershell
$exe = 'C:\Path With Spaces\tool.exe'
$args = @(
    '--input'
    'C:\Data Folder\input.json'
    '--empty'
    ''
)

& $exe @args

$exitCode = $LASTEXITCODE
if ($exitCode -ne 0) {
    throw "$exe failed with exit code $exitCode"
}
```

Rules:

- Treat every native argument as one array item.
- Invoke executable paths stored in variables with `&`.
- Capture `$LASTEXITCODE` immediately.
- Do not use `Invoke-Expression`.
- Do not add a `cmd.exe /c` layer merely to launch an executable.
- Do not use Bash-style `\"` escaping in PowerShell.
- Do not silently remove empty arguments; omitted argument, `''`, and `$null` are different.

## Cmdlets And Files

Use hashtable splatting for cmdlets:

```powershell
$params = @{
    LiteralPath = 'C:\Data[1]\input.txt'
    Destination = 'C:\Output'
    Force       = $true
    ErrorAction = 'Stop'
}

Copy-Item @params
```

Rules:

- Use `-LiteralPath` for real paths unless wildcard expansion is intentional.
- Use `$ErrorActionPreference = 'Stop'` or `-ErrorAction Stop` for cmdlet failures.
- Do not use `$LASTEXITCODE` to test a normal cmdlet.
- Before recursive delete, move, or overwrite, resolve absolute root and target paths and verify the target is inside the intended root.
- Keep filesystem mutations in PowerShell instead of enumerating paths in PowerShell and passing them to another shell for deletion or moving.

## Complex Commands

Use a `.ps1` file or here-string when a command contains:

- multiline code
- nested quotes
- JSON, XML, regular expressions
- pipes or redirection
- SSH remote scripts
- WSL/Bash scripts
- `$()`, `$VAR`, `%VAR%`
- non-ASCII paths or Chinese output

Prefer objects plus serialization for JSON:

```powershell
$data = [ordered]@{
    name = $name
    path = $path
}

$json = $data | ConvertTo-Json -Depth 10
```

Use single quotes for literal strings and paths. Use double quotes only when PowerShell expansion is needed. Avoid backtick line continuation; use arrays, hashtables, splatting, parentheses, or script blocks.

## Remote Shells

PowerShell parses before SSH, WSL, Bash, Python, or Git receive arguments.

Avoid:

```powershell
ssh root@example.com "backup=/opt/app/app.backup.$(date +%Y%m%d%H%M%S)"
```

Use single quotes for simple remote Bash, or pipe a here-string to `bash -s` for complex scripts:

```powershell
$script = @'
set -e
backup=/opt/app/app.backup.$(date +%Y%m%d%H%M%S)
echo "$backup"
'@

$script | ssh root@example.com 'bash -s'
```

Do not write Bash heredoc syntax directly in PowerShell:

```powershell
python - <<'PY'
print("hello")
PY
```

Use a PowerShell here-string instead:

```powershell
@'
print("hello")
'@ | python -
```

## Encoding And Locks

For cross-platform text, prefer UTF-8 without BOM. Terminal mojibake does not prove the file is corrupt; inspect bytes or read with explicit encoding.

Do not truncate UTF-8 strings by byte index unless the cut point is a character boundary.

Windows cannot overwrite a running `.exe`. If a build fails with access denied on `target\debug\*.exe`, find and stop the old process before rebuilding.

## Troubleshooting

When invocation corruption occurs:

1. Remove `cmd.exe /c`.
2. Remove `-Command`.
3. Remove `Invoke-Expression`.
4. Remove manually nested quotes.
5. Put code in a minimal `.ps1` file.
6. Invoke the native executable directly with `& $exe @args`.
7. Print every argument and length.
8. Capture `$LASTEXITCODE` immediately.
