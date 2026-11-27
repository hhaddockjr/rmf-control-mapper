# collect_evidence.ps1
# Sample evidence collector for RMF Control Mapper
# Demonstrates PowerShell evidence collection for AC-2 and IA-2

param(
    [string]$InputFile = "data/sample_users.csv",
    [string]$OutputFile = "data/sample_users_mfa.csv"
)

Write-Host "=== RMF Evidence Collector ===" -ForegroundColor Cyan
Write-Host "Reading user inventory from: $InputFile"

if (-not (Test-Path $InputFile)) {
    Write-Error "Input file not found: $InputFile"
    exit 1
}

$users = Import-Csv -Path $InputFile

# Enrich with collection metadata
$evidence = foreach ($user in $users) {
    [PSCustomObject]@{
        username        = $user.username
        display_name    = $user.display_name
        mfa_enabled     = $user.mfa_enabled
        last_logon      = $user.last_logon
        account_status  = $user.account_status
        collected_at    = (Get-Date -Format "yyyy-MM-dd HH:mm:ss")
        evidence_for    = "AC-2,IA-2"
    }
}

# Ensure output directory exists
$outputDir = Split-Path -Parent $OutputFile
if (-not (Test-Path $outputDir)) {
    New-Item -ItemType Directory -Path $outputDir | Out-Null
}

$evidence | Export-Csv -Path $OutputFile -NoTypeInformation

Write-Host "Evidence written to: $OutputFile" -ForegroundColor Green
Write-Host "Records collected: $($evidence.Count)"
Write-Host "Controls supported: AC-2 (Account Management), IA-2 (Identification and Authentication)"
Write-Host "=== Done ===" -ForegroundColor Cyan
