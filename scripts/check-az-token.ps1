$ErrorActionPreference = 'Continue'
Write-Host 'az account:'
az account show --query '{name:name,user:user.name}' -o json 2>&1 | Out-Host

Write-Host '--- SP token length ---'
$sp = az account get-access-token --resource 'https://gustavogarciacoutinho991.sharepoint.com' -o json 2>&1
Write-Host $sp

Write-Host '--- Graph token length ---'
$g = az account get-access-token --resource 'https://graph.microsoft.com' -o json 2>&1
Write-Host $g
