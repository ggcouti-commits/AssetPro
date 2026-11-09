# Mapeamento — Base Modelo Gás Canalizado (André)

> Arquivo: `OneDrive\Desktop\Power Apps\AssetPro\Base Modelo Gas Canalizado.xlsx`  
> Abas: **BASE** (itens) · **LISTA** (catálogos)  
> Ata: `docs/reunioes/2026-11-05-andre.md`  
> Amostra BASE: empreendimento **ACRINOR** (Camaçari), UC `05` ERPM, tramo DUPLO; ~24 linhas de exemplo.

## Cabeçalho BASE (linha de título)

`INDEX · NÚMERO ASSET · MUNICÍPIO · OSI · Cód C.I. · DESCRIÇÃO DO EMPREENDIMENTO · SEGMENTO · UC · DESCRIÇÃO TIPO UNIDADE DE CADASTRO · DESCRIÇÃO RESUMIDA DO BEM · DESCRIÇÃO TÉCNICA COMPLEMENTAR · DIÂMETRO · CLASSE DE PRESSÃO · TIPO DE TRAMO · QUANTIDADE · UNIDADE DE MEDIDA · ELEGÍVEL · RESERVA · FABRICANTE · MODELO · NÚMERO DE SÉRIE · ANO · TAG · NÚMERO DE PATRIMÔNIO · COORDENADA X · COORDENADA Y · OBSERVAÇÃO`

**Não existem** colunas A1–A6, TI MCPSE, CM, Bay, Arranjo, LocalInstalação ANEEL.

## Onde cada coluna entra (proposta)

| Coluna na base | Destino | Campo SP (proposta) | Notas |
|----------------|---------|---------------------|--------|
| INDEX | item | `IdItem` / ordem | Ordem em campo |
| NÚMERO ASSET | item | `CodAsset` | Ex.: `ASSET-00008-003425` |
| MUNICÍPIO | local | `Municipio` (já existe) | Catálogo aba LISTA |
| OSI | local | **`NomeSE`** (já existe) | Fenômeno 07.11.2026: OSI = nome do local |
| Cód C.I. | local | **`CodSE`** (já existe) | Fenômeno 07.11.2026: Cód C.I. = código do local |
| DESCRIÇÃO DO EMPREENDIMENTO | local | `NomeSE` | Mesmo campo do OSI / nome do local |
| SEGMENTO | local | `Segmento` (coluna nova) | Lista: AUTOMOTIVO…GERAÇÃO |
| UC | item | `CodTUC` | Código **por empresa** |
| DESCRIÇÃO TIPO UNIDADE DE CADASTRO | item | `DescricaoTUC` | Ex.: ERPM |
| DESCRIÇÃO RESUMIDA DO BEM | item | lista / `DescricaoBem` curta | Catálogo LISTA |
| DESCRIÇÃO TÉCNICA COMPLEMENTAR | item | complementar | Opcional em campo; escritório concatena |
| DIÂMETRO | item | Diâmetro | Lista pol + mm (LISTA) |
| CLASSE DE PRESSÃO | item | ClassePressao | Lista 100…1000 |
| TIPO DE TRAMO | **local** (`Subestacoes`) | `Tramo` | SIMPLES / DUPLO / TRIPLO — Fenômeno 07.11.2026: tipo de ramo da **localidade**, não do item (na planilha vem repetido por linha) |
| QUANTIDADE | item | Quantidade | |
| UNIDADE DE MEDIDA | item | Unidade | UN, CJ, M, M² |
| ELEGÍVEL / RESERVA | item | Elegivel / Reserva | SIM/NÃO |
| FABRICANTE / MODELO / SÉRIE / ANO | item | iguais elétrica | |
| TAG | item | Tag | Às vezes vem |
| NÚMERO DE PATRIMÔNIO | item | Imobilizado / patrimônio | |
| COORDENADA X / Y | **item** na amostra | CoordX / CoordY | Repetidas no local ACRINOR — confirmar se local ou item |
| OBSERVAÇÃO | item | Observacoes | |

## Aba LISTA (catálogos)

| Bloco | Conteúdo |
|-------|----------|
| TIPO / SEGMENTO | AUTOMOTIVO, RESIDENCIAL, COMERCIAL, INFRAESTRUTURA, INDUSTRIAL, GERAÇÃO |
| MUNICÍPIO | código + nome (Bahia / Bahiagás na amostra) |
| TUC | código 01–25… + descrição + Tipo Individual/Em Massa |
| DIÂMETRO | `1/2-POL` … `22-POL` e `20-MM` … `600-MM` |
| CLASSE DE PRESSÃO | 100, 150, 300, 400, 600, 1000 |
| TIPO DE TRAMO | SIMPLES, DUPLO, TRIPLO |
| DESCRIÇÃO RESUMIDA DO BEM | lista longa (válvulas, manômetros, filtros, UTR…) |
| UNIDADE DE MEDIDA | UN, CJ, M, M² |
| ELEGÍVEL / RESERVA | SIM / NÃO |

## Aberto no planejamento

1. Flag de tipo no projeto/campanha (`Elétrica` / `Gás`).
2. Local gás = mesma lista `Subestacoes` com campos extras, ou lista própria.
3. Coord no **local** vs no **item** (amostra traz no item).
4. TUC por empresa: como versionar catálogo sem quebrar elétrica.
5. Ficha: tela nova vs mesma `Tela_EditarItem` (ver chat / plano).
