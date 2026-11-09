# Pastas de fotos no SharePoint — projeto / SE / Visão geral / item

> Decisão 2026-09-10 (Fenômeno). **Corte 18.09.2026** (André × João × Bruno): pasta do item = **só o código**; `Ambiente` vira **Visão geral**.  
> Ata: `docs/reunioes/2026-09-18.md`.  
> Site: `https://gustavogarciacoutinho991.sharepoint.com/sites/AssetPro`  
> Front: **Projeto**. Back: lista `Campanhas`, fluxo `flxImportarCampanha`.
>
> Mockup tela: `docs/screens/mockup-home-importar-exportar.html` · PNG `docs/screens/exportar-planilha-fotos.png`  
> Mockup pastas: `docs/screens/mockup-pastas-fotos.html` · PNG `pastas-fotos-apos-importar.png` · `pastas-fotos-apos-visita.png`

A lista **`Fotos`** continua sendo o que o app consulta (galeria, desktop).  
A biblioteca **`Projetos`** é onde a foto mora. O André baixa a pasta no SharePoint. **Não** zipar agora.

`TipoFoto` na lista **não muda**: `AMBIENTE` / `ITEM`. Só o **nome da pasta** e o rótulo da câmera de cima mudam.

## Quando cria o quê

| Momento | Quem | O que cria |
|---------|------|------------|
| Importar projeto (`flxImportarCampanha`) | Automate | Pasta raiz `{PastaProjeto}` + uma pasta por SE importada + `Visão geral/` vazia em cada SE |
| Enviar visita (Patch na lista `Fotos`) | `flxPastaFotosVisita` (um `Run` após o ForAll) | Pasta do item se faltar; JPG. **Não** gatilho por linha |
| Exportar planilha (`btnExportarCamp` → `flxExportarCampanha`) | Automate | Só o `.xlsx` em `Exportacoes` — SEs `Status = "Finalizada"`. `TI`, `LocalInstalacao`, `ArranjoFisico` saem da linha de `Inventario`. |
| Exportar fotos (`btnExportarFotos` → `flxExportarFotos`) | **Stand-by** | ZIP futuro. Não montar. |
| Excluir projeto (`btnExcluirCamp` → `flxExcluirCampanha`) | Automate | Apaga Campanhas + SEs + Inventario + Fotos + Alocacoes + pasta `{PastaProjeto}` + xlsx em Importacoes/Exportacoes |

O `ForAll` do `btnEnviarVisitaExec` **não muda**: continua Patch na lista `Fotos`. A pasta nasce no fluxo, fora do app, para não estourar timeout.

## Árvore

```
Projetos/                                          ← biblioteca (Documentos)
  {PastaProjeto}/                                  ← 1 pasta por campanha
    {CodSE} - {NomeSE}/                            ← 1 pasta por subestação
      Visão geral/                                 ← fotos TipoFoto = AMBIENTE
        20260910-143022_12.jpg
      50018784/                                    ← item: só o código exclusivo
        20260910-144110_13.jpg
      ASSET-7SEGU001-200219/                       ← sem imobilizado: cai no CodAsset
        20260910-145001_14.jpg
```

`Visão geral` é nome reservado. Pasta de item = **só o número exclusivo** (imobilizado, ou PM se a base foi montada assim, senão `CodAsset`). **Sem** `DescricaoBem` no path — Bruno (18.09): projeto + SE + descrição estoura o limite do SharePoint (~400). André: Ctrl+F nesse número acha o cara.

Chave no app continua `CodAsset`. O nome da pasta é rótulo para o escritório achar a foto.

Regra do código (sanitizar `\ / : * ? " < > | # %`):

```
Coalesce(Imobilizado; CodAsset; "SEM-IMOB")
```

Não concatenar descrição. Não usar `CodTemp` se já tem `CodAsset`.

Campanha velha que só tem pasta `Ambiente`: o lote **grava em `Ambiente` se ela existir e `Visão geral` não**. Importação nova **só cria `Visão geral`**. Não migrar pasta antiga no fluxo.

## SharePoint — uma vez

### 1. Biblioteca `Projetos`

1. Site **AssetPro** → **Conteúdo do site** → **Novo** → **Biblioteca de documentos**
2. Nome: `Projetos` (interno igual)
3. Sem versionamento obrigatório. Sem checkout.

Não misturar com a lista `Fotos` nem com a biblioteca `Exportacoes` (lá fica o `.xlsx` de saída).

### 2. Coluna `Campanhas.PastaProjeto`

1. Site **AssetPro** → lista **`Campanhas`**
2. **+ Adicionar coluna** → Texto de uma linha → `PastaProjeto`
3. Studio → **Dados** → **`Campanhas`** → **Atualizar**

Grava **uma vez** na importação. Se o Fenômeno renomear o projeto na lista, a pasta no disco **não** muda.

Formato do valor (relativo à biblioteca):

```
{NomeSanitizado}_{8 primeiros do CodInventario}
```

Ex.: `Revisao tarifaria Celpe_a1b2c3d4`

Sanitizar: tirar `\ / : * ? " < > | # %` e cortar o nome em 80 caracteres. GUID completo no nome da pasta estoura path do SharePoint (limite ~400). Por isso a pasta do item **não leva descrição**.

## Fluxo — `flxImportarCampanha` (acrescento)

Depois de criar o item em `Campanhas` e as linhas em `Subestacoes`:

1. Calcular `PastaProjeto` (sanitizar + 8 chars do guid).
2. **Patch** `Campanhas.PastaProjeto`.
3. SharePoint — **Create new folder**: biblioteca `Projetos`, pasta `{PastaProjeto}`.
4. **Apply to each** nas SEs recém-criadas:
   - pasta `{PastaProjeto}/{CodSE} - {NomeSE sanitizado}`
   - pasta `{...}/Visão geral` (ação pode continuar `Criar_pasta_Ambiente`; o **Nome** da pasta é `Visão geral`)
5. Se a pasta já existir (reimport / retry), seguir. Não falhar o fluxo.

Nome da pasta da SE: `{CodSE} - {NomeSE}`. `CodSE` na frente para não colidir duas SEs com nome parecido.

## Fluxo — `flxPastaFotosVisita` (passo a passo)

Spec completo: `docs/automate/flxPastaFoto.md`.

**Gatilho:** um `Run` no fim do `btnEnviarVisitaExec`. **Não** *When an item is created* (300 fotos = 300 runs).

1. Ler `CodInventario`, `CodSE`, `TipoFoto`, `CodAsset`, `FotoCampo`, `ID`.
2. **Get item** `Campanhas` onde `CodInventario` = o da foto → `PastaProjeto`.
3. **Get item** `Subestacoes` onde `CodInventario` + `CodSE` → `NomeSE`.
4. Se `ITEM`: **Get item** `Inventario` onde `CodInventario` + `CodAsset` → `Imobilizado` (**não** precisa `DescricaoBem` para o path). O `ForAll` do envio grava o item **antes** da foto; se o Get vier vazio, Delay 10s e tenta de novo.
5. Montar caminho:

| `TipoFoto` | Pasta destino |
|------------|----------------|
| `AMBIENTE` (ou Title começa com `AMBIENTE`) | `{PastaProjeto}/{CodSE} - {NomeSE}/Visão geral` (fallback: `…/Ambiente` se só ela existir) |
| `ITEM` | `{PastaProjeto}/{CodSE} - {NomeSE}/{Coalesce(Imobilizado; CodAsset; "SEM-IMOB")}` |

6. **Create new folder** no destino se Get folder der 404.
7. **Get file content** do `FotoCampo` (campo imagem da lista).
8. **Create file** na pasta:

```
{yyyyMMdd-HHmmss}_{ID}.jpg
```

`ID` da lista `Fotos` no nome: reenvio não sobrescreve foto antiga.

Se `PastaProjeto` estiver vazio (campanha velha, criada antes desta coluna): o fluxo calcula o mesmo padrão, cria a pasta raiz e **Patch** `Campanhas.PastaProjeto`. Não deixa foto órfã.

Não apagar a linha da lista `Fotos`. App e pasta convivem.

## Fluxo — `flxExportarCampanha` (só planilha)

`.xlsx`, nunca CSV. Spec: `docs/automate/flxExportarCampanha.md`.

`CodInventario` → SEs Finalizada → itens dessas SEs → copia `modelo-exportacao.xlsx` → script `PreencherExportacao` preenche `tblItens` (`TI` / local / arranjo da linha de Inventario) → `link` em `Exportacoes`.

**Não** zipar foto neste fluxo.

## Fluxo — `flxExportarFotos` (stand-by)

Não montar. Foto já está em `Projetos`. Quando for a vez: ZIP das pastas das SEs Finalizada.

## App — um botão no card

Fórmulas: `docs/powerfx/Tela_Exportar-formulas.txt`.

| Controle | Texto | Fluxo | Fill |
|----------|-------|-------|------|
| `btnExportarCamp` | Planilha / Sem saída | `flxExportarCampanha` | `Cor.PrimaryD60` |
| `btnExcluirCamp` | Excluir | `flxExcluirCampanha` (depois do popup) | ghost `Cor.Delete` |

Zero SE Finalizada: **Sem saída** (`DisplayMode.Disabled`). **Não** duplicar `btnExportarFotos`. Excluir fica no slot do Fotos.

Apagar o projeto: spec `docs/automate/flxExcluirCampanha.md`. Mockup: `docs/screens/excluir-projeto.png`.

`btnEnviarVisitaExec` chama **um** `flxPastaFotosVisita.Run` depois do `ForAll`. Foto → lista `Fotos` → lote copia JPG.

Rótulo da câmera de cima no mobile: **Visão geral** (não “Ambiente”). Controle pode continuar `btnFotosAmbiente`.

## O que não fazer

- Não gravar JPG só na biblioteca e apagar a lista — a consulta desktop filtra `Fotos`.
- Não criar pasta de item na importação (milhares de pastas vazias).
- Não usar `Subestacoes.CM` / `gblSEselecionada.CM` no path.
- Não nomear pasta de item com `DescricaoBem`. Rótulo = **código exclusivo**.
- Não criar pasta no Power Apps (`ForAll` + Automate por foto = timeout).
- Não `Remove`/`ForAll` no App para apagar projeto. É `flxExcluirCampanha`.
- Não mudar `TipoFoto` de `AMBIENTE` para outro valor só porque a pasta mudou de nome.

## Ordem de montagem

1. Biblioteca `Projetos` + coluna `Campanhas.PastaProjeto`.
2. `flxImportarCampanha` cria a raiz + SEs + `Visão geral`.
3. `flxPastaFotosVisita` (lote no envio).
4. `flxExportarCampanha` gera só o Excel (com TI / local / arranjo). ZIP de fotos = stand-by.
5. Studio: `btnExportarCamp`. Não duplicar botão Fotos. Rótulo da câmera de cima = Visão geral.
6. `flxExcluirCampanha` + `btnExcluirCamp` no card (popup confirma).
