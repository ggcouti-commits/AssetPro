$ErrorActionPreference = 'Stop'
# Prefer PnP 2.x on PS 7.2 if 3.x not loadable
try {
    Import-Module PnP.PowerShell -ErrorAction Stop
} catch {
    Write-Host "PnP 3.x failed: $($_.Exception.Message)"
    Write-Host 'Trying Install-Module PnP.PowerShell 1.12 / 2.x ...'
    Install-Module PnP.PowerShell -Scope CurrentUser -RequiredVersion 2.12.0 -Force -AllowClobber -ErrorAction Stop
    Import-Module PnP.PowerShell -RequiredVersion 2.12.0 -Force
}

$site = 'https://gustavogarciacoutinho991.sharepoint.com/sites/AssetPro'
# PnP Management Shell multi-tenant app id (device/interactive)
$clientId = '31359c7f-bd69-4f18-a61c-9d8cbe3eaed3'

Write-Host "Connecting to $site ..."
Connect-PnPOnline -Url $site -Interactive -ClientId $clientId
Write-Host 'CONNECTED'

function Ensure-TextField {
    param(
        [string]$ListName,
        [string]$InternalName,
        [string]$DisplayName,
        [int]$MaxLength = 255
    )
    $existing = Get-PnPField -List $ListName -Identity $InternalName -ErrorAction SilentlyContinue
    if ($existing) {
        Write-Host "OK exists: $ListName.$InternalName"
        return
    }
    Add-PnPField -List $ListName -DisplayName $DisplayName -InternalName $InternalName -Type Text -AddToDefaultView | Out-Null
    Write-Host "ADDED: $ListName.$InternalName ($DisplayName)"
}

# Inventario — campos item gás
Ensure-TextField -ListName 'Inventario' -InternalName 'Diametro' -DisplayName 'Diâmetro'
Ensure-TextField -ListName 'Inventario' -InternalName 'ClassePressao' -DisplayName 'Classe de pressão'
Ensure-TextField -ListName 'Inventario' -InternalName 'Tramo' -DisplayName 'Tipo de tramo'
Ensure-TextField -ListName 'Inventario' -InternalName 'Tag' -DisplayName 'TAG'
Ensure-TextField -ListName 'Inventario' -InternalName 'DescricaoComplementar' -DisplayName 'Descrição técnica complementar' -MaxLength 255

# Subestacoes — campos local gás (Municipio já existe)
Ensure-TextField -ListName 'Subestacoes' -InternalName 'OSI' -DisplayName 'OSI'
Ensure-TextField -ListName 'Subestacoes' -InternalName 'CodCI' -DisplayName 'Cód C.I.'
Ensure-TextField -ListName 'Subestacoes' -InternalName 'Segmento' -DisplayName 'Segmento'

Write-Host 'DONE — refresh SharePoint connectors in Studio'
Disconnect-PnPOnline
