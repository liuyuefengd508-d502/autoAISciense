# Build the CPU-only AI-Scientist image for the HTR research workflow.
# Run from the AI-Scientist repository root.
$ErrorActionPreference = "Stop"

$imageName = "ai-scientist-htr-cpu:latest"
Write-Host "Building $imageName ..." -ForegroundColor Cyan

docker build -f Dockerfile.htr-cpu -t $imageName .

if ($LASTEXITCODE -ne 0) {
    Write-Error "Docker build failed."
    exit 1
}

Write-Host "Done. Run .\docker-run.ps1 to start an interactive container." -ForegroundColor Green
