# Studio — Tela_ItensVisita (reunião 18.09)

> Locale PT-BR: `;` nos argumentos, `;;` nas instruções.
> Ata: `docs/reunioes/2026-09-18.md`.
> Um controle = um passo. Apaga o que estiver na propriedade e cola o bloco.
>
> Este pacote: **card sem nome da SE** + filtro **Falta**. **IdUC** no card (coluna já no SP, 20.09). Sem sequencial.

Na tela: card mostra Imobilizado · TUC.A1 · descrição (sem “— SE Asa Sul…”). Terceira aba **Falta (N)** lista só o que ainda não salvou.

---

## A. Card — some o nome da SE

### A1. galItensBase → Text18 → Text

Apaga o que estiver lá. Cola:

```
With(
    {
        imob: Coalesce(Text(ThisItem.Imobilizado); "—");
        iduc: Trim(
            Coalesce(
                ThisItem.RegistroCampo.IdUC;
                ThisItem.IdUC;
                ""
            )
        );
        prefixo: ThisItem.CodTUC & "." & Text(Coalesce(ThisItem.AtributoA1; ThisItem.A1); "00") & " - ";
        descBruta: Trim(
            Coalesce(
                ThisItem.RegistroCampo.DescricaoBem;
                ThisItem.DescricaoBem;
                ""
            )
        );
        corte: " — " & Coalesce(gblSEselecionada.NomeSE; "")
    };
    With(
        {
            desc: If(
                !IsBlank(corte)
                    && corte <> " — "
                    && !IsBlank(Find(corte; descBruta));
                Trim(
                    Left(
                        descBruta;
                        Find(corte; descBruta) - 1
                    )
                );
                descBruta
            )
        };
        imob
            & " · "
            & If(
                StartsWith(desc; Trim(Text(ThisItem.CodTUC)) & ".");
                desc;
                prefixo & desc
            )
            & If(IsBlank(iduc); ""; " · " & iduc)
    )
)
```

# Imobilizado na frente. Corta o sufixo ` — {NomeSE}` se a base veio com ele. IdUC entra depois.

### A2. galItensSobras → Text18_1 → Text

Apaga o que estiver lá. Cola o **mesmo** bloco do passo A1.

---

## B. Filtro “Falta” (não inventariados)

# Bruno: SE grande (~300) o técnico se perde. Terceira aba ao lado de BASE / SOBRAS.
# `varAbaItens`: `"BASE"` | `"FALTA"` | `"SOBRAS"`.

### B1. Tela_ItensVisita → OnVisible

Cola **no começo** (antes do ForAll das sobras):

```
If(
    IsBlank(varAbaItens);
    Set(varAbaItens; "BASE")
);;
```

### B2. Button3_4 → OnSelect

Apaga o que estiver lá. Cola:

```
Set(varAbaItens; "BASE")
```

### B3. Button3_4 → Fill

Apaga o que estiver lá. Cola:

```
If(varAbaItens = "BASE"; Cor.PrimaryL90; Cor.BackgroundStandard)
```

### B4. Button3_4 → Color

Apaga o que estiver lá. Cola:

```
If(varAbaItens = "BASE"; Cor.PrimaryD30; Cor.NeutralL30)
```

### B5. Button3_5 → OnSelect

Apaga o que estiver lá. Cola:

```
Set(varAbaItens; "SOBRAS")
```

### B6. Button3_5 → Fill

Apaga o que estiver lá. Cola:

```
If(varAbaItens = "SOBRAS"; Cor.PrimaryL90; Cor.BackgroundStandard)
```

### B7. Button3_5 → Color

Apaga o que estiver lá. Cola:

```
If(varAbaItens = "SOBRAS"; Cor.PrimaryD30; Cor.NeutralL30)
```

### B8. Tela_ItensVisita → duplicar Button3_4 → btnFiltroFalta

# Cola ao lado de SOBRAS, **antes** do `btnAddItem`. Mesma altura. Text / Fill / Color / OnSelect abaixo. Sem Icon.

### B9. btnFiltroFalta → OnSelect

Apaga o que estiver lá. Cola:

```
Set(varAbaItens; "FALTA")
```

### B10. btnFiltroFalta → Text

Apaga o que estiver lá. Cola:

```
"Falta ("
    & CountRows(
        Filter(
            Filter(
                colInventarioBase;
                CodSE = gblSEselecionada.CodSE
                && Coalesce(Origem; "") <> "CAMPO"
                && Coalesce(Sobra; "") <> "SOBRA_FISICA"
                && !StartsWith(Coalesce(Text(CodAsset); ""); "SOBRA-")
            ) As itemBase;
            IsBlank(
                LookUp(
                    colCampoOffline;
                    CodSE = gblSEselecionada.CodSE
                    && CodAsset = itemBase.CodAsset
                    && CodInventario = gblInventarioSelecionado.CodInventario
                )
            )
        )
    )
    & ")"
```

### B11. btnFiltroFalta → Fill

Apaga o que estiver lá. Cola:

```
If(varAbaItens = "FALTA"; Cor.PrimaryL90; Cor.BackgroundStandard)
```

### B12. btnFiltroFalta → Color

Apaga o que estiver lá. Cola:

```
If(varAbaItens = "FALTA"; Cor.PrimaryD30; Cor.NeutralL30)
```

### B13. btnFiltroFalta → BorderColor

Apaga o que estiver lá. Cola:

```
If(varAbaItens = "FALTA"; Cor.Primary; Cor.Border)
```

### B14. galItensBase → Visible

Apaga o que estiver lá. Cola:

```
varAbaItens <> "SOBRAS"
```

### B15. galItensSobras → Visible

Apaga o que estiver lá. Cola:

```
varAbaItens = "SOBRAS"
```

### B16. galItensBase → Items

Apaga o que estiver lá. Cola:

```
Filter(
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
                || inpBuscaItens.Text in Coalesce(IdUC; "")
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
    );
    varAbaItens <> "FALTA" || IsBlank(RegistroCampo)
)
```

# BASE = todos. FALTA = sem rascunho em `colCampoOffline`. `As itemBase` continua obrigatório.

---

Na tela: três chips (Base / Falta / Sobras). Falta mostra só o que ainda não salvou. Card sem o nome da SE. IdUC e ordem da planilha ficam pro próximo.
