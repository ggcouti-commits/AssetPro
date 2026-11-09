# Fluxo `flxImportarCampanha` — passo a passo Automate

> App já criou o item em `Campanhas`. Este fluxo lê o `.xlsx`, identifica **todas** as SEs (`CÓDIGO ODI`), grava `Subestacoes` + pastas e responde o app. Itens entram depois.
> Site: `https://gustavogarciacoutinho991.sharepoint.com/sites/AssetPro`
> Script: `scrLerBaseEletrica` (já salvo no Excel).
> Só **`.xlsx`**.

Renomeia cada ação **exatamente** como está em negrito. As expressões usam esses nomes.

---

## Antes — SharePoint (uma vez)

- **Inventario:** `Imobilizado`, `Elegivel`, `Reserva`, `Bay`, `Projeto` (texto)
- **Subestacoes:** `ArranjoFisico`, `LocalInstalacao` (número), `ClasseTensao` (texto)
- **Campanhas:** `PastaProjeto` (texto)
- Biblioteca **`Importacoes`**
- Biblioteca **`Projetos`** (já combinada)

---

## Criar o fluxo

make.powerautomate.com → **Criar** → **Fluxo da nuvem instantâneo** → pular o gatilho da lista → em branco.

Nome: `flxImportarCampanha`

O canvas **não** serializa `.xlsx` (`JSON` = `appres://blobmanager`). O gatilho PowerApps antigo **não existe** mais. O App faz `Patch` na biblioteca **`Importacoes`** (`{Content}` resolve o blob). O fluxo só lê o arquivo já gravado.

---

### 1. Gatilho — Power Apps (V2)

Apaga o gatilho vazio. Adiciona **Power Apps (V2)**.

**Adicionar uma entrada** — nesta ordem:

1. Tipo **Arquivo** → nome `arquivo`
2. Tipo **Texto** → nome `CodInventario`

O tipo **Arquivo** só aceita **Blob**. No App, o valor tem que vir de `addPlanilha.Media` (controle **Adicionar imagem**). `attPlanilha.Attachments.Value` (controle **Anexos**) **não** é Blob — é o `appres://blobmanager` que derrubou tudo.

Depois de mexer no gatilho: **Publicar** (Salvar não chega no App). Aí no Studio → Power Automate → `flxImportarCampanha` → **⋯** → **Atualizar**.

**Nome interno ≠ nome da entrada.** Arquivo vira `file`, texto vira `text`, na ordem em que você criou (não reindexa se apagar). Nas ações, clica no **conteúdo dinâmico** em vez de digitar. Para conferir: **⋯** → **Exibição de código** no gatilho.

---

### 2. Compor — `CodLimpo`

O App manda o código no padrão **`INV-XXX`**. Só aparar espaço:

```
trim(coalesce(triggerBody()?['text'], ''))
```

Não usa `toLower` nem tira `{ }` — isso era do GUID e quebrava a comparação com `INV-001`.

---

### 3. Condição — `EhXlsx`

**Modo avançado**:

```
endsWith(toLower(triggerBody()?['file']?['name']), '.xlsx')
```

é igual a `true`.

**Se não (lado FALSO):**

#### 3a. Responder a um Power App — `Responder_NaoXlsx`

Adiciona as saídas (todas texto): `erro`, `qtdSEs`, `qtdItens`, `pasta`, `listaSEs`.

| Saída | Valor |
|-------|--------|
| erro | `Manda .xlsx. Este fluxo não abre .xls / .xlsb` |
| qtdSEs | `0` |
| qtdItens | `0` |
| pasta | (vazio) |
| listaSEs | (vazio) |

#### 3b. Encerrar — `Encerrar_NaoXlsx`

Status: **Falha** · Código: `ArquivoInvalido`

**Se sim (lado VERDADEIRO):** segue do passo 4 **dentro** desse ramo.

---

### 4. SharePoint — Criar arquivo — `Criar_arquivo`

- Site: AssetPro
- Biblioteca: `Importacoes`
- Pasta: `/`
- Nome do arquivo (fx) — **não** depende do `name` do anexo (se vier vazio, o arquivo nasce sem extensão e o Excel não abre) e **nunca** repete:

```
concat(outputs('CodLimpo'), '-', utcNow('yyyyMMdd-HHmmss'), '.xlsx')
```

Nome fixo dá `foi bloqueado para uso compartilhado` quando o arquivo anterior está aberto no Excel ou com check-out.

- Conteúdo do arquivo: conteúdo dinâmico **arquivo** / **Conteúdo do arquivo**. Não envolve em `base64ToBinary` se o seletor já for o arquivo.

Se o seletor só oferecer texto, fx:

```
base64ToBinary(triggerBody()?['file']?['contentBytes'])
```

O nome pode ser `INV-001.xlsx` (o que está no Studio hoje). A exclusão **não** usa o nome — usa a coluna `CodInventario` (passo 4b).

---

### 4a. SharePoint — coluna na biblioteca (uma vez)

Biblioteca **Importacoes** → + Coluna → Texto de uma linha → nome `CodInventario`.  
Não precisa ser obrigatória. Sem essa coluna o excluir não acha o arquivo.

---

### 4b. SharePoint — Atualizar propriedades do arquivo — `Gravar_CodInventario`

Cola **logo depois** do `Criar_arquivo`, **antes** do script. Sem isso o `.xlsx` nasce e a coluna fica vazia.

- Site: AssetPro
- Biblioteca: **Importacoes**
- Id: conteúdo dinâmico **Id** do `Criar_arquivo` (é o ID do item da biblioteca, não o path)
- `CodInventario` (**fx**):

```
outputs('CodLimpo')
```

---

### 5. Excel Online (Business) — Executar script — `Executar_script`

- Local: **SharePoint** (não OneDrive)
- Biblioteca: `Importacoes`
- Arquivo: identificador do `Criar_arquivo` (conteúdo dinâmico **Id**)
- Script: `scrLerBaseEletrica`

O script copia o cabeçalho `IdUC` / `IDUC` da base para a coluna `IdUC` de `tblImportItens`. Sem essa coluna na planilha, a célula sai vazia. O passo 20a já grava `Inventario.IdUC` — não muda o fluxo.

---

### 6. Operação de dados — Analisar JSON — `Analisar_JSON`

Conteúdo (fx):

```
body('Executar_script')?['result']
```

Se o seletor dinâmico tiver **resultado**, usa ele.

Schema — **Usar carga de exemplo** ou cola:

```json
{
  "type": "object",
  "properties": {
    "erro": { "type": "string" },
    "qtdSEs": { "type": "number" },
    "qtdItens": { "type": "number" },
    "listaSEs": { "type": "string" }
  }
}
```

---

### 7. Condição — `ScriptOk`

Duas linhas (E):

1. `empty(body('Analisar_JSON')?['erro'])` é igual a `true`
2. `body('Analisar_JSON')?['qtdSEs']` é maior que `0`

**Se não:**

#### 7a. Responder — `Responder_ErroScript`

| Saída | Valor |
|-------|--------|
| erro | `@{if(empty(body('Analisar_JSON')?['erro']), 'A base não tem nenhuma SE (CÓDIGO ODI vazio)', body('Analisar_JSON')?['erro'])}` |
| qtdSEs | `0` |
| qtdItens | `0` |
| pasta | (vazio) |
| listaSEs | (vazio) |

#### 7b. Encerrar — `Encerrar_ErroScript` · Falha · `Script`

**Se sim:** passo 8 neste ramo.

---

### 8. SharePoint — Obter itens — `Obter_Campanha`

- Lista: `Campanhas` (a mesma do app; se tiver espaço no nome, escolhe no dropdown)
- Consulta de filtro:

```
CodInventario eq '@{outputs('CodLimpo')}'
```

---

### 9. Condição — `TemCampanha`

```
length(body('Obter_Campanha')?['value'])
```

é maior que `0`.

**Se não:** Responder `erro` = `Projeto não encontrado em Campanhas` + Encerrar.

**Se sim:** passo 10.

---

### 10. Compor — `NomeSanitizado`

A raiz era mais fraca que o `NomeSE_Sanitizado`: não tirava `\`, `&`, `{ } ~` nem espaço nas pontas. SharePoint: “caracteres que não são permitidos”.

```
trim(replace(replace(replace(replace(replace(replace(replace(replace(replace(replace(replace(replace(replace(replace(replace(
  string(first(body('Obter_Campanha')?['value'])?['NomeInventario'])
, '\', '-'), '/', '-'), ':', '-'), '*', ''), '?', ''), '"', ''), '<', ''), '>', ''), '|', ''), '#', ''), '%', ''), '&', 'E'), '{', ''), '}', ''), '~', ''))
```

---

### 11. Compor — `PastaProjeto`

`trim` no resultado: `substring` em 80 pode deixar espaço no fim, e o SharePoint também recusa.

```
trim(concat(
  substring(outputs('NomeSanitizado'), 0, if(greater(length(outputs('NomeSanitizado')), 80), 80, length(outputs('NomeSanitizado')))),
  '_',
  outputs('CodLimpo')
))
```

---

### 12. ~~SharePoint — Atualizar item — `Atualizar_Campanha`~~ — **APAGAR**

**Não usar.** O conector **Atualizar item** grava **vazio** em todo campo que ficar em branco no card. Ele apagou `CodInventario`, `NomeInventario`, `Periodo`, `Setor`, `Status` e `Ativo` do projeto recém-criado (item 23 do teste 13.09).

Quem grava `PastaProjeto` é o **App**, com o `saida.pasta` da resposta do fluxo:

```
Patch(
    'Campanhas ';
    varNovaCampanha;
    {PastaProjeto: saida.pasta}
)
```

Se um dia precisar atualizar a lista pelo fluxo, preenche **todos** os campos no card (repetindo os valores de `Obter_Campanha`) ou usa **Enviar solicitação HTTP para o SharePoint**.

---

### 13. SharePoint — Criar nova pasta — `Criar_pasta_raiz`

- Site: AssetPro
- Biblioteca: `Projetos`
- Caminho da pasta: `/@{outputs('PastaProjeto')}`

O conector recebe no **caminho** a pasta inteira a criar, nome incluído — é assim que o
`Criar_pasta_SE` funciona (`/{PastaProjeto}/{CodSE} - {NomeSE}`). Caminho `/` sozinho, sem nome,
dá **BadRequest** (run 13.09 do `INV-003`). As pastas apareciam mesmo assim porque o
`Criar_pasta_SE` cria os níveis que faltam no caminho.

---

### 14. SharePoint — Obter itens — `Obter_SEs_existentes`

- Lista: `Subestacoes`
- Filtro:

```
CodInventario eq '@{outputs('CodLimpo')}'
```

**Configurar execução após** desta ação: êxito **e** falha (se a pasta raiz já existia no 13).

---

### 15. Condição — `JaImportou`

```
length(body('Obter_SEs_existentes')?['value'])
```

é maior que `0`.

**Se sim:** Responder `erro` = `Esse projeto já tem instalações. Não reimporta.` + Encerrar.

**Se não:** passo 16.

---

### 16. Excel — Listar linhas presentes em uma tabela — `Listar_SEs`

- Local: SharePoint · `Importacoes`
- Arquivo: Id do `Criar_arquivo`
- Tabela: `tblImportSEs`
- **Configurações** (engrenagem) → Paginação **ligada** · limite 100

Esta tabela é a lista oficial: **1 linha = 1 SE**. O loop abaixo percorre **todas**. Não usa `first()`.

---

### 17. Aplicar a cada — `Aplicar_SEs`

Saída: `body('Listar_SEs')?['value']`

#### 17a. SharePoint — Criar item — `Criar_SE`

Lista: `Subestacoes`

| Campo | Valor |
|-------|--------|
| Title | `items('Aplicar_SEs')?['CodSE']` |
| CodSE | `items('Aplicar_SEs')?['CodSE']` |
| NomeSE | `items('Aplicar_SEs')?['NomeSE']` |
| CodInventario | `outputs('CodLimpo')` |
| TI | `items('Aplicar_SEs')?['TI']` |
| LocalInstalacao | `items('Aplicar_SEs')?['LocalInstalacao']` |
| ArranjoFisico | `items('Aplicar_SEs')?['ArranjoFisico']` |
| ClasseTensao | `items('Aplicar_SEs')?['ClasseTensao']` |
| UF | `first(body('Obter_Campanha')?['value'])?['UF']` |
| Status | `Pendente` |

**Não** criar coluna `QtdItens` em `Subestacoes` só para o popup. A contagem por SE já vem na
resposta do fluxo: o script escreve `CodSE — NomeSE (qtd)` dentro de `listaSEs`. Contar
`Inventario` no app também não serve — o `Responder_OK` responde antes do `Aplicar_Itens`
terminar (run 13.09: 65 itens criados, popup mostrando 0 / 4 / 0 / 1 / 1).

Número vazio quebrar: deixa o campo em branco nessa linha.

#### 17b. Compor — `NomeSE_Sanitizado`

```
trim(replace(replace(replace(replace(replace(replace(replace(replace(replace(replace(replace(replace(replace(replace(
  items('Aplicar_SEs')?['NomeSE']
, '/', '-'), ':', '-'), '*', ''), '?', ''), '"', ''), '<', ''), '>', ''), '|', ''), '#', ''), '%', ''), '&', 'E'), '{', ''), '}', ''), '~', ''))
```

`trim` no fim e `& { } ~` na lista: o SharePoint normaliza o nome ao criar a pasta (corta espaço
nas pontas, rejeita esses caracteres). Sem isso, o nome gravado fica diferente da string que o
`Criar_pasta_Ambiente` remonta — e o caminho dele dá **BadRequest** (teste 13.09, `INV-003`).

#### 17c. Criar nova pasta — `Criar_pasta_SE`

- Biblioteca: `Projetos`
- Caminho: `/@{outputs('PastaProjeto')}`
- Nome:

```
concat(items('Aplicar_SEs')?['CodSE'], ' - ', outputs('NomeSE_Sanitizado'))
```

Configurar execução após: êxito e falha.

#### 17d. Criar nova pasta — `Criar_pasta_Ambiente`

# Nome interno da ação pode ficar. O **Nome** da pasta (18.09) é `Visão geral`.

- Caminho:

```
concat('/', outputs('PastaProjeto'), '/', items('Aplicar_SEs')?['CodSE'], ' - ', outputs('NomeSE_Sanitizado'))
```

- Nome: `Visão geral`

Configurar execução após: êxito e falha.

#### 17e. Operação de dados — Compor — `FimPastasSE`

Entradas: `ok`

**Configurar execução após:** marcar **com êxito**, **falhou**, **foi ignorado** e **atingiu o tempo limite**.

Por que existe: pasta é secundária, item é o produto. Sem esta ação a cadeia do loop termina no
`Criar_pasta_Ambiente` — se ela falhar (e ela falha sempre que o `Criar_pasta_SE` falhou, porque o
caminho dela é a pasta da SE), o `Aplicar_SEs` fica **Failed** e tudo depois dele com
"execução após = com êxito" é **pulado**: `Listar_Itens`, `Aplicar_Itens`, nenhum item criado.
Terminando a cadeia num Compose que aceita falha, o loop fecha verde e os itens entram mesmo
quando a pasta não pôde ser criada. Teste 13.09 (`INV-003`): 5 SEs, 0 itens, por causa disso.

---

### 18. Responder a um Power App — `Responder_OK`

**Posição (decisão 13.09 — "quase total"): primeira ação do ramo `Se não` do `JaImportou`,
ANTES do `Listar_SEs` (16).** Não fica mais depois do `Aplicar_SEs`.

| Saída | Valor |
|-------|--------|
| erro | `@{variables('varRespErro')}` |
| qtdSEs | `@{body('Analisar_JSON')?['qtdSEs']}` |
| qtdItens | `@{body('Analisar_JSON')?['qtdItens']}` |
| pasta | `@{outputs('PastaProjeto')}` |
| listaSEs | `@{body('Analisar_JSON')?['listaSEs']}` |

As cinco saídas já existem nesse ponto: `qtdSEs`, `qtdItens` e `listaSEs` saem do
`Analisar_JSON` (6) e `pasta` do `PastaProjeto` (11). Nada depende do `Aplicar_SEs`.

**`erro` vai com a variável, não vazio.** Chegando aqui ela está sempre em branco (todo
ramo de erro anterior responde e encerra por conta própria — 3a/3b, 7a/7b, 9, 15), e
branco é o que o app lê como sucesso (regra do 18b). Deixar a variável em vez de vazio
custa nada e é rede: se um dia um ramo gravar a mensagem e esquecer o **Encerrar**, o app
recebe o texto do erro em vez de um "importado com sucesso" falso.

**Por que subiu:** enquanto o `Run` não volta, o app está travado numa linha de fórmula —
Timer não dispara, `Set` não roda, tela congelada no spinner. Respondendo aqui, o app é
solto em ~12 s (upload + script + composes + pasta raiz) em vez de ~35 s, e a barra de
progresso passa a cobrir **SEs + pastas + itens** (89% do tempo em vez de 63%).
Medições da amostra 5 SEs / 65 itens: upload ~6 s · script ~4 s · SEs ~10 s ·
pastas ~15 s · itens ~60 s.

**O que se perde:** erro de `Criar_pasta_raiz`, `Criar_SE` ou `Criar_Item` não chega mais
ao app pela resposta — os quatro erros que **importam** (não-xlsx, script, projeto
inexistente, já importado) são todos anteriores e continuam respondendo e encerrando.
Falha depois da resposta aparece como **barra parada** no popup e no histórico do fluxo.

**Não responder duas vezes:** uma run só pode ter um `Responder a um Power App`
executado. Ver 18c — o `Responder App` genérico se muda para o ramo Falso da condição.

**As duas ações de resposta têm de ter o mesmo schema:** nomes (`erro`, `qtdSEs`,
`qtdItens`, `pasta`, `listaSEs`) e tipos idênticos nas duas. É desse schema que o Power Apps
monta o `saida.` — divergência entre os dois Responder muda a assinatura do fluxo e derruba
o `btnImportarProjeto`.

**Erro `ActionSchemaInvalid` ao salvar** — "The schema definitions for actions with same
status code must match". É isso: os dois Responder divergem em campo ou tipo. O jeito de
não errar é **não digitar o segundo**: nos `⋯` do Responder existente → **Copiar para minha
área de transferência**, depois **Colar uma ação** no lugar novo e trocar **só os valores**.
Tipo entra pelo dedo: `qtdSEs`/`qtdItens` no fluxo atual são **texto** (as variáveis
`varRespQtdSEs`/`varRespQtdItens` vêm de `concat('', ...)`), e criar o novo como Número
quebra o salvamento. Texto serve — o app faz `Value(saida.qtdses)`.
Conferência: `⋯ → Exibição de código` nos dois e comparar o bloco `"schema"`.

---

### 18a. Desenho real do fluxo (conferido no Studio 14.09)

O fluxo **não** tem um `Responder` por ramo. Ele tem **um Responder genérico** que lê cinco
variáveis, e cada caminho preenche as variáveis antes de chegar nele:

| Variável | Quem grava | Valor |
|----------|------------|-------|
| `varRespErro` | ramo de erro (mensagem) · sucesso (`Definir variável 4`) | mensagem ou `-` |
| `varRespQtdSEs` | `Definir variável 5` | `concat('', body('Analisar_JSON')?['qtdSEs'])` |
| `varRespQtdItens` | `Definir variável 6` | `concat('', body('Analisar_JSON')?['qtdItens'])` |
| `varRespPasta` | `Definir variável 7` | `concat('', outputs('PastaProjeto'))` |
| `varRespListaSEs` | `Definir variável 8` | `concat('', body('Analisar_JSON')?['listaSEs'])` |

As cinco `Definir variável` de sucesso ficam **depois do `Aplicar_SEs`**, e os ramos de erro
não precisam de `Encerrar`: quando um ramo de condição termina, a execução continua na ação
seguinte ao `If`, no nível de fora — os dois caminhos convergem naturalmente no `Responder`.

**Consequência para o "responder cedo" (18):** o `Responder_OK_Cedo` roda **antes** dessas
cinco ações, então não pode usar `variables('varResp...')` — elas ainda estão vazias ali.
Ele usa as expressões diretas (`body('Analisar_JSON')?[...]` e `outputs('PastaProjeto')`),
que já existem nesse ponto. É a tabela do passo 18.

### 18b. `varRespErro` — a variável que decide sucesso

**Regra:** **vazio** significa "sem erro". Quem escreve na variável é só ramo de erro.
Nada de comparar com `-`: o hífen digitado e o hífen colado podem ser caracteres diferentes
(`-` U+002D vs `–` U+2013) e a igualdade dá Falso com os dois lados parecendo iguais na tela —
foi o que travou o run 13.09 do `INV-003` (5 SEs, 0 itens).

#### Inicializar variável — `varRespErro` (primeira ação depois do gatilho)

| Campo | Valor |
|-------|--------|
| Nome | `varRespErro` |
| Tipo | Cadeia de caracteres |
| Valor | **em branco** |

#### Ramos de erro — `Definir variável`

Cada ramo de erro grava a mensagem antes de cair na condição final:

| Ramo | Mensagem |
|------|----------|
| `EhXlsx` falso | `Manda um arquivo .xlsx` |
| `ScriptOk` falso | `if(empty(body('Analisar_JSON')?['erro']), 'A base não tem nenhuma SE (CÓDIGO ODI vazio)', body('Analisar_JSON')?['erro'])` |
| `TemCampanha` falso | `Projeto não encontrado em Campanhas` |
| `JaImportou` verdadeiro | `Esse projeto já tem instalações. Não reimporta.` |

### 18c. Condição — `Condicao Sucesso`

Primeiro valor (fx):

```
or(empty(trim(coalesce(variables('varRespErro'), ''))), equals(trim(variables('varRespErro')), '-'))
```

Operador **é igual a**. Segundo valor: `true`.

Aceita vazio, só espaços e o hífen — nenhum dos três depende de o campo ter o caractere certo.

- **Verdadeiro:** `Listar_Itens` → `Aplicar_Itens`. Sem `Responder` aqui: o app
  já foi respondido pelo `Responder_OK_Cedo`, antes do `Listar_SEs`.
  **Demo (≤5000 itens):** sem Fazer até, sem `varSkipItens`. Paginação 5000 no Listar.
  **Stand-by (>5000):** fatiar `tblImportItens` no script — Ignorar do Excel não pagina.
- **Falso:** é para cá que o `Responder App` genérico **se muda** (ele estava solto entre o
  `JaImportou` e esta condição). Continua lendo `variables('varResp...')`.

Por que funciona sem responder duas vezes: os quatro erros que preenchem `varRespErro` com
mensagem — `EhXlsx`, `ScriptOk`, `TemCampanha`, `JaImportou` — acontecem **antes** do
`Responder_OK_Cedo` e em ramos irmãos, então nunca passam por ele; caem aqui no Falso e são
respondidos. O caminho de sucesso responde cedo e nunca entra no Falso. Uma resposta por run,
que é o limite do Automate ("response already sent" derruba a segunda).

O App trata sucesso como `saida.erro` em branco **ou** igual a `-`
(`!IsBlank(saida.erro) && saida.erro <> "-"` no `btnImportarProjeto`), então os dois casos casam.

---

### 18d. ~~Variável — `varSkipItens`~~ — **APAGAR (demo)**

Não usa. Ignorar do Excel não pagina (teste 16.09: parou em 321 / 602). Volta quando o script
fatiar `tblImportItens_0`, `_1`, …

---

### 19. Excel — Listar linhas — `Listar_Itens`

No ramo **Verdadeiro** da `Condicao Sucesso`. **Sem** Fazer até.

- Arquivo: conteúdo dinâmico **Id** do `Criar_arquivo` — **não** escolher pelo navegador de arquivos.
- Tabela: `tblImportItens` (aba `_ImportItens`, criada pelo script)
- **⋯ → Configurações:** Paginação **ligada** · limite **5000**
- Opções avançadas: **Contagem superior** e **Ignorar** **vazios**

Teto do fluxo disparado: 5000. 3714 entra numa chamada. Acima disso = stand-by (fatiar tabela).

**Este passo e o 20 ficam no mesmo ramo do `Criar_SE`** — Verdadeiro da `Condicao Sucesso`. Se caírem no Se sim do `JaImportou` (ou dentro do `Aplicar_SEs`), o run fecha verde e nenhum item é criado.

---

### 20. Aplicar a cada — `Aplicar_Itens`

Saída: `body('Listar_Itens')?['value']`

**⋯ → Configurações** → Controle de simultaneidade **ligado** · **20**.

**Depois** do `Listar_Itens`, no mesmo ramo (não dentro de Fazer até).

#### 20a. SharePoint — Criar item — `Criar_Item`

Lista: `Inventario`

| Campo | Valor |
|-------|--------|
Tudo por **fx** (`N` = campo numérico, precisa do `null` — ver 20b):

| Campo | Expressão |
|-------|-----------|
| Title | `if(empty(string(items('Aplicar_Itens')?['CodAsset'])), items('Aplicar_Itens')?['DescricaoBem'], items('Aplicar_Itens')?['CodAsset'])` |
| CodInventario | `outputs('CodLimpo')` |
| CodSE | `items('Aplicar_Itens')?['CodSE']` |
| NomeSE | `items('Aplicar_Itens')?['NomeSE']` |
| CodAsset | `items('Aplicar_Itens')?['CodAsset']` |
| IdItem **N** | `if(empty(string(items('Aplicar_Itens')?['IdItem'])), null, items('Aplicar_Itens')?['IdItem'])` |
| Imobilizado | `items('Aplicar_Itens')?['Imobilizado']` |
| CodTUC | `items('Aplicar_Itens')?['CodTUC']` |
| DescricaoTUC | `coalesce(items('Aplicar_Itens')?['DescricaoTUC'], items('Aplicar_Itens')?['TIPO DE UNIDADE DE CADASTRO'])` |
| IdUC | `coalesce(items('Aplicar_Itens')?['IdUC'], items('Aplicar_Itens')?['IDUC'])` |
| TI **N** | `if(empty(string(items('Aplicar_Itens')?['TI'])), null, items('Aplicar_Itens')?['TI'])` |
| LocalInstalacao **N** | `if(empty(string(items('Aplicar_Itens')?['LocalInstalacao'])), null, items('Aplicar_Itens')?['LocalInstalacao'])` |
| ArranjoFisico **N** | `if(empty(string(items('Aplicar_Itens')?['ArranjoFisico'])), null, items('Aplicar_Itens')?['ArranjoFisico'])` |
| AtributoA1 **N** | `if(empty(string(items('Aplicar_Itens')?['A1'])), 0, float(items('Aplicar_Itens')?['A1']))` |
| AtributoA2 **N** | `if(empty(string(items('Aplicar_Itens')?['A2'])), 0, float(items('Aplicar_Itens')?['A2']))` |
| AtributoA3 **N** | `if(empty(string(items('Aplicar_Itens')?['A3'])), 0, float(items('Aplicar_Itens')?['A3']))` |
| AtributoA4 **N** | `if(empty(string(items('Aplicar_Itens')?['A4'])), 0, float(items('Aplicar_Itens')?['A4']))` |
| AtributoA5 **N** | `if(empty(string(items('Aplicar_Itens')?['A5'])), 0, float(items('Aplicar_Itens')?['A5']))` |
| AtributoA6 **N** | `if(empty(string(items('Aplicar_Itens')?['A6'])), 0, float(items('Aplicar_Itens')?['A6']))` |
| DescricaoBem | `items('Aplicar_Itens')?['DescricaoBem']` |
| Quantidade **N** | `if(empty(string(items('Aplicar_Itens')?['Quantidade'])), null, items('Aplicar_Itens')?['Quantidade'])` |
| Unidade | `items('Aplicar_Itens')?['Unidade']` |
| Elegivel | `items('Aplicar_Itens')?['Elegivel']` |
| Reserva | `items('Aplicar_Itens')?['Reserva']` |
| Fabricante | `items('Aplicar_Itens')?['Fabricante']` |
| Modelo | `items('Aplicar_Itens')?['Modelo']` |
| NumSerie | `items('Aplicar_Itens')?['NumSerie']` |
| Ano **N** | `if(empty(string(items('Aplicar_Itens')?['Ano'])), null, items('Aplicar_Itens')?['Ano'])` |
| Bay | `items('Aplicar_Itens')?['Bay']` |
| CodOperacao | `items('Aplicar_Itens')?['CodOperacao']` |
| Projeto | `items('Aplicar_Itens')?['Projeto']` |
| Observacoes | `items('Aplicar_Itens')?['Observacoes']` |
| CM **N** | `if(empty(string(items('Aplicar_Itens')?['CM'])), null, items('Aplicar_Itens')?['CM'])` |
| Status | `Pendente` (texto digitado, sem fx) |

Não preenche `Sobra`. `Elegivel` ≠ `Status`.

#### 20b. Campo numérico vazio — `null`, nunca `""`

Coluna **Número** na lista + célula vazia na base = falha na hora de criar o item:

```
Input parameter 'item/AtributoA2' is required to be of type 'Number/double'.
The runtime value '""' to be converted doesn't have the expected format 'Number/double'.
```

O script **mantém** `00` (é código, não vazio). Célula realmente vazia vira `"00"`.
No SharePoint (Número) isso grava **0** — a tela formata `Text(...; "00")`.

Cada campo numérico de atributo vai por **fx** (`0` no lugar de `null`):

```
if(empty(string(items('Aplicar_Itens')?['A2'])), 0, float(items('Aplicar_Itens')?['A2']))
```

Cabeçalho da tabela e o `fx` usam o **mesmo** nome: `A1` … `A6`.

O `string()` protege quando o Excel devolve número em vez de texto — `empty()` sozinho quebra
com número.

**Lista fechada dos campos que precisam do `fx`:**

| Ação | Campo | Coluna do Excel |
|------|-------|-----------------|
| `Criar_SE` | `TI` | `TI` |
| `Criar_SE` | `LocalInstalacao` | `LocalInstalacao` |
| `Criar_SE` | `ArranjoFisico` | `ArranjoFisico` |
| `Criar_item` | `TI` | `TI` |
| `Criar_item` | `LocalInstalacao` | `LocalInstalacao` |
| `Criar_item` | `ArranjoFisico` | `ArranjoFisico` |
| `Criar_item` | `AtributoA1` … `AtributoA6` | `A1` … `A6` |
| `Criar_item` | `Quantidade` | `Quantidade` |
| `Criar_item` | `Ano` | `Ano` |
| `Criar_item` | `CM` | `CM` |
| `Criar_item` | `IdItem` | `IdItem` |

Conferir em `Inventario` se **`Imobilizado`** é Número — se for, entra na lista.

Campo de **texto** aceita `""`: `CodSE`, `NomeSE`, `ClasseTensao`, `CodAsset`, `CodTUC`,
`DescricaoBem`, `Unidade`, `Elegivel`, `Reserva`, `Fabricante`, `Modelo`, `NumSerie`, `Bay`,
`CodOperacao`, `Projeto`, `Observacoes` ficam com o token dinâmico normal.

**Decisão pendente:** `AtributoA1`…`A6` são **códigos** de atributo (a chave de avaliação é
TI + CM + TUC + A1–A6), não grandezas. Como Número, um código `01` grava `1` e o casamento por
código pode falhar. Avaliar trocar essas seis colunas para **Texto** — aí o `""` deixa de ser
problema e o zero à esquerda sobrevive.

### 20c. ~~Incrementar variável — `IncSkipItens`~~ — **APAGAR (demo)**

---

O App manda **2 textos**: `pacoteArquivo` (`nome|JSON`) e `CodInventario`. O fluxo grava o `.xlsx` e preenche SE / TI / item.

Mudou o gatilho: **Publicar** o fluxo. Só depois o Studio → **Atualizar** o `flxImportarCampanha`. Salvar sozinho não muda o `Run`.

`Tela_Exportar` → `Image6_close_sharp_6` → `OnSelect`: fórmula do passo 19 em `docs/powerfx/Tela_Exportar-formulas.txt`.

Sucesso = `saida.erro` igual a `"-"`.
