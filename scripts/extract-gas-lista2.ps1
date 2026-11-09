$ErrorActionPreference = 'Stop'
$path = 'C:\Users\Asus\OneDrive\Desktop\Power Apps\AssetPro\Base Modelo Gas Canalizado.xlsx'
$outDir = 'C:\Users\Asus\Projects\AssetPro\docs\bases\gas-lista'
New-Item -ItemType Directory -Force -Path $outDir | Out-Null

Add-Type -AssemblyName System.IO.Compression.FileSystem
$zip = [System.IO.Compression.ZipFile]::OpenRead($path)

function Read-EntryXml([string]$fullName) {
    $e = $zip.Entries | Where-Object { $_.FullName -eq $fullName } | Select-Object -First 1
    if (-not $e) { throw "Missing $fullName" }
    $sr = New-Object System.IO.StreamReader($e.Open())
    $txt = $sr.ReadToEnd()
    $sr.Close()
    return [xml]$txt
}

$sharedXml = Read-EntryXml 'xl/sharedStrings.xml'
$ns = New-Object System.Xml.XmlNamespaceManager($sharedXml.NameTable)
$ns.AddNamespace('m', 'http://schemas.openxmlformats.org/spreadsheetml/2006/main')
$shared = @()
foreach ($si in $sharedXml.SelectNodes('//m:si', $ns)) {
    $shared += (($si.SelectNodes('.//m:t', $ns) | ForEach-Object { $_.InnerText }) -join '')
}

$wb = Read-EntryXml 'xl/workbook.xml'
$rels = Read-EntryXml 'xl/_rels/workbook.xml.rels'
$rns = New-Object System.Xml.XmlNamespaceManager($rels.NameTable)
$rns.AddNamespace('pr', 'http://schemas.openxmlformats.org/package/2006/relationships')

$idToTarget = @{}
foreach ($rel in $rels.DocumentElement.ChildNodes) {
    if ($rel.LocalName -ne 'Relationship') { continue }
    $idToTarget[$rel.GetAttribute('Id')] = $rel.GetAttribute('Target')
}

$sheets = @()
foreach ($sh in $wb.SelectNodes('//m:sheets/m:sheet', $ns)) {
    $name = $sh.GetAttribute('name')
    $rid = $sh.Attributes.GetNamedItem('id', 'http://schemas.openxmlformats.org/officeDocument/2006/relationships').Value
    if (-not $rid) { $rid = $sh.GetAttribute('r:id') }
    $target = $idToTarget[$rid]
    Write-Host "Sheet=$name rid=$rid target=$target"
    $sheets += [pscustomobject]@{ Name = $name; Target = $target }
}

$lista = $sheets | Where-Object { $_.Name -eq 'LISTA' } | Select-Object -First 1
$sheetPath = 'xl/' + ($lista.Target -replace '^/+','')
Write-Host "Opening $sheetPath"

$sheet = Read-EntryXml $sheetPath
$rowsOut = New-Object System.Collections.Generic.List[string]
foreach ($row in $sheet.SelectNodes('//m:sheetData/m:row', $ns)) {
    $map = @{}
    foreach ($c in $row.SelectNodes('m:c', $ns)) {
        $ref = $c.GetAttribute('r')
        $col = ($ref -replace '[0-9]','')
        $v = $c.SelectSingleNode('m:v', $ns)
        $val = if ($v) { $v.InnerText } else { '' }
        if ($c.GetAttribute('t') -eq 's') { $val = $shared[[int]$val] }
        $map[$col] = $val
    }
    $cols = 65..80 | ForEach-Object { [char]$_ }  # A-P
    $line = ($cols | ForEach-Object { if ($map.ContainsKey([string]$_)) { $map[[string]$_] } else { '' } }) -join "`t"
    if ($line.Trim().Length -gt 0) { $rowsOut.Add($line) }
}

$outFile = Join-Path $outDir 'lista-raw.tsv'
$rowsOut | Set-Content -Encoding UTF8 $outFile
Write-Host "Wrote $($rowsOut.Count) rows -> $outFile"
$zip.Dispose()
