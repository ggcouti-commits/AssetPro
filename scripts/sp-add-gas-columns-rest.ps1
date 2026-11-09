$ErrorActionPreference = 'Stop'

# Try get token via Azure CLI (SharePoint)
$token = $null
try {
    $token = (az account get-access-token --resource https://gustavogarciacoutinho991.sharepoint.com --query accessToken -o tsv 2>$null)
} catch {}

if (-not $token) {
    Write-Host 'No az token. Trying Graph for Sites.ReadWrite.All via az graph...'
    try {
        $token = (az account get-access-token --resource https://graph.microsoft.com --query accessToken -o tsv 2>$null)
        if ($token) { Write-Host 'Have Graph token — will use Graph lists API' }
    } catch {}
}

if (-not $token) {
    Write-Host 'FAIL: no token. Run: az login'
    exit 1
}

$siteUrl = 'https://gustavogarciacoutinho991.sharepoint.com/sites/AssetPro'
$headers = @{
    Authorization = "Bearer $token"
    Accept = 'application/json;odata=verbose'
    'Content-Type' = 'application/json;odata=verbose'
}

function Add-SpTextField {
    param($ListTitle, $InternalName, $DisplayName)
    $checkUrl = "$siteUrl/_api/web/lists/getbytitle('$ListTitle')/fields?`$filter=InternalName eq '$InternalName'"
    $existing = Invoke-RestMethod -Uri $checkUrl -Headers $headers -Method Get
    if ($existing.d.results.Count -gt 0) {
        Write-Host "OK exists: $ListTitle.$InternalName"
        return
    }
    $body = @{
        __metadata = @{ type = 'SP.Field' }
        Title = $DisplayName
        FieldTypeKind = 2
        StaticName = $InternalName
        InternalName = $InternalName
        Required = $false
        MaxLength = 255
    } | ConvertTo-Json
    $addUrl = "$siteUrl/_api/web/lists/getbytitle('$ListTitle')/fields"
    try {
        Invoke-RestMethod -Uri $addUrl -Headers $headers -Method Post -Body $body | Out-Null
        Write-Host "ADDED: $ListTitle.$InternalName"
    } catch {
        Write-Host "ERR $ListTitle.$InternalName : $($_.Exception.Message)"
        if ($_.ErrorDetails) { Write-Host $_.ErrorDetails.Message }
    }
}

Write-Host 'Using SharePoint REST...'
Add-SpTextField 'Inventario' 'Diametro' 'Diâmetro'
Add-SpTextField 'Inventario' 'ClassePressao' 'Classe de pressão'
Add-SpTextField 'Inventario' 'Tramo' 'Tipo de tramo'
Add-SpTextField 'Inventario' 'Tag' 'TAG'
Add-SpTextField 'Inventario' 'DescricaoComplementar' 'Descrição técnica complementar'
Add-SpTextField 'Subestacoes' 'OSI' 'OSI'
Add-SpTextField 'Subestacoes' 'CodCI' 'Cód C.I.'
Add-SpTextField 'Subestacoes' 'Segmento' 'Segmento'
Write-Host 'DONE'
