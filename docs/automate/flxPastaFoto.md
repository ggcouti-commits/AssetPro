# `flxPastaFotosVisita` — um run por visita (lote)

> 100 itens × 3 fotos + ambiente passa de 300 JPG. Gatilho “item criado” = 300 runs. Não escala.  
> Site: `https://gustavogarciacoutinho991.sharepoint.com/sites/AssetPro`  
> App: **um** `Run` no fim do `btnEnviarVisitaExec`, **depois** do `ForAll` das fotos.  
> O app **não** espera a cópia (Responder cedo, igual import/excluir).

Árvore igual:

```
Projetos/{PastaProjeto}/{CodSE} - {NomeSE}/Visão geral/{yyyyMMdd-HHmmss}_{ID}.jpg
Projetos/{PastaProjeto}/{CodSE} - {NomeSE}/{Imobilizado ou CodAsset}/{yyyyMMdd-HHmmss}_{ID}.jpg
```

Corte 18.09: pasta do item **sem** descrição. `Ambiente` vira **Visão geral**. `TipoFoto` continua `AMBIENTE` / `ITEM`. Spec: `docs/exportacao-fotos-pastas.md`.

**Desliga** o fluxo antigo com gatilho *Quando um item é criado* (⋯ → **Desativar**). Senão cada Patch ainda dispara um run.

**Não** `Atualizar item` em `Campanhas` nem em `Fotos` (zera coluna). Flag `CopiadoPasta` via HTTP PATCH.

Renomeia cada ação **exatamente** como está em negrito.

---

## Antes — SharePoint (uma vez)

Lista **Fotos** → coluna **Sim/Não** → `CopiadoPasta`. Padrão **Não**. Sem obrigatoriedade.

Studio → Dados → **Fotos** → Atualizar. (O fluxo usa HTTP; o app não precisa gravar essa coluna no Patch.)

---

## Criar o fluxo

make.powerautomate.com → **Criar** → **Fluxo da nuvem instantâneo** → em branco.

Nome: `flxPastaFotosVisita`

⋯ do fluxo → **Configurações** → Tempo limite `PT30M`.

---

### 1. Gatilho — Power Apps (V2) — `Quando_o_Power_Apps`

Uma entrada **Texto** → nome `CodInventario`.

**Publicar.** Studio → Power Automate → o fluxo → **⋯** → **Atualizar**.

---

### 2. Compor — `CodLimpo`

```
trim(coalesce(triggerBody()?['text'], triggerBody()?['CodInventario'], ''))
```

---

### 3. Atraso — `Espera_arquivo`

**8** segundos. **Uma vez** por visita (a coluna Imagem termina de gravar no SiteAssets depois do `ForAll`).

---

### 4. SharePoint — Obter itens — `Obter_Fotos`

- Lista: **Fotos**
- Filtro **só** (não filtra `CopiadoPasta` aqui — `ne 1` no SharePoint **pula coluna vazia**):

```
CodInventario eq '@{outputs('CodLimpo')}'
```

**⋯ → Configurações:** Paginação **ligada**, limite **500**. Campo **Contagem superior / Top**: **500**.

---

### 4b. Filtrar matriz — `Filtrar_Pendentes`

De: `body('Obter_Fotos')?['value']`

Designer novo, três caixas: esquerda **CopiadoPasta** (dinâmico do item), **não é igual a**, direita `true`.

Ou **fx** na condição:

```
@not(equals(item()?['CopiadoPasta'], true))
```

Vazio, Não e false entram. Só Sim (já copiou) sai.

---

### 5. Responder a um Power App — `Responder_OK`

**Aqui.** Antes do loop. O `Run` do app libera em segundos.

| Saída | Valor |
|-------|--------|
| erro | `-` |
| qtdFotos | `@{string(length(body('Filtrar_Pendentes')))}` |

Se `qtdFotos` = `0`, o loop abaixo não roda (não tem foto nova). Fluxo ainda fica verde.

**Reenviar / Testar no Automate:** o `Responder_OK` fica **ignorado** (não tem Power Apps esperando). Sem o passo abaixo, `Obter_Campanha` e tudo depois nascem cinza.

---

### 6. SharePoint — Obter itens — `Obter_Campanha`

- Lista: **Campanhas** (a do app)
- Filtro: `CodInventario eq '@{outputs('CodLimpo')}'`
- Top: 1

**⋯ → Configurações → Execução após / run after** da ação **`Responder_OK`:** marca **êxito** **e** **foi ignorado**. (Aba Configurações desta ação, não o ⋯ do canvas.)

---

### 7. Compor — `NomeSanitizado`

Igual o import (só se `PastaProjeto` vier vazio):

```
trim(replace(replace(replace(replace(replace(replace(replace(replace(replace(replace(replace(replace(replace(replace(replace(
  string(coalesce(first(body('Obter_Campanha')?['value'])?['NomeInventario'], 'projeto'))
, '\', '-'), '/', '-'), ':', '-'), '*', ''), '?', ''), '"', ''), '<', ''), '>', ''), '|', ''), '#', ''), '%', ''), '&', 'E'), '{', ''), '}', ''), '~', ''))
```

---

### 8. Compor — `PastaProjeto`

```
trim(coalesce(
  first(body('Obter_Campanha')?['value'])?['PastaProjeto'],
  concat(
    substring(outputs('NomeSanitizado'), 0, if(greater(length(outputs('NomeSanitizado')), 80), 80, length(outputs('NomeSanitizado')))),
    '_',
    outputs('CodLimpo')
  )
))
```

---

### 9. SharePoint — Obter itens — `Obter_SEs`

- Lista: **Subestacoes**
- Filtro: `CodInventario eq '@{outputs('CodLimpo')}'`
- Paginação ligada, limite **200**

---

### 10. SharePoint — Obter itens — `Obter_Inventario`

- Lista: **Inventario**
- Filtro: `CodInventario eq '@{outputs('CodLimpo')}'`
- Paginação ligada, limite **2000**

# Uma SE de visita ~100 linhas. Campanha inteira de 3700 também cabe. Filter array no loop usa esta lista em memória (sem 300 Gets).

---

### 11. Aplicar a cada — `Aplicar_Fotos`

Saída: `body('Filtrar_Pendentes')`

**⋯ → Configurações:** Controle de simultaneidade **ligado**, grau **20**.

Se `UrlRelativa` (ou outra ação) fica vermelha, o loop **para**. Resultado típico: **1 pasta vazia**, resto nem nasce. Depois de corrigir a expressão: **Histórico → o run → Reenviar**. Não precisa Enviar visita de novo (`CopiadoPasta` ainda Não).

300 fotos / 20 ≈ 15 levas. Sem 300 fluxos.

Dentro do loop, nesta ordem. A foto do loop **não** aparece no conteúdo dinâmico. Sempre **fx**:

```
items('Aplicar_Fotos')?['ID']
items('Aplicar_Fotos')?['CodSE']
items('Aplicar_Fotos')?['CodAsset']
items('Aplicar_Fotos')?['TipoFoto']
```

`item()` no Filter array é a linha filtrada (SE / Inventario), **não** a foto.

#### 11a. Compor — `TipoFotoLinha`

```
toUpper(trim(coalesce(
  items('Aplicar_Fotos')?['TipoFoto'],
  if(startsWith(toUpper(trim(coalesce(items('Aplicar_Fotos')?['Title'], ''))), 'AMBIENTE'), 'AMBIENTE', 'ITEM')
)))
```

#### 11b. Filtrar matriz — `SE_desta_foto`

De: `body('Obter_SEs')?['value']`  
Onde `CodSE` **é igual a** `items('Aplicar_Fotos')?['CodSE']`

#### 11c. Compor — `NomeSE_Sanitizado`

```
trim(replace(replace(replace(replace(replace(replace(replace(replace(replace(replace(replace(replace(replace(replace(
  string(coalesce(first(body('SE_desta_foto'))?['NomeSE'], ''))
, '/', '-'), ':', '-'), '*', ''), '?', ''), '"', ''), '<', ''), '>', ''), '|', ''), '#', ''), '%', ''), '&', 'E'), '{', ''), '}', ''), '~', ''))
```

#### 11d. Compor — `CaminhoSE`

```
concat('/', outputs('PastaProjeto'), '/', items('Aplicar_Fotos')?['CodSE'], ' - ', outputs('NomeSE_Sanitizado'))
```

#### 11e. Condição — `EhAmbiente`

Esquerda **fx:** `outputs('TipoFotoLinha')`  
é igual a  
direita: `AMBIENTE`

**Se sim**

- Criar pasta `Criar_pasta_Ambiente` — biblioteca **Projetos**, **Caminho da Pasta** **fx:**

```
concat(outputs('CaminhoSE'), '/Visão geral')
```

(caminho **inteiro**; este conector não tem “Nome da pasta”. Sem execução depois: é a 1ª do ramo.)

Campanha velha só com `Ambiente`: se `Visão geral` 404 e `Ambiente` existir, usar `Ambiente`. Importação nova só cria `Visão geral`.

- Compor `CaminhoDestino_Amb` **fx:** `concat(outputs('CaminhoSE'), '/Visão geral')`  
  ⋯ execução depois: êxito **e** falha do criar pasta.

**Se não**

- Filtrar matriz `Item_desta_foto`  
  De: `body('Obter_Inventario')?['value']`  
  `CodAsset` é igual a `items('Aplicar_Fotos')?['CodAsset']`

- Compor `ImobilizadoLimpo` / `NomePastaItem` — `first(body('Item_desta_foto'))` no lugar de `Obter_Inventario`. **Não** usa `DescricaoBem` no path (18.09).

`NomePastaItem`:

```
if(
  empty(outputs('ImobilizadoLimpo')),
  if(empty(items('Aplicar_Fotos')?['CodAsset']), 'SEM-IMOB', items('Aplicar_Fotos')?['CodAsset']),
  outputs('ImobilizadoLimpo')
)
```

- Criar pasta — Caminho **fx:** `concat(outputs('CaminhoSE'), '/', outputs('NomePastaItem'))`
- Compor `CaminhoDestino_Item` — mesmo concat; execução depois êxito **e** falha da pasta.

#### 11f. Compor — `CaminhoDestino` (fora da condição, no loop)

**fx:**

```
if(
  equals(outputs('TipoFotoLinha'), 'AMBIENTE'),
  outputs('CaminhoDestino_Amb'),
  outputs('CaminhoDestino_Item')
)
```

# Os dois Compor dos ramos têm que existir. No ramo que não rodou o Compor fica vazio; o `if` pega o outro.

⋯ execução depois desta ação: êxito **e** foi ignorado dos dois Compor de caminho (os dois ramos). Marca as duas origens se o canvas deixar; senão só “êxito” — o ramo que rodou chega aqui.

#### 11g. Compor — `Ler_FotoCampo`

O app grava em `FotoCampo` (coluna Imagem → SiteAssets). **Não** é anexo da linha. `Obter_anexos` volta `[]` → pasta nasce, JPG não.

```
items('Aplicar_Fotos')?['FotoCampo']
```

#### 11h. Compor — `UrlRelativa`

```
coalesce(
  outputs('Ler_FotoCampo')?['serverRelativeUrl'],
  uriPath(outputs('Ler_FotoCampo')?['Url']),
  json(string(outputs('Ler_FotoCampo')))?['serverRelativeUrl'],
  uriPath(json(string(outputs('Ler_FotoCampo')))?['Url'])
)
```

No run: se isto sair vazio, o `Get items` não trouxe a imagem. Aí entra um **Obter item** (`Fotos`, Id = `items('Aplicar_Fotos')?['ID']`) e troca `Ler_FotoCampo` para `body('Obter_Foto')?['FotoCampo']`.

#### 11i. SharePoint — Enviar uma solicitação HTTP — `Obter_bytes`

- Método: **GET**
- URI:

```
concat('_api/web/GetFileByServerRelativeUrl(''', outputs('UrlRelativa'), ''')/$value')
```

- Cabeçalho `Accept` = `application/octet-stream`

Não usa anexo. Se ainda existir `Obter_anexos` / `Obter_conteudo_anexo`, desliga.

#### 11j. Compor — `NomeArquivo`

```
concat(
  formatDateTime(convertTimeZone(utcNow(), 'UTC', 'E. South America Standard Time'), 'yyyyMMdd-HHmmss'),
  '_',
  string(items('Aplicar_Fotos')?['ID']),
  '.jpg'
)
```

#### 11k. Criar arquivo — `Criar_jpg`

- Biblioteca **Projetos**
- Caminho da pasta **fx:** `outputs('CaminhoDestino')`
- Nome: saída `NomeArquivo`
- Conteúdo: **Corpo** do `Obter_bytes` (o HTTP do `FotoCampo`). Não o anexo.

#### 11l. HTTP — `Marca_Copiada`

Só se o JPG gravou. GET não. **PATCH**.

- URI: `_api/web/lists/getbytitle('Fotos')/items()` + ID do loop + nada de `$select`
- Cabeçalhos:

  `Accept` = `application/json;odata=nometadata`  
  `Content-Type` = `application/json;odata=nometadata`  
  `If-Match` = `*`

- Corpo:

```
{ "CopiadoPasta": true }
```

⋯ execução depois: só **êxito** do `Criar_jpg`.

Se uma foto falhar, `CopiadoPasta` fica Não. Próximo Enviar visita (ou um Run manual) pega só as que faltam — não copia 300 de novo.

---

### 12. Compor — `Fim`

Entradas: `ok`  
Execução depois do `Aplicar_Fotos`: êxito, falha, ignorado.

---

## App — um `Run` (não no ForAll)

### Studio → Power Automate → adicionar `flxPastaFotosVisita` → Atualizar.

### `Tela_Home` → `btnEnviarVisitaExec` → OnSelect

No **fim** do `ForAll` das fotos (depois do `SaveData` de `colFotosCampo`), **antes** do toast, cola:

```
IfError(
    flxPastaFotosVisita.Run(gblInventarioSelecionado.CodInventario);
    Blank()
);;
```

O `Run` volta no `Responder_OK` (passo 5). A cópia segue no Automate. Toast do envio não espera 300 JPG.

**Não** ponha o `Run` dentro do `ForAll`.

---

## Conferência

| Fotos na visita | Runs | Ordem de grandeza |
|-----------------|------|-------------------|
| Gatilho antigo (desligado) | 300 | 20–40 min + fila |
| Este lote, grau 20 | **1** | ~5–15 min no fundo |

1. Desativa o fluxo do gatilho lista.
2. Envia uma SE de teste com 2–3 fotos.
3. Um run verde, `qtdFotos` = 2 ou 3. JPG na pasta certa. `CopiadoPasta` = Sim nessas linhas.
4. Envia de novo sem foto nova: `qtdFotos` = 0, pasta igual.
5. SE grande: o técnico sai da tela; André olha `Projetos` uns minutos depois.
