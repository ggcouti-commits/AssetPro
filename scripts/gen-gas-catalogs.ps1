$ErrorActionPreference = 'Stop'
$rows = Get-Content 'C:\Users\Asus\Projects\AssetPro\docs\bases\gas-lista\lista-wide.tsv' -Encoding UTF8
function Get-Cols($line) { return ,($line -split "`t") }

# Column indices from header (0-based) by scanning first row labels
$h = Get-Cols $rows[0]
function FindCol([string]$label) {
    for ($i = 0; $i -lt $h.Count; $i++) {
        if ($h[$i] -and ($h[$i].Trim() -eq $label -or $h[$i].Trim().StartsWith($label))) { return $i }
    }
    return -1
}

# Fixed positions from earlier layout (blank cols between)
# B=1 TIPO, D=3 COD MUN, E=4 MUNICIPIO, G=6 TUC, H=7 Desc UC, I=8 Tipo,
# K=10 DIAMETRO, M=12 PRESSAO, O=14 TRAMO, Q=16 DESC RESUMIDA, S=18 UM, U=20 ELEGIVEL, W=22 RESERVA
$iTipo = 1; $iCodMun = 3; $iMun = 4; $iTuc = 6; $iTucDesc = 7; $iTucTipo = 8
$iDiam = 10; $iPress = 12; $iTramo = 14; $iDesc = 16; $iUm = 18; $iEleg = 20; $iRes = 22

$seg = [System.Collections.Generic.HashSet[string]]::new()
$mun = New-Object System.Collections.Generic.List[object]
$tuc = New-Object System.Collections.Generic.List[object]
$diam = [System.Collections.Generic.HashSet[string]]::new()
$press = [System.Collections.Generic.HashSet[string]]::new()
$tramo = [System.Collections.Generic.HashSet[string]]::new()
$desc = [System.Collections.Generic.HashSet[string]]::new()
$um = [System.Collections.Generic.HashSet[string]]::new()

foreach ($line in $rows | Select-Object -Skip 1) {
    $c = Get-Cols $line
    if ($c.Count -le $iTipo) { continue }
    if ($c[$iTipo]) { [void]$seg.Add($c[$iTipo].Trim()) }
    if ($c[$iCodMun] -or $c[$iMun]) {
        $mun.Add([pscustomobject]@{ Codigo = $c[$iCodMun].Trim(); Nome = $c[$iMun].Trim() })
    }
    if ($c[$iTuc]) {
        $tuc.Add([pscustomobject]@{ Codigo = $c[$iTuc].Trim(); Descricao = $c[$iTucDesc].Trim(); Tipo = $c[$iTucTipo].Trim() })
    }
    if ($c[$iDiam]) { [void]$diam.Add($c[$iDiam].Trim()) }
    if ($c[$iPress]) { [void]$press.Add($c[$iPress].Trim()) }
    if ($c[$iTramo]) { [void]$tramo.Add($c[$iTramo].Trim()) }
    if ($c.Count -gt $iDesc -and $c[$iDesc]) { [void]$desc.Add($c[$iDesc].Trim()) }
    if ($c.Count -gt $iUm -and $c[$iUm]) { [void]$um.Add($c[$iUm].Trim()) }
}

function Esc([string]$s) { return ($s -replace '"', '""') }

$sb = New-Object System.Text.StringBuilder
[void]$sb.AppendLine('// Catálogos gás — Bahiagás (aba LISTA Base Modelo Gas Canalizado)')
[void]$sb.AppendLine('// Locale Studio ao vivo: vírgula. Colar no App.OnStart após colLocalInstalacao.')
[void]$sb.AppendLine()

function Emit-Simple($name, $items, $field) {
    [void]$script:sb.AppendLine("ClearCollect(")
    [void]$script:sb.AppendLine("    $name,")
    $arr = @($items | Where-Object { $_ } | Sort-Object)
    for ($i = 0; $i -lt $arr.Count; $i++) {
        $comma = if ($i -lt $arr.Count - 1) { ',' } else { '' }
        [void]$script:sb.AppendLine(('    {{{0}: "{1}"}}{2}' -f $field, (Esc $arr[$i]), $comma))
    }
    [void]$script:sb.AppendLine(');')
    [void]$script:sb.AppendLine()
}

Emit-Simple 'colGasSegmento' $seg 'Valor'
Emit-Simple 'colGasDiametro' $diam 'Valor'
Emit-Simple 'colGasClassePressao' $press 'Valor'
Emit-Simple 'colGasTramo' $tramo 'Valor'
if ($um.Count -eq 0) {
    Emit-Simple 'colGasUM' @('UN','CJ','M','M²') 'Valor'
} else {
    Emit-Simple 'colGasUM' $um 'Valor'
}
Emit-Simple 'colGasElegivel' @('SIM','NÃO') 'Valor'
Emit-Simple 'colGasReserva' @('SIM','NÃO') 'Valor'
Emit-Simple 'colGasDescResumida' $desc 'Valor'

[void]$sb.AppendLine('ClearCollect(')
[void]$sb.AppendLine('    colGasMunicipio,')
$mi = 0
foreach ($m in ($mun | Sort-Object Codigo)) {
    if (-not $m.Codigo -and -not $m.Nome) { continue }
    $mi++
}
$idx = 0
foreach ($m in ($mun | Sort-Object { [int]($_.Codigo) })) {
    if (-not $m.Codigo -and -not $m.Nome) { continue }
    $idx++
    $comma = if ($idx -lt $mi) { ',' } else { '' }
    [void]$sb.AppendLine(('    {{Codigo: "{0}", Nome: "{1}", Resumo: "{0} - {1}"}}{2}' -f (Esc $m.Codigo), (Esc $m.Nome), $comma))
}
[void]$sb.AppendLine(');')
[void]$sb.AppendLine()

[void]$sb.AppendLine('ClearCollect(')
[void]$sb.AppendLine('    colGasUC,')
$ti = ($tuc | Where-Object { $_.Codigo }).Count
$idx = 0
foreach ($t in ($tuc | Sort-Object { [int]($_.Codigo) })) {
    if (-not $t.Codigo) { continue }
    $idx++
    $comma = if ($idx -lt $ti) { ',' } else { '' }
    [void]$sb.AppendLine(('    {{Codigo: "{0}", Descricao: "{1}", Tipo: "{2}", Resumo: "{0} - {1}"}}{3}' -f (Esc $t.Codigo), (Esc $t.Descricao), (Esc $t.Tipo), $comma))
}
[void]$sb.AppendLine(');')

$out = 'C:\Users\Asus\Projects\AssetPro\docs\powerfx\catalogos-gas.txt'
[System.IO.File]::WriteAllText($out, $sb.ToString(), [System.Text.UTF8Encoding]::new($false))
Write-Host "Wrote $out"
Write-Host "seg=$($seg.Count) mun=$($mun.Count) tuc=$($tuc.Count) diam=$($diam.Count) press=$($press.Count) tramo=$($tramo.Count) desc=$($desc.Count) um=$($um.Count)"
