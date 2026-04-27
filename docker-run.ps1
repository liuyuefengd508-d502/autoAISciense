# Start the AI-Scientist HTR container.
# - Mounts the repo at /workspace
# - Passes API keys & OpenAI-compatible proxy URL via env vars
#
# Set the following env vars in your PowerShell session BEFORE running:
#   $Env:OPENAI_API_KEY = "sk-..."
#   $Env:OPENAI_BASE_URL = "http://shareapi.cloud/"     # optional, defaults below
#   $Env:OPENALEX_MAIL_ADDRESS = "you@example.com"
$ErrorActionPreference = "Stop"

$imageName = "ai-scientist-htr-cpu:latest"

if (-not $Env:OPENAI_API_KEY) {
    Write-Warning "OPENAI_API_KEY is not set. The LLM calls will fail."
}

$baseUrl = $Env:OPENAI_BASE_URL
if (-not $baseUrl) { $baseUrl = "http://shareapi.cloud/" }

$mail = $Env:OPENALEX_MAIL_ADDRESS
if (-not $mail) { $mail = "you@example.com" }

# Aider reads OPENAI_API_BASE; openai SDK reads OPENAI_BASE_URL. Set both.
docker run --rm -it `
    -e OPENAI_API_KEY=$Env:OPENAI_API_KEY `
    -e OPENAI_BASE_URL=$baseUrl `
    -e OPENAI_API_BASE=$baseUrl `
    -e OPENALEX_MAIL_ADDRESS=$mail `
    -v "${PWD}:/workspace" `
    -w /workspace `
    $imageName bash
