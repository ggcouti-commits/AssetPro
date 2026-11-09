# Studio — reunião 17.09.2026

> Locale PT-BR: `;` nos argumentos, `;;` nas instruções.
> Ata: `docs/reunioes/2026-09-17.md`.
> Um controle = um passo. Apaga o que estiver na propriedade e cola o bloco.

---

## A. SharePoint (uma vez)

### A1. Lista `Inventario` → coluna `QuantidadeCampo`

Tipo **Número**. Sem obrigatoriedade. Studio → Dados → `Inventario` → Atualizar.

# Quantidade da base não muda. Campo (visita) grava aqui. Não encontrado = 0.

### A2. Lista `Inventariantes` → coluna `SessaoVersao`

Número. Se já existe, pula.

---

## B. Tela_ItensVisita — galeria

### B1. galItensBase → btnConfirmarBase → Visible

Apaga o que estiver lá. Cola:

```
false
```

### B2. galItensBase → btnNaoEncontradoBase → Visible

Apaga o que estiver lá. Cola:

```
false
```

# Desfecho só na Tela_EditarItem. Chip Button3_16 (desfazer) pode ficar.

### B3. Tela_ItensVisita → inserir Texto moderno → inpBuscaItens

# Acima da galeria BASE (e da SOBRAS, o mesmo campo serve nas duas).
# HintText = "Buscar item". DelayOutput = true. Width = Parent.Width.

### B4. inpBuscaItens → OnChange

Apaga o que estiver lá. Cola:

```
true
```

# Só pra galeria recalcular. Sem Set.

### B5. galItensBase → Items

Apaga o que estiver lá. Cola:

```
AddColumns(
    Filter(
        colInventarioBase;
        CodSE = gblSEselecionada.CodSE
        && Coalesce(Origem; "") <> "CAMPO"
        && Coalesce(Sobra; "") <> "SOBRA_FISICA"
        && !StartsWith(Coalesce(Text(CodAsset); ""); "SOBRA-")
        && (
            IsBlank(Trim(inpBuscaItens.Text))
            || inpBuscaItens.Text in Coalesce(DescricaoBem; "")
            || inpBuscaItens.Text in Text(Coalesce(CodTUC; ""))
            || inpBuscaItens.Text in Coalesce(Imobilizado; "")
            || inpBuscaItens.Text in Coalesce(CodAsset; "")
        )
    ) As itemBase;
    RegistroCampo;
    LookUp(
        colCampoOffline;
        CodSE = gblSEselecionada.CodSE
        && CodAsset = itemBase.CodAsset
        && CodInventario = gblInventarioSelecionado.CodInventario
    )
)
```

# Sem o `As itemBase`, `CodAsset = CodAsset` é sempre verdade — Salvar pinta todos Confirmado.

### B6. galItensSobras → Items

# Se a galeria de sobras também busca, envolve o Filter atual com o mesmo `in` em DescricaoBem / CodTUC / CodAsset. Se o Items atual já filtra `SobraTipo = "SOBRA_FISICA"`, só acrescenta o bloco da busca.

### B7. galItensBase → Text18 → Text

Apaga o que estiver lá. Cola:

```
With(
    {
        imob: Coalesce(Text(ThisItem.Imobilizado); "—");
        prefixo: ThisItem.CodTUC & "." & Text(Coalesce(ThisItem.AtributoA1; ThisItem.A1); "00") & " - ";
        desc: Trim(
            Coalesce(
                ThisItem.RegistroCampo.DescricaoBem;
                ThisItem.DescricaoBem;
                ""
            )
        )
    };
    imob
        & " · "
        & If(
            StartsWith(desc; Trim(Text(ThisItem.CodTUC)) & ".");
            desc;
            prefixo & desc
        )
)
```

# Imobilizado na frente da TUC. Descrição vem do rascunho se já salvou.

---

## C. Tela_EditarItem — não encontrado = 0 · reserva · Salvar

### C1. Tela_EditarItem → OnVisible (depois do Set varDesfecho)

Cola no fim do bloco de vars técnicas (junto com varFabricante…):

```
Set(
    varReserva;
    Upper(
        Coalesce(
            varRegistroAtual.Reserva;
            varItemFoto.Reserva;
            "NÃO"
        )
    ) = "SIM"
);;
If(
    varDesfecho = "NAO_ENCONTRADO";
    Set(varQuantidade; 0)
)
```

### C2. Controle do desfecho Não encontrado → OnSelect

# O botão / chip da ficha que seta `varDesfecho`. Nome na árvore: confirma o teu. Cola o Set da quantidade **no fim** do OnSelect que já existe.

Cola no fim:

```
Set(varDesfecho; "NAO_ENCONTRADO");;
Set(varQuantidade; 0);;
Reset(inpQuantidade)
```

### C3. Controle do desfecho Confirmar → OnSelect

Cola no fim:

```
Set(varDesfecho; "CONFIRMACAO");;
Set(
    varQuantidade;
    Coalesce(varRegistroAtual.Quantidade; varItemFoto.Quantidade; 1)
);;
Reset(inpQuantidade)
```

### C4. inpQuantidade → Default

Apaga o que estiver lá. Cola:

```
If(
    varDesfecho = "NAO_ENCONTRADO";
    0;
    Coalesce(varQuantidade; varItemFoto.Quantidade)
)
```

### C5. inpQuantidade → DisplayMode

Apaga o que estiver lá. Cola:

```
If(
    varDesfecho = "NAO_ENCONTRADO";
    DisplayMode.View;
    DisplayMode.Edit
)
```

### C6. Card Reserva

# Duplica `cCardAno`. Renomeia `cCardReserva`. Apaga o input de ano. Insere Toggle → `tglReserva`.
# Label do card = `"RESERVA"`. Posição: depois de Imobilizado, antes de Observações.

### C7. tglReserva → Default

Apaga o que estiver lá. Cola:

```
varReserva
```

### C8. tglReserva → OnCheck

Apaga o que estiver lá. Cola:

```
Set(varReserva; true)
```

### C9. tglReserva → OnUncheck

Apaga o que estiver lá. Cola:

```
Set(varReserva; false)
```

### C10. tglReserva → FalseText / TrueText

```
"Não"
```

```
"Sim"
```

### C11. Botão Salvar → OnSelect

Apaga o que estiver lá. Cola o bloco inteiro:

```
If(
    IsBlank(varModo);
    Set(varModo; If(IsBlank(varCodRef); "NOVO"; "EDITAR"))
);;
If(varModo <> "NOVO"; Set(varCodTemp; Blank()));;

RemoveIf(
    colCampoOffline;
    CodInventario = gblInventarioSelecionado.CodInventario
    && !IsBlank(varCodRef)
    && CodAsset = varCodRef
);;

Collect(
    colCampoOffline;
    {
        IdRegistro: If(IsBlank(varRegistroAtual.IdRegistro); GUID(); varRegistroAtual.IdRegistro);
        TipoRegistro: If(varModo = "NOVO"; "SOBRA_FISICA"; varDesfecho);
        CodInventario: gblInventarioSelecionado.CodInventario;
        CodSE: Coalesce(varCodSE; gblSEselecionada.CodSE);
        NomeSE: Coalesce(varItemFoto.NomeSE; gblSEselecionada.NomeSE);
        CodAsset: Coalesce(varCodRef; "");
        CodTemp: "";
        CodTUC: varTUCSelecionado;
        AtributoA1: varA1;
        AtributoA2: varA2;
        AtributoA3: varA3;
        AtributoA4: varA4;
        AtributoA5: varA5;
        AtributoA6: varA6;
        ValorA2: If(Upper(Trim(varTipoA2)) = "FAIXA"; Coalesce(varValorA2; inpA2Faixa.Text; ""); If(Upper(Trim(varTipoA2)) = "LIVRE"; Coalesce(inpA2Livre.Text; varValorA2; ""); ""));
        ValorA3: If(Upper(Trim(varTipoA3)) = "FAIXA"; Coalesce(varValorA3; inpA3Faixa.Text; ""); If(Upper(Trim(varTipoA3)) = "LIVRE"; Coalesce(inpA3Livre.Text; varValorA3; ""); ""));
        ValorA4: If(Upper(Trim(varTipoA4)) = "FAIXA"; Coalesce(varValorA4; inpA4Faixa.Text; ""); If(Upper(Trim(varTipoA4)) = "LIVRE"; Coalesce(inpA4Livre.Text; varValorA4; ""); ""));
        ValorA5: If(Upper(Trim(varTipoA5)) = "FAIXA"; Coalesce(varValorA5; inpA5Faixa.Text; ""); If(Upper(Trim(varTipoA5)) = "LIVRE"; Coalesce(inpA5Livre.Text; varValorA5; ""); ""));
        ValorA6: If(Upper(Trim(varTipoA6)) = "FAIXA"; Coalesce(varValorA6; inpA6Faixa.Text; ""); If(Upper(Trim(varTipoA6)) = "LIVRE"; Coalesce(inpA6Livre.Text; varValorA6; ""); ""));
        DescricaoBem: With(
            {
                prefixo: Trim(
                    Coalesce(Text(varTUCSelecionado); "")
                    & If(IsBlank(varA1); ""; "." & Text(varA1; "00"))
                ) & " - ";
                texto: Trim(Coalesce(varDescSelecionada; ""))
            };
            If(
                StartsWith(texto; prefixo);
                Mid(texto; Len(prefixo) + 1; Len(texto));
                texto
            )
        );
        Quantidade: If(
            varDesfecho = "NAO_ENCONTRADO";
            0;
            Coalesce(varQuantidade; varItemFoto.Quantidade; 1)
        );
        Reserva: If(varReserva; "SIM"; "NÃO");
        Fabricante: Coalesce(varFabricante; "");
        Modelo: Coalesce(varModelo; "");
        NumSerie: Coalesce(varNumSerie; "");
        CodOperacao: Coalesce(varCodOperacao; "");
        CM: varCM;
        Ano: varAno;
        Unidade: Coalesce(varUnidadeItem; "");
        Observacoes: Coalesce(varObservacoes; "");
        SobraTipo: If(varModo = "NOVO"; "SOBRA_FISICA"; "");
        Sincronizada: false;
        IdInventario: Coalesce(varRegistroAtual.IdInventario; varItemFoto.ID; varItemFoto.IdInventario; 0)
    }
);;

If(
    varModo <> "NOVO" && !IsBlank(varCodRef);
    UpdateIf(
        colInventarioBase;
        CodAsset = varCodRef
        && CodInventario = gblInventarioSelecionado.CodInventario;
        {
            DescricaoBem: LookUp(colCampoOffline; CodAsset = varCodRef).DescricaoBem;
            Reserva: If(varReserva; "SIM"; "NÃO")
        }
    );;
    IfError(SaveData(colInventarioBase; "cache_InventarioBase"); Blank())
);;

IfError(SaveData(colCampoOffline; "cache_CampoOffline"); Blank());;
Back()
```

# Salvar é só coleção + SaveData. Sem Patch no SharePoint — visita offline quebra.
# O `UpdateIf` é o que faz a galeria mostrar a descrição nova sem esperar o envio.

### C12. App.OnStart — schema Inventario inteiro

# Dummy canonico: docs/powerfx/schema-inventario.txt
# Apaga os ClearCollect de colCampoOffline / colInventarioBase e o Collect({CM:0}).
# Cola os passos 1, 2 e 3 desse arquivo (ClearCollect + forcar DEPOIS do LoadData).

---

## D. Tela_Home (Mobile) — enviar visita

### D1. Patch CONFIRMACAO (dentro do ForAll do btnEnviarVisitaExec)

No objeto do `Patch(Inventario; …)` do bloco `TipoRegistro = "CONFIRMACAO"`, **apaga** `Quantidade:`. A base não entra nesse Patch. O achado vai em `QtdeContado` (coluna que existe na lista; `QuantidadeCampo` não está no conector):

```
QtdeContado: linhaAtual.Quantidade;
Reserva: linhaAtual.Reserva
```

# Se `Quantidade:` continuar no Patch da confirmação, a base vira quantidade de campo. Desmembrado é a exceção: um segundo Patch grava a quantidade da parte.

### D2. Patch NAO_ENCONTRADO — acrescenta no objeto. Não inclui `Quantidade`.

```
QtdeContado: 0;
Reserva: linhaAtual.Reserva
```

### D3. Fim do btnEnviarVisitaExec — **antes** do Notify de sucesso

Cola depois do `SaveData` das filas, **antes** do `Notify("Alterações enviadas…")`. Mobile usa Notify; Desktop usa cmpToast.

```
With(
    {
        cod: gblInventarioSelecionado.CodInventario
    };
    Patch(
        'Campanhas ';
        LookUp('Campanhas '; CodInventario = cod);
        {Status: "Em andamento"}
    );;
    UpdateIf(
        colCampanhas;
        CodInventario = cod;
        {Status: "Em andamento"}
    );;
    IfError(SaveData(colCampanhas; "cache_Campanhas"); Blank())
);;
```

# Concluído não sai daqui. Só o Desktop, no Finalizar projeto, e só se nenhuma SE estiver aberta.

# Nome da lista no Studio: se for `Campanhas` sem espaço, tira o espaço. Confere no conector.

---

## E. Mobile só vê o designado

Spec completo (inventariante recorta; escritório vê tudo): `docs/powerfx/mobile-filtro-alocacao.txt`

Cola os 8 passos de lá. Não filtres a galeria só com `CodInventario in colAlocacoes` — apaga busca/status e trava o escritório.

---

## F. Tela_Alocacoes — várias SEs + bump de sessão

# Bloco BumpSessao (cola no FIM de cada OnSelect desta seção, menos Cancelar):

```
If(
    !IsBlank(varUsrSel.ID);
    Patch(
        Inventariantes;
        LookUp(Inventariantes; ID = varUsrSel.ID);
        {
            SessaoVersao:
                Coalesce(
                    LookUp(Inventariantes; ID = varUsrSel.ID).SessaoVersao;
                    0
                ) + 1
        }
    );;
    Set(varUsrSel; LookUp(Inventariantes; ID = varUsrSel.ID))
)
```

### F1. Tela_Alocacoes → OnVisible

No fim do que já existe, cola:

```
Clear(colAloSEsSel)
```

### F2. galAloProjetos → OnSelect

No fim (depois de setar `varAloCamp`), cola:

```
Clear(colAloSEsSel)
```

### F3. galAloSEs → template → OnSelect do card (ou do checkbox)

# Se ainda não tem checkbox: o clique no card alterna a seleção. Só SE livre (sem alocação ativa).

Apaga o que estiver lá. Cola:

```
With(
    {
        a: LookUp(
            Alocacoes;
            CodInventario = ThisItem.CodInventario
                && CodSE = ThisItem.CodSE
                && Ativo = "Sim"
        )
    };
    If(
        !IsBlank(a);
        false;
        If(
            !IsBlank(LookUp(colAloSEsSel; CodSE = ThisItem.CodSE));
            RemoveIf(colAloSEsSel; CodSE = ThisItem.CodSE);
            Collect(
                colAloSEsSel;
                {
                    CodSE: ThisItem.CodSE;
                    NomeSE: ThisItem.NomeSE;
                    CodInventario: ThisItem.CodInventario
                }
            )
        )
    )
)
```

### F4. Fundo do card (Fill do template ou de um retângulo)

# Marca visual da seleção.

```
If(
    !IsBlank(LookUp(colAloSEsSel; CodSE = ThisItem.CodSE));
    Cor.PrimaryL90;
    Cor.BackgroundStandard
)
```

### F5. Inserir botão → btnAloDesignarVarias

# No cabeçalho da coluna de SEs. Text = "Designar selecionadas".
# Fill = Cor.PrimaryD30. Color = Cor.TextInverted. Height 36. Radius 8.

### F6. btnAloDesignarVarias → Visible

Apaga o que estiver lá. Cola:

```
CountRows(colAloSEsSel) > 0
```

### F7. btnAloDesignarVarias → Text

Apaga o que estiver lá. Cola:

```
"Designar " & CountRows(colAloSEsSel) & If(CountRows(colAloSEsSel) = 1; " instalação"; " instalações")
```

### F8. btnAloDesignarVarias → OnSelect

Apaga o que estiver lá. Cola:

```
If(
    IsBlank(varUsrSel);
    With(
        {_: true};
        Set(varToastMsg; "Volte e escolha um slot.");;
        Set(varToastTipo; "AVISO");;
        Set(varToastOn; false);;
        Set(varToastOn; true)
    );
    ForAll(
        colAloSEsSel As sel;
        If(
            IsBlank(
                LookUp(
                    Alocacoes;
                    CodInventario = sel.CodInventario
                        && CodSE = sel.CodSE
                        && Ativo = "Sim"
                )
            );
            Patch(
                Alocacoes;
                Defaults(Alocacoes);
                {
                    Title: varUsrSel.Login & "-" & sel.CodSE;
                    Login: varUsrSel.Login;
                    CodUsuario: varUsrSel.CodUsuario;
                    UsadoPor: varUsrSel.UsadoPor;
                    CodInventario: sel.CodInventario;
                    NomeInventario: varAloCamp.NomeInventario;
                    CodSE: sel.CodSE;
                    NomeSE: sel.NomeSE;
                    Ativo: "Sim"
                }
            )
        )
    );;
    Clear(colAloSEsSel);;
    Refresh(Alocacoes);;
    If(
        !IsBlank(varUsrSel.ID);
        Patch(
            Inventariantes;
            LookUp(Inventariantes; ID = varUsrSel.ID);
            {
                SessaoVersao:
                    Coalesce(
                        LookUp(Inventariantes; ID = varUsrSel.ID).SessaoVersao;
                        0
                    ) + 1
            }
        );;
        Set(varUsrSel; LookUp(Inventariantes; ID = varUsrSel.ID))
    );;
    Set(varToastMsg; "Instalações designadas. O campo precisa entrar de novo.");;
    Set(varToastTipo; "OK");;
    Set(varToastOn; false);;
    Set(varToastOn; true)
)
```

### F9. btnAloAdd → OnSelect

Cola o bloco BumpSessao **no fim** (depois do toast "Instalação designada"). Troca a msg do toast para:

```
Set(varToastMsg; "Instalação designada. O campo precisa entrar de novo.")
```

### F10. btnAloRemover → OnSelect

Apaga o que estiver lá. Cola:

```
Patch(
    Alocacoes;
    ThisItem;
    {Ativo: "Nao"}
);;
Refresh(Alocacoes);;
If(
    !IsBlank(varUsrSel.ID);
    Patch(
        Inventariantes;
        LookUp(Inventariantes; ID = varUsrSel.ID);
        {
            SessaoVersao:
                Coalesce(
                    LookUp(Inventariantes; ID = varUsrSel.ID).SessaoVersao;
                    0
                ) + 1
        }
    );;
    Set(varUsrSel; LookUp(Inventariantes; ID = varUsrSel.ID))
)
```

# `btnUsrSalvar` já incrementa. `btnUsrExcluirConfirmar` apaga a linha — o timer do mobile cai no LookUp vazio.

---

## Conferência

| Na tela | O que tem que acontecer |
|---------|-------------------------|
| Galeria BASE | Sem Confirmar / Não encontrado. Imobilizado · TUC. Busca filtra. |
| Salvar 1 item | Só aquele card fica Confirmado / Não encontrado. |
| Mudar descrição e voltar | Título da galeria já mudou. Desktop continua ok. |
| Não encontrado | Quantidade trava em 0. Envio grava `QuantidadeCampo = 0`. Base intacta. |
| Toggle Reserva | Vai `SIM`/`NÃO` no rascunho e no Patch. |
| Login do Ricardo | Só projetos/SEs dele. |
| Designar 4 SEs | Um clique. Tablet pede login de novo (com internet, até 15 s). |
| Enviar 1ª SE | Card do projeto no desktop = Em andamento. Concluído só no Finalizar projeto do Desktop, com todas as SEs finalizadas. |
