# AssetPro / Infralytics

App de inventário em subestações elétricas: compara o físico com a base (SAP/GIS) e gera a saída para revisão tarifária (ANEEL MCPSE).

Front no desktop: **Projeto**. Lista SharePoint e fluxos: **`Campanhas`**. Spec: `.cursor/rules/projetos-nomenclatura.mdc`.

## Stack

- **App:** Power Apps Canvas (desktop + mobile)
- **Dados:** SharePoint Lists (`Campanhas`, `Subestacoes`, `Inventario`, `Fotos`, …)
- **Arquivos:** biblioteca `Projetos` (fotos em pasta) · `Exportacoes` (`.xlsx`)
- **Automação:** Power Automate (`flxImportarCampanha`, `flxExportarCampanha`, `flxExcluirCampanha`, `flxPastaFoto`)

## Saída (decisão 2026-09-15)

Um botão na `Tela_Exportar`: **Planilha** → `flxExportarCampanha` → `.xlsx` das SEs Finalizada.  
`TI`, `LocalInstalacao` e `ArranjoFisico` saem da linha de `Inventario`.

Foto **não** zipa. Está na biblioteca `Projetos`. `flxExportarFotos` = stand-by.

**Excluir projeto** (`btnExcluirCamp` na `Tela_Exportar`): popup → `flxExcluirCampanha` apaga Campanhas, SEs, itens, fotos, alocações, a pasta em `Projetos` e os xlsx em `Importacoes` / `Exportacoes`. Spec: `docs/automate/flxExcluirCampanha.md`.

Pasta do item = só o código (`Imobilizado` ou `CodAsset`). Pasta da SE para foto de ambiente: `Visão geral`.

Importar o projeto já cria a pasta raiz + SEs + `Visão geral`. Enviar visita grava o JPG via `flxPastaFotosVisita` (lote).

Spec: `docs/exportacao-fotos-pastas.md`  
Mockups: `docs/screens/exportar-planilha-fotos.png` · `pastas-fotos-apos-importar.png` · `pastas-fotos-apos-visita.png`

## Estrutura

```
AssetPro/
├── docs/            # contexto, specs, Power Fx, mockups
├── exports/         # solution / .msapp
├── .cursor/rules/   # nomenclatura, pastas, Power Fx PT-BR
└── README.md
```

Contexto vivo: `docs/00-contexto-projeto.md`.

Manual com as telas: `docs/entrega/manual-de-instrucoes.md`.  
Campos, listas e fluxos: `docs/entrega/Asset-Pro-manual.md`.
