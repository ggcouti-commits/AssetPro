# TI — tipo de instalação

> Fonte: áudio André 11.09.2026 + planilha `docs/mcpse/Tabela-TI-CM-LI.xlsx`.  
> Campo no app: `Subestacoes.TI` (na planilha de campanha vem repetido em cada linha).  
> Catálogo: `docs/mcpse/catalogos-aneel.md` · fórmulas: `docs/powerfx/catalogos-mcpse.txt`.

## O que é

**Tipo de instalação** = o que aquele **local** é no sistema elétrico. Código único por instalação. Todos os ativos daquele local carregam o **mesmo** TI.

Não é só subestação. Qualquer instalação elétrica tem TI: geração, SE, linha, rede, medidores, administrativo, telecom, etc.

**Não é** tensão kV, **não é** o `U`/`R` do nome (`SE U 138KV` = urbana), **não é** local MCPSE (`LocalInstalacao` 0–4), **não é** centro modular.

## Para que serve

Na revisão tarifária / valoração da base existe **banco de preço referencial por tipo de instalação**. Filtrar pela TI recorta o universo.

| Recorte | TI (tabela oficial) |
|---------|---------------------|
| Geração / usina | 10–19 (`10-HID`, térmicas, solar, eólica…) |
| SE transmissão (DIT) | 20–23 |
| SE distribuição urbana | **30–34** (`30-SDU` … `34-SDU`) |
| SE distribuição rural | **50–54** (`50-SDR` … `54-SDR`) |
| Rede aérea urbana / rural | **40** / **41** (`40-RAU`, `41-RAR`) |
| Sistema de medição urbana / rural | **93** / **96** (`93-SMU`, `96-SMR`) |
| Administrativo / telecom / outros | 70–72, 80–82, 90–92, 94–95, 97–99 |

**Áudio vs tabela:** André citou 93/96 como SE. Na planilha, 93/96 são **medição**. SE da amostra da base (`31`, `32`, `33`, `52`, `53`) bate com SDU/SDR.

## Subestação: maior tensão + urbana/rural

A SE classifica pela **maior tensão** da instalação. Entra 138 kV e sai 13 kV → faixa de **138**. Urbana vs rural escolhe SDU (30–34) ou SDR (50–54). DIT (transmissão) usa 20–23.

`ClasseTensao` na lista (`138 kV`) é o rótulo. TI é o **código** da tipologia.

## TI × centro modular × TUC

| Código | De quem é | Muda o quê |
|--------|-----------|------------|
| **TI** | o **local** | o tipo da instalação. Igual em todos os itens dali |
| **CM** (`Inventario.CM`) | o **equipamento** | a que o bem está ligado (trafo, entrada de linha, alimentador…) |
| **LI** (`Subestacoes.LocalInstalacao`) | a **SE** | RD / DIT / RBSE / RBNI (0–4) |
| **TUC + A1–A6** | o **bem** | tipo de unidade de cadastro e atributos |

Chave de critério de avaliação (André): **TI + CM + TUC + atributos**. Com ela o Tomazelli / ANEEL casa preço sem olhar descrição em texto.

Na avaliação há ainda **cesta de índices** (IPCA, IGP-M, índice de material) por essa mesma chave. Fora do escopo do app de campo.

## App / SharePoint

- Grava em **`Subestacoes.TI`**. Importação: coluna `TI` da planilha, sobe com a SE.
- Catálogo estático **`colTipoInstalacao`** no `App.OnStart`. Sem lista SharePoint.
- Exibir: `LookUp(colTipoInstalacao; Codigo = ThisItem.TI; Resumo)` → `33-SDU`.
- **Quem preenche (André, 05.10.2026):** se a base trouxer o código, a visita só mostra. Se `Subestacoes.TI` vier em branco, o **inventariante** escolhe no catálogo. Não é o escritório. Um valor por local.
- **Não** usar `Subestacoes.CM` como CM MCPSE. CM oficial: `Inventario.CM`.

## Pendências (2026-09-11)

- [x] Tabela oficial de TI / CM / LI no repo (`Tabela-TI-CM-LI.xlsx`).
- [ ] Studio: colar `colTipoInstalacao` + CM/LI atualizados no `App.OnStart` (mobile e desktop).
- [x] **Quem preenche TI (05.10, André):** vem da base quando a planilha traz. Em branco, o inventariante preenche na visita. `docs/reunioes/pauta-proxima-andre.md`.
