/**
 * Office Script — PreencherExportacao
 * Excel Online no modelo-exportacao.xlsx → Automatizar → Novo script.
 * Parâmetros no Automate: jsonItens, jsonSEs (os dois string).
 *
 * Cabeçalhos da tblItens = chaves do JSON (A1…A6, não AtributoA1).
 */
function main(
    workbook: ExcelScript.Workbook,
    jsonItens: string,
    jsonSEs: string
) {
    type Linha = Record<string, unknown>;

    const itens = asArray(jsonItens);
    const ses = asArray(jsonSEs);
    const nomePorSE: Record<string, string> = {};
    const xPorSE: Record<string, string> = {};
    const yPorSE: Record<string, string> = {};
    for (const se of ses) {
        const cod = texto(se["CodSE"]);
        if (cod !== "") {
            nomePorSE[cod] = texto(se["NomeSE"]);
            xPorSE[cod] = texto(se["CoordX"]);
            yPorSE[cod] = texto(se["CoordY"]);
        }
    }

    const tabela = workbook.getTable("tblItens");
    tabela.setPredefinedTableStyle("TableStyleLight1");
    const n = tabela.getRowCount();
    if (n > 0) {
        tabela.deleteRowsAt(0, n);
    }

    garantirColuna(tabela, "CoordX");
    garantirColuna(tabela, "CoordY");
    forcarTexto(tabela, "CoordX");
    forcarTexto(tabela, "CoordY");

    const headers = tabela.getHeaderRowRange().getValues()[0] as string[];
    const linhas = itens.map((item) => {
        const codSE = texto(ler(item, "CodSE"));
        return headers.map((h) => {
            const chave = String(h).trim();
            if (chave === "NomeSE") {
                return (
                    texto(ler(item, "NomeSE")) || nomePorSE[codSE] || ""
                );
            }
            if (chave === "CoordX") {
                if (ehRede(codSE)) {
                    return comoTexto(texto(ler(item, "CoordXItem", "CoordX")));
                }
                return comoTexto(xPorSE[codSE] || "");
            }
            if (chave === "CoordY") {
                if (ehRede(codSE)) {
                    return comoTexto(texto(ler(item, "CoordYItem", "CoordY")));
                }
                return comoTexto(yPorSE[codSE] || "");
            }
            if (chave === "A1" || chave === "A2" || chave === "A3"
                || chave === "A4" || chave === "A5" || chave === "A6") {
                return atr(ler(item, chave, "Atributo" + chave));
            }
            if (chave === "CodTUC") {
                return texto(ler(item, "CodTUC", "TUC"));
            }
            if (chave === "Sobra") {
                return texto(ler(item, "Sobra"));
            }
            if (chave === "Observacoes") {
                return texto(ler(item, "Observacoes", "Observacao"));
            }
            return texto(ler(item, chave));
        });
    });

    if (linhas.length > 0) {
        tabela.addRows(-1, linhas);
        const corpo = tabela.getRangeBetweenHeaderAndTotal();
        const fmt = corpo.getFormat();
        fmt.getFill().clear();
        fmt.getFont().setColor("000000");
        fmt.getFont().setBold(false);
        fmt.setHorizontalAlignment(ExcelScript.HorizontalAlignment.left);
        fmt.setVerticalAlignment(ExcelScript.VerticalAlignment.center);

        const iDesc = headers.indexOf("DescricaoBem");
        if (iDesc >= 0) {
            corpo.getColumn(iDesc).getFormat().setHorizontalAlignment(
                ExcelScript.HorizontalAlignment.left
            );
            corpo.getColumn(iDesc).getFormat().setWrapText(true);
        }
    }
}

function ehRede(codSE: string): boolean {
    return codSE.indexOf("REDE-") === 0;
}

function forcarTexto(tabela: ExcelScript.Table, nome: string) {
    tabela.getColumnByName(nome).getRange().setNumberFormat("@");
}

function comoTexto(valor: string): string {
    if (valor === "") {
        return "";
    }
    return "'" + valor;
}

function garantirColuna(tabela: ExcelScript.Table, nome: string) {
    const headers = tabela.getHeaderRowRange().getValues()[0] as string[];
    const tem = headers.some((h) => String(h).trim() === nome);
    if (!tem) {
        const coluna = tabela.addColumn();
        coluna.setName(nome);
    }
}

function asArray(raw: string): Record<string, unknown>[] {
    if (raw == null || raw === "undefined" || String(raw).trim() === "") {
        return [];
    }
    const parsed = JSON.parse(raw) as unknown;
    if (Array.isArray(parsed)) {
        return parsed as Record<string, unknown>[];
    }
    if (parsed && typeof parsed === "object") {
        const o = parsed as Record<string, unknown>;
        if (Array.isArray(o.body)) {
            return o.body as Record<string, unknown>[];
        }
        if (Array.isArray(o.value)) {
            return o.value as Record<string, unknown>[];
        }
    }
    return [];
}

function ler(
    item: Record<string, unknown>,
    ...chaves: string[]
): unknown {
    for (let i = 0; i < chaves.length; i++) {
        const v = item[chaves[i]];
        if (v != null && v !== "") {
            return v;
        }
    }
    return "";
}

function texto(valor: unknown): string {
    if (valor == null) {
        return "";
    }
    if (typeof valor === "object") {
        const o = valor as Record<string, unknown>;
        if (o.Value != null) {
            return texto(o.Value);
        }
        return "";
    }
    return String(valor);
}

function atr(valor: unknown): string {
    const t = texto(valor).trim();
    if (t === "") {
        return "";
    }
    const n = Number(t);
    if (!isNaN(n)) {
        const s = String(Math.round(n));
        return s.length === 1 ? "0" + s : s;
    }
    return t;
}
