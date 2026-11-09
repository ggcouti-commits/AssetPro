# Tela_EditarItem — UI Dados Técnicos

> Padrão: igual aos cards Quantidade / TUC / A1  
> Locale: **PT-BR** (`;` e `;;`)  
> Posição: dentro de `cCardsAtributos`, **depois** de `cCardClassificacao` (TUC), **antes** de `cCardA1`

---

## 1b. Unidade no card de Quantidade (sem card separado)

Quantidade e unidade medida ficam **no mesmo card** — ex.: `3 UN`, `12 M`.

**Layout do `Container46` (campo):**

```
[inpQuantidade] [drpUnidadeItem] [lblDiverge]
```

| Controle | Propriedade | Fórmula |
|----------|-------------|---------|
| `Text23` (base) | Text | `="base: " & varItemFoto.Quantidade & " " & Coalesce(varItemFoto.Unidade; "—")` |
| `inpQuantidade` | Default | `=Coalesce(varQuantidade; varItemFoto.Quantidade)` |
| `inpQuantidade` | OnChange | `Set(varQuantidade; Value(Self.Text))` |
| `inpQuantidade` | Width | `=Parent.Width - drpUnidadeItem.Width - lblDiverge.Width - 6` |
| `drpUnidadeItem` | **Tipo** | **ModernDropdown** (menu suspenso) |
| `drpUnidadeItem` | Items | `colUnidadeMedida` (coleção inteira, **não** `.Unidade`) |
| `drpUnidadeItem` | ItemDisplayText | `ThisItem.Unidade` |
| `drpUnidadeItem` | Default | `LookUp(colUnidadeMedida; Unidade = Trim(Upper(varUnidadeItem)))` |
| `drpUnidadeItem` | OnChange | `Set(varUnidadeItem; Self.Selected.Unidade)` |
| `drpUnidadeItem` | Width | `=100` |

> `Default` do Dropdown moderno espera **um registro do mesmo schema de `Items`** — não um texto.
> Por isso `varUnidadeItem` sozinho dá *"Esperado um valor compatível com 'Items'"*, e `{Unidade: varUnidadeItem}`
> passa na validação mas não seleciona (registro sintético, não pertence a `Items`). Use `LookUp`.
| `lblDiverge` | Text | ver abaixo |
| `lblDiverge` | Color | `If(/* confere */; Cor.Success; Cor.Delete)` |

**`lblDiverge.Text`:**

```powerfx
If(
    Value(inpQuantidade.Text) = varItemFoto.Quantidade
    && varUnidadeItem = varItemFoto.Unidade;
    "confere";
    "diverge"
)
```

**`colUnidadeMedida` no `App.OnStart`:**

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

**Não confundir** `varUnidadeItem` / `Inventario.Unidade` com `Unidade`/`UnidadeAlt` dos atributos ANEEL (kV, kVA).

---

## 1. Título da seção

Inserir **acima** dos cards técnicos (mesmo nível de `Text21_1` “BASE CONTÁBIL × CAMPO”):

| Controle | Tipo | Text |
|----------|------|------|
| `TextDadosTecnicos` | ModernText | `"DADOS TÉCNICOS DO EQUIPAMENTO"` |

Propriedades iguais ao `Text21_1`: Color `Cor.NeutralL30`, Size 22, PaddingLeft 25, FontWeight Semibold.

---

## 2. Cards — um por campo

Cada card segue o template:

- **Height:** `106+40` (146) — observações usa `106+80` ou `MinHeight` maior
- **Fill:** `Cor.BackgroundStandard`
- **Border:** 1, `Cor.Border`, Radius 15
- **Topo:** rótulo à esquerda + `"base: …"` à direita
- **Campo:** `ModernTextInput` ou `ModernCombobox` largura total

### 2.1 Fabricante — `cCardFabricante`

| Controle | Propriedade | Fórmula |
|----------|-------------|---------|
| `lblFabricante` | Text | `"Fabricante"` |
| `lblFabricanteBase` | Text | `="base: " & Coalesce(varItemFoto.Fabricante; "—")` |
| `inpFabricante` | Default | `=varFabricante` |
| `inpFabricante` | Placeholder | `"Informe o fabricante"` |
| `inpFabricante` | OnChange | `Set(varFabricante; Self.Text)` |
| `inpFabricante` | Width | `=Parent.Width - Self.X * 2` |

### 2.2 Modelo — `cCardModelo`

| Controle | Propriedade | Fórmula |
|----------|-------------|---------|
| `lblModeloBase` | Text | `="base: " & Coalesce(varItemFoto.Modelo; "—")` |
| `inpModelo` | Default | `=varModelo` |
| `inpModelo` | OnChange | `Set(varModelo; Self.Text)` |

### 2.3 Nº de série — `cCardNumSerie`

| Controle | Propriedade | Fórmula |
|----------|-------------|---------|
| `lblNumSerie` | Text | `"Nº de série"` |
| `lblNumSerieBase` | Text | `="base: " & Coalesce(varItemFoto.NumSerie; "—")` |
| `inpNumSerie` | Default | `=varNumSerie` |
| `inpNumSerie` | OnChange | `Set(varNumSerie; Self.Text)` |

### 2.4 Cód. operação — `cCardCodOperacao`

SAP/Excel traz coluna **vazia** — o técnico preenche em campo.

| Controle | Propriedade | Fórmula |
|----------|-------------|---------|
| `lblCodOperacao` | Text | `"Cód. operação"` |
| `lblCodOperacaoBase` | Text | `If(IsBlank(varItemFoto.CodOperacao); "base: —"; "base: " & varItemFoto.CodOperacao)` |
| `inpCodOperacao` | Default | `=varCodOperacao` |
| `inpCodOperacao` | Placeholder | `"Código lido em campo (plaqueta/painel)"` |
| `inpCodOperacao` | OnChange | `Set(varCodOperacao; Self.Text)` |

### 2.5 Centro modular — `cCardCM`

Coluna **`Inventario.CM`** (já existe, **número 0–9**). Catálogo estático `colCentroModular` no `App.OnStart` — sem lista SharePoint. Nomes **curtos** (reunião 08.09). Sem texto de composição na tela.

Não usar `gblSEselecionada.CM` — CM MCPSE é do equipamento. Arranjo / local são da SE.

| Controle | Tipo | Propriedade | Fórmula |
|----------|------|-------------|---------|
| `lblCM` | ModernText | Text | `"Centro modular"` |
| `lblCMBase` | ModernText | Text | ver `Tela_EditarItem-formulas.txt` |
| `drpCM` | **ModernDropdown** | Items | `colCentroModular` |
| `drpCM` | | ItemDisplayText | `ThisItem.Codigo & " — " & ThisItem.Nome` |
| `drpCM` | | Default | `LookUp(colCentroModular; Codigo = varCM)` |
| `drpCM` | | OnChange | `Set(varCM; Self.Selected.Codigo)` |
| `lblCMDesc` | ModernText | Visible | `false` |

Se o card ainda tiver `inpCM` (texto), **apaga** e coloca o Dropdown.

Posição: **primeiro da seção Dados técnicos** — depois de `cCardClassificacao` (e do título, se existir), **antes** de `cCardFabricante`.

### 2.6 Ano — `cCardAno`

Duplicar `cCardQuantidade` (input numérico).

| Controle | Propriedade | Fórmula |
|----------|-------------|---------|
| `lblAno` | Text | `"Ano"` |
| `lblAnoBase` | Text | `If(IsBlank(varItemFoto.Ano); "base: —"; "base: " & Text(varItemFoto.Ano; "0000"))` |
| `inpAno` | Default | `=If(IsBlank(varAno); ""; Text(varAno; "0000"))` |
| `inpAno` | Placeholder | `"Ex.: 2018"` |
| `inpAno` | Format | `Number` (teclado numérico) |
| `inpAno` | OnChange | ver `Tela_EditarItem-formulas.txt` |
| `lblAnoDiverge` | Text (opcional) | `If(Value(inpAno.Text) = varItemFoto.Ano; "confere"; "diverge")` |
| `lblAnoDiverge` | Visible | `!IsBlank(inpAno.Text) && IsNumeric(inpAno.Text) && !IsBlank(varItemFoto.Ano)` |

Posição sugerida: **depois** de `cCardCM`, **antes** de `cCardObservacoes`.

### 2.7 Observações — `cCardObservacoes`

| Controle | Propriedade | Fórmula |
|----------|-------------|---------|
| `lblObservacoes` | Text | `"Observações de campo"` |
| `inpObservacoes` | Mode | `Multiline` |
| `inpObservacoes` | Height | `80` (container campo ~106) |
| `inpObservacoes` | Default | `=varObservacoes` |
| `inpObservacoes` | Placeholder | `"Ex.: plaqueta ilegível, dados lidos do painel"` |
| `inpObservacoes` | OnChange | `Set(varObservacoes; Self.Text)` |

Sem label `base:` — observações são sempre novas anotações de campo.

---

## 3. OnVisible — bloco completo (adicionar)

Depois dos `Set(varA1…varA6)` e **antes** dos `Reset` dos combos A1–A6:

```powerfx
Set(varFabricante; Coalesce(varRegistroAtual.Fabricante; varItemFoto.Fabricante; ""));;
Set(varModelo; Coalesce(varRegistroAtual.Modelo; varItemFoto.Modelo; ""));;
Set(varNumSerie; Coalesce(varRegistroAtual.NumSerie; varItemFoto.NumSerie; ""));;
Set(varCodOperacao; Coalesce(varRegistroAtual.CodOperacao; varItemFoto.CodOperacao; ""));;
Set(varCM; Coalesce(varRegistroAtual.CM; varItemFoto.CM; Blank()));;
Set(varAno; Coalesce(varRegistroAtual.Ano; varItemFoto.Ano; Blank()));;
Set(varUnidadeItem; Coalesce(varRegistroAtual.Unidade; varItemFoto.Unidade; ""));;
Set(varObservacoes; Coalesce(varRegistroAtual.Observacoes; varItemFoto.Observacoes; ""));;
Set(varIdUC; Coalesce(varRegistroAtual.IdUC; varItemFoto.IdUC; ""));;

Reset(inpFabricante);;
Reset(inpModelo);;
Reset(inpNumSerie);;
Reset(inpCodOperacao);;
Reset(drpCM);;
Reset(inpAno);;
Reset(drpUnidadeItem);;
Reset(inpObservacoes)
```

---

## 4. cmbTUC.OnChange — zerar dados técnicos ao trocar TUC

No final do OnChange existente, adicionar:

```powerfx
Set(varFabricante; Blank());;
Set(varModelo; Blank());;
Set(varNumSerie; Blank());;
Set(varCodOperacao; Blank());;
Set(varCM; Blank());;
Set(varAno; Blank());;
Set(varUnidadeItem; Blank());;
Set(varObservacoes; Blank());;

Reset(inpFabricante);;
Reset(inpModelo);;
Reset(inpNumSerie);;
Reset(inpCodOperacao);;
Reset(drpCM);;
Reset(inpAno);;
Reset(drpUnidadeItem);;
Reset(inpObservacoes)
```

(Opcional: se quiser **manter** dados técnicos ao só mudar TUC, não zere — só zere atributos A1–A6.)

---

## 5. Ordem final do scroll (`cCardsAtributos`)

```
1. cCardQuantidade
2. cCardClassificacao (cmbTUC)
3. TextDadosTecnicos          ← título da seção
4. cCardCM                    ← primeiro da seção
5. cCardFabricante
6. cCardModelo
7. cCardNumSerie
8. cCardCodOperacao
9. cCardAno
10. cCardObservacoes
11. cCardA1 … cCardA6

(Unidade de medida: **dentro** de `cCardQuantidade`, **Dropdown** `drpUnidadeItem` — sem card próprio.)
```

---

## 6. Checklist Studio

- [ ] Refresh conector `Inventario`
- [ ] `colUnidadeMedida` no OnStart
- [ ] **`drpUnidadeItem` (Dropdown) dentro de `cCardQuantidade`** (sem card de unidade)
- [ ] 7 cards técnicos + título na tela (inclui `cCardCM`)
- [ ] OnVisible + Resets
- [ ] Salvar (`Tela_EditarItem`, botão verde Salvar — **não** `Image6_48`) — já em `Tela_EditarItem-formulas.txt`
- [ ] Testar: editar → Salvar → reabrir → valores nos inputs

---

## 7. Atalho — duplicar card no Studio

1. Selecione `cCardQuantidade` → **Ctrl+C / Ctrl+V**
2. Renomeie para `cCardFabricante`
3. Troque rótulos, `inpQuantidade` → `inpFabricante`, remova `lblDiverge`
4. Repita para os outros campos

Isso mantém padding, borda e layout idênticos ao resto da tela.
