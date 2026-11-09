# Colunas SharePoint — Módulo Gás (1ª entrega Bahia)

Site: `https://gustavogarciacoutinho991.sharepoint.com/sites/AssetPro`  
Inventario list GUID: `{b509ef8f-89cc-4887-b1b8-fbf24f933471}`  
Subestacoes list GUID: `{bcb725d6-a54d-4bc7-9a84-d8ae1287fd5a}`

## Inventario (item gás)

| InternalName | Display | Tipo |
|--------------|---------|------|
| Diametro | Diâmetro | Texto (255) |
| ClassePressao | Classe de pressão | Texto (255) |
| Tag | TAG | Texto (255) |
| DescricaoComplementar | Descrição técnica complementar | Texto (255) |

**Não** criar `Tramo` no Inventario — tramo é da localidade.  
A1–A6 / CM / Bay ficam em branco no gás.

## Subestacoes (local gás)

| Base Excel | Coluna SP | Notas |
|------------|-----------|-------|
| OSI (local) | **`NomeSE`** (já existe) | Não criar coluna OSI |
| Cód C.I. | **`CodSE`** (já existe) | Não criar coluna CodCI |
| DESCRIÇÃO DO EMPREENDIMENTO | espelha / UI com `NomeSE` | mesmo campo do local |
| MUNICÍPIO | **`Municipio`** (já existe) | |
| SEGMENTO | **`Segmento`** — **criar** | Texto (255) |
| TIPO DE TRAMO | **`Tramo`** — **criar** | Texto (255) · SIMPLES / DUPLO / TRIPLO · **da localidade**, não do item |

**Criar em Subestacoes:** `Segmento` · `Tramo` (Texto uma linha, 255).

`PendenteCriacao` é **só coleção local** (`colSubestacoes`) — não criar no SP. Materializa no Enviar visita via `Patch(Subestacoes)` quando `ID` vazio.

## Após criar

Studio → Dados → Inventario / Subestacoes → **Atualizar**.

Script: `scripts/sp-add-gas-columns.ps1` (PnP, conta dona do site).
