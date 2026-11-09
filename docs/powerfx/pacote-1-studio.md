# Pacote 1 — Studio (Salvar + offline + sync)

> Fenômeno · ordem de aplicação no Power Apps Studio  
> Fórmulas completas em `Tela_EditarItem-formulas.txt`

## Passo 0 — Conector (obrigatório)

1. **Dados** → `Inventario` → **Atualizar** (refresh)
2. Confirmar colunas: `AtributoA1`…`AtributoA6`, `CodOperacao`, **`CM`**, **`Ano`**, `Fabricante`, `Modelo`, `NumSerie`, `Unidade`, `Observacoes`

> Se o cache local antigo não tiver as colunas novas, limpe dados do app no celular ou rode uma vez com `Clear(colCampoOffline)` antes do `LoadData`.

---

## Passo 1 — `App.OnStart`

Substituir schemas de `colInventarioBase` e `colCampoOffline` — `docs/powerfx/schema-inventario.txt` (todas as colunas da lista `Inventario`).

Campos novos em `colCampoOffline`:
- `AtributoA1`…`AtributoA6` (no lugar de A1…A6)
- `Fabricante`, `Modelo`, `NumSerie`, `CodOperacao`, **`CM`**, **`Ano`**, `Unidade`

**Lista fixa de unidades** (cole **depois** das tabelas mestres, ex. após `colLookup`):

```powerfx
ClearCollect(
    colUnidadeMedida;
    {Unidade: "UN"; Rotulo: "UN - Unidade"};
    {Unidade: "PC"; Rotulo: "PC - Peça"};
    {Unidade: "M"; Rotulo: "M - Metro"};
    {Unidade: "M2"; Rotulo: "M² - Metro quadrado"};
    {Unidade: "KG"; Rotulo: "KG - Quilograma"}
);;
```

Não precisa de `SaveData` — são 5 linhas fixas, recriadas a cada abertura do app.

**Lista fixa de centros modulares** (cole **depois** de `colUnidadeMedida`):

Ver `docs/powerfx/catalogos-mcpse.txt`. Sem `SaveData`. `Inventario.CM` = `Codigo` (0–9). Nome curto na tela; `lblCMDesc` oculto.

Na mesma cola: `colArranjoFisico` (SE, 1–5), `colLocalInstalacao` (SE, 0–4) e `colTipoInstalacao` (TI do local). Dropdown na visita só quando `Subestacoes.TI` vier em branco — quem preenche é o inventariante (André, 05.10.2026).

---

## Passo 2 — `Tela_EditarItem` → botão **Salvar** (`OnSelect`)

Colar fórmula da seção **Tela_EditarItem — botão Salvar** em `Tela_EditarItem-formulas.txt`.

`Image6_48` no Studio atual é o **Cancelar** do overlay de exclusão de sobra (`Tela_ItensVisita`) — não é o Salvar.

Usa:
- `varA1`…`varA6` (valores editados)
- `varFabricante`, `varModelo`, `varNumSerie`, `varCodOperacao`, **`varCM`**, **`varAno`**, `varUnidadeItem`, `varObservacoes`
- `inpQuantidade` (não `txtQuantidade`)

---

## Passo 3 — `Tela_EditarItem.OnVisible`

**3a — Início (se ainda não tiver):** `varRegistroAtual` via `LookUp` em `colCampoOffline` — ver `Tela_EditarItem-formulas.txt` seção **OnVisible — início**.

**3b — Vars dados técnicos** (final do OnVisible, antes de `Set(varCarregando; false)`):

```powerfx
Set(varFabricante; Coalesce(varRegistroAtual.Fabricante; varItemFoto.Fabricante; ""));;
Set(varModelo; Coalesce(varRegistroAtual.Modelo; varItemFoto.Modelo; ""));;
Set(varNumSerie; Coalesce(varRegistroAtual.NumSerie; varItemFoto.NumSerie; ""));;
Set(varCodOperacao; Coalesce(varRegistroAtual.CodOperacao; varItemFoto.CodOperacao; ""));;
Set(varCM; Coalesce(varRegistroAtual.CM; varItemFoto.CM; Blank()));;
Set(varAno; Coalesce(varRegistroAtual.Ano; varItemFoto.Ano; Blank()));;
Set(varUnidadeItem; Coalesce(varRegistroAtual.Unidade; varItemFoto.Unidade; ""));;
Set(varObservacoes; Coalesce(varRegistroAtual.Observacoes; varItemFoto.Observacoes; ""));;
```

---

## Passo 3c — Cards técnicos: `OnChange` + `Default`

Sem `OnChange`, o que o técnico digita **não chega no Salvar**.

| Controle | Default | OnChange |
|----------|---------|----------|
| `inpFabricante` | `varFabricante` | `Set(varFabricante; Self.Text)` |
| `inpModelo` | `varModelo` | `Set(varModelo; Self.Text)` |
| `inpNumSerie` | `varNumSerie` | `Set(varNumSerie; Self.Text)` |
| `inpCodOperacao` | `varCodOperacao` | `Set(varCodOperacao; Self.Text)` |
| `drpCM` | `LookUp(colCentroModular; Codigo = varCM)` | `Set(varCM; Self.Selected.Codigo)` |
| `inpAno` | `If(IsBlank(varAno); ""; Text(varAno; "0000"))` | ver `formulas.txt` |
| `inpObservacoes` | `varObservacoes` | `Set(varObservacoes; Self.Text)` |
| `inpQuantidade` | `Coalesce(varQuantidade; varItemFoto.Quantidade)` | `Set(varQuantidade; Value(Self.Text))` |

Demais correções (rótulo de observações, `lblDiverge` com base vazia, bugs A5/A6): ver
`Tela_EditarItem-formulas.txt`, seções **Cards técnicos** e **Bugs pendentes**.

---

## Passo 4 — `Tela_Home` → Enviar visita (`btnEnviarVisitaExec`)

YAML 2026-09-03 ainda **não** manda `CM` no `Patch`. Incluir `CM: linhaAtual.CM` no bloco de **CONFIRMACAO** e no de **SOBRA/NOVO** (depois de `CodOperacao`).

**NAO_ENCONTRADO** — não precisa de `CM` (só Status / Sobra / ValidadoPor / Observacoes).

**Já ok no YAML:** `btnConfirmarBase` e `btnNaoEncontradoBase` passam `ThisItem.CM`.

---

## Passo 5 — UI dados técnicos (próxima sessão)

Seção **DADOS TÉCNICOS DO EQUIPAMENTO** — ver `docs/inventario-campos.md`.

Controles sugeridos → vars no `OnChange`:

| Controle | Var |
|----------|-----|
| `inpFabricante` | `varFabricante` |
| `inpModelo` | `varModelo` |
| `inpNumSerie` | `varNumSerie` |
| `inpCodOperacao` | `varCodOperacao` |
| `drpCM` | `varCM` (código 0–9) |
| `inpAno` | `varAno` |
| `inpObservacoes` | `varObservacoes` |

Unidade: **`drpUnidadeItem`** (Dropdown) dentro de **`cCardQuantidade`** (não card separado).

---

## Teste rápido

1. Abrir item da base com `CM` preenchido → dropdown deve vir selecionado
2. Trocar o CM no `drpCM` → Salvar → reabrir → valor persistido no offline
3. Confirmar rápido na lista (sem editar) → `colCampoOffline.CM` = CM da base
4. Finalizar SE → Enviar visita → conferir `Inventario.CM` no SharePoint

---

## Visita 2026-09-03 — sobra / finalizar / fotos

Fórmulas canônicas:

- Sobra na BASE + duplicar: `Tela_EditarItem-formulas.txt` seção **Visita 2026-09-03**
- Finalizar por Status + fotos só leitura: `Tela_FotosSE-formulas.txt` (`btnFinalizarSE.DisplayMode` e trava `varSETravada`)
