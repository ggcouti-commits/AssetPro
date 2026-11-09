$ErrorActionPreference = 'Stop'
$appPath = 'C:\Users\Asus\Projects\AssetPro\.canvas\desktop-gas-modulo\App.pa.yaml'
$catPath = 'C:\Users\Asus\Projects\AssetPro\docs\powerfx\catalogos-gas.txt'
$app = Get-Content $appPath -Raw -Encoding UTF8
if ($app -match 'colGasSegmento') { Write-Host 'Already injected'; exit 0 }
$cat = Get-Content $catPath -Encoding UTF8 | Where-Object { $_ -notmatch '^//' -and $_.Trim().Length -gt 0 }
$indented = ($cat | ForEach-Object { if ($_ -match '^\s*$') { '' } else { '      ' + $_.TrimEnd() } }) -join "`r`n"
$pattern = '(ClearCollect\(colTabelasCatalogo, TabelasCatalogo\);\r?\n)'
if ($app -notmatch $pattern) { throw 'No insertion point (colTabelasCatalogo)' }
$app2 = [regex]::Replace($app, $pattern, [System.Text.RegularExpressions.MatchEvaluator]{
    param($m)
    return $m.Groups[1].Value + "`r`n" + $indented + "`r`n`r`n"
}, 1)
[System.IO.File]::WriteAllText($appPath, $app2, [System.Text.UTF8Encoding]::new($false))
Write-Host 'Desktop catalogs injected'
