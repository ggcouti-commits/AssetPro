# Lista `Subestacoes` — campos e incrementos

> SharePoint: site AssetPro · lista `Subestacoes`  
> Última atualização: 2026-09-11

## Incremento 2026-09-11 — o que é `TI` (André)

**Fonte:** áudio 11.09.2026 · `docs/reunioes/2026-09-11-andre-ti.md` · spec `docs/mcpse/ti-tipo-instalacao.md`

`Subestacoes.TI` já existe. Não é “número tarifário” genérico nem kV.

**TI = tipo de instalação** (tipologia do **local**). O que aquele lugar é: SE, rede, usina, medidores, administrativo, telecom, quadro de energia. Todos os ativos do local têm o **mesmo** código. Na SE, classifica pela **maior tensão**.

**Não confundir** com `ClasseTensao` (rótulo kV), `LocalInstalacao` (0–4 MCPSE) nem `Inventario.CM` (centro modular do equipamento).

Catálogo `colTipoInstalacao` no OnStart (planilha 11.09). **André, 05.10.2026:** se a base trouxer o código, a visita só exibe. Se vier em branco, o inventariante preenche. `docs/reunioes/pauta-proxima-andre.md`

## Incremento 2026-09-08 — Arranjo físico + Local de instalação (André)

**Fonte:** reunião 08.09.2026 · tabelas MCPSE · `docs/mcpse/catalogos-aneel.md`

Estes dois campos são da **subestação inteira**. Não vão no card do equipamento.

| Campo | Tipo SP | Valores | UI |
|-------|---------|---------|-----|
| `ArranjoFisico` | Número | 1–5 | Dropdown `colArranjoFisico` — mostra `código — sigla` (BS, BD, BDDD, BPT, DJM) |
| `LocalInstalacao` | Número | 0–4 | Dropdown `colLocalInstalacao` — mostra `código — sigla` (RD, DIT-RPC, RBSE, RBNI, DIT-RCDM) |

**Regras:**

- Arranjo = configuração de barra da SE (investimento). Igual para todos os itens da SE.
- Local = onde a SE está no sistema. **Distribuição = sempre 0 (RD).** 2/3/4 = transmissão / RBSE / RBNI (e correlatos).
- Catálogos estáticos no `App.OnStart`. SharePoint grava só o código.
- `Subestacoes.CM` **não** é o centro modular MCPSE. CM oficial é `Inventario.CM`. Não apagar `CM` da SE ainda (legado da importação / `Tela_SelecionarSE`).

### Passo a passo — SharePoint (`Subestacoes`)

1. Site **AssetPro** → lista **`Subestacoes`**
2. **+ Adicionar coluna** → **Número** → `ArranjoFisico` (min 1, max 5)
3. **+ Adicionar coluna** → **Número** → `LocalInstalacao` (min 0, max 4)
4. Studio → **Dados** → **`Subestacoes`** → **Atualizar**

### Passo a passo — Power Apps (schema)

**1.** `App` → **`OnStart`** — colar `colArranjoFisico` e `colLocalInstalacao` (ver `docs/powerfx/catalogos-mcpse.txt`). No schema de `colSubestacoes` (mobile), incluir:

```
ArranjoFisico: 0;
LocalInstalacao: 0
```

**2.** Onde monta `gblSEselecionada`, incluir:

```
ArranjoFisico: ThisItem.ArranjoFisico;
LocalInstalacao: ThisItem.LocalInstalacao
```

**3.** Importação: a base do André **não tem aba de SE**. `LocalInstalacao` e `ArranjoFisico` vêm **repetidos em cada item**. O fluxo agrupa por `CÓDIGO ODI` e sobe os dois para `Subestacoes` (valor mais frequente da ODI). Spec: `docs/bases/mapeamento-base-eletrica.md`.

UI dos dropdowns na SE (quando o card existir): `docs/powerfx/catalogos-mcpse.txt` (ItemDisplayText).

---

## Incremento 2026-09-06 — `ClasseTensao`

**Responsável:** Fenômeno (Guga)  
**Motivo:** card da `Tela_Subestacoes` (consulta desktop) exibe a tensão nominal da SE (ex.: **138 kV**). Esse dado **não existe** na modelagem atual e **não é** o campo `TI`.

| Campo | Tipo SP | Nome interno sugerido | Origem | Preenchimento |
|-------|---------|----------------------|--------|---------------|
| `ClasseTensao` | Texto (uma linha, 255) | `ClasseTensao` | Base GIS / SAP / Excel na **importação da campanha** | **Somente leitura** no app (consulta). Técnico **não** altera em campo no MVP. |

**Regra de negócio:** classe / tensão nominal **da instalação** (subestação), usada em cards, filtros e relatórios de campanha. Exemplos válidos: `138 kV`, `69 kV`, `230 kV`.

**Formato recomendado na base:** texto com unidade — `138 kV` (não só `138`). O app aceita os dois e normaliza na exibição.

**Não confundir:**

| Campo | Onde | O que é |
|-------|------|---------|
| `Subestacoes.ClasseTensao` | Lista **Subestacoes** | Tensão nominal **da SE** (este incremento) |
| `Subestacoes.TI` | Lista **Subestacoes** | **Tipo de instalação** (código do local — **não** kV). Spec: `docs/mcpse/ti-tipo-instalacao.md` |
| `Subestacoes.ArranjoFisico` | Lista **Subestacoes** | Arranjo de barra da SE (1–5: BS…DJM) — reunião 08.09 |
| `Subestacoes.LocalInstalacao` | Lista **Subestacoes** | Local MCPSE da SE (0–4: RD…DIT-RCDM) |
| `Subestacoes.CM` | Lista **Subestacoes** | **Legado** — não é o CM MCPSE. CM oficial: `Inventario.CM` |
| Atributo ANEEL “classe de tensão” | **Inventario** / TUC | Por **equipamento** (A2, faixa, etc.) — escopo do item, não da SE |

---

## Passo a passo — SharePoint

1. Site **AssetPro** → lista **`Subestacoes`**
2. **+ Adicionar coluna** → **Texto de uma linha**
3. Nome de exibição: **`ClasseTensao`**
4. Salvar
5. Preencher linhas existentes (manual ou planilha de importação) — ex.: `138 kV`, `69 kV`

---

## Passo a passo — Power Apps (após criar a coluna)

**1.** Studio → **Dados** → **`Subestacoes`** → **…** → **Atualizar** (refresh da lista)

> Reiniciar o Studio **nao** atualiza schema. Precisa **Atualizar** a tabela ou refazer a conexao (ver troubleshooting abaixo).

**2.** `App` → **`OnStart`** — no schema de `colSubestacoes` (mobile, bloco antes do `Clear`), incluir:

```
ClasseTensao: ""
```

**3.** Desktop (`AppDesktop-OnStart`): não precisa de schema fake — `ClearCollect(colSubestacoes; Subestacoes)` já traz a coluna após o refresh.

**4.** Onde monta `gblSEselecionada` (ex.: `Tela_SelecionarSE` → `OnSelect` da galeria), incluir no registro:

```
ClasseTensao: ThisItem.ClasseTensao
```

**5.** `Tela_Subestacoes` → galeria → **`lblKV`** → **`Text`**:

```
If(
    IsBlank(Coalesce(ThisItem.ClasseTensao; ""));
    "—";
    If(
        EndsWith(Lower(Trim(ThisItem.ClasseTensao)); "kv");
        ThisItem.ClasseTensao;
        ThisItem.ClasseTensao & " kV"
    )
)
```

**6.** Importação / Excel: incluir coluna **`ClasseTensao`** na planilha de subestações da campanha (junto com `CodSE`, `NomeSE`, `Municipio`, etc.).

---

- [ ] Criar colunas **`ArranjoFisico`** e **`LocalInstalacao`** no SharePoint
- [ ] Refresh da fonte **`Subestacoes`** no app
- [ ] `colArranjoFisico` + `colLocalInstalacao` no OnStart (mobile e desktop)
- [ ] Incluir os dois campos no schema `colSubestacoes` e no `Set(gblSEselecionada; …)`
- [ ] Ajustar importação Excel (`tblSEs`)
- [ ] UI dropdown na tela da SE (não na `Tela_EditarItem`)
- [ ] Criar coluna **`ClasseTensao`** no SharePoint
- [ ] Refresh da fonte **`Subestacoes`** no app
- [ ] Atualizar schema `colSubestacoes` no `OnStart` mobile
- [ ] Incluir `ClasseTensao` no `Set(gblSEselecionada; …)` onde aplicável
- [ ] Ligar **`lblKV`** na `Tela_Subestacoes`
- [ ] Ajustar fluxo de importação (Power Automate / Excel) para popular o campo

---

## Campos já existentes em `Subestacoes` (referência)

| Campo | Função |
|-------|--------|
| `CodSE` | Código da SE |
| `CodInventario` | Campanha |
| `NomeSE` | Nome |
| `Municipio`, `UF`, `Regional` | Localização |
| `SubODI` | Sub-ODI |
| `TI` | Tipo de instalação (código do local; ≠ kV, ≠ CM) |
| `CM` | Legado da SE — **não** usar como CM MCPSE |
| `ArranjoFisico` | Arranjo de barra (1–5) — reunião 08.09 |
| `LocalInstalacao` | Local MCPSE (0–4); distribuição = 0 |
| `Status` | Pendente / Em campo / Finalizada |

**Planejados (contexto):** `ResponsavelId`, `AtribuidaEm` — editor único por SE.

---

## Troubleshooting — coluna no SP mas App nao reconhece

### 1. Confirmar site e lista corretos

O app aponta para **`https://…/sites/AssetPro`** (env var `dfs_AssetProSite`). A coluna tem que estar na lista **`Subestacoes`** **desse** site — nao em outro site, copia da lista ou ambiente diferente.

### 2. Nome interno da coluna (causa mais comum)

Se no SharePoint o titulo foi **"Classe de Tensão"** (com espaco/acento), o nome no Power Apps **nao** e `ClasseTensao`.

**Como ver o nome interno:**

1. SharePoint → lista **Subestacoes** → **Configuracoes da lista** → clique na coluna
2. Na URL do browser, procure **`Field=`** — ex.: `Field=ClasseTensao` ou `Field=Classe_x0020_de_x0020_Tens_x00e3_o`

Use **esse** identificador nas formulas:

```
First(Subestacoes).'Classe de Tensão'
```

(aspas simples se tiver espaco/acento)

**Recomendacao:** recriar coluna com nome **`ClasseTensao`** sem espaco ni acento (texto uma linha).

### 3. Forcar refresh do schema (na ordem)

**A.** Painel **Dados** → **Subestacoes** → **…** → **Atualizar**

**B.** Se nao aparecer no autocomplete `First(Subestacoes).`:

- **Dados** → **Conexoes** → conexao **SharePoint** do app → **…** → **Atualizar**
- Voltar em **Subestacoes** → **Atualizar** de novo

**C.** Ainda nao:

1. Anote quais telas usam `Subestacoes` / `colSubestacoes`
2. **Dados** → **Subestacoes** → **…** → **Remover** (so a tabela, nao apagar lista SP)
3. **+ Adicionar dados** → **SharePoint** → mesmo site **AssetPro** → lista **Subestacoes**
4. Salvar app, fechar aba, reabrir pelo [make.powerapps.com](https://make.powerapps.com)

### 4. Teste rapido no Studio

**App** → **`OnStart`** — no **final**, colar temporariamente:

```
Notify(Coalesce(First(Subestacoes).ClasseTensao; "ok — vazio"); NotificationType.Information)
```

- Se a formula **nao compila** (nome vermelho) → schema sem a coluna OU nome interno errado (passo 2)
- Se compila e notify mostra **ok — vazio** → coluna reconhecida; falta valor na linha SP
- Se mostra **138 kV** → tudo certo

Opcional — ver todas as chaves do registro:

```
Notify(JSON(First(Subestacoes)); NotificationType.Information)
```

Remover o `Notify` depois do teste.

### 5. Mobile — cache `LoadData` (nao impede Studio, impede runtime)

No **celular**, `LoadData(colSubestacoes; "cache_Subestacoes")` guarda schema **antigo**. Apos refresh:

- **Baixar dados** de novo na campanha, **ou**
- limpar dados locais do app / reinstalar preview

No **desktop** (`ClearCollect(colSubestacoes; Subestacoes)`) nao usa esse cache — so o refresh da fonte basta.

### 6. Uma linha preenchida no SharePoint

Algumas colunas novas so entram no metadata DEPOIS que **pelo menos 1 item** tem valor salvo. Edite uma SE, ponha `138 kV` em **ClasseTensao**, salve, **Atualizar** de novo no app.
