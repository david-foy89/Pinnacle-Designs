# Enable Cloudflare Google Tag Gateway for pinnacle-designs.com
# Requires a Cloudflare API token with Zone:Edit permission.
#
# Usage:
#   $env:CLOUDFLARE_API_TOKEN = "your_token_here"
#   .\scripts\configure-cloudflare-gtag-gateway.ps1
#
# Or create the token at: Cloudflare Dashboard → My Profile → API Tokens

$ZoneId = "c26951ac3b07f630d0862e8eefebd476"
$ApiUrl = "https://api.cloudflare.com/client/v4/zones/$ZoneId/settings/google-tag-gateway/config"

if (-not $env:CLOUDFLARE_API_TOKEN) {
  Write-Error "Set CLOUDFLARE_API_TOKEN first. Example: `$env:CLOUDFLARE_API_TOKEN = 'your_token'"
  exit 1
}

$body = @{
  enabled        = $true
  endpoint       = "/metrics"
  hideOriginalIp = $true
  measurementId  = "G-Y3XVJXG5KW"
  setUpTag       = $true
} | ConvertTo-Json

$headers = @{
  Authorization = "Bearer $env:CLOUDFLARE_API_TOKEN"
  "Content-Type" = "application/json"
}

Write-Host "Enabling Google Tag Gateway for G-Y3XVJXG5KW at /metrics ..."
$response = Invoke-RestMethod -Method Put -Uri $ApiUrl -Headers $headers -Body $body

if ($response.success) {
  Write-Host "Success. Gateway enabled:"
  $response.result | ConvertTo-Json
  Write-Host ""
  Write-Host "Next steps:"
  Write-Host "  1. Visit https://pinnacle-designs.com/ (disable ad blockers)"
  Write-Host "  2. Check GA4 Realtime report"
  Write-Host "  3. View page source — Cloudflare should inject first-party tag at /metrics"
} else {
  Write-Error ($response.errors | ConvertTo-Json -Depth 5)
  exit 1
}
