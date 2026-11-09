# `flxBaixarCampanha` — JSON da campanha (Mobile)

> Decisão 2026-09-16 (Fenômeno). **Baixar dados** não faz `ClearCollect` em `Inventario`.
> Delegação 2000 e ForAll SE a SE ficam lentos. O fluxo pagina no SharePoint (até 5000)
> e devolve JSON. O App monta `colInventarioBase` / `colSubestacoes` com `ParseJSON`.
>
> Site: `https://gustavogarciacoutinho991.sharepoint.com/sites/AssetPro`  
> App: `Tela_Home` → `btnBaixarDados` (Baixar dados) → `flxBaixarCampanha.Run(CodInventario)`
>
> Mesmo recorte do `flxExportarCampanha` no **Obter itens**: filtro `CodInventario`,
> paginação ligada. **Select** obrigatório — body cru do SharePoint estoura o `Respond`.

Renomeia cada ação **exatamente** como está em negrito.

**Uma vez no SharePoint:** índice em `Inventario.CodInventario` e `Subestacoes.CodInventario`
(lista já passa de 3.000; em 5.000 o filtro sem índice cai).

---

## Criar o fluxo

make.powerautomate.com → **Criar** → **Fluxo da nuvem instantâneo** → em branco.

Nome: `flxBaixarCampanha`

---

### 1. Gatilho — Power Apps (V2) — `Quando_o_Power_Apps`

Uma entrada **Texto** → nome `CodInventario`.

**Publicar.** Studio → Power Automate → adicionar `flxBaixarCampanha` → **⋯** → **Atualizar**.

---

### 2. Compor — `CodLimpo`

```
trim(coalesce(triggerBody()?['text'], ''))
```

Se o V2 expuser o nome da entrada, usa `trim(triggerBody()?['CodInventario'])`.

---

### 3. Condição — `TemCodigo`

```
not(empty(outputs('CodLimpo')))
```

é igual a `true`.

**Se não:**

#### 3a. Responder a um Power App — `Responder_SemCodigo`

Saídas (todas **Texto**), nesta ordem:

| Saída | Valor |
|-------|--------|
| erro | `CodInventario vazio` |
| jsonItens | `[]` |
| jsonSEs | `[]` |
| qtdItens | `0` |
| qtdSEs | `0` |

Encerrar.

**Se sim:** segue.

---

### 4. SharePoint — Obter itens — `Obter_SEs`

- Lista: **Subestacoes**
- Consulta de filtro:

```
CodInventario eq '@{outputs('CodLimpo')}'
```

**⋯** da ação → **Configurações** → **Paginação** = **Ligada**. Limite **100**.

---

### 5. SharePoint — Obter itens — `Obter_Itens`

- Lista: **Inventario**
- Consulta de filtro:

```
CodInventario eq '@{outputs('CodLimpo')}'
```

**⋯** → **Configurações** → **Paginação** = **Ligada**. Limite **5000**.

Sem isso o conector corta em 100 e o tablet fica com SE vazia.

---

### 6. Operação de dados — Selecionar — `SelecionarSEs`

De:

```
body('Obter_SEs')?['value']
```

Modo: **Mapa**. Chave = nome no App:

| Chave | Valor (fx) |
|-------|------------|
| ID | `item()?['ID']` |
| CodInventario | `item()?['CodInventario']` |
| CodSE | `item()?['CodSE']` |
| NomeSE | `item()?['NomeSE']` |
| SubODI | `item()?['SubODI']` |
| Regional | `item()?['Regional']` |
| Municipio | `item()?['Municipio']` |
| UF | `item()?['UF']` |
| TI | `item()?['TI']` |
| CM | `item()?['CM']` |
| ClasseTensao | `item()?['ClasseTensao']` |
| ArranjoFisico | `item()?['ArranjoFisico']` |
| LocalInstalacao | `item()?['LocalInstalacao']` |
| Status | `item()?['Status']` |

---

### 7. Operação de dados — Selecionar — `SelecionarItens`

De:

```
body('Obter_Itens')?['value']
```

Modo: **Mapa**. **Não** manda o body cru (`Author`, `@odata`, anexos).

| Chave | Valor (fx) |
|-------|------------|
| ID | `item()?['ID']` |
| CodInventario | `item()?['CodInventario']` |
| CodSE | `item()?['CodSE']` |
| NomeSE | `item()?['NomeSE']` |
| CodTUC | `item()?['CodTUC']` |
| AtributoA1 | `item()?['AtributoA1']` |
| AtributoA2 | `item()?['AtributoA2']` |
| AtributoA3 | `item()?['AtributoA3']` |
| AtributoA4 | `item()?['AtributoA4']` |
| AtributoA5 | `item()?['AtributoA5']` |
| AtributoA6 | `item()?['AtributoA6']` |
| DescricaoBem | `item()?['DescricaoBem']` |
| Quantidade | `item()?['Quantidade']` |
| Unidade | `item()?['Unidade']` |
| Origem | `item()?['Origem']` |
| Status | `item()?['Status']` |
| Sobra | `item()?['Sobra']` |
| ValidadoPor | `item()?['ValidadoPor']` |
| CodAsset | `item()?['CodAsset']` |
| Fabricante | `item()?['Fabricante']` |
| Modelo | `item()?['Modelo']` |
| NumSerie | `item()?['NumSerie']` |
| CodOperacao | `item()?['CodOperacao']` |
| Ano | `item()?['Ano']` |
| CM | `item()?['CM']` |
| Observacoes | `item()?['Observacoes']` |
| Imobilizado | `item()?['Imobilizado']` |
| Elegivel | `item()?['Elegivel']` |
| Reserva | `item()?['Reserva']` |
| Bay | `item()?['Bay']` |
| Projeto | `item()?['Projeto']` |
| IdItem | `item()?['IdItem']` |
| DescricaoTUC | `item()?['DescricaoTUC']` |
| IdUC | `item()?['IdUC']` |
| TI | `item()?['TI']` |
| LocalInstalacao | `item()?['LocalInstalacao']` |
| ArranjoFisico | `item()?['ArranjoFisico']` |
| QuantidadeCampo | `item()?['QuantidadeCampo']` |
| Title | `item()?['Title']` |

---

### 8. Responder a um Power App — `Responder_OK`

Saídas **Texto**, **nesta ordem** (o `.Run` casa pela ordem):

| Saída | Valor (fx) |
|-------|------------|
| erro | `-` |
| jsonItens | `string(body('SelecionarItens'))` |
| jsonSEs | `string(body('SelecionarSEs'))` |
| qtdItens | `string(length(body('SelecionarItens')))` |
| qtdSEs | `string(length(body('SelecionarSEs')))` |

Se o seletor tiver **Saída** do Select, usa. Não envolve `json()` em volta do `string()` — já é array.

**Publicar** de novo. Studio → o fluxo → **Atualizar**.

---

## App (resumo)

`flxBaixarCampanha.Run(varCodCampanha)` → `saida.erro` / `saida.jsonitens` / `saida.jsonses` / `saida.qtditens` / `saida.qtdses` (Studio baixa o nome).

`ParseJSON` + `ForAll` + `ClearCollect`. Spec: `docs/powerfx/Tela_Home-mobile-formulas.txt`.

Não consulta `Inventario` no canvas nesse botão.

---

## Se o `Run` falhar por tamanho

Select já corta o lixo do SharePoint. 3700 linhas magras cabem. Se ainda estourar:

1. Tira do mapa o que a visita não usa (`Projeto`, `Bay`, `Elegivel`, `Reserva`).
2. Só então partir `jsonItens` em dois Selects (ID par / ímpar). Não começa por isso.

---

## Conferência

1. Testar o fluxo com `INV-` da campanha de 3700. `qtdItens` tem que ser ~3700, não 100 nem 2000.
2. Baixar dados no tablet. Chip da campanha = `saida.qtditens`. Galeria da SE mostra item.
3. Aviao: lista da SE continua (SaveData).
