# `flxExcluirCampanha` — apaga o projeto e os derivados

> Decisão 2026-09-15 (Fenômeno). Front: **Excluir projeto**. Back: lista `Campanhas`.  
> Site: `https://gustavogarciacoutinho991.sharepoint.com/sites/AssetPro`  
> App: `Tela_Exportar` → `btnExcluirCamp` → popup → este fluxo.  
> **Não** apagar no `ForAll` do Power Apps: Inventario passa de 2.000 linhas e estoura.

Apaga, nesta ordem, tudo com o mesmo `CodInventario`:

1. Guarda `ID` + `PastaProjeto`
2. Item em `Campanhas` (cedo — o App some o card e o `Run` não espera 3.000 deletes)
3. **Responder_OK** (antes dos loops — senão o Power Apps estoura em ~2 min)
4. `Fotos` → `Inventario` → `Alocacoes` → `Subestacoes`
5. Pasta raiz `{PastaProjeto}` na biblioteca `Projetos` (a raiz já leva SEs / Visão geral / itens)
6. Arquivos em `Importacoes` com coluna `CodInventario` = o código (não filtra por nome)
7. Arquivos `Exportacao-{CodInventario}-*.xlsx` em `Exportacoes`

O `Run` do App espera no máximo ~120 s. Os loops podem levar 10+ min. Responder cedo, igual o import.

**Não** apaga: `Concessionarias`, `Inventariantes`, catálogos, `modelo-exportacao.xlsx`.

Renomeia cada ação **exatamente** como está em negrito.

---



## Criar o fluxo

make.powerautomate.com → **Criar** → **Fluxo da nuvem instantâneo** → em branco.

Nome: `flxExcluirCampanha`

Configurações do fluxo (⋯ no canvas → **Configurações**): **Tempo limite** `PT20M` (20 min). Projeto grande demora.

---



### 1. Gatilho — Power Apps (V2) — `Quando_o_Power_Apps`

Uma entrada **Texto** → nome `CodInventario`.

Publicar. No Studio: Power Automate → `flxExcluirCampanha` → **⋯** → **Atualizar**.

---



### 2. Compor — `CodLimpo`

```
trim(coalesce(triggerBody()?['text'], ''))
```

Se o V2 expuser o nome da entrada, usa `trim(triggerBody()?['CodInventario'])`.

---



### 3. SharePoint — Obter itens — `Obter_Campanha`

- Lista: **Campanhas** (a mesma do app; se tiver espaço no nome, escolhe no dropdown)
- Consulta de filtro:

```
CodInventario eq '@{outputs('CodLimpo')}'
```

---



### 4. Condição — `TemCampanha`

```
length(body('Obter_Campanha')?['value'])
```

é maior que `0`.

**Se não:**

#### 4a. Responder a um Power App — `Responder_NaoAchou`


| Saída | Valor                    |
| ----- | ------------------------ |
| ok    | `false`                  |
| erro  | `Projeto não encontrado` |


Encerrar.

**Se sim:** segue. Tudo abaixo fica **dentro** deste ramo.

---



### 5. Compor — `IdCampanha`

```
first(body('Obter_Campanha')?['value'])?['ID']
```

---



### 6. Compor — `Pasta`

```
trim(coalesce(first(body('Obter_Campanha')?['value'])?['PastaProjeto'], ''))
```

---

### 6b. SharePoint — Excluir item — `Excluir_Campanha`

- Lista: **Campanhas**
- Id: **fx** `outputs('IdCampanha')`

Sobe pra cá. Sem o item, o `Refresh` do App não traz o card de volta. `Pasta` e `ID` já estão nos Compor.

**Sintoma se ficar no fim:** SEs / Inventario somem, a linha em `Campanhas` fica. O `Reciclar_Pasta` (passo 11) falha (pasta vazia, 404) e o fluxo para **antes** de apagar a campanha. Conferir na run: `Excluir_Campanha` tem que aparecer **antes** de `Responder_OK`.

---

### 6c. Responder a um Power App — `Responder_OK`

**Arrasta** o Responder que estava no fim. **Não** cria um segundo (uma run só responde uma vez).

⋯ da ação → **Configurações** → **Resposta assíncrona** = **Ligado**.

Isso **não** substitui a posição: se o Responder continuar **depois** dos Fazer até, o App ainda espera 120 s e falha. Tem que estar **antes** dos loops.

`IdCampanha` é número. **Não** usa `empty()`.

| Saída | Tipo | Valor (**fx**) |
|-------|------|----------------|
| ok | Texto | `if(greater(outputs('IdCampanha'), 0), 'true', 'false')` |
| erro | Texto | `if(greater(outputs('IdCampanha'), 0), '-', '-')` |

Depois disto o App é solto. Os escopos 7–15 **continuam** na mesma run.

---

### 7. Escopo — `Esvaziar_Fotos`

Dentro do escopo, nesta ordem:

#### 7a. Fazer até — `Ate_Fotos`

Configurações do **Fazer até**: contagem `50` · tempo limite `PT15M`.

Condição — **não** cola `equals(...)` solto (o salvar quebra). Dois jeitos:

**A — campos (preferido, igual o TemCampanha):**
1. Esquerdo → **fx**: `length(body('Obter_Fotos')?['value'])`
2. Meio → **é igual a**
3. Direito → `0` direto, sem fx

**B — modo avançado:** a linha **tem** que começar com `@`:

```
@equals(length(body('Obter_Fotos')?['value']), 0)
```

O **Fazer até** avalia **depois** da primeira volta. Primeira volta sempre roda. Monta o Obter_Fotos **dentro** do até **antes** de colar a condição (senão a ação ainda não existe).

Mesma regra nos quatro até: Fotos · Itens · Alocacoes · SEs. Troca só o nome do Obter.

**Dentro** do Ate_Fotos:

##### 7a-1. SharePoint — Obter itens — `Obter_Fotos`

- Lista: **Fotos**
- Consulta de filtro: `CodInventario eq '@{outputs('CodLimpo')}'`
- Linhas principais: **200**
- Paginação: desligada (o loop já pagina)



##### 7a-2. Aplicar a cada — `Apagar_Fotos`

De: `body('Obter_Fotos')?['value']`  
Configurações: **Grau de paralelismo** 20.

Dentro:

###### 7a-2a. SharePoint — Excluir item — `Excluir_Foto`

- Lista: **Fotos**
- Id: `items('Apagar_Fotos')?['ID']`

A linha da lista some. `FotoCampo` some com ela. JPG na biblioteca **Projetos** some no passo da pasta.

---



### 8. Escopo — Esvaziar_Inventario

Igual o 7, nomes:


| Ação           | Nome                                                                                                   |
| -------------- | ------------------------------------------------------------------------------------------------------ |
| Fazer até      | `Ate_Inventario`                                                                                       |
| Obter itens    | `Obter_Itens` · lista **Inventario** · filtro `CodInventario eq '@{outputs('CodLimpo')}'` · 200 linhas |
| Aplicar a cada | `Apagar_Itens` · paralelismo 20                                                                        |
| Excluir item   | `Excluir_Item` · lista **Inventario** · Id `items('Apagar_Itens')?['ID']`                              |


Condição do até — campos: esquerdo fx `length(body('Obter_Itens')?['value'])` · é igual a · `0`.  
Modo avançado: `@equals(length(body('Obter_Itens')?['value']), 0)`

Alocacoes: `body('Obter_Alocacoes')`. SEs: `body('Obter_SEs')`.

---



### 9. Escopo — `Esvaziar_Alocacoes`

Mesmo padrão. Lista **Alocacoes**. Nomes: `Ate_Alocacoes` · `Obter_Alocacoes` · `Apagar_Alocacoes` · `Excluir_Alocacao`.

Sem isso o slot continua apontando para SE morta.

---



### 10. Escopo — `Esvaziar_Subestacoes`

Mesmo padrão. Lista **Subestacoes**. Nomes: `Ate_SEs` · `Obter_SEs` · `Apagar_SEs` · `Excluir_SE`.

---



### 11. Condição — `TemPasta`

```
empty(outputs('Pasta'))
```

é igual a `false`.

**Se sim:**

#### 11a. SharePoint — Enviar uma solicitação HTTP — `Reciclar_Pasta`

- Site: AssetPro
- Método: **POST**
- URI (fx):

```
concat(
  '_api/web/GetFolderByServerRelativeUrl(''/sites/AssetPro/Projetos/',
  uriComponent(outputs('Pasta')),
  ''')/Recycle()'
)
```

- Cabeçalhos:


| Chave  | Valor                               |
| ------ | ----------------------------------- |
| Accept | `application/json;odata=nometadata` |


Recycle manda a **raiz** da campanha para a lixeira. SEs, `Visão geral` (ou `Ambiente` velho) e pastas de item vão junto. Não precisa apagar arquivo por arquivo.

Se a pasta já não existir (campanha velha, import falhou no meio): ⋯ da ação → **Configurar execução posterior** → também **se êxito** e **se falhou**. O fluxo segue.

**Se não** (`PastaProjeto` vazio): pula. Não cria pasta vazia.

---



### 12. SharePoint — Obter arquivos (somente propriedades) — `Obter_Importacoes`

- Biblioteca: **Importacoes**
- Pasta: `/`
- Consulta de filtro:

```
CodInventario eq '@{outputs('CodLimpo')}'
```

Limite: 200. Paginação ligada.

**Não** filtra por `FileLeafRef`. O conector ignora ou falha; e o arquivo hoje se chama `INV-001.xlsx`, não `INV-001-…xlsx`. A chave é a coluna `CodInventario` (o import grava no `Gravar_CodInventario`).

Arquivos velhos, importados **antes** da coluna: a coluna está vazia. Ou reimporta, ou preenche na grade da biblioteca.

---



### 13. Aplicar a cada — `Apagar_Importacoes`

De: `body('Obter_Importacoes')?['value']` · paralelismo 10.

#### 13a. SharePoint — Excluir arquivo — `Excluir_Importacao`

- Biblioteca: **Importacoes**
- Identificador: `items('Apagar_Importacoes')?['{Identifier}']`

Se o seletor tiver **Identificador**, usa esse.

---



### 14. SharePoint — Obter arquivos (somente propriedades) — `Obter_Exportacoes`

- Biblioteca: **Exportacoes**
- Pasta: `/`
- Consulta de filtro:

```
startswith(FileLeafRef,'Exportacao-@{outputs('CodLimpo')}-')
```

**Não** pega `modelo-exportacao.xlsx` (nome diferente).

---



### 15. Aplicar a cada — `Apagar_Exportacoes`

De: `body('Obter_Exportacoes')?['value']` · paralelismo 10.

#### 15a. SharePoint — Excluir arquivo — `Excluir_Exportacao`

- Biblioteca: **Exportacoes**
- Identificador: `items('Apagar_Exportacoes')?['{Identifier}']`

---



### 16. ~~Excluir_Campanha~~ — **já no 6b, não repetir**

Se ainda estiver no fim do fluxo, **não apaga** ainda: **arrasta** para entre `Pasta` e `Responder_OK` (vira o 6b). Só apaga se já existir um 6b no lugar certo — uma run não pode excluir o mesmo ID duas vezes.

Se a campanha órfã já está na lista (SEs = 0, card ainda em `Campanhas`): SharePoint → lista **Campanhas** → excluir a linha. Não depende do fluxo. O App some o card no próximo play (`OnStart` recarrega `colCampanhas`).

### 17. ~~Responder_OK~~ — **já no 6c, não repetir**

Uma run só pode executar **um** Responder. O do fim some; fica o que está depois de `Pasta`.


---



## App

`Tela_Exportar` → `btnExcluirCampConfirmar` → `OnSelect`: `docs/powerfx/Tela_Exportar-formulas.txt` (bloco Excluir).

Um botão **Excluir** no card. Popup confirma. `Run` espera o fluxo.

---



## O que não fazer

- Não `Remove` / `ForAll` nas listas no Power Apps.
- Não apagar `modelo-exportacao.xlsx`.
- Não apagar `Concessionarias` nem catálogos.
- Não apagar só `Campanhas.Ativo = "Nao"` — o pedido é apagar de verdade.
- Não criar pasta no `ForAll` do envio da visita (já era regra).
- Não zipar foto neste fluxo.

