# Studio — Tela_Alocacoes · selecionar todas (18.09)

> Fenômeno. Locale PT-BR: `;` nos argumentos, `;;` nas instruções.
> Ata: `docs/reunioes/2026-09-18.md` (João, ~300 SEs).
> Tela já existe: `docs/powerfx/Tela_Alocacoes-formulas.txt`.
> Desktop: toast `cmpToast` (`varToastMsg` / `varToastTipo` / `varToastOn`). Sem `Notify`.
> Um controle = um passo. Apaga o que estiver na propriedade e cola o bloco.

Na tela: **Selecionar todas** marca só as livres do projeto. **Designar N instalações** grava. Ocupada (outro slot) não entra.
Studio real (YAML 20.09): `cSelecionarTodas` = `btnAloSelTodas` + `Image6_close_sharp_6` (Limpar) + `Image6_add_sharp_1` (Designar). Mundo Power: só o primeiro `With`.

---

## 1. `Tela_Alocacoes` → `OnVisible`

Apaga o que estiver lá. Cola:

```
Refresh(Alocacoes);;
If(
    IsBlank(varAloCamp);
    Set(varAloCamp; First(SortByColumns(colCampanhas; "NomeInventario"; SortOrder.Ascending)))
);;
Set(varCarregando; false);;
ClearCollect(
    colAloSEsSel;
    {CodSE: ""; NomeSE: ""; CodInventario: ""}
);;
Clear(colAloSEsSel)
```

## 2. `galAloProjetos` → `OnSelect`

Apaga o que estiver lá. Cola:

```
Set(varAloCamp; ThisItem);;
Clear(colAloSEsSel)
```

## 3. `galAloSEs` → template do card → `OnSelect`

# Clique no card (não no `btnAloAdd`) alterna a seleção. SE já alocada: não faz nada.

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

## 4. `galAloSEs` → `TemplateFill`

Apaga o que estiver lá. Cola:

```
With(
    {
        a: LookUp(
            Alocacoes;
            CodInventario = ThisItem.CodInventario
                && CodSE = ThisItem.CodSE
                && Ativo = "Sim"
        );
        sel: !IsBlank(LookUp(colAloSEsSel; CodSE = ThisItem.CodSE))
    };
    If(
        sel;
        Cor.PrimaryL90;
        IsBlank(a);
        Cor.BackgroundStandard;
        a.Login = varUsrSel.Login;
        Cor.PrimaryL90;
        ColorFade(Cor.Delete; 90%)
    )
)
```

## 5. Inserir botão → `btnAloSelTodas`

# Cabeçalho da coluna de SEs (`cAloSE` / ao lado de `lblAloSECab`).
# Height 36 · Radius 8 · Fill `Cor.BackgroundStandard` · Color `Cor.PrimaryD30` · BorderColor `Cor.Primary`.

## 6. `btnAloSelTodas` → `Text`

Apaga o que estiver lá. Cola:

```
With(
    {
        n: CountRows(
            Filter(
                AddColumns(
                    Filter(colSubestacoes; CodInventario = varAloCamp.CodInventario) As se;
                    Ocupada;
                    !IsBlank(
                        LookUp(
                            Alocacoes;
                            CodInventario = se.CodInventario
                                && CodSE = se.CodSE
                                && Ativo = "Sim"
                        )
                    )
                );
                !Ocupada
            )
        )
    };
    If(n = 0; "Todas designadas"; "Selecionar todas (" & n & ")")
)
```

## 7. `btnAloSelTodas` → `OnSelect`

Apaga o que estiver lá. Cola:

```
Clear(colAloSEsSel);;
ForAll(
    Filter(
        AddColumns(
            Filter(colSubestacoes; CodInventario = varAloCamp.CodInventario) As se;
            Ocupada;
            !IsBlank(
                LookUp(
                    Alocacoes;
                    CodInventario = se.CodInventario
                        && CodSE = se.CodSE
                        && Ativo = "Sim"
                )
            )
        );
        !Ocupada
    ) As livre;
    Collect(
        colAloSEsSel;
        {
            CodSE: livre.CodSE;
            NomeSE: livre.NomeSE;
            CodInventario: livre.CodInventario
        }
    )
);;
If(
    CountRows(colAloSEsSel) = 0;
    Set(varToastMsg; "Não há instalação livre neste projeto.");;
    Set(varToastTipo; "AVISO");;
    Set(varToastOn; false);;
    Set(varToastOn; true)
)
```

## 8. `btnAloSelTodas` → `DisplayMode`

Apaga o que estiver lá. Cola:

```
If(
    !IsBlank(varAloCamp) && !IsBlank(varUsrSel);
    DisplayMode.Edit;
    DisplayMode.Disabled
)
```

## 9. Inserir botão → `btnAloLimparSel`

# Ao lado do Selecionar todas. Height 36 · Radius 8 · Fill `Cor.NeutralL90` · Color `Cor.NeutralL30`.

## 10. `btnAloLimparSel` → `Text`

Apaga o que estiver lá. Cola:

```
"Limpar"
```

## 11. `btnAloLimparSel` → `Visible`

Apaga o que estiver lá. Cola:

```
CountRows(colAloSEsSel) > 0
```

## 12. `btnAloLimparSel` → `OnSelect`

Apaga o que estiver lá. Cola:

```
Clear(colAloSEsSel)
```

## 13. Inserir botão → `btnAloDesignarVarias`

# Mesmo cabeçalho, à direita. Height 36 · Radius 8 · Fill `Cor.PrimaryD30` · Color `Cor.TextInverted`.

## 14. `btnAloDesignarVarias` → `Visible`

Apaga o que estiver lá. Cola:

```
CountRows(colAloSEsSel) > 0
```

## 15. `btnAloDesignarVarias` → `Text`

Apaga o que estiver lá. Cola:

```
"Designar "
    & CountRows(colAloSEsSel)
    & If(CountRows(colAloSEsSel) = 1; " instalação"; " instalações")
```

## 16. `btnAloDesignarVarias` → `OnSelect`

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
    With(
        {ok: true};
        Set(varCarregando; true);;
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
        Set(varCarregando; false);;
        Set(varToastMsg; "Instalações designadas. O campo precisa entrar de novo.");;
        Set(varToastTipo; "OK");;
        Set(varToastOn; false);;
        Set(varToastOn; true)
    )
)
```

## 17. `btnAloAdd` → `OnSelect`

# No **fim**, depois do toast de uma SE, cola o bump (o tablet reloga):

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
);;
Set(varToastMsg; "Instalação designada. O campo precisa entrar de novo.");;
Set(varToastTipo; "OK");;
Set(varToastOn; false);;
Set(varToastOn; true)
```

# Se o OnSelect atual já tem o toast "Instalação designada.", **troca** essa mensagem pela de cima. Não duplica o toast.

## 18. `lblAloSECabSub` → `Text`

Apaga o que estiver lá. Cola:

```
Coalesce(varAloCamp.NomeInventario; "")
    & If(
        CountRows(colAloSEsSel) = 0;
        "";
        " · " & CountRows(colAloSEsSel) & " selecionadas"
    )
```

## 19. `lblAloVazioSub` → `Text`

Apaga o que estiver lá. Cola:

```
"Selecionar todas ou clica Adicionar em cada uma."
```

## 20. Inserir retângulo → `recAloLoad`

# Por cima de `cAloBody`. X/Y 0 · Width/Height = Parent. Fill `ColorFade(Black; 40%)`.

## 21. `recAloLoad` → `Visible`

Apaga o que estiver lá. Cola:

```
varCarregando
```

## 22. Inserir rótulo → `lblAloLoad`

# Centro do `recAloLoad`. Color `Cor.TextInverted`. Size 16.

## 23. `lblAloLoad` → `Text`

Apaga o que estiver lá. Cola:

```
"Designando instalações…"
```

## 24. `lblAloLoad` → `Visible`

Apaga o que estiver lá. Cola:

```
varCarregando
```

---

Na tela: escolhe o slot → projeto → **Selecionar todas (N)** pinta as livres de azul → **Designar N instalações**. Já ocupada por outro slot fica vermelha e fora da conta. 300 SEs: o `ForAll` + `Patch` demora; o overlay cobre. O campo só vê as SEs novas depois de entrar de novo (`SessaoVersao`).

