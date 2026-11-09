$ErrorActionPreference = 'Continue'
$json = az account get-access-token --resource 'https://gustavogarciacoutinho991.sharepoint.com' -o json | ConvertFrom-Json
$token = $json.accessToken
$siteUrl = 'https://gustavogarciacoutinho991.sharepoint.com/sites/AssetPro'
$headers = @{
    Authorization = "Bearer $token"
    Accept = 'application/json;odata=nometadata'
}

Write-Host 'Lists:'
try {
    $r = Invoke-RestMethod -Uri "$siteUrl/_api/web/lists?`$select=Title,Id&`$top=30" -Headers $headers -Method Get
    $r.value | ForEach-Object { Write-Host (" - " + $_.Title) }
} catch {
    Write-Host ("LIST ERR: " + $_.Exception.Message)
    if ($_.ErrorDetails) { Write-Host $_.ErrorDetails.Message }
}

Write-Host '--- Inventario fields sample ---'
try {
    $f = Invoke-RestMethod -Uri "$siteUrl/_api/web/lists/getbytitle('Inventario')/fields?`$select=InternalName,Title&`$top=5" -Headers $headers -Method Get
    $f.value | ForEach-Object { Write-Host (" - " + $_.InternalName) }
} catch {
    Write-Host ("FIELD ERR: " + $_.Exception.Message)
    if ($_.ErrorDetails) { Write-Host $_.ErrorDetails.Message }
}
