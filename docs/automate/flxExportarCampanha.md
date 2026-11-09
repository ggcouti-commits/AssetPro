# `flxExportarCampanha` — planilha `.xlsx`

> Decisão 2026-09-15 (Fenômeno). **Não** zipar foto. Foto fica na biblioteca `Projetos`.  
> ZIP (`flxExportarFotos`) = stand-by.  
> Site: AssetPro. Biblioteca de saída: **`Exportacoes`**.  
> Template: `docs/bases/modelo-exportacao.xlsx`. Script: `docs/automate/PreencherExportacao.ts`.

Canvas não lê Excel. `btnExportarCamp` chama este fluxo e abre `saida.link` (URL de **download**, não o `{Link}` do Criar arquivo — essa propriedade **não existe** na saída do SharePoint Create file, então o App via `Launch` em branco).

Recorte: só itens de SE com `Status = "Finalizada"` daquele `CodInventario`.  
`TI`, `LocalInstalacao`, `ArranjoFisico` saem da linha de **Inventario** (já estão na lista). `Obter_SEs` só filtra quem está Finalizada.

---

## Correção 2026-09-17 — o clique não baixava

O xlsx até podia nascer em **Exportacoes**. O App não baixava porque `Responder_OK` lia `{Link}` do Criar arquivo (chave inexistente → `saida.link` vazio) e o `Launch` ia pro nada.

No fluxo **já montado**, só isto:

1. `CodLimpo` → Inputs. Apaga. Cola:

```
trim(coalesce(triggerBody()?['text'], triggerBody()?['CodInventario'], ''))
```

2. Nova ação **Compor**, nome `LinkDownload`, **depois** do `CriarArquivo`. Cola:

```
concat(
  'https://gustavogarciacoutinho991.sharepoint.com/sites/AssetPro/_layouts/15/download.aspx?SourceUrl=',
  encodeUriComponent(
    concat('/sites/AssetPro/Exportacoes/', body('CriarArquivo')?['Name'])
  )
)
```

3. Nova ação **Atraso**, nome `Atraso_Graph`, **depois** do `LinkDownload` e **antes** do `Executar_script`. Intervalo **10** segundos.

4. `Responder_OK` → saída **`link`** (nome exatamente `link`, não `text`). Apaga o `{Link}`. Cola:

```
@{body('LinkDownload')}
```

5. **Salvar** → **Publicar**. Studio → o fluxo → **⋯** → **Atualizar**.

6. Studio: `btnExportarCamp` OnSelect — cola o bloco em `docs/powerfx/Tela_Exportar-formulas.txt` (passo 2).

Confere **Exportacoes**: se só existe `modelo-exportacao.xlsx`, sobe de novo `docs/bases/modelo-exportacao.xlsx` (o arquivo tinha sumido do repo).

---

## Uma vez (antes do fluxo)

### A. Template

Sobe `docs/bases/modelo-exportacao.xlsx` na biblioteca **Exportacoes** (mesmo site).  
Aba **Itens**, tabela **`tblItens`**. Colunas (nesta ordem):

`CodAsset`, `Imobilizado`, `IdUC`, `CodSE`, `NomeSE`, `TI`, `LocalInstalacao`, `CM`, `ArranjoFisico`, `CodTUC`, `DescricaoTUC`, `A1`…`A6`, `DescricaoBem`, `Quantidade`, `QuantidadeCampo`, `Unidade`, `Elegivel`, `Reserva`, `Fabricante`, `Modelo`, `NumSerie`, `Ano`, `Bay`, `CodOperacao`, `Projeto`, `Observacoes`, `Status`, `ValidadoPor`, `Origem`, `Sobra`, `CoordX`, `CoordY`

Estilo **TableStyleLight1** (não Medium2 — aquele pinta o corpo de azul). `DescricaoBem` alinhada à esquerda.

Substitui o arquivo antigo na biblioteca.

### B. Script Excel Online

Abre o `modelo-exportacao.xlsx` no Excel Online → **Automatizar** → **Novo script**.  
Nome: **`PreencherExportacao`**. Cola o arquivo `docs/automate/PreencherExportacao.ts`. Salva.

Dois parâmetros de texto: `jsonItens` e `jsonSEs`.

---

## Fluxo (uma caixa = um passo)

Nomeia cada ação **igual** ao título.

### 1. Power Apps (V2) — `Quando_o_Power_Apps`

Uma entrada **Texto**: `CodInventario`.

### 2. Compor — `CodLimpo`

```
trim(coalesce(triggerBody()?['text'], triggerBody()?['CodInventario'], ''))
```

O V2 às vezes manda `text`, às vezes `CodInventario`. Sem o `coalesce`, `CodLimpo` sai vazio → filtro não acha SE → `Responder_SemSaida` mesmo com Finalizada no card.

### 3. SharePoint — Obter itens — `Obter_SEs`

- Lista: **Subestacoes**
- Consulta de filtro:

```
CodInventario eq '@{outputs('CodLimpo')}' and Status eq 'Finalizada'
```

Paginação **ligada**. Limite 100.

### 4. Condição — `TemSEFinalizada`

```
length(body('Obter_SEs')?['value'])
```

é maior que `0`.

**Se não:**

#### 4a. Responder ao Power App — `Responder_SemSaida`

| Saída | Valor |
|-------|--------|
| link | (vazio) |
| erro | `Nenhuma SE Finalizada` |

Encerrar.

**Se sim:** segue.

### 5. SharePoint — Obter itens — `Obter_Itens`

- Lista: **Inventario**
- Consulta de filtro:

```
CodInventario eq '@{outputs('CodLimpo')}'
```

Paginação **ligada**. Limite **5000**.

### 6. Operação de dados — Selecionar — `ListaCodSE`

- De: `body('Obter_SEs')?['value']`
- Modo: **Texto** (não mapa de objeto)
- Mapa (fx):

```
item()?['CodSE']
```

### 6b. Operação de dados — Selecionar — `SelecionarSEs`

- De: `body('Obter_SEs')?['value']`
- Mapa:

| Chave | Valor (fx) |
|-------|------------|
| CodSE | `item()?['CodSE']` |
| NomeSE | `item()?['NomeSE']` |
| CoordX | `coalesce(item()?['CoordX'], '')` |
| CoordY | `coalesce(item()?['CoordY'], '')` |

### 7. Operação de dados — Filtrar matriz — `ItensFinalizados`

- De: `body('Obter_Itens')?['value']`
- Filtro avançado (fx):

```
@contains(body('ListaCodSE'), item()?['CodSE'])
```

### 8. Operação de dados — Selecionar — `SelecionarColunas`

De: `body('ItensFinalizados')`

Mapa (chave = cabeçalho da `tblItens`):

| Chave | Valor (fx) |
|-------|------------|
| CodAsset | `item()?['CodAsset']` |
| Imobilizado | `item()?['Imobilizado']` |
| IdUC | `item()?['IdUC']` |
| CodSE | `item()?['CodSE']` |
| NomeSE | `item()?['NomeSE']` |
| TI | `item()?['TI']` |
| LocalInstalacao | `item()?['LocalInstalacao']` |
| CM | `item()?['CM']` |
| ArranjoFisico | `item()?['ArranjoFisico']` |
| CodTUC | `coalesce(string(item()?['CodTUC']), string(item()?['TUC']), '')` |
| DescricaoTUC | `item()?['DescricaoTUC']` |
| A1 | `coalesce(string(item()?['AtributoA1']), string(item()?['A1']), '')` |
| A2 | `coalesce(string(item()?['AtributoA2']), string(item()?['A2']), '')` |
| A3 | `coalesce(string(item()?['AtributoA3']), string(item()?['A3']), '')` |
| A4 | `coalesce(string(item()?['AtributoA4']), string(item()?['A4']), '')` |
| A5 | `coalesce(string(item()?['AtributoA5']), string(item()?['A5']), '')` |
| A6 | `coalesce(string(item()?['AtributoA6']), string(item()?['A6']), '')` |
| DescricaoBem | `item()?['DescricaoBem']` |
| Quantidade | `item()?['Quantidade']` |
| QuantidadeCampo | `item()?['QuantidadeCampo']` |
| Unidade | `item()?['Unidade']` |
| Elegivel | `item()?['Elegivel']` |
| Reserva | `item()?['Reserva']` |
| Fabricante | `item()?['Fabricante']` |
| Modelo | `item()?['Modelo']` |
| NumSerie | `item()?['NumSerie']` |
| Ano | `item()?['Ano']` |
| Bay | `item()?['Bay']` |
| CodOperacao | `item()?['CodOperacao']` |
| Projeto | `item()?['Projeto']` |
| Observacoes | `coalesce(item()?['Observacoes'], item()?['Observacao'])` |
| Status | `item()?['Status']` |
| ValidadoPor | `item()?['ValidadoPor']` |
| Origem | `item()?['Origem']` |
| Sobra | `coalesce(item()?['Sobra']?['Value'], item()?['Sobra'], '')` |
| CoordX | Rede (`CodSE` começa com `REDE-`): `coalesce(item()?['CoordX'], '')`. Subestação: coordenada X da SE com o mesmo `CodSE`. |
| CoordY | Rede: `coalesce(item()?['CoordY'], '')`. Subestação: coordenada Y da SE com o mesmo `CodSE`. |
| CoordXItem | `coalesce(item()?['CoordX'], '')` |
| CoordYItem | `coalesce(item()?['CoordY'], '')` |

### 9. SharePoint — Obter conteúdo do arquivo — `Obter_Modelo`

Biblioteca **Exportacoes** → arquivo `modelo-exportacao.xlsx`.

### 10. SharePoint — Criar arquivo — `CriarArquivo`

- Biblioteca: **Exportacoes**
- Nome:

```
concat('Exportacao-', outputs('CodLimpo'), '-', utcNow('yyyyMMdd-HHmm'), '.xlsx')
```

- Conteúdo: o **body** do `Obter_Modelo` (o modelo, **não** JSON).

### 11. Compor — `LinkDownload`

O `CriarArquivo` **não** devolve `{Link}`. Monta a URL de download:

```
concat(
  'https://gustavogarciacoutinho991.sharepoint.com/sites/AssetPro/_layouts/15/download.aspx?SourceUrl=',
  encodeUriComponent(
    concat('/sites/AssetPro/Exportacoes/', body('CriarArquivo')?['Name'])
  )
)
```

`Name` é só o arquivo (`Exportacao-INV-….xlsx`). Não usa `Path` — o conector às vezes manda sem a barra.

### 12. Atraso — `Atraso_Graph`

**Intervalo:** `10` segundos.

O Graph não indexa o xlsx no instante. Sem isso o `Executar_script` cai em `ItemNotFound`.

### 13. Excel Online — Executar um script — `Executar_script`

- Local: **SharePoint** (não OneDrive)
- Biblioteca: **Exportacoes**
- Arquivo: identificador do `CriarArquivo` (conteúdo dinâmico **Id**). **Não** deixa path fixo.
- Script: `PreencherExportacao`
- **Dois** parâmetros. Os dois em **fx** com `string(...)`:
  - `jsonItens`:

```
string(body('SelecionarColunas'))
```

  - `jsonSEs`:

```
string(body('SelecionarSEs'))
```

A ação **Selecionar** das colunas tem que se chamar `SelecionarColunas`. A das SEs, `SelecionarSEs`. Sem o `string(...)` o script recebe `"undefined"`.

Se o campo `jsonSEs` **não aparece**: Excel Online → script `PreencherExportacao` → apaga tudo → cola `docs/automate/PreencherExportacao.ts` → Salvar. No Automate, escolhe o script de novo.

### 14. Responder ao Power App — `Responder_OK`

Os dois nomes da saída têm que ser exatamente `link` e `erro` (minúsculo). Se o designer gravou `text` / `text_1`, o App lê `saida.link` vazio e não baixa.

| Saída | Valor |
|-------|--------|
| link | `@{body('LinkDownload')}` |
| erro | `-` |

`body('LinkDownload')` é a URL (texto). `outputs('LinkDownload')` às vezes manda o objeto inteiro e o `Launch` ignora.

**Não** use `body('CriarArquivo')?['{Link}']` — vem vazio e o App não dispara o download.

---

## App

`Tela_Exportar` → `btnExportarCamp` → `OnSelect`: `docs/powerfx/Tela_Exportar-formulas.txt`.

Um botão. Sem `btnExportarFotos`.

---

## Conferência

Abre make.powerautomate.com → `flxExportarCampanha` → **Execuções de 28 dias** → a mais recente.

| Onde parou | O que está quebrado | O que fazer |
|------------|---------------------|-------------|
| `CodLimpo` vazio | V2 mandou `CodInventario`, não `text` | Passo 2 (`coalesce`) |
| `Obter_SEs` = 0 / `Responder_SemSaida` | Filtro não achou Finalizada **ou** código vazio | Confere `Status` na lista + `CodLimpo` |
| Falhou em `Obter_Modelo` | `modelo-exportacao.xlsx` não está em **Exportacoes** | Sobe `docs/bases/modelo-exportacao.xlsx` |
| Falhou em `CriarArquivo` | Permissão / biblioteca errada | Biblioteca **Exportacoes**, mesmo site |
| Falhou em `Executar_script` (`ItemNotFound`) | Graph ainda não indexou o xlsx | `Atraso_Graph` **10 s** (ou 15) **antes** do script |
| Chegou em `Responder_OK` e `link` vazio / `{Link}` | Create file **não tem** `{Link}` | Passos 11 + 14 (`LinkDownload`) |
| `Responder_OK` com URL `download.aspx` e **Exportacoes** tem o xlsx | App ainda faz `Launch(saida.link)` sem aba nova, ou `link` antigo no Studio | Cola o OnSelect + **Atualizar** o fluxo no Studio |
| Fluxo **sucesso** e pasta só tem o modelo | Clique no App nem chegou no fluxo | DisplayMode do botão / `varLockCod` |

Teste no **player publicado** (browser). `Launch` no Preview do Studio costuma engolir o download.

5. App → **Planilha**: o browser baixa o `.xlsx`.

## O que não fazer

- Não **Criar CSV**.
- Não zipar pasta / `flxExportarFotos` neste fluxo.
- Não lookup de TI na SE — a coluna já está em `Inventario`.
- Não responder `body('CriarArquivo')?['{Link}']` — essa chave **não existe** no Criar arquivo.
