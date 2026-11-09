# Fluxo `flxSubirXlsx` — do zero

> Sobe o `.xlsx` do picker para a biblioteca **`Importacoes`**.  
> Site: `https://gustavogarciacoutinho991.sharepoint.com/sites/AssetPro`  
> Gatilho: **Power Apps (V2)** — o antigo **não existe** mais neste tenant.  
> **Publica** depois de salvar. Senão o App não vê o `Run`.

O canvas **não** manda bytes por `JSON` (`appres://blobmanager`). Este fluxo usa entrada **Arquivo**. Se o Studio barrar `contentBytes` (Blob), não luta: o App faz `Patch` em `Importacoes` e **não** chama este fluxo.

---

## Criar

make.powerautomate.com → **Criar** → **Fluxo da nuvem instantâneo** → pular o gatilho da lista → em branco.

Nome: `flxSubirXlsx`

---

### 1. Gatilho — Power Apps (V2)

Apaga o gatilho vazio. Adiciona **Power Apps (V2)**.

**Adicionar uma entrada** — nesta ordem:

1. Tipo **Arquivo** → nome `arquivo`
2. Tipo **Texto** → nome `nomeArquivo`

`nomeArquivo` já vem com o prefixo do App: `{CodInventario}-{nome.xlsx}`.

---

### 2. SharePoint — Criar arquivo — `Criar_xlsx`

- Site: AssetPro
- Biblioteca: `Importacoes`
- Pasta: `/`
- **Nome do arquivo** — conteúdo dinâmico **`nomeArquivo`**.  
  Se não aparecer, fx:

```
triggerBody()?['text']
```

Se o peek code mostrar `text_1` (não `text`), usa:

```
triggerBody()?['text_1']
```

- **Conteúdo do arquivo** — conteúdo dinâmico **`arquivo`** / **Conteúdo do arquivo**.  
  **Não** envolve `base64ToBinary` se o seletor já for o arquivo.

Se o seletor só tiver bytes em texto, fx:

```
base64ToBinary(triggerBody()?['arquivo']?['contentBytes'])
```

---

### 3. Responder a um Power App — `Responder_App`

Uma saída, tipo **Texto**:

| Nome | fx |
|------|-----|
| `ok` | `'sim'` |

Um Responder só. Sem Encerrar.

---

### 4. Salvar → **Publicar**

---

## App

Studio → Power Automate → **Adicionar fluxo** → `flxSubirXlsx`.

`Tela_Exportar` → `Image6_close_sharp_6` → no `OnSelect`, **antes** do `flxImportarCampanha.Run`:

```
flxSubirXlsx.Run(
    {
        file: {
            name: First(attPlanilha.Attachments).Name;
            contentBytes: First(attPlanilha.Attachments).Value
        }
    };
    varNovaCampanha.CodInventario & "-" & First(attPlanilha.Attachments).Name
)
```

Digita `flxSubirXlsx.Run(` e casa a ordem do IntelliSense: **arquivo + nomeArquivo**.  
Se o 1º parâmetro se chamar `arquivo`, troca `file:` por `arquivo:` no record.

Se o Studio disser **coluna `contentBytes` ausente (Blob)**: apaga esse `Run`. O upload é o `Patch` da biblioteca `Importacoes` (`{FilenameWithExtension}` + `{Content}`). Spec: `docs/powerfx/Tela_Exportar-formulas.txt` passo 19.

---

## Depois

O `flxImportarCampanha` **não** cria o arquivo de novo. Ele **obtém metadados** do caminho:

```
concat(outputs('CodLimpo'), '-', triggerBody()?['text_1'])
```

`text_1` do import = nome original (`amostra-importacao-5ses.xlsx`). O arquivo na biblioteca = `{CodInventario}-{esse nome}`.
