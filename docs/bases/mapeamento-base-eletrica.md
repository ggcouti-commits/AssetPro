# Mapeamento — Base Física Padrão Elétrica (André)

> Arquivo: `Base Fisica Padrao Eletrica-xls.csv` (mesmo conteúdo do `.xlsx` / `.xlsb`).  
> Amostra: **3.349 itens**, várias SEs (ex.: `7SEGU001` Guará II 138 kV, `7SEVA001` Vale do Amanhecer 69 kV, `7SE02000` / `7SE05000` 34,5 kV).  
> Planilha **única e achatada** (item = linha). Não tem aba de SE.

Cabeçalho real (linha 2; coluna `..` vazia, ignorar):

`Nº ASSET EXPERTS; NÚMERO IMOBILIZADO; CÓDIGO ODI; DESCRIÇÃO DE ODI; TI; LOCAL INSTALAÇÃO; CENTRO MODULAR; ARRANJO FÍSICO; TUC; TIPO DE UNIDADE DE CADASTRO; A1; A2; A3; A4; A5; A6; DESCRIÇÃO TÉCNICA DO ATIVO; QUANT; UNIDADE; ELEGÍVEL; RESERVA; FABRICANTE; MODELO; NÚMERO SÉRIE; ANO; BAY; CÓDIGO OPERAÇÃO; PROJETO; OBSERVAÇÃO`

**Não existe coluna BI** nesta base. O “BI” da reunião 08.09 não aparece no arquivo — o identificador extra é `NÚMERO IMOBILIZADO`. Bem de projeto = coluna **`PROJETO`** (no arquivo de exemplo está `XOXOXOXOXO`).

## Onde cada coluna entra

| Coluna na base | Destino | Campo SP | Já tem? |
|----------------|---------|----------|---------|
| Nº ASSET EXPERTS | item | `Inventario.CodAsset` | Sim |
| NÚMERO IMOBILIZADO | item | `Inventario.Imobilizado` | **Não** |
| **IdItem** (André preenche na base) | item | `Inventario.IdItem` | Coluna **já no SP** (21.09). Cabeçalho do Excel = **`IdItem`**. Ordem da visita. **Não** é `IdUC`. |
| CÓDIGO ODI | SE + item | `Subestacoes.CodSE` / `Inventario.CodSE` | Sim |
| DESCRIÇÃO DE ODI | SE | `Subestacoes.NomeSE` | Sim |
| TI | SE (repetido na linha) | `Subestacoes.TI` | Sim — **tipo de instalação** (código do **local**). Amostra `31`/`32`/`33` = SDU urbana; `52`/`53` = SDR rural. Rede **40/41**. Usina **10–19**. **93/96 = medição**, não SE. **Não** é o `U`/`R` do nome. **Não** é kV. Spec: `docs/mcpse/ti-tipo-instalacao.md`. |
| LOCAL INSTALAÇÃO | SE (código 0–4) | `Subestacoes.LocalInstalacao` | **Não** |
| CENTRO MODULAR | **item** (0–9, muda na linha) | `Inventario.CM` | Sim |
| ARRANJO FÍSICO | SE (código 1–5) | `Subestacoes.ArranjoFisico` | **Não** |
| TUC | item | `Inventario.CodTUC` | Sim |
| TIPO DE UNIDADE DE CADASTRO | item | `Inventario.DescricaoTUC` | Sim — nome da TUC. Também sai do catálogo no Salvar da visita. |
| **IdUC** ou **IDUC** (patrimônio da placa) | item | `Inventario.IdUC` | Coluna **já no SP** (20.09). Cabeçalho fechado 13.10: `IdUC`. O script grava em `tblImportItens.IdUC`. Sem a coluna, o item sobe em branco e o inventariante preenche na visita. **Não** é `NÚMERO SÉRIE` nem `NÚMERO IMOBILIZADO`. |
| A1…A6 | item | `AtributoA1`…`A6` (trim; `00` grava **0**, a tela mostra `00`) | Sim |
| DESCRIÇÃO TÉCNICA DO ATIVO | item | `Inventario.DescricaoBem` | Sim |
| QUANT | item | `Inventario.Quantidade` (`1,00` → 1) | Sim |
| UNIDADE | item | `Inventario.Unidade` | Sim |
| ELEGÍVEL | item | `Inventario.Elegivel` (`SIM`/`NÃO`) | **Não** — **não** misturar com `Status` |
| RESERVA | item | `Inventario.Reserva` (`SIM`/`NÃO`) | **Não** |
| FABRICANTE | item | `Inventario.Fabricante` | Sim |
| MODELO | item | `Inventario.Modelo` | Sim |
| NÚMERO SÉRIE | item | `Inventario.NumSerie` | Sim |
| ANO | item | `Inventario.Ano` | Sim |
| BAY | item | `Inventario.Bay` | **Não** |
| CÓDIGO OPERAÇÃO | item | `Inventario.CodOperacao` | Sim — **já vem preenchido** (T2, 6025…). Técnico confirma, não nasce vazio |
| PROJETO | item (último) | `Inventario.Projeto` | **Não** |
| OBSERVAÇÃO | item | `Inventario.Observacoes` | Sim |

`CodAsset` nesta base às vezes é `ASSET-7SEGU001-200219`, às vezes código curto (`BF50018784`, `BE50000526`). Continua chave do item.

## Importação (uma planilha → duas listas)

## Exportação — `TI`, `LocalInstalacao`, `ArranjoFisico` por linha (decisão 2026-09-13)

A base traz os três repetidos em **toda linha de item**, e a planilha exportada também precisa
deles em cada linha. Mesmo assim eles **não** são gravados em `Inventario`: ficam só em
`Subestacoes` (é o que o script faz — agrega por ODI em `tblImportSEs`).

Na exportação, `flxExportarCampanha` lê **TI**, **LocalInstalacao** e **ArranjoFisico**
da própria linha de `Inventario` (já estão na lista). Sem lookup na SE.
`Obter_SEs` só define quais `CodSE` estão Finalizada. Sem CSV.
ZIP de fotos = stand-by (2026-09-15).

**Por que não copiar para o item na importação:** `TI` ainda não tem dono definido (base do
cliente / escritório / campo — `docs/reunioes/pauta-proxima-andre.md`), logo vai ser **editado
depois** da importação. Valor copiado em 3.000 itens não se corrige num lugar só: a SE muda e a
planilha exportada continua saindo com o dado velho, sem erro nenhum aparecendo. `CM` é o caso
oposto e por isso vive no item: é do equipamento e muda de linha para linha.

1. **Identificar todas as SEs:** cada `CÓDIGO ODI` distinto (trim + maiúsculo) = **uma** linha em `Subestacoes`. Não pular ODI, não pegar só a primeira. Campos: `CodSE`, `NomeSE`, `TI`, `LocalInstalacao`, `ArranjoFisico`. `ClasseTensao` sai da descrição (ex.: `138KV`, `69 KV`, `34.5KV`). `QtdItens` = quantas linhas da base caíram nessa ODI.
2. Cada linha → `Inventario` com os campos de item.
3. **CM** fica no item. **TI**, **local** e **arranjo** sobem para a SE (André: TI e local/arranjo não mudam por equipamento — TI é do local; CM é do equipamento).

Neste arquivo de exemplo o arranjo **às vezes varia na mesma ODI** (lixo de planilha). Na importação: usa o valor **mais frequente** da ODI; se empatar, o primeiro. Não gravar arranjo no item.

Local nesta amostra é **sempre 0** (RD / distribuição), como o André falou.

## SharePoint ainda faltando

**Inventario:** `Imobilizado`, `Elegivel`, `Reserva`, `Bay`, `Projeto` (texto); **`DescricaoTUC`**, **`IdUC`**, **`IdItem`** já no SP.  
**Subestacoes:** `ArranjoFisico`, `LocalInstalacao` (número).

Não criar coluna `BI`.
