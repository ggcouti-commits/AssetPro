# Catálogos MCPSE / RN 674/2015

> Fonte: `docs/mcpse/Tabela-TI-CM-LI.xlsx` (André, 11.09.2026) + tabelas 08.09 + PDF RN 674/2015.  
> No app: coleções estáticas no `App.OnStart` — **sem** lista SharePoint. O SharePoint grava só o **código**.  
> Fórmulas: `docs/powerfx/catalogos-mcpse.txt`.  
> Coluna **CAMPO RESUMO PARA APLICATIVO** = `Resumo` (ex.: `31-SDU`, `0 - MIG`, `0-RD`).

## TI — tipo de instalação (do **local**, `Subestacoes.TI`)

Código do que o local é. Igual em todos os itens dali. Na SE: **maior tensão**. Spec: `docs/mcpse/ti-tipo-instalacao.md`.

Coleção `colTipoInstalacao`. Se a base trouxer o código, a visita só exibe. Se `Subestacoes.TI` vier em branco, o inventariante escolhe aqui (André, 05.10.2026). LookUp para exibir:

`LookUp(colTipoInstalacao; Codigo = ThisItem.TI; Resumo)`

### Geração (10–19)

| Código | Sigla | Resumo | Descrição |
|--------|-------|--------|-----------|
| 10 | HID | 10-HID | Hidroelétrica |
| 11 | TER | 11-TER | Térmica a combustão — óleo/gás/diesel |
| 12 | TER | 12-TER | Térmica a vapor — carvão |
| 13 | TER | 13-TER | Térmica a vapor — gás |
| 14 | TER | 14-TER | Térmica a vapor — diesel/querosene/óleo |
| 15 | TER | 15-TER | Térmica a vapor — biomassa |
| 16 | TER | 16-TER | Térmica a vapor — nuclear |
| 17 | SOL | 17-SOL | Solar |
| 18 | EOL | 18-EOL | Eólica |
| 19 | OUT | 19-OUT | Outras |

### Transmissão DIT (20–29)

| Código | Sigla | Resumo | Descrição |
|--------|-------|--------|-----------|
| 20 | DIT | 20-DIT | SE < 230 kV (DIT) |
| 21 | DIT | 21-DIT | SE ≥ 230 kV e < 345 kV |
| 22 | DIT | 22-DIT | SE ≥ 345 kV e < 500 kV |
| 23 | DIT | 23-DIT | SE ≥ 500 kV |
| 24 | DIT | 24-DIT | LT < 138 kV (DIT) |
| 25 | DIT | 25-DIT | LT ≥ 138 kV e < 230 kV (DIT) |
| 26 | DIT | 26-DIT | LT ≥ 230 kV e < 345 kV |
| 27 | DIT | 27-DIT | LT ≥ 345 kV e < 500 kV |
| 28 | DIT | 28-DIT | LT ≥ 500 kV |
| 29 | DIT | 29-DIT | Transmissão de interesse restrito (SE ou linha) |

### Distribuição urbana — SE e linha (30–39)

| Código | Sigla | Resumo | Descrição |
|--------|-------|--------|-----------|
| 30 | SDU | 30-SDU | SE urbana ≤ 13,8 kV |
| 31 | SDU | 31-SDU | SE urbana > 13,8 kV e ≤ 34,5 kV |
| 32 | SDU | 32-SDU | SE urbana > 34,5 kV e ≤ 69 kV |
| 33 | SDU | 33-SDU | SE urbana > 69 kV e ≤ 138 kV |
| 34 | SDU | 34-SDU | SE urbana > 138 kV e ≤ 230 kV |
| 35 | LAU | 35-LAU | Linha de distribuição urbana ≤ 13,8 kV |
| 36 | LAU | 36-LAU | Linha de distribuição urbana > 13,8 kV e ≤ 34,5 kV |
| 37 | LAU | 37-LAU | Linha de distribuição urbana > 34,5 kV e ≤ 69 kV |
| 38 | LAU | 38-LAU | Linha de distribuição urbana > 69 kV e ≤ 138 kV |
| 39 | LAU | 39-LAU | Linha de distribuição urbana > 138 kV e ≤ 230 kV |

### Redes de distribuição (40–44)

| Código | Sigla | Resumo | Descrição |
|--------|-------|--------|-----------|
| 40 | RAU | 40-RAU | Rede aérea urbana |
| 41 | RAR | 41-RAR | Rede aérea rural |
| 42 | RSU | 42-RSU | Rede subterrânea urbana |
| 43 | RSR | 43-RSR | Rede subterrânea rural |
| 44 | RSA | 44-RSA | Rede submersa |

### Distribuição rural — SE e linha (50–59)

| Código | Sigla | Resumo | Descrição |
|--------|-------|--------|-----------|
| 50 | SDR | 50-SDR | SE rural ≤ 13,8 kV |
| 51 | SDR | 51-SDR | SE rural > 13,8 kV e ≤ 34,5 kV |
| 52 | SDR | 52-SDR | SE rural > 34,5 kV e ≤ 69 kV |
| 53 | SDR | 53-SDR | SE rural > 69 kV e ≤ 138 kV |
| 54 | SDR | 54-SDR | SE rural > 138 kV e ≤ 230 kV |
| 55 | LDR | 55-LDR | Linha de distribuição rural ≤ 13,8 kV |
| 56 | LDR | 56-LDR | Linha de distribuição rural > 13,8 kV e ≤ 34,5 kV |
| 57 | LDR | 57-LDR | Linha de distribuição rural > 34,5 kV e ≤ 69 kV |
| 58 | LDR | 58-LDR | Linha de distribuição rural > 69 kV e ≤ 138 kV |
| 59 | LDR | 59-LDR | Linha de distribuição rural > 138 kV e ≤ 230 kV |

### Linhas LSS (60–69)

Mesmas faixas de tensão que DIT / distribuição; sigla da tabela = **LSS**.

| Código | Sigla | Resumo | Descrição |
|--------|-------|--------|-----------|
| 60 | LSS | 60-LSS | LT < 138 kV (DIT) |
| 61 | LSS | 61-LSS | LT ≥ 138 kV e < 230 kV (DIT) |
| 62 | LSS | 62-LSS | LT ≥ 230 kV e < 345 kV |
| 63 | LSS | 63-LSS | LT ≥ 345 kV e < 500 kV |
| 64 | LSS | 64-LSS | LT ≥ 500 kV |
| 65 | LSS | 65-LSS | Linha de distribuição ≤ 13,8 kV |
| 66 | LSS | 66-LSS | Linha de distribuição > 13,8 kV e ≤ 34,5 kV |
| 67 | LSS | 67-LSS | Linha de distribuição > 34,5 kV e ≤ 69 kV |
| 68 | LSS | 68-LSS | Linha de distribuição > 69 kV e ≤ 138 kV |
| 69 | LSS | 69-LSS | Linha de distribuição > 138 kV e ≤ 230 kV |

### Administração central (70–72)

| Código | Sigla | Resumo | Descrição |
|--------|-------|--------|-----------|
| 70 | TER | 70-TER | Terrenos, edificações, obras civis e benfeitorias |
| 71 | EQP | 71-EQP | Equipamento geral, informática e veículos |
| 72 | EQP | 72-EQP | Sistema de comunicação |

### Administração específica (80–82)

| Código | Sigla | Resumo | Descrição |
|--------|-------|--------|-----------|
| 80 | TER | 80-TER | Terrenos, edificações, obras civis e benfeitorias |
| 81 | EQP | 81-EQP | Equipamento geral, informática e veículos |
| 82 | EQP | 82-EQP | Sistema de comunicação |

### Outras ODI / telecom / medição (90–99)

| Código | Sigla | Resumo | Descrição |
|--------|-------|--------|-----------|
| 90 | TER | 90-TER | Terrenos, edificações e benfeitorias que não integram outras ODI |
| 91 | TEL | 91-TEL | Equipamento geral / informática / veículos que não integram ODI específicas |
| 92 | TEL | 92-TEL | Telecom, telecontrole, teleprocessamento, proteção, controle e supervisão |
| 93 | SMU | 93-SMU | Sistema de medição (fora de usina/SE) — área urbana |
| 94 | AUX | 94-AUX | Serviços auxiliares gerais (oficinas, laboratórios) |
| 95 | OUT | 95-OUT | Apoio operacional (ODI de usina e SE) |
| 96 | SMR | 96-SMR | Sistema de medição (fora de usina/SE) — área rural |
| 97 | OUT | 97-OUT | Sistema de despacho de carga |
| 98 | RES | 98-RES | Reserva imobilizada (exceto reservas exclusivas de usina/SE) |
| 99 | INT | 99-INT | Intangível (exceto servidões da ODI específica) |

**Áudio 11.09 vs tabela:** André citou 93/96 como SE. Na tabela, **93/96 = medição**. SE urbana = **30–34 (SDU)**; SE rural = **50–54 (SDR)**; SE DIT = **20–23**. Rede aérea **40/41** e usina **10** batem com o áudio. Amostra da base (`31`, `32`, `33`, `52`, `53`) = SE distribuição.

## Centro modular — por **equipamento** (`Inventario.CM`, 0–9)

Dropdown: `código — nome curto`. Sem o parágrafo de composição. `Resumo` = coluna da planilha (chip compacto).

| Código | Sigla | Resumo | Nome na tela |
|--------|-------|--------|----------------|
| 0 | MIG | 0 - MIG | Infraestrutura geral |
| 1 | EQP | 1 EQP | Equipamentos |
| 2 | EL | 2 - EL | Entrada de linha |
| 3 | IB | 3 - IB | Interligação de barra |
| 4 | CT | 4 - CT | Conexão de trafo |
| 5 | CCP | 5 - CCP | Conexão de banco |
| 6 | CRL | 6 - CRL | Conexão de reator de linha |
| 7 | CRB | 7 - CRB | Conexão de reator de barra |
| 8 | CC | 8 - CC | Conexão de compensador |
| 9 | CCA | 9 - CCA | Conexão de circuito/alimentador |

Código 1: planilha **EQP** (antes sem sigla). Código 4/5: resumo **CT** / **CCP** (CTA e CCS ficam só na descrição longa). Código 7: planilha do app **CRB** (o PDF 08.09 trazia CRH). Vale esta planilha.

## Arranjo físico — por **subestação** (`Subestacoes.ArranjoFisico`, 1–5)

Não veio nesta xlsx (só TI / CM / LI). Catálogo 08.09 permanece.

| Código | Sigla | Descrição (não mostrar no dropdown) |
|--------|-------|--------------------------------------|
| 1 | BS | Barra simples |
| 2 | BD | Barra dupla |
| 3 | BDDD | Barra dupla e disjuntor duplo |
| 4 | BPT | Barra principal e de transferência |
| 5 | DJM | Disjuntor e meio |

## Local de instalação — por **subestação** (`Subestacoes.LocalInstalacao`, 0–4)

Onde a SE está no sistema. **Distribuição = sempre 0.** Dropdown: `código — sigla`.

| Código | Sigla | Resumo | Nome na tela |
|--------|-------|--------|----------------|
| 0 | RD | 0-RD | Distribuição |
| 1 | DIT-RPC | 1-DIT-RPC | DIT — RBSE / interesse restrito |
| 2 | RBSE | 2-RBSE | Rede Básica — sistema existente |
| 3 | RBNI | 3-RBNI | Rede Básica — novas instalações |
| 4 | DIT - RCDM | 4-DIT - RCDM | DIT — RBNI |
