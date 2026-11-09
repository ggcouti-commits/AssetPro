# Asset Pro — Documentação técnica

Documento para o cliente.  
Data: 15 de outubro de 2026.

O passo a passo de tela e botão está no [manual de instruções](manual-de-instrucoes.md). Este arquivo descreve a plataforma, onde os dados ficam, o que cada campo guarda e quais fluxos rodam.

O Asset Pro inventaria equipamentos de subestações elétricas. O escritório sobe a base, designa as instalações e acompanha o retorno. O inventariante, no tablet, compara o pátio com a base, tira foto e devolve a visita. A saída é uma planilha `.xlsx` e as fotos em pastas no SharePoint.

Na tela, o conjunto de instalações se chama **Projeto**. No SharePoint, a lista se chama **Campanhas**.

No tablet a marca é **Asset Pro**. No escritório, o menu leva a marca **assetexperts**. Os dois aplicativos leem o mesmo site.

## Arquivos para download

Pasta **Documentos Compartilhados / AssetPro**, no site `AssetPro493`:

https://assetexpertsdados.sharepoint.com/sites/AssetPro493/Documentos%20Compartilhados/Forms/AllItems.aspx?id=%2Fsites%2FAssetPro493%2FDocumentos%20Compartilhados%2FAssetPro&viewid=40b0572b%2D91d9%2D4e1c%2D9bdb%2D6abc4e60d514

| Arquivo | Para quê |
|---------|----------|
| `AssetProDesktop-Setup.exe` | Instalador do aplicativo de escritório, no Windows |
| `Asset-Pro-Mobile.apk` | Aplicativo de campo, no tablet Android |
| `base-modelo-para-importacao.xlsx` | Planilha modelo da base usada no **Importar projeto** |

---

## 1. Stack

| Camada | O que é |
|--------|---------|
| Aplicativo | Microsoft Power Apps, Canvas. Dois apps: tablet e escritório |
| Dados | Listas do SharePoint Online |
| Arquivos | Bibliotecas de documentos do mesmo site (fotos e planilhas) |
| Automação | Power Automate (fluxos de nuvem) |
| Identidade do aparelho | Uma conta Microsoft 365 no tablet |
| Identidade de quem está em campo | Slot cadastrado pelo escritório (login e senha na lista `Inventariantes`) |
| Trabalho sem sinal | Coleções gravadas no aparelho (`SaveData`). O SharePoint só recebe a visita no envio |
| Catálogo do equipamento | Listas `TabelaTUC`, `TabelaAtributos` e `TabelasUnificadas` (MCPSE) |
| Planilha de saída | Excel `.xlsx`, preenchida por script do Excel Online dentro do fluxo de exportação |

Não há banco Dataverse nem SQL. Não há pacote ZIP de fotos.

Publicar o app de campo atualiza o tablet já instalado. O pacote nativo (APK, Android 10 ou mais novo) não precisa ser gerado de novo a cada ajuste de tela.

---

## 2. Quem usa

| Papel | Onde entra | O que vê |
|-------|------------|---------|
| Escritório | Navegador e também o tablet, com o slot de perfil **Escritório** | Todas as campanhas e todas as subestações, inclusive as que ainda não foram designadas. No navegador cadastra slot, importa, inclui rede, cria subestação, designa, consulta, finaliza e baixa a planilha |
| Inventariante | Tablet, com o slot de perfil **Inventariante** | Só as campanhas e as subestações designadas àquele slot. Baixa, levanta e envia a visita |

Uma conta Microsoft abre o tablet. Quem opera naquele dia entra com o slot. Vários prestadores revezam o mesmo aparelho, cada um com o seu slot, sem licença Microsoft por prestador.

O recorte é o perfil do slot. Escritório no tablet vê o projeto inteiro. Inventariante vê só o que foi designado para ele.

Uma subestação tem um inventariante por vez.

---

## 3. Aplicativos

| App | Uso | Menu |
|-----|-----|------|
| Asset Pro | Tablet | Login do slot. Escritório vê todas as campanhas e subestações. Inventariante vê só as designadas. Baixar, levantar, enviar |
| Escritório | Navegador | Home, Importar / Exportar, Conferência, Inventários, Usuários |

**Inventários**, no escritório, é o caminho de coleta no navegador, no mesmo modelo da visita. A consulta do que voltou do campo é Home → subestações → itens, somente leitura.

---

## 4. Onde os dados ficam

Tudo mora no site SharePoint do ambiente.

### 4.1 Listas

| Lista | Um item é |
|-------|-----------|
| `Campanhas` | Um projeto |
| `Subestacoes` | Uma instalação (subestação ou rede) do projeto |
| `Inventario` | Um equipamento |
| `Fotos` | O registro da foto que o app mostra |
| `Alocacoes` | O vínculo entre um slot e uma instalação |
| `Inventariantes` | Um slot (escritório ou campo) |
| `Concessionarias` | Uma concessionária |
| `TabelaTUC` | Um tipo de unidade de cadastro |
| `TabelaAtributos` | Um atributo (A1–A6) de um TUC, com o tipo de entrada |
| `TabelasUnificadas` | O lookup dos códigos (lista, faixa, texto livre) |

### 4.2 Bibliotecas

| Biblioteca | Conteúdo |
|------------|----------|
| `Projetos` | Pastas das fotos |
| `Importacoes` | O `.xlsx` que o escritório subiu |
| `Exportacoes` | O `.xlsx` gerado na exportação, e o modelo `modelo-exportacao.xlsx` |

### 4.3 Projeto (`Campanhas`)

| Campo | O que guarda |
|-------|----------------|
| `CodInventario` | Código do projeto. Nasce na importação. Amarra subestações, itens, fotos e alocações |
| `NomeInventario` | Nome do projeto, o que aparece no card |
| `Periodo` | Mês e ano, em texto |
| `Concessionaria` / `CodConcessionaria` | Concessionária escolhida ou cadastrada na hora |
| `Status` | `Pendente`, `Em andamento` ou `Concluído` |
| `PastaProjeto` | Nome da pasta raiz em `Projetos`, gravado uma vez |
| `Ativo` | `Sim` enquanto o projeto existe para o app |

Setor (no exemplo das telas, Elétrico) entra no cadastro do projeto junto com o período.

### 4.4 Instalação (`Subestacoes`)

Uma linha por subestação e, quando houver rede no mesmo projeto, uma linha por rede (`REDE-01`, `Rede 01`).

| Campo | Tipo | De quem é | O que guarda |
|-------|------|-----------|----------------|
| `CodInventario` | Texto | Projeto | Liga a instalação ao projeto |
| `CodSE` | Texto | Instalação | Código ODI, ou `REDE-01` na rede sem base |
| `NomeSE` | Texto | Instalação | Descrição da ODI, ou `Rede 01` |
| `Status` | Texto | Instalação | `Pendente` ou `Finalizada` |
| `TI` | Número | O local | Tipo de instalação. O mesmo código em todos os equipamentos dali |
| `LocalInstalacao` | Número 0–4 | O local | Onde a instalação está no sistema |
| `ArranjoFisico` | Número 1–5 | O local | Arranjo de barra |
| `ClasseTensao` | Texto | O local | Tensão nominal, por exemplo `138 kV`. Sai do nome da ODI quando ele traz o kV. Não é o TI |
| `CoordX` | Texto | O local | Longitude. Quem grava é **Coletar coordenadas** |
| `CoordY` | Texto | O local | Latitude |
| `CM` | Número | Legado | Não é o centro modular do equipamento. O CM oficial está em `Inventario.CM` |

TI, local de instalação e arranjo são da instalação. Se a mesma ODI vier com valores diferentes na planilha, a importação grava o valor mais frequente. Com a subestação aberta, o inventariante corrige esses três no popup **Local**. Valor vindo da base não trava. Subestação finalizada abre o popup só para leitura.

`ClasseTensao` é consulta. O inventariante não altera a tensão nominal na visita.

### 4.5 Equipamento (`Inventario`)

Uma linha da planilha vira um item. Sobra e desmembramento também nascem aqui, no envio da visita.

| Campo | O que guarda |
|-------|----------------|
| `CodInventario` | Projeto |
| `CodSE` / `NomeSE` | Instalação |
| `CodAsset` | Chave do item. Na base, Nº ASSET EXPERTS. Na sobra, `SOBRA-{CodSE}-{nn}`. No desmembramento, a primeira parte fica com o código original e as seguintes levam `{código}-P2`, `-P3` |
| `IdItem` | Ordem da linha na planilha. A lista da visita ordena por este campo |
| `Imobilizado` | NÚMERO IMOBILIZADO |
| `IdUC` | IdUC, se a coluna existir na planilha |
| `CodTUC` / `DescricaoTUC` | TUC e o texto do tipo de unidade de cadastro |
| `AtributoA1` … `AtributoA6` | Códigos dos atributos. A1 é o subtipo. Vazio na planilha sobe como `00` |
| `DescricaoBem` | Descrição técnica do ativo |
| `Quantidade` | Quantidade da base. Confirmar o item não altera este número |
| `QtdeContado` | O que o inventariante achou. Não encontrado grava `0` |
| `Unidade` | UN, M, e assim por diante |
| `CM` | Centro modular do equipamento, código 0 a 9 |
| `Elegivel` / `Reserva` | `SIM` ou `NÃO`. Reserva é do equipamento, não é um tipo de instalação |
| `Fabricante`, `Modelo`, `NumSerie`, `Ano` | Identificação. Podem vir na base e ser corrigidos na visita |
| `Bay` | Bay (138KV, PAINEL, CFTV…) |
| `CodOperacao` | Código de operação. Pode vir preenchido na base |
| `Projeto` | Coluna PROJETO da base (bem de projeto). Não é o nome do projeto do app |
| `Observacoes` | Texto livre |
| `Status` | Situação do item depois da visita |
| `Sobra` | Marca de sobra física |
| `ValidadoPor` | Quem salvou o item |
| `Origem` | De onde o item nasceu (base, sobra, desmembramento) |
| `TI`, `LocalInstalacao`, `ArranjoFisico` | Cópia dos códigos da instalação na linha do item. A planilha de saída lê daqui |

A quantidade da parte desmembrada é gravada em `Quantidade`, porque aquela parte não existia como linha da base. A sobra grava em `QtdeContado` a quantidade achada, porque não havia quantidade de base.

### 4.6 Foto (`Fotos`)

A lista é o que o app consulta. O arquivo JPG mora na biblioteca `Projetos`.

| Campo | O que guarda |
|-------|----------------|
| `TipoFoto` | `AMBIENTE` (visão geral da instalação) ou `ITEM` (equipamento) |
| `CodInventario` / `CodSE` | Projeto e instalação |
| `CodAsset` | Vazio na visão geral. No item, a mesma chave de `Inventario.CodAsset` |
| `FotoCampo` | A imagem |
| `DataCaptura` | Quando a foto foi tirada |

Foto de visão geral não tem teto. Foto de equipamento tem teto de **5**.

Apagar no tablet pede confirmação (miniatura, data, **Excluir**).

### 4.7 Slot (`Inventariantes`)

| Campo | O que guarda |
|-------|----------------|
| Código `USR-00N` | Nasce sozinho |
| `Login` | O que a pessoa digita. No campo, por exemplo `INV01`. Só se edita na criação |
| `Senha` | Senha do tablet. No editar, vazio não troca a senha |
| Perfil | `ESCRITORIO` ou `INVENTARIANTE` |
| `UsadoPor` | Quem está com o aparelho. É o nome da boas-vindas no tablet |
| `Ativo` | Desligado, o tablet deixa de aceitar o login. O cadastro continua na lista |

O login do tablet confere o slot nessa lista.

Trocar senha, desativar o slot ou mudar a designação pede que o tablet entre de novo quando houver rede.

### 4.8 Alocação (`Alocacoes`)

Liga um slot a uma instalação daquele projeto. Subestação ocupada não entra em outro slot. O **X** na coluna da direita tira a designação e a instalação volta a ficar livre.

Na aba **Redes**, **Adicionar** e **Selecionar todas** marcam as redes livres daquele slot.

### 4.9 Concessionária (`Concessionarias`)

Nome, sigla, CNPJ, UF e código ANEEL. Na importação dá para escolher uma já cadastrada (`Ativo = Sim`) ou cadastrar na hora.

### 4.10 Catálogo MCPSE

| Lista | Função |
|-------|--------|
| `TabelaTUC` | Tipos de unidade de cadastro |
| `TabelaAtributos` | Por TUC, cada atributo e o tipo de entrada: `LISTA`, `FAIXA` ou `LIVRE` |
| `TabelasUnificadas` | Valores do lookup |

Atributo `LIVRE` grava o código `0`. O texto livre vai em `DescricaoBem`. Faixa com limite superior vazio grava `0`. Potência em kVA, tensão em kV.

O centro modular não tem lista no SharePoint. O app carrega o catálogo 0–9 na abertura:

| Código | Sigla | Nome |
|--------|-------|------|
| 0 | MIG | Infraestrutura geral |
| 1 | EQP | Equipamentos |
| 2 | EL | Entrada de linha |
| 3 | IB | Interligação de barra |
| 4 | CT | Conexão de trafo |
| 5 | CCP | Conexão de banco |
| 6 | CRL | |
| 7 | CRB | |
| 8 | CC | |
| 9 | CCA | |

---

## 5. Planilha de entrada

Uma aba, uma linha por equipamento. A linha de título pode estar nas primeiras doze linhas. Cada **CÓDIGO ODI** distinto vira uma subestação. Cada linha vira um item.

| Na planilha | Vai para |
|-------------|----------|
| Nº ASSET EXPERTS | `Inventario.CodAsset` |
| NÚMERO IMOBILIZADO | `Inventario.Imobilizado` |
| IdItem | `Inventario.IdItem` |
| CÓDIGO ODI | `Subestacoes.CodSE` e `Inventario.CodSE` |
| DESCRIÇÃO DE ODI | `Subestacoes.NomeSE` |
| TI | `Subestacoes.TI` |
| LOCAL INSTALAÇÃO | `Subestacoes.LocalInstalacao` |
| CENTRO MODULAR | `Inventario.CM` |
| ARRANJO FÍSICO | `Subestacoes.ArranjoFisico` |
| TUC | `Inventario.CodTUC` |
| TIPO DE UNIDADE DE CADASTRO | `Inventario.DescricaoTUC` |
| A1 … A6 | `Inventario.AtributoA1` … `AtributoA6` |
| DESCRIÇÃO TÉCNICA DO ATIVO | `Inventario.DescricaoBem` |
| QUANT / UNIDADE | `Quantidade` / `Unidade` |
| ELEGÍVEL / RESERVA | `Elegivel` / `Reserva` |
| FABRICANTE, MODELO, NÚMERO SÉRIE, ANO | os campos de mesmo nome |
| BAY, CÓDIGO OPERAÇÃO, PROJETO, OBSERVAÇÃO | `Bay`, `CodOperacao`, `Projeto`, `Observacoes` |
| IdUC ou IDUC | `Inventario.IdUC` |

A importação exige arquivo `.xlsx` e as colunas **CÓDIGO ODI** e **Nº ASSET EXPERTS**. Se o projeto já tiver subestações, a carga não duplica.

Enquanto a importação roda, o card na Home fica **Importando**.

### Subestação que não veio na planilha

No desktop, **Nova subestação** grava código, nome, prefixo de tensão, TI, local de instalação, arranjo e, se quiser, o inventariante. **Incluir na lista** só prepara. **Criar (n)** grava. O botão fica apagado enquanto a lista do popup está vazia. A subestação nasce sem nenhum item. O equipamento entra depois, na visita.

---

## 6. Códigos da revisão tarifária

A chave de avaliação é **TI + CM + TUC + A1 a A6**. O preço casa pelo código, não pelo texto da descrição.

| Código | De quem é | Valores |
|--------|-----------|---------|
| TI | A instalação | Tipo de instalação. Na SE, a faixa segue a maior tensão. Urbana 30–34 (SDU), rural 50–54 (SDR), rede 40 e 41, usina 10–19. **93 e 96 são medição, não subestação** |
| CM | O equipamento | 0 a 9, tabela acima |
| Local de instalação | A instalação | 0 RD (distribuição), 1 DIT-RPC, 2 RBSE, 3 RBNI, 4 DIT-RCDM. Distribuição é 0 |
| Arranjo físico | A instalação | 1 BS, 2 BD, 3 BDDD, 4 BPT, 5 DJM |
| TUC + A1…A6 | O equipamento | A1 é o subtipo. Atributos técnicos começam em A2 |

TI não é kV, não é o centro modular e não é o arranjo da barra.

---

## 7. Status e sincronização

| Onde | Valor | Significado |
|------|--------|-------------|
| Projeto | Pendente | Importado. Nenhuma visita enviada |
| Projeto | Em andamento | Pelo menos uma visita já subiu |
| Projeto | Concluído | O escritório finalizou, e nenhuma instalação está aberta |
| Instalação | Pendente | Ainda não levantada |
| Instalação | Finalizada | O inventariante encerrou e o envio gravou esse status |
| No tablet, antes do envio | Aguard. envio | A instalação já foi finalizada neste aparelho e está na fila |

**Concluído** só nasce no desktop, em **Finalizar projeto**, e só se nenhuma instalação estiver aberta. Se ainda houver instalação fora de **Finalizada**, o projeto permanece **Em andamento**.

Enviar a visita grava o projeto como **Em andamento**. Não conclui o projeto.

Com o projeto **Concluído**, o tablet não reabre instalação. O desktop reabre o projeto; aí a instalação pode ser reaberta.

### Sem sinal

1. **Baixar dados**, com sinal. O fluxo `flxBaixarCampanha` traz subestações, itens e fotos já enviadas das instalações daquele slot. O tablet guarda essa carga no aparelho.
2. Levantamento, com ou sem sinal. **Salvar** grava no aparelho. Não grava em `Inventario` nesse momento.
3. **Finalizar** a instalação. Ela entra na fila (**Aguard. envio**). Dá para **Reabrir**: volta para em campo. O que já tinha sido enviado permanece. O que mudar sobe no próximo envio, depois de finalizar de novo.
4. **Enviar visita**, com sinal. Sobe fichas e fotos. Em seguida o fluxo de pastas grava os JPG.

O escritório, antes desse envio, vê a base importada. Ficha preenchida e foto nova aparecem depois.

### Desfecho do item

| Ação | Efeito |
|------|--------|
| Confirmado | `QtdeContado` recebe a quantidade encontrada. `Quantidade` permanece |
| Não encontrado | `QtdeContado` = 0. `Quantidade` não zera |
| Sobra (`+ Item`) | Código `SOBRA-{CodSE}-{nn}`. A quantidade achada é a contada |
| Desmembrar | A soma das partes fecha a quantidade da base. Fabricante, modelo, número de série, ano, bay, código de operação e observações nascem vazios. O restante copia. As partes novas nascem sem o chip Confirmado |

Salvar um item não confirma os outros.

### Coordenada

Na subestação, longitude e latitude ficam em `Subestacoes.CoordX` e `CoordY`. O botão **Coletar coordenadas** grava. A foto não grava coordenada. Sem GPS no momento, a coordenada sobe no envio. A planilha de saída repete a coordenada da subestação em cada item dela.

---

## 8. Fotos no SharePoint

```text
Projetos/
  {PastaProjeto}/
    {CodSE} - {NomeSE}/
      Visão geral/                 TipoFoto = AMBIENTE
      {Imobilizado ou CodAsset}/   TipoFoto = ITEM
```

A importação cria a raiz, a pasta de cada subestação e **Visão geral**. A pasta do equipamento nasce no envio da foto. O nome é só o código (`Imobilizado`, senão `CodAsset`, senão `SEM-IMOB`). A descrição do bem não entra no caminho.

`Visão geral` é nome reservado. A importação cria essa pasta.

O nome do arquivo leva data e hora. Excluir o projeto recicla a pasta `{PastaProjeto}` inteira.

---

## 9. Planilha de saída

`flxExportarCampanha` gera um `.xlsx` na biblioteca `Exportacoes`, só com itens de instalação `Finalizada`.

No card do projeto:

| Estado | O que a tela mostra |
|--------|---------------------|
| Nenhuma instalação finalizada | **Sem saída** |
| Há finalizada e o arquivo ainda não está pronto | **Planilha** |
| O arquivo já foi gerado | **Planilha pronta**, com **Atualizar** (gera de novo) e **Baixar** |

Colunas do modelo, nesta ordem: `CodAsset`, `Imobilizado`, `IdUC`, `CodSE`, `NomeSE`, `TI`, `LocalInstalacao`, `CM`, `ArranjoFisico`, `CodTUC`, `DescricaoTUC`, `A1`…`A6`, `DescricaoBem`, `Quantidade`, `QuantidadeCampo`, `Unidade`, `Elegivel`, `Reserva`, `Fabricante`, `Modelo`, `NumSerie`, `Ano`, `Bay`, `CodOperacao`, `Projeto`, `Observacoes`, `Status`, `ValidadoPor`, `Origem`, `Sobra`, `CoordX`, `CoordY`.

`QuantidadeCampo` na planilha é o que foi contado (`QtdeContado`). `TI`, `LocalInstalacao` e `ArranjoFisico` saem da linha do item. Na subestação, `CoordX` e `CoordY` são os da instalação. Na rede (`CodSE` começando com `REDE-`), `CoordX` e `CoordY` são os do equipamento.

---

## 10. Rede

A rede entra no projeto que já existe. Não nasce outro card na Home.

| Modo | O que grava |
|------|-------------|
| **Com base** | A planilha da rede sobe para a campanha escolhida. As subestações dessa campanha ficam como estão |
| **Sem base** | A quantidade do passo é quantas redes nascem agora. A numeração continua do maior `Rede NN` da campanha. Campanha sem rede começa em `Rede 01`. Cada uma é uma linha em `Subestacoes`, com 0 itens, em **Pendente**. A pessoa é escolhida depois, na alocação |

A lista **Incluir rede** mostra campanhas **Pendente** ou **Em andamento**, mesmo as que já têm rede.

No tablet, o botão **Rede** fica na home do projeto. **Visitas deste inventário** continua só com subestação. O equipamento da rede sem base entra na visita como sobra.

---

## 11. Fluxos

| Fluxo | Quando roda | O que faz |
|-------|-------------|-----------|
| `flxImportarCampanha` | **Importar projeto**, e **Incluir rede** com base | Lê o `.xlsx`, cria subestações e itens, cria as pastas de foto |
| `flxProgressoImportacao` | Durante a importação | A barra pergunta quantas subestações e itens já nasceram |
| `flxBaixarCampanha` | **Baixar dados** no tablet | Devolve JSON de subestações e itens daquele projeto |
| `flxPastaFotosVisita` | Um run depois do envio da visita | Grava os JPG nas pastas, em lote |
| `flxExportarCampanha` | **Planilha** / **Atualizar** | Gera o `.xlsx` das instalações finalizadas e devolve o link de download |
| `flxExcluirCampanha` | **Excluir** no card | Apaga o projeto, subestações, itens, fotos, alocações, a pasta em `Projetos` e os `.xlsx` daquele código em `Importacoes` e `Exportacoes`. Não desfaz |
