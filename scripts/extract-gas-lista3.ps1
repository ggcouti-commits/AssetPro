$ErrorActionPreference = 'Stop'
$path = 'C:\Users\Asus\OneDrive\Desktop\Power Apps\AssetPro\Base Modelo Gas Canalizado.xlsx'
$outDir = 'C:\Users\Asus\Projects\AssetPro\docs\bases\gas-lista'
Add-Type -AssemblyName System.IO.Compression.FileSystem
$zip = [System.IO.Compression.ZipFile]::OpenRead($path)
function Read-EntryXml([string]$fullName) {
    $e = $zip.Entries | Where-Object { $_.FullName -eq $fullName } | Select-Object -First 1
    $sr = New-Object System.IO.StreamReader($e.Open()); $txt = $sr.ReadToEnd(); $sr.Close(); [xml]$txt
}
$sharedXml = Read-EntryXml 'xl/sharedStrings.xml'
$ns = New-Object System.Xml.XmlNamespaceManager($sharedXml.NameTable)
$ns.AddNamespace('m', 'http://schemas.openxmlformats.org/spreadsheetml/2006/main')
$shared = @(); foreach ($si in $sharedXml.SelectNodes('//m:si', $ns)) {
    $shared += (($si.SelectNodes('.//m:t', $ns) | ForEach-Object { $_.InnerText }) -join '')
}
$sheet = Read-EntryXml 'xl/worksheets/sheet2.xml'
function ColName([int]$n) {
    $s = ''; while ($n -ge 0) { $s = [char](65 + ($n % 26)) + $s; $n = [math]::Floor($n / 26) - 1 }; $s
}
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
    $parts = 0..40 | ForEach-Object {
        $cn = ColName $_
        if ($map.ContainsKey($cn)) { $map[$cn] } else { '' }
    }
    $line = $parts -join "`t"
    if ($line.Trim().Length -gt 0) { $rowsOut.Add($line) }
}
$outFile = Join-Path $outDir 'lista-wide.tsv'
$rowsOut | Set-Content -Encoding UTF8 $outFile
Write-Host "rows=$($rowsOut.Count)"
Write-Host "HEADER:"
Write-Host $rowsOut[0]
$zip.Dispose()
