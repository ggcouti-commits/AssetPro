# Studio + Automate — pastas Visão geral + código do item (18.09)

> Fenômeno. Ata: `docs/reunioes/2026-09-18.md`. Spec: `docs/exportacao-fotos-pastas.md`.
> Fluxos: `docs/automate/flxImportarCampanha.md` · `docs/automate/flxPastaFoto.md`.
> `TipoFoto` continua `AMBIENTE` / `ITEM`. ZIP não monta.
> Um controle / uma ação = um passo. Dentro do loop, foto = `items('Aplicar_Fotos')`.

Árvore: `Projetos/{PastaProjeto}/{CodSE} - {NomeSE}/Visão geral` ou `.../{Imobilizado|CodAsset}`.

---

## A. SharePoint (uma vez — pula se já tem)

1. Biblioteca **`Projetos`** no site AssetPro.
2. Lista **`Campanhas`** → coluna texto **`PastaProjeto`**.
3. Lista **`Fotos`** → coluna Sim/Não **`CopiadoPasta`** (padrão Não).
4. Studio → Dados → Atualizar `Campanhas` e `Fotos`.

---

## B. `flxImportarCampanha` → `Criar_pasta_Ambiente`

O **nome interno** da ação pode ficar. O **Nome** da pasta:

```
Visão geral
```

Caminho (não mexe):

```
concat('/', outputs('PastaProjeto'), '/', items('Aplicar_SEs')?['CodSE'], ' - ', outputs('NomeSE_Sanitizado'))
```

Execução depois: êxito **e** falha. **Publicar.**

---

## C. `flxPastaFotosVisita` — pasta destino

### C1. `Criar_pasta_Ambiente` (ramo AMBIENTE) → Caminho da Pasta

```
concat(outputs('CaminhoSE'), '/Visão geral')
```

### C2. `CaminhoDestino_Amb` → Entradas

```
concat(outputs('CaminhoSE'), '/Visão geral')
```

# Campanha velha: se `Visão geral` 404 e só existir `Ambiente`, o lote ainda grava em `Ambiente`. Importação nova só cria `Visão geral`. Não migrar pasta antiga.

### C3. `ImobilizadoLimpo` → Entradas

```
trim(replace(replace(replace(replace(replace(replace(replace(replace(replace(replace(replace(replace(replace(replace(
  string(coalesce(first(body('Item_desta_foto'))?['Imobilizado'], ''))
, '/', '-'), ':', '-'), '*', ''), '?', ''), '"', ''), '<', ''), '>', ''), '|', ''), '#', ''), '%', ''), '&', 'E'), '{', ''), '}', ''), '~', ''))
```

### C4. `NomePastaItem` → Entradas

```
if(
  empty(outputs('ImobilizadoLimpo')),
  if(empty(items('Aplicar_Fotos')?['CodAsset']), 'SEM-IMOB', items('Aplicar_Fotos')?['CodAsset']),
  outputs('ImobilizadoLimpo')
)
```

**Não** concatena `DescricaoBem`.

### C5. Criar pasta do item → Caminho da Pasta

```
concat(outputs('CaminhoSE'), '/', outputs('NomePastaItem'))
```

**Publicar.** Studio → o fluxo → **Atualizar**.

---

## D. Mobile — rótulo da câmera de cima

### D1. `Tela_ItensVisita` → `btnFotosAmbiente` → `Text` (botão clássico)

```
"Visão geral"
```

### D2. Se for Image Mundo Power → `Image` — só o primeiro `With`

`IconText`: `"Visão geral"`

O nome do controle **não** muda. `TipoFoto` no Patch continua `"AMBIENTE"`.

---

## E. `btnEnviarVisitaExec` → `OnSelect`

No **fim** do `ForAll` das fotos, **depois** do `SaveData` de `colFotosCampo`, **antes** do toast. Se já tem, não duplica:

```
IfError(
    flxPastaFotosVisita.Run(gblInventarioSelecionado.CodInventario);
    Blank()
);;
```

**Não** chama o fluxo dentro do `ForAll`.
