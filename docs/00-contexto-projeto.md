# AssetPro / Infralytics — Contexto do projeto

> Extraído do export Claude (Opção A — filtrado). Última atualização: 2026-10-13.

## 1. Visão geral

- **Nome atual:** Infralytics (antes: **Asset Pro**)
- **Descrição no Claude:** App de inventário
- **Problema que resolve:** Coleta de inventário em campo em **subestações elétricas**, comparando achados físicos com base importada (SAP/GIS) e gerando relatórios regulatórios (ANEEL MCPSE — RN 674/2015)
- **Público-alvo:** Empresas de gestão de ativos que fazem **Revisão Tarifária Elétrica** (comercial SaaS — não ferramenta interna)
- **Responsável:** Guga (decisor principal)
- **Status:** MVP em Power Apps **ativo** + migração planejada para **Expo + TypeScript + Supabase**

## 2. Stack

| Camada | Atual (MVP) | Planejado |
|--------|-------------|-----------|
| App | Power Apps (Canvas) | Expo + React Native + TypeScript |
| Dados | SharePoint Lists + Excel | Supabase (Postgres) |
| Offline | `colCacheOffline` / `SaveData` | SQLite local + fila outbox |
| Automação | Power Automate | — |
| Fotos | Lista `Fotos` (app) + biblioteca `Projetos` (pastas) | Fila separada de upload |

## 3. Decisões arquiteturais (já definidas)

- **Um editor por SE:** só uma pessoa edita cada subestação por vez → sem sync concorrente; outbox pattern basta
- **Fotos em fila separada** dos dados (evita bloqueio por arquivos grandes)
- **Sync manual em 3 ações:** Baixar dados → Finalizar SE → Enviar Visitas
- **A1 = código decimal do subtipo** (ex.: 160.01 = Seccionadora); atributos técnicos começam em **A2**
- **`LIVRE`:** atributo grava `0`; texto livre vai em `DescricaoBem`
- **Faixas:** `LimiteSuperior` com `0` em vez de vazio; potência em kVA, tensão em kV
- **Subestações:** colunas `ResponsavelId` e `AtribuidaEm` para reforçar regra de editor único
- **Desktop — perfis (2026-09-07):** `varPerfil` = `ESCRITORIO` | `INVENTARIANTE`. Inventariante: menu só **Inventários**, abre em `Tela_Inventarios`. Escritório: menu completo, `Tela_Campanhas`. Spec: `docs/powerfx/desktop-menu.txt`
- **Login de campo (2026-09-14):** uma conta M365 no tablet. Slot (`Inventariante01` + senha + `UsadoPor`) na lista **`Inventariantes`**. Mobile: `Tela_Login` com `LookUp` (sem fluxo). Desktop: `Tela_Usuarios` (CRUD). `varPerfil` no Desktop fica `ESCRITORIO`. Spec: `docs/powerfx/Tela_Login-formulas.txt` · `Tela_Usuarios-formulas.txt`
- **Sessão fica no tablet (2026-10-19):** `StartScreen` = `Tela_Login`. Timer `tmrSessaoLogin` faz `LoadData(cache_Sessao)` e navega (não depende só do OnStart). OnStart offline usa cache das tabelas mestras (não chama SP). Login avisa com `Notify` se `SaveData` falhar.
- **Mobile — recorte por perfil (2026-09-18):** inventariante só lista/baixa projeto + SE em `Alocacoes`. Escritório (`varPerfil = "ESCRITORIO"`) vê tudo. Spec: `docs/powerfx/mobile-filtro-alocacao.txt`
- **Desktop — duas trilhas (2026-09-06):** **Projetos/Subestações** = consulta e visualização (o que foi feito, fotos). **Inventários** = coleta de dados no escritório (clone do mobile), para quem não usa celular em campo. Lista SharePoint continua **`Campanhas`**; no front o rótulo é **Projeto**. Spec: `.cursor/rules/projetos-nomenclatura.mdc`
- **Desktop — importar projeto (2026-09-10):** botão na `Tela_Exportar` abre container: nome, período, setor, concessionária existente **ou** cadastro novo + planilha. Mockup: `docs/screens/mockup-importar-projeto.html`
- **Pastas de foto + planilha (2026-09-10 / 15 / 18):** importar cria pasta na biblioteca `Projetos`. Enviar visita grava JPG via `flxPastaFotosVisita`. Pasta do item = **só o código**. Pasta de ambiente = **`Visão geral`**. **Planilha** → `flxExportarCampanha`. ZIP = stand-by. Spec: `docs/exportacao-fotos-pastas.md` · `docs/automate/flxExportarCampanha.md`.

## 4. Modelo de dados (principal)

| Entidade | Função |
|----------|--------|
| `TabelasUnificadas` | Lookup unificado (substitui várias tabelas) |
| `TabelaAtributos` | 1 linha por atributo por TUC; `TipoEntrada`: LISTA / FAIXA / LIVRE |
| `Inventario` | Itens de campo; … `CodOperacao`, **`CM`**, **`Ano`**, **`Imobilizado`**, **`Bay`**, **`Elegivel`**, **`Reserva`**, **`Projeto`**, **`DescricaoTUC`**, **`IdUC`** (SP 20.09), **`IdItem`** (ordem da planilha, SP 21.09) — ver `docs/inventario-campos.md` e `docs/bases/mapeamento-base-eletrica.md` |
| `Subestacoes` | SEs da campanha; `ClasseTensao`, **`TI`** (tipo de instalação — código do local), **`ArranjoFisico`** (1–5), **`LocalInstalacao`** (0–4) — ver `docs/subestacoes-campos.md` · TI: `docs/mcpse/ti-tipo-instalacao.md` |
| Fotos | `CodInventario`, `CodSE`, `CodAsset`, `CodTemp`, **`TipoFoto`** (`AMBIENTE` / `ITEM`), `FotoCampo`, `DataCaptura` — ver `docs/fotos-campos.md`. **Pendente:** lat/long no clique da câmera. |

**Domínio tarifário:** **TI** (tipo do local) + **CM** (equipamento) + TUC + atributos A1–A6. Classe de tensão, potência, sobra física/contábil. Chave de preço ANEEL é codificada (não texto).

## 5. Conversas Claude relevantes (filtradas)

| Conversa | Relevância |
|----------|------------|
| **App Power Apps para revisão tarifária elétrica** (389 msgs) | ⭐ Core — modelo de dados, telas, Power Fx, TUC/atributos |
| **Reconfiguração da câmera** (184 msgs) | Captura de fotos no app |
| **Geolocalização no registro de equipamentos** | Coordenadas em subestações |
| **Montagem de Bases para upar** | Listas SharePoint |
| **Manual do projeto para especialista em Lovable** | Manual para colaborador |
| **Escolher linguagem para projeto** | Decisão TypeScript/Expo/Supabase |
| **Erro Power Automate SharePoint/Excel** | Fluxo Excel → SharePoint (em andamento na época) |

**Ruído (não é AssetPro):** checklist Petrobras, Saneago/Ajuste 3, postes/trafo DXF, app financeiro SharePoint, automação de reuniões.

## 6. O que já foi feito (Power Apps)

- Estrutura de tabelas SharePoint desenhada
- App canvas para inserir itens de campo em SEs
- Lookup de TUC + atributos (A1–A6) ao inserir item
- Campos: quantidade, sobra física, classe de tensão, potência, etc.
- Tela de câmera (frontal/traseira, qualidade)
- Cache offline (`colCacheOffline`)
- Normalização de `TabelasUnificadas` e `TabelaAtributos` (977 linhas, faixas)
- Geolocalização discutida para registro

## 7. Em andamento / pendente

- [ ] **PRIORIDADE MÁXIMA — filtro SE no mobile (20.10 → corrigir 21.10).** `Tela_SelecionarSE`: chip **Finalizadas** não lista nada (há SE finalizada). Chip **Em campo** lista certo Em campo + Aguardando envio, mas **também lista Finalizadas** (errado). Rule: `.cursor/rules/pendencia-mobile-filtro-se.mdc`.
- [ ] **PRIORIDADE MÁXIMA (2ª) — criar SE com flag Linha (20.10 → amanhã).** Ao criar subestação, setar se é **Linha** (poste/torre entre SEs). Se Linha: mesmo esquema da Rede — coordenada no item, **sem** popup Local. Rule: `.cursor/rules/pendencia-criar-se-linha.mdc`.
- [ ] **Opção de criação de subestação (13.10).** A subestação hoje só nasce na importação da base. Falta a opção de criar uma no projeto. Não fazer até fechar a tela. (Ver flag Linha acima.)
- [x] **Toast no canto inferior direito (14.10).** No Desktop, o `cmpToast` fica a 15 px da direita e de baixo, com 500 de largura. O celular continua no `Notify` nativo.
- [ ] **Filtro do inventariante na tela de subestações (13.10).** No Desktop, `Tela_Subestacoes` filtra só por status (Todas, Pendente, Em campo, Finalizada). Falta filtrar pelo técnico. O nome no card hoje sai de `ValidadoPor`. Não fazer até fechar o controle.

- [ ] **Inventário de rede (10.10) — o que falta configurar.** A rede entra na **mesma** campanha. Não nasce outra lista nem outro card. Tela já no Desktop (`Tela_Exportar`): **Incluir rede** abre a lista de campanhas Pendente ou Em andamento, **mesmo as que já têm rede** (Fenômeno, 10.10): pode incluir mais, ou não. **Escolher** abre o diálogo com a campanha travada na tela. **Com base** anexa a planilha (`Container71` / `attPlanilha_1`). **Sem base** pergunta quantos inventariantes entram agora. A pessoa de cada uma é depois, na alocação. **`btnConfirmarModoRede` (10.10):** Com base chama `flxImportarCampanha.Run` na campanha escolhida (`attPlanilha_1`), no mesmo caminho do importar (barra e `varOpArquivo`). Sem base grava as linhas em `Subestacoes` (`REDE-01` / `Rede 01`…), continuando do maior `Rede NN`. A pasta `{PastaProjeto}/Rede NN` continua a cargo do fluxo, que só roda com planilha. Mockups: `docs/screens/mockup-incluir-rede-lista.html` · `mockup-incluir-rede-modo.html`.
  - [ ] **Marca de rede.** Sem coluna ainda. A lista de **Incluir rede** não esconde campanha que já tem rede. A marca, se vier, é para o celular separar subestação de rede. Não criar a coluna sem o ok.
  - [ ] **Com base — gravar.** `flxImportarCampanha` inclui os projetos e os itens na campanha escolhida (`CodInventario`). Não mexe nas subestações, na alocação nem nas visitas. Se a rede já existir vazia, o arquivo completa a mesma campanha. Se o sobra e o arquivo forem o mesmo projeto e o mesmo item, atualiza a base e mantém a coordenada já coletada.
  - [ ] **Sem base — gravar.** A quantidade é o que entra **agora**. A numeração continua do maior `Rede NN` já gravado nesta campanha: só `Rede 01` → os próximos são `Rede 02`, `Rede 03`… Campanha sem rede começa em `Rede 01`. Cada uma é uma linha em `Subestacoes`, itens 0, TI em branco. Pasta `{projeto}/Rede 01`. Equipamento entra na visita, como sobra.
  - [ ] **Coordenada do item.** `Inventario.CoordX` e `CoordY` já existem (texto, 09.10). No Studio, atualizar a fonte **Inventario**. Na visita de rede, coletar a coordenada no item. Na SE, a coordenada continua em `Subestacoes` e o item fica vazio. A foto não grava coordenada.
  - [ ] **Exportação.** Rede usa `Inventario.CoordX/Y`. SE copia `Subestacoes.CoordX/Y` para cada item. O `PreencherExportacao` ainda precisa da versão que cria essas colunas no Excel.
  - [ ] **Celular.** O bloco **Inventário** da `Tela_Home` vira **Rede** e lista só os projetos de rede desta campanha. **Levantamento** continua as subestações. A galeria “Visitas deste inventário” não recebe rede.
  - [ ] **Começar a campanha já com rede.** O **Incluir rede** cobre a campanha que já existe. Falta, no **Novo projeto**, a rede junto da planilha de subestação (com base, sem base ou não tem), no mesmo confirmar.

- [ ] **Desmembramento — ordem na lista (05.10):** as partes criadas a mais (`{CodAsset}-P2`, `-P3`…) ainda aparecem só no final da galeria da visita (`galItensBase`). Têm que ficar logo abaixo do item original. A tentativa de 05.10 (`IdItem` da base + `parte.N / 1000`, e a galeria ordenando por `IdItem` e depois por `CodAsset`) não mudou o teste. As partes já nascem em aberto, sem o chip Confirmado.

- [ ] **Campo — bugs 02.10 (Fenômeno, testar um de cada vez):**
  - [x] **Quantidade da base (05.10):** o envio da confirmação não grava mais em `Quantidade`. O que o técnico achou vai em `QtdeContado` (é o nome da coluna na lista `Inventario`; `QuantidadeCampo` não existe nela). Não encontrado grava `QtdeContado` 0 e não mexe na base. Desmembrado ainda grava em `Quantidade` a quantidade da parte. Sobra física grava a quantidade achada, porque não havia base.
  - [x] **Projeto Concluído com SE aberta (05.10):** Concluído só sai no Desktop, em **Finalizar projeto**, e só quando nenhuma subestação está aberta. Se ainda houver SE fora de `Finalizada`, o projeto volta para **Em andamento**. Com o projeto concluído, o celular **não** reabre subestação. O Desktop reabre o projeto; aí o usuário reabre a subestação. O envio da visita continua gravando **Em andamento**.
  - [x] **Enviar subestação muda o status do projeto (05.10, conferido no aparelho):** o envio grava o projeto como **Em andamento**. **Concluído** não sai daqui.
  - [x] **Finalizar projeto no Desktop (05.10):** a ação já existe. **Concluído** só sai nesse botão, e só quando nenhuma subestação está aberta. O filtro das concluídas na lista de projetos também já existe.
  - [ ] **Sobras na contagem (desktop):** quando existe sobra, `Tela_ItensConsulta` e `Tela_Subestacoes` têm que contabilizar as sobras também.
  - [x] **Para-raios = disjuntor (05.10, conferido):** TUC 310 entra no mesmo grupo de 570/575: a descrição não recebe o nome da TUC na frente, porque o A1 já traz esse texto. O card da visita (base e sobras) não coloca `TUC.A1 -` de novo se a descrição já começa com o código.
  - [x] **A1 em branco na edição (05.10, conferido):** ao abrir `Tela_EditarItem`, `varA1` nasce do rascunho e, se estiver vazio ou 0, da base (`varItemFoto.AtributoA1`). O `cmbA1` seleciona esse código em `colLookup`.
  - [x] **Salvar o item só offline (05.10, conferido):** o Salvar grava em `colCampoOffline` e no cache do aparelho. Não faz `Patch` em `Inventario`. O SharePoint recebe o item no envio da visita.
- [x] **Fotos do que já foi enviado (04.10):** no **Baixar dados**, entram as fotos da lista `Fotos` das subestações deste aparelho que ainda não estão em `colFotosCampo`. Casa pelo id da lista ou pelo guid do título. Ambiente e item. A linha fica `Sincronizada` para não reenviar. A imagem abre da lista quando há sinal.

- [x] **Desktop — recorte Home / arquivo (2026-09-05):** `Tela_Home` = galeria de campanhas (StartScreen). Arquivo = `Tela_Exportar`. Clique no card → `Tela_Subestacoes` (consulta). `Tela_Inventarios` = menu Inventários — entrada de dados (clone mobile). Conferência = 2.0 (placeholder).
- [x] **Áudio 11.09 (André) — TI:** tipo de instalação (do local), ≠ CM, ≠ kV. Spec: `docs/mcpse/ti-tipo-instalacao.md`
- [x] **TI — tabela oficial (11.09):** `docs/mcpse/Tabela-TI-CM-LI.xlsx` + `colTipoInstalacao`. 93/96 = medição; SE = 30–34 / 50–54.
- [x] **Pauta André — TI quem preenche (05.10):** se a base trouxer, fica. Se vier em branco, o inventariante preenche na visita. Não é o escritório. `docs/reunioes/pauta-proxima-andre.md`. O dropdown na visita ainda não está na tela.
- [x] **Escritório vê o que não foi designado (conferido 04.10):** perfil `ESCRITORIO` vê projeto, subestação e inventário sem linha em `Alocacoes`. O recorte (`varPerfil = "ESCRITORIO" || …`) está na lista de projetos, na lista de SEs, nas visitas e no **Baixar dados**. Inventariante continua só no que foi designado. Spec: `docs/powerfx/mobile-filtro-alocacao.txt`.
- [ ] **Reunião 18.09 (apresentação — FALTA FAZER):** ata `docs/reunioes/2026-09-18.md`. Spec de pastas já cortada. Itens:
  - [x] Card mobile: `IdUC` no fim do texto (`imobilizado · TUC · descrição · IdUC`). Nome da SE sai da descrição. Conferido 04.10.
  - [x] Galeria na **ordem da planilha** (`SortByColumns` por `IdItem`). Import grava `IdItem`. Conferido 04.10.
  - [x] Alocação: **selecionar todas** as livres (`btnAloSelTodas` + Limpar + Designar N). Ocupada não entra. Conferido 04.10.
  - [x] Filtro **“falta levantar” (05.10, conferido):** aba `FALTA` na `Tela_ItensVisita` (`btnFalta`). Mostra só o que ainda não foi inventariado: sem rascunho em `colCampoOffline` e sem `ValidadoPor`. O botão traz a contagem.
  - [x] Pastas: import cria **`Visão geral`**; `flxPastaFotosVisita` grava item só com o código (`Imobilizado`, senão `CodAsset`). Câmera de cima = Visão geral. 04.10: pasta da SE no import passou a usar o **nome da SE** (antes usava o nome do projeto).
  - [x] Busca mobile inclui `IdUC` na galeria da base (04.10). Sobras já buscava.
  - [x] Export: `flxExportarCampanha` já manda **Fabricante** e **Sobra**; o script preenche a coluna do modelo. Conferido 04.10.
  - **Não fazer agora:** ficha de item no desktop (André mexe no Excel); coordenada no item (rede); ZIP de fotos. TI em branco na visita ficou para o inventariante (05.10); o dropdown ainda não está na tela.
- [ ] **Reunião 17.09 (campo + escritório):** reserva no mobile; só o designado; Imobilizado na frente da TUC; sem Confirmar/Não encontrado na galeria; Salvar não confirma todos; descrição atualiza na galeria; slot → relogar; enviar SE muda status do projeto; não encontrado = qtd campo 0; designar várias SEs; busca mobile. Spec: `docs/reunioes/2026-09-17.md` · Studio: `docs/powerfx/pauta-2026-09-17-studio.md`
- [ ] **Reunião 08.09 (André):** catálogo CM curto; colunas da base elétrica (`Imobilizado`, `Bay`, `Elegivel`, `Reserva`, `Projeto`; SE: arranjo + local). Sem `BI`. Spec: `docs/bases/mapeamento-base-eletrica.md`
- [ ] **Desktop — `Tela_ItensConsulta`:** itens da SE (consulta) — clique em `Tela_Subestacoes`. Painel lateral (lista → Informações / Fotos). Mockups: `docs/screens/itens-consulta-fase1-lista.png` · `fase2-info.png` · `fase3-fotos.png`. Fórmulas: `docs/powerfx/Tela_ItensConsulta-formulas.txt`
- [ ] **Desktop — `Tela_Subestacoes`:** galeria de SEs da campanha; visualização, fotos, progresso (sem inserção). Mockup: `docs/screens/subestacoes-desktop.png`
- [ ] **`Subestacoes.ClasseTensao`:** criar coluna no SharePoint + importação + `lblKV` — spec: `docs/subestacoes-campos.md`
- [ ] **Desktop — `Tela_Inventarios`:** fluxo de coleta (cópia do mobile); SE → itens → editar/inserir/fotos.
- [x] **Centro modular (conferido 04.10):** `cCardCM` / `drpCM`, schema `colInventarioBase.CM`, **Baixar dados** traz `CM`, `btnSalvarItem` grava `CM: varCM`, envio faz Patch em confirmação e sobra física.
- [x] **Anexar foto da galeria (20.10):** `AddMediaCamera` + `AddMediaAnexar` lado a lado na `Tela_CapturaFoto`. Rule: `.cursor/rules/pendencia-foto-galeria.mdc` · spec: `docs/powerfx/Tela_FotosSE-formulas.txt`
- [ ] **Desktop — código de sobra na coluna Imobilizado (19.10):** em `Tela_ItensConsulta`, sobra física deixa a coluna IMOBILIZADO vazia. Mostrar `CodAsset` (`SOBRA-…`) no lugar. Base continua com Imobilizado. Rule: `.cursor/rules/pendencia-desktop-sobra-imobilizado.mdc`
- [ ] **Desktop — itens duplicados após envio (19.10):** SE JAGUARIBARA (`I012300000-0`) enviada; SharePoint sem duplicata; no **Desktop** (`Tela_ItensConsulta`) todos os itens aparecem em dobro. Não é mobile. Rule: `.cursor/rules/pendencia-desktop-itens-duplicados.mdc`
- [ ] Migração Power Apps → Expo/Supabase. **Último dos últimos** (08.10).
- [x] **Coordenada da subestação (08.10):** `CoordX` (longitude) e `CoordY` (latitude) em `Subestacoes`. Quem grava é o botão **Coletar coordenada** no popup Local da `Tela_ItensVisita`. A foto não grava. Sem sinal, sobe no envio. A exportação copia essa coordenada para cada item da SE. O script `PreencherExportacao` no Excel ainda precisa da versão nova para criar as colunas na planilha.
- [ ] **Pastas de foto no SharePoint (2026-09-10 / 18):** biblioteca `Projetos` (projeto → SE → `Visão geral` / `{código}`). Spec já atualizada; falta colar no Automate + rótulo no mobile. `docs/exportacao-fotos-pastas.md`
- [ ] **Exportar planilha xlsx (2026-09-15):** `flxExportarCampanha` + `modelo-exportacao.xlsx` + script `PreencherExportacao`. `TI`, `LocalInstalacao`, `ArranjoFisico` da linha de `Inventario`. Sem CSV. ZIP de fotos em stand-by. Spec: `docs/automate/flxExportarCampanha.md`
- [ ] **Excluir projeto (2026-09-15):** `btnExcluirCamp` na `Tela_Exportar` + popup + `flxExcluirCampanha`. Apaga Campanhas, SEs, Inventario, Fotos, Alocacoes, pasta `{PastaProjeto}` e xlsx de Importacoes/Exportacoes. Sem `Remove` no App. Spec: `docs/automate/flxExcluirCampanha.md`. Mockup: `docs/screens/excluir-projeto.png`.
- [ ] Power Automate: Excel → SharePoint (erros de conexão Graph/Excel Online)
- [ ] Colaborador Lovable/Supabase/Java (manual preparado)
- [ ] Expansão futura: saneamento e gás

## 8. Princípios de trabalho (Guga)

- Comunicação direta; prefere decisões confirmadas a textos longos
- Claude deve **sinalizar riscos** proativamente
- Power Fx: **ponto-e-vírgula** (`;`) e **`;;`** para encadeamento
- Entregar **código completo**, não snippets parciais
- Testar persistência em **dispositivo real** (não só preview)

## 9. Solution Power Platform (recebida)

**Arquivo:** `exports/Infralytics_1_0_0_1_managed.zip` (~366 KB, managed)

**Canvas app:** `dfs_infralytics_5e45e` (Infralytics)

**Environment variables (listas SharePoint):**
- `dfs_TabelaTUC`, `dfs_TabelaAtributos`, `dfs_TabelaUnificadas`
- `dfs_Subestacoes`, `dfs_Inventario`, `dfs_Fotos`
- `dfs_Inventariantes`, `dfs_Campanhas`, `dfs_Concessionarias`
- `dfs_AssetProSite` (site SharePoint)
- Conexão SharePoint Online

**YAMLs locais (Desktop):** `OneDrive\Desktop\Power Apps\AssetPro\YAMLs\`

## 10. O que ainda falta para o Cursor ficar 100%

- [x] Solution em `exports/`
- [ ] Excel/base atual (`teste_09_Inventario_v2.xlsx` ou similar)
- [ ] Lista exata de listas SharePoint criadas + URLs
- [ ] Screenshots das telas atuais
- [ ] Confirmar: continua só Power Apps ou já iniciou Expo?
- [ ] Estado atual do fluxo Power Automate

## 11. Arquivos deste repositório

```
docs/
├── 00-contexto-projeto.md
├── exportacao-fotos-pastas.md  # árvore SharePoint + Planilha / Fotos
├── fotos-campos.md
├── inventario-campos.md
├── subestacoes-campos.md
├── reunioes/                  # 08.09 CM · 11.09 TI · 17.09 campo · 18.09 apresentação
├── mcpse/                     # catálogos + ti-tipo-instalacao.md
├── powerfx/                    # Tela_Exportar-formulas.txt = dois botões
├── screens/                    # mockups + PNG
└── claude-exports/
```
