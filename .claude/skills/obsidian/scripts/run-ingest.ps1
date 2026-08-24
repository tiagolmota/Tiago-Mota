<#
.SYNOPSIS
  Windows helper for the "obsidian" Claude Code skill: downloads
  ingest_folder.py and runs it against a local source folder and vault.

.DESCRIPTION
  This script exists because ingest_folder.py has to run on YOUR machine
  (it needs real filesystem access to the source folder, e.g. D:\Documentos)
  -- it cannot be run from a remote Claude session. This wrapper handles
  finding Python, downloading the script, and running a safe dry run first.

.EXAMPLE
  .\run-ingest.ps1 -SourcePath "D:\Documentos" -VaultPath "C:\Users\you\MyVault"

.EXAMPLE
  # Skip specific folders (repeatable):
  .\run-ingest.ps1 -SourcePath "D:\" -VaultPath "C:\Users\you\MyVault" -ExcludeDir "IRS","CV"

.EXAMPLE
  # After checking the dry-run counts look right, actually write the notes:
  .\run-ingest.ps1 -SourcePath "D:\Documentos" -VaultPath "C:\Users\you\MyVault" -Apply
#>
param(
    [Parameter(Mandatory = $true)][string]$SourcePath,
    [Parameter(Mandatory = $true)][string]$VaultPath,
    [switch]$Apply,
    # Directory names to skip, on top of the script's built-in defaults
    # (node_modules, .git, Windows, Program Files, AppData, recycle bins, etc.)
    [string[]]$ExcludeDir = @(),
    # Branch/ref to download ingest_folder.py from. Once PR #3 merges, switch
    # this to "main".
    [string]$Ref = "claude/obsidian-skills-plugin-6dredp"
)

$ErrorActionPreference = "Stop"

# 1. Find Python (Windows installs usually expose "python", sometimes "python3").
$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) { $python = Get-Command python3 -ErrorAction SilentlyContinue }
if (-not $python) {
    Write-Host "Python not found on PATH." -ForegroundColor Red
    Write-Host "Install it from https://www.python.org/downloads/ -- check 'Add python.exe to PATH' during setup -- then re-run this script."
    exit 1
}

# 2. Download ingest_folder.py next to this script.
$scriptUrl = "https://raw.githubusercontent.com/tiagolmota/Tiago-Mota/$Ref/.claude/skills/obsidian/scripts/ingest_folder.py"
$localScript = Join-Path $PSScriptRoot "ingest_folder.py"
Write-Host "Downloading ingest_folder.py from $scriptUrl ..."
Invoke-WebRequest -Uri $scriptUrl -OutFile $localScript

# 3. Sanity-check the paths before running anything.
if (-not (Test-Path $SourcePath)) {
    Write-Host "Source path not found: $SourcePath" -ForegroundColor Red
    exit 1
}
if (-not (Test-Path $VaultPath)) {
    Write-Host "Vault path not found: $VaultPath" -ForegroundColor Red
    Write-Host "This should be the folder Obsidian opened as a vault (Settings -> About in Obsidian shows it)."
    exit 1
}

# 4. Warn if there are PDFs but no pdftotext -- they'll silently be skipped otherwise.
$hasPdfs = Get-ChildItem -Path $SourcePath -Recurse -Filter *.pdf -ErrorAction SilentlyContinue | Select-Object -First 1
if ($hasPdfs -and -not (Get-Command pdftotext -ErrorAction SilentlyContinue)) {
    Write-Host "Note: found PDFs under $SourcePath but 'pdftotext' isn't on PATH -- PDFs will be skipped." -ForegroundColor Yellow
    Write-Host "To include them, install Poppler for Windows (https://github.com/oschwartz10612/poppler-windows/releases) and add its bin/ folder to PATH."
}

# 5. Run it -- dry run unless -Apply was passed.
$extraArgs = @()
if (-not $Apply) { $extraArgs += "--dry-run" }
foreach ($dir in $ExcludeDir) { $extraArgs += "--exclude-dir"; $extraArgs += $dir }

Write-Host ""
Write-Host "Running ingest_folder.py $(if ($Apply) { '(APPLYING CHANGES)' } else { '(dry run)' })..." -ForegroundColor Cyan
Write-Host ""
& $python.Source $localScript $SourcePath $VaultPath @extraArgs

if (-not $Apply) {
    Write-Host ""
    Write-Host "This was a dry run -- no notes were written. If the counts above look right, re-run with -Apply." -ForegroundColor Yellow
}
