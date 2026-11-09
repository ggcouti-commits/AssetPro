$ErrorActionPreference = 'Stop'
$appPath = 'C:\Users\Asus\Projects\AssetPro\.canvas\mobile-gas-modulo\App.pa.yaml'
$catPath = 'C:\Users\Asus\Projects\AssetPro\docs\powerfx\catalogos-gas.txt'

$app = Get-Content $appPath -Raw -Encoding UTF8
$cat = Get-Content $catPath -Encoding UTF8 |
    Where-Object { $_ -notmatch '^//' -and $_.Trim().Length -gt 0 }

# Indent catalog lines for OnStart block (6 spaces)
$indented = ($cat | ForEach-Object {
    if ($_ -match '^\s*$') { '' } else { '      ' + $_.TrimEnd() }
}) -join "`r`n"

$marker = @'
      ClearCollect(
          colLocalInstalacao,
'@

# Find end of colLocalInstalacao block: after `);` that follows colLocalInstalacao
$pattern = '(?s)(ClearCollect\(\r?\n\s+colLocalInstalacao,.*?\r?\n\s+\);\r?\n)'
if ($app -notmatch $pattern) { throw 'colLocalInstalacao block not found' }

$replacement = $Matches[1] + "`r`n" + $indented + "`r`n`r`n"
$app2 = [regex]::Replace($app, $pattern, [System.Text.RegularExpressions.MatchEvaluator]{
    param($m)
    return $m.Groups[1].Value + "`r`n" + $indented + "`r`n`r`n"
}, 1)

if ($app2 -eq $app) { throw 'No change applied' }
# Avoid double-inject
if ($app -match 'colGasSegmento') { throw 'Already injected' }

[System.IO.File]::WriteAllText($appPath, $app2, [System.Text.UTF8Encoding]::new($false))
Write-Host 'Injected gas catalogs into App.OnStart'
Write-Host ("chars before=" + $app.Length + " after=" + $app2.Length)
