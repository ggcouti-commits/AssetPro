# Lista `Inventario` — campos e incrementos

> SharePoint: site AssetPro · lista `Inventario`  
> Última atualização: 2026-09-20

## Incremento 2026-09-08 — base elétrica (André)

**Fonte:** `docs/bases/mapeamento-base-eletrica.md` · reunião 08.09.2026

Planilha única do André. **Não tem coluna BI.** Imobilizado = `NÚMERO IMOBILIZADO`. Bem de projeto = coluna **`PROJETO`**.

| Campo SP | Tipo | Coluna na base | Preenchimento |
|----------|------|----------------|---------------|
| `CodAsset` | já na lista | Nº ASSET EXPERTS | Importação |
| `Imobilizado` | Texto | NÚMERO IMOBILIZADO | Importação |
| `Elegivel` | Texto (`SIM`/`NÃO`) | ELEGÍVEL | Importação — **≠** `Status` |
| `Reserva` | Texto (`SIM`/`NÃO`) | RESERVA | Importação |
| `Bay` | Texto | BAY | Importação (138KV, PAINEL, CFTV…) |
| `Projeto` | Texto | PROJETO | Importação; **último** da ficha |

`CodOperacao` **pode vir preenchido** na base (ex.: T2, 6025). A regra antiga “vem vazio na carga” **não vale** para esta base.

**Pasta de foto do item** (biblioteca `Projetos`, não a lista): só o código — `Coalesce(Imobilizado; CodAsset; "SEM-IMOB")`. **Sem** descrição no path. Pasta da SE para foto de ambiente: `Visão geral` (`TipoFoto` continua `AMBIENTE`). Spec: `docs/exportacao-fotos-pastas.md` · ata 18.09.

### Passo a passo — SharePoint (`Inventario`)

1. Site **AssetPro** → lista **`Inventario`**
2. **+ Adicionar coluna** → **Texto de uma linha** → `Imobilizado`
3. Idem → `Elegivel`
4. Idem → `Reserva`
5. Idem → `Bay`
6. Idem → `Projeto`
7. Studio → **Dados** → **`Inventario`** → **Atualizar**

Não criar `BI`.

---

## Incremento 2026-09-01 — `CM` (centro modular)

**Responsável:** Fenômeno (Guga)  
**Ação:** coluna **`CM` já existe** na lista `Inventario`. Falta UI + persistência no app.

| Campo | Tipo SP | Origem SAP/Excel/GIS | Preenchimento |
|-------|---------|----------------------|---------------|
| `CM` | já na lista | Coluna na base (quando houver) | Coleta/atualização **em campo** |

**Regra de negócio:** identifica o centro modular (vão/bay GIS) onde o equipamento está instalado na SE. Vem da base quando existir; o técnico confirma ou preenche na visita.

**Não usar** `Subestacoes.CM` / `gblSEselecionada.CM` no card do item — CM MCPSE é **do equipamento** (`Inventario.CM`). Arranjo físico e local de instalação são da **SE** (reunião 08.09). **TI** é do **local** (`Subestacoes.TI`) — tipologia da instalação, igual para todos os itens dali; não vai no card do equipamento (áudio 11.09, `docs/mcpse/ti-tipo-instalacao.md`).

**UI:** card `cCardCM` — **primeiro da seção** Dados técnicos. Dropdown `drpCM` com `colCentroModular` (catálogo estático no `App.OnStart`, sem lista SharePoint). `Inventario.CM` grava o **código 0–9**. Rótulo: `código — nome curto` (sem texto de composição). `lblCMDesc` **oculto**.

**Catálogo `colCentroModular` (estático):** 0 MIG Infraestrutura geral · 1 EQP Equipamentos · 2 EL Entrada de linha · 3 IB Interligação de barra · 4 CT Conexão de trafo · 5 CCP Conexão de banco · 6 CRL · 7 **CRB** · 8 CC · 9 CCA. Planilha 11.09. Fórmulas: `docs/powerfx/catalogos-mcpse.txt`.

**Conferido no YAML do Studio (2026-09-03):** `colCentroModular` no OnStart · `colCampoOffline.CM` · `cCardCM`/`drpCM` · `OnVisible` (`varCM`) · `btnConfirmarBase` / `btnNaoEncontradoBase` já passam `ThisItem.CM`.

**Pendente no app:**

1. ~~Criar coluna no SharePoint~~ → já existe: `Inventario.CM`
2. ~~Lista SharePoint de catálogo~~ → `colCentroModular` no OnStart
3. ~~Card na `Tela_EditarItem`~~ → `cCardCM` + `drpCM` no YAML
4. ~~`OnVisible` (`varCM`)~~ → no YAML
5. [ ] `colInventarioBase` schema + forçar `CM` depois do `LoadData`
6. [ ] `btnSalvarItem` — `CM: varCM` no `Collect`
7. [ ] `btnEnviarVisitaExec` — `CM: linhaAtual.CM` no Patch CONFIRMACAO e SOBRA

---

## Incremento 2026-08-22 — `Ano`

**Responsável:** Fenômeno (Guga)  
**Ação:** coluna criada manualmente na lista `Inventario` no SharePoint.

| Campo | Tipo SP sugerido | Origem SAP/Excel | Preenchimento |
|-------|------------------|------------------|---------------|
| `Ano` | Número | Coluna na base (quando houver) | Coleta/atualização **em campo** (ano fabricação, instalação, etc.) |

**UI:** card `cCardAno` na seção **Dados técnicos** — duplicar `cCardQuantidade`, input numérico (`inpAno`).

---

## Incremento 2026-08-19 — `CodOperacao`

**Responsável:** Fenômeno (Guga)  
**Ação:** coluna criada manualmente na lista `Inventario` no SharePoint.

| Campo | Tipo | Origem SAP/Excel | Preenchimento |
|-------|------|------------------|---------------|
| `CodOperacao` | Texto | Coluna existe na base SAP/Excel | **Vem vazio na importação** — deve ser preenchido **em campo** pelo app |

**Regra de negócio:** o código de operação **pode vir na base** (planilha do André já traz T2, 6025, etc.). Técnico confirma ou corrige em campo. Se vier vazio, preenche na visita.

**Pendente no app (quando retomar):**

1. ~~Atualizar conector SharePoint no Power Apps (refresh da lista `Inventario`)~~ → **Studio: Passo 0**
2. ~~Incluir `CodOperacao` em `colInventarioBase` (schema + `LoadData`)~~ → **no repo `App.pa.yaml`**
3. ~~Incluir campos técnicos + `AtributoA*` em `colCampoOffline`~~ → **no repo `App.pa.yaml`**
4. ~~`Salvar` → gravar offline~~ → **no repo + `pacote-1-studio.md`**
5. ~~`Tela_Home` → `Patch` no envio de visitas~~ → **no repo `Tela_Home.pa.yaml`**
6. [ ] UI em `Tela_EditarItem` — seção **Dados técnicos do equipamento**
7. [ ] `OnVisible` — vars `varFabricante`…`varObservacoes`
8. [ ] `Tela_ItensVisita` — trocar `A1` por `AtributoA1` nos Collect rápidos

---

## Campos técnicos do equipamento (identificação em campo)

Estes campos já existiam na lista (export antigo) ou foram discutidos para a tela de edição. **Ainda sem UI completa no app.**

| Campo SP | Descrição | Origem base | Coleta em campo |
|----------|-----------|-------------|-----------------|
| `Fabricante` | Fabricante | SAP/Excel (quando houver) | Sim — input livre |
| `Modelo` | Modelo | SAP/Excel (quando houver) | Sim |
| `NumSerie` | Número de série | SAP/Excel (quando houver) | Sim |
| `CodOperacao` | Código de operação | Coluna na base **pode vir preenchida** | Sim — confirmar/alterar em campo |
| `CM` | Centro modular (código 0–9) | CENTRO MODULAR | Sim — **dropdown** `colCentroModular` (nome curto) |
| `Imobilizado` | Número de imobilizado | NÚMERO IMOBILIZADO | Importação |
| `Elegivel` | Elegível tarifário | ELEGÍVEL | Importação (`SIM`/`NÃO`) |
| `Reserva` | Item reserva | RESERVA | Importação (`SIM`/`NÃO`) |
| `Bay` | Bay / área no pátio | BAY | Importação |
| `Projeto` | Bem de projeto | PROJETO | Importação — **último** da ficha |
| `Ano` | Ano (fabricação/instalação) | SAP/Excel (quando houver) | Sim — input numérico |
| `Unidade` | Unidade de medida do item (UN, PC, M, M², KG…) | SAP/Excel | Sim — **combo no card Quantidade** (não card separado) |
| `Observacoes` | Observações de campo | — | Sim — text area |

**Não confundir** com `Unidade` / `UnidadeAlt` em `TabelasCatalogo` — essas são grandezas dos **atributos ANEEL** (kV, kVA, V), não unidade de quantidade do item.

---

## Campos tarifários / inventário (já em desenvolvimento)

| Campo SP | Descrição |
|----------|-----------|
| `CodTUC` | Classificação TUC |
| `AtributoA1` … `AtributoA6` | Atributos ANEEL (renomeados de A1–A6) |
| `DescricaoBem` | Descrição do bem |
| `Quantidade` | Quantidade |
| `CodAsset` | Identificador do item na base |
| `Status` | PENDENTE / ADERENTE / NÃO_ELEGIVEL |
| `Sobra` | Tipo de sobra |

---

## Seção proposta na `Tela_EditarItem`

```
DADOS TÉCNICOS DO EQUIPAMENTO
├── Centro modular      (base: …)  ← primeiro da seção · dropdown curto
├── Fabricante          (base: …)
├── Modelo              (base: …)
├── Nº de série         (base: …)
├── Cód. operação       (base: vazio — preencher em campo)
├── Ano                 (base: …)
├── Bay                 (base: …)
├── Imobilizado         (base: …)  ← importação
├── Unidade de medida   → no card **Quantidade** (combo ao lado do input)
├── Observações         (text area)
└── Projeto             ← último da ficha (coluna PROJETO)
```

Posição sugerida: após **Quantidade/TUC**, antes dos cards **A1–A6**.

---

## Incremento 2026-09-17 — visita (reunião)

**Fonte:** `docs/reunioes/2026-09-17.md` · Studio: `docs/powerfx/pauta-2026-09-17-studio.md`

| Campo SP | Tipo | Regra |
|----------|------|--------|
| `Quantidade` | já na lista | Base. **Não** zerar no Não encontrado. **Não** sobrescrever no envio. |
| `QuantidadeCampo` | Número | O que o técnico achou. Não encontrado = **0** sempre. |
| `Reserva` | já na lista (`SIM`/`NÃO`) | Importação **e** toggle na `Tela_EditarItem`. ≠ TI 98-RES. |

### Passo a passo — SharePoint (`QuantidadeCampo`)

1. Site **AssetPro** → lista **`Inventario`**
2. **+ Adicionar coluna** → **Número** → `QuantidadeCampo`
3. Studio → **Dados** → **`Inventario`** → **Atualizar**

Schema das coleções (dummy completo): `docs/powerfx/schema-inventario.txt`. `colCampoOffline` = lista + fila. `colInventarioBase` / `colItensSEConsulta` = lista. Forçar o dummy **depois** do `LoadData`.

---

## Incremento 2026-09-18 — apresentação (André × João × Bruno)

**Fonte:** `docs/reunioes/2026-09-18.md`. **Falta fazer** — ver lista em `docs/00-contexto-projeto.md`.

| Campo SP | Tipo | Regra |
|----------|------|--------|
| `IdUC` | Texto | MCPSE — Individualizador da UC (patrimônio da placa). **Não** é `Imobilizado` nem `CodAsset`. Coluna **já criada** (Fenômeno, 20.09). Card da galeria. Vem do AIS / Excel quando a planilha trouxer; senão o técnico preenche. |
| `DescricaoTUC` | Texto | Nome da TUC no catálogo (`colTUC.DescricaoTUC`). Coluna **já criada** (Fenômeno, 20.09). O Salvar da visita grava ao escolher o TUC. Importação: `DescricaoTUC` ou `TIPO DE UNIDADE DE CADASTRO`. |
| `IdItem` | Número | Ordem da visita = ordem da planilha (entrada de linha → 138 / 69 / 13 → civil → painel). **Não** é `IdUC` nem `IdInventario`. André preenche na base. Coluna **já criada** (Fenômeno, 21.09). `Sort` na galeria. |

### Passo a passo — SharePoint

1. Site **AssetPro** → lista **`Inventario`**
2. ~~**+ Adicionar coluna** → **Texto de uma linha** → `IdUC`~~ → **já criada** (20.09)
3. ~~**+ Adicionar coluna** → **Texto de uma linha** → `DescricaoTUC`~~ → **já criada** (20.09)
4. ~~**+ Adicionar coluna** → **Número** → `IdItem`~~ → **já criada** (21.09). Não criar `Sequencial` / `Ordem`.
5. Studio → **Dados** → **`Inventario`** → **Atualizar**

Card mobile: `{Imobilizado} · {TUC.A1} · {Descricao} · {IdUC}`. **Sem** `{NomeSE}`.

Pasta de foto **não** usa `IdUC` — usa o código exclusivo da base (`Imobilizado` / `CodAsset`). Spec: `docs/exportacao-fotos-pastas.md`.

## Incremento 2026-10-09 — coordenada do item (rede)

**Fonte:** Fenômeno, 09.10. Ok para criar na lista. Site AssetPro (`AssetPro493`), lista `Inventario`.

| Campo SP | Tipo | Regra |
|----------|------|--------|
| `CoordX` | Texto | Longitude do **item** de rede. Seis casas, ponto. **Já criada** (09.10). |
| `CoordY` | Texto | Latitude do **item** de rede. Seis casas, ponto. **Já criada** (09.10). |

Na subestação as duas ficam vazias. A coordenada do local continua em `Subestacoes.CoordX` / `CoordY`. A lista `Fotos` não recebe coordenada.

