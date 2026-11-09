$ErrorActionPreference = 'Stop'
$path = 'C:\Users\Asus\OneDrive\Desktop\Power Apps\AssetPro\Base Modelo Gas Canalizado.xlsx'
$outDir = 'C:\Users\Asus\Projects\AssetPro\docs\bases\gas-lista'
New-Item -ItemType Directory -Force -Path $outDir | Out-Null

Add-Type -AssemblyName System.IO.Compression.FileSystem
$zip = [System.IO.Compression.ZipFile]::OpenRead($path)
$shared = $null
$sharedEntry = $zip.Entries | Where-Object { $_.FullName -eq 'xl/sharedStrings.xml' }
if ($sharedEntry) {
    $sr = New-Object System.IO.StreamReader($sharedEntry.Open())
    $sharedXml = [xml]$sr.ReadToEnd()
    $sr.Close()
    $ns = New-Object System.Xml.XmlNamespaceManager($sharedXml.NameTable)
    $ns.AddNamespace('m', 'http://schemas.openxmlformats.org/spreadsheetml/2006/main')
    $shared = @()
    foreach ($si in $sharedXml.SelectNodes('//m:si', $ns)) {
        $t = ($si.SelectNodes('.//m:t', $ns) | ForEach-Object { $_.InnerText }) -join ''
        $shared += $t
    }
}

function Get-SheetRows($sheetPath) {
    $entry = $zip.Entries | Where-Object { $_.FullName -eq $sheetPath }
    if (-not $entry) { return @() }
    $sr = New-Object System.IO.StreamReader($entry.Open())
    $xml = [xml]$sr.ReadToEnd()
    $sr.Close()
    $ns = New-Object System.Xml.XmlNamespaceManager($xml.NameTable)
    $ns.AddNamespace('m', 'http://schemas.openxmlformats.org/spreadsheetml/2006/main')
    $rows = @()
    foreach ($row in $xml.SelectNodes('//m:sheetData/m:row', $ns)) {
        $cells = @{}
        foreach ($c in $row.SelectNodes('m:c', $ns)) {
            $ref = $c.GetAttribute('r')
            $col = ($ref -replace '[0-9]', '')
            $vNode = $c.SelectSingleNode('m:v', $ns)
            $val = if ($vNode) { $vNode.InnerText } else { '' }
            if ($c.GetAttribute('t') -eq 's' -and $shared) {
                $val = $shared[[int]$val]
            }
            $cells[$col] = $val
        }
        $rows += ,$cells
    }
    return $rows
}

# Find sheet names
$wbEntry = $zip.Entries | Where-Object { $_.FullName -eq 'xl/workbook.xml' }
$sr = New-Object System.IO.StreamReader($wbEntry.Open())
$wb = [xml]$sr.ReadToEnd()
$sr.Close()
$ns = New-Object System.Xml.XmlNamespaceManager($wb.NameTable)
$ns.AddNamespace('m', 'http://schemas.openxmlformats.org/spreadsheetml/2006/main')
$ns.AddNamespace('r', 'http://schemas.openxmlformats.org/officeDocument/2006/relationships')
Write-Host 'Sheets:'
$wb.SelectNodes('//m:sheets/m:sheet', $ns) | ForEach-Object {
    Write-Host (" - " + $_.GetAttribute('name') + " rId=" + $_.GetAttribute('id'))
}

# workbook relationships for sheet paths
$relEntry = $zip.Entries | Where-Object { $_.FullName -eq 'xl/_rels/workbook.xml.rels' }
$sr = New-Object System.IO.StreamReader($relEntry.Open())
$rels = [xml]$sr.ReadToEnd()
$sr.Close()
$rns = New-Object System.Xml.XmlNamespaceManager($rels.NameTable)
$rns.AddNamespace('r', 'http://schemas.openxmlformats.org/package/2006/relationships')
$idToTarget = @{}
foreach ($rel in $rels.SelectNodes('//r:Relationship', $rns)) {
    $idToTarget[$rel.GetAttribute('Id')] = $rel.GetAttribute('Target')
}

$listaSheet = $wb.SelectNodes('//m:sheets/m:sheet', $ns) | Where-Object { $_.GetAttribute('name') -match 'LISTA' } | Select-Object -First 1
if (-not $listaSheet) { throw 'LISTA sheet not found' }
$rid = $listaSheet.GetAttribute('id')
$target = $idToTarget[$rid]
if ($target -notlike 'worksheets/*') { $target = 'worksheets/' + ($target -replace '^/','') }
if ($target -notlike 'xl/*') { $sheetPath = 'xl/' + $target.TrimStart('/') } else { $sheetPath = $target.TrimStart('/') }
Write-Host "LISTA path: $sheetPath"

$rows = Get-SheetRows $sheetPath
Write-Host ("LISTA rows: " + $rows.Count)
# dump first 80 rows as CSV-like
$lines = @()
foreach ($r in $rows | Select-Object -First 120) {
    $cols = 'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P'
    $parts = foreach ($c in $cols) { if ($r.ContainsKey($c)) { $r[$c] } else { '' } }
    $lines += ($parts -join "`t")
}
$lines | Set-Content -Encoding UTF8 (Join-Path $outDir 'lista-raw.tsv')
Write-Host "Wrote $($lines.Count) lines to lista-raw.tsv"
$zip.Dispose()
