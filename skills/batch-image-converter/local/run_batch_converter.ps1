param(
    [string]$ImagesPath = "assets\image_objects",
    [string]$PromptPath = "assets\prompt.txt",
    [switch]$Execute,
    [int]$Limit = 0,
    [switch]$Force
)

$ErrorActionPreference = "Stop"

$ScriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Resolve-Path -LiteralPath (Join-Path $ScriptRoot "..\..\..")

Set-Location $ProjectRoot

$ResolvedImagesPath = (Resolve-Path -LiteralPath $ImagesPath).Path
$ResolvedPromptPath = (Resolve-Path -LiteralPath $PromptPath).Path
$OutputPath = Join-Path (Split-Path -Parent $ResolvedImagesPath) ((Split-Path -Leaf $ResolvedImagesPath) + "_converted")
$ManifestPath = Join-Path $OutputPath "_codex_conversion_manifest.jsonl"

if (Test-Path -LiteralPath $ManifestPath) {
    Write-Host "Using existing manifest:"
    Write-Host $ManifestPath
} else {
    python main.py `
        --images $ResolvedImagesPath `
        --prompt $ResolvedPromptPath `
        --imgformats JPG PNG JPEG
}

Write-Host ""
Write-Host "Manifest prepared at:"
Write-Host $ManifestPath
Write-Host ""

if ($Execute) {
    $CommandArgs = @("scripts\run_codex_batch.py", "--manifest", $ManifestPath)

    if ($Limit -gt 0) {
        $CommandArgs += @("--limit", "$Limit")
    }

    if ($Force) {
        $CommandArgs += "--force"
    }

    python @CommandArgs
} else {
    Write-Host "To ask Codex to generate real converted images for every entry, run:"
    Write-Host ".\skills\batch-image-converter\local\run_batch_converter.ps1 -Execute"
    Write-Host ""
    Write-Host "For a small first test, run:"
    Write-Host ".\skills\batch-image-converter\local\run_batch_converter.ps1 -Execute -Limit 3"
}
