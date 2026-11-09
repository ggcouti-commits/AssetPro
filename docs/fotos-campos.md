# Fotos — schema e gravação

Lista SharePoint: `Fotos`. Locale Power Fx: `;` / `;;`.

## Problema que isso fecha

O tipo ia no `Title` (`AMBIENTE | guid` / `ITEM | guid`). Sobra gravava foto com `CodAsset` vazio e só `CodTemp`. Consulta quebrava: ou todas as sobras viam as mesmas fotos, ou as órfãs sumiam.

## Coluna nova — `TipoFoto`

Criar na lista **Fotos** (SharePoint):

| Campo | Tipo | Valores | Obrigatório |
|-------|------|---------|-------------|
| `TipoFoto` | Uma linha de texto | `AMBIENTE` ou `ITEM` | Sim |

- `AMBIENTE` = foto da SE (sem item).
- `ITEM` = foto de equipamento (base ou sobra física).

Uma linha de texto, não Choice — no Power Apps Choice vira `TipoFoto.Value` e quebra Filter.

`Title` deixa de ser a fonte do tipo. Pode continuar `TipoFoto | guid` só para leitura humana na lista.

## Chave única — `CodAsset`

Uma chave. Sempre. Item, foto, fila offline, consulta desktop.

| Quem | Valor |
|------|--------|
| Item da **base** | o `CodAsset` importado (`ASSET-…`, `BF…`, `BE…`) |
| **Sobra física** | gerado na hora do "Adicionar item": `SOBRA-{CodSE}-{nn}` |
| Foto `ITEM` | o mesmo `CodAsset` do item (`varCodRef`) |
| Foto `AMBIENTE` | `CodAsset` vazio (liga por `CodSE` + `TipoFoto`) |

**Padrão da sobra:** `SOBRA-{CodSE}-{nn}`, gerado **uma vez** em `varCodRef`, copiado para `CodAsset` em todo Collect/Patch. Ex.: `SOBRA-7SE06N00-01`. O `nn` é o próximo número daquela SE já conhecido no telefone (fila local e base baixada), com dois dígitos. Sobra antiga com GUID permanece como está.

O prefixo `SOBRA-` não colide com a base (`ASSET-…` / `BF…` / `BE…`) e o `StartsWith("SOBRA-")` já identifica sobra no restante do app. Item desmembrado não usa esse prefixo: a primeira parte fica com o `CodAsset` da base e as seguintes levam `{CodAsset}-P2`, `-P3`, `-P4`.

`CodTemp` **não é chave**. Não filtrar, não LookUp, não gravar valor novo. Coluna pode ficar vazia (schema antigo). Leitura de foto velha, se ainda existir linha só com `CodTemp`:

```
Coalesce(CodAsset; If(!IsBlank(CodTemp); "SOBRA-" & Text(CodTemp); ""))
```

`Inventario` **não tem** `CodTemp`. Não criar.

## Chaves na gravação (`Fotos`)

| Tipo | `TipoFoto` | `Fotos.CodAsset` | `Inventario.CodAsset` |
|------|------------|------------------|------------------------|
| SE | `AMBIENTE` | vazio | — |
| Equipamento base | `ITEM` | o do item | o mesmo |
| Sobra física | `ITEM` | `SOBRA-{CodSE}-{nn}` | o mesmo valor |

Sobra **nunca** grava `Fotos.CodAsset` vazio. `varCodRef` já nasce preenchido no "Adicionar item".

## Filtro canônico (consulta e captura)

```
Coalesce(
    TipoFoto;
    If(StartsWith(Coalesce(Title; ""); "AMBIENTE"); "AMBIENTE"; "ITEM")
)
```

- Fotos da SE: resultado `= "AMBIENTE"`
- Fotos do item: resultado `<> "AMBIENTE"` + `CodAsset` = chave do item (`varCodRef`)

O `Coalesce` cobre linha antiga sem a coluna preenchida.

## Backfill das 4 fotos de teste (SE-005)

| ID | `TipoFoto` | `CodAsset` |
|----|------------|------------|
| 5 | `ITEM` | `ASSET-PE-034` (já está) |
| 6 | `ITEM` | `SOBRA-1defd90f-4d93-4be2-a453-5440f3d838d9` |
| 7 | `AMBIENTE` | vazio |
| 8 | `ITEM` | `SOBRA-65c1f98d-8adc-4202-8401-2addf189248d` |

Conferir no **Inventario** se as sobras têm o mesmo `CodAsset` `SOBRA-` + guid. Se estiver vazio, preencher igual.

## Pastas na biblioteca (exportação)

A lista `Fotos` **não é** a árvore de pastas. JPG para o André vai na biblioteca **`Projetos`**: `{projeto}/{SE}/Visão geral` ou `{projeto}/{SE}/{Imobilizado ou CodAsset}`.

Criação: importar projeto → pasta raiz + SEs + `Visão geral`. Enviar visita → um `Run` de `flxPastaFotosVisita` (não o `ForAll` do app). `TipoFoto` continua `AMBIENTE` / `ITEM`.

Spec: `docs/exportacao-fotos-pastas.md`.  
Mockups: `docs/screens/pastas-fotos-apos-importar.png` · `pastas-fotos-apos-visita.png`.

## Coordenadas (05.10 / rede 09.10)

Na **subestação**, a coordenada é do local, não da foto e não de cada item.

- Colunas: `Subestacoes.CoordX` e `Subestacoes.CoordY` (texto).
- `CoordX` = longitude. `CoordY` = latitude. Seis casas, ponto decimal.
- Grava no botão **Coletar coordenada** do popup Local (`Tela_ItensVisita`). A foto não grava coordenada.
- A lista `Fotos` não recebe esses campos.
- Sem sinal, fica em `colSubestacoes` e sobe no envio da visita, nas SEs finalizadas.
- Na planilha, cada item da SE recebe o `CoordX` / `CoordY` dessa SE.

Na **rede**, a coordenada é do item. Colunas `Inventario.CoordX` e `Inventario.CoordY` (texto, criadas 09.10 no site AssetPro). Na subestação essas duas colunas do item ficam vazias.
