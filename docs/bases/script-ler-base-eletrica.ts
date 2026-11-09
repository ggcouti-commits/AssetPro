function main(workbook: ExcelScript.Workbook): string {
    const src = workbook.getFirstWorksheet();
    const used = src.getUsedRange();
    if (!used) {
        return saida("Planilha vazia", 0, 0, "");
    }

    const values = used.getValues();
    const achado = acharCabecalho(values);
    if (achado.row < 0) {
        return saida("Não achei o cabeçalho (CÓDIGO ODI / Nº ASSET EXPERTS)", 0, 0, "");
    }

    const col = achado.col;
    if (col.codOdi < 0 || col.asset < 0) {
        return saida("Falta coluna CÓDIGO ODI ou Nº ASSET EXPERTS", 0, 0, "");
    }

    const itens: (string | number)[][] = [];
    const seMap: { [cod: string]: SeAgg } = {};

    for (let r = achado.row + 1; r < values.length; r++) {
        const row = values[r];
        const codSE = chaveSE(celula(row, col.codOdi));
        if (codSE === "") {
            continue;
        }

        const nomeSE = txt(celula(row, col.nomeOdi));
        itens.push([
            codSE,
            nomeSE,
            txt(celula(row, col.asset)),
            num(celula(row, col.idItem)),
            txt(celula(row, col.imobilizado)),
            txt(celula(row, col.iduc)),
            txt(celula(row, col.tuc)),
            txt(celula(row, col.tipoTuc)),
            txt(celula(row, col.ti)),
            num(celula(row, col.local)),
            num(celula(row, col.arranjo)),
            atr(celula(row, col.a1)),
            atr(celula(row, col.a2)),
            atr(celula(row, col.a3)),
            atr(celula(row, col.a4)),
            atr(celula(row, col.a5)),
            atr(celula(row, col.a6)),
            txt(celula(row, col.descricao)),
            num(celula(row, col.quant)),
            txt(celula(row, col.unidade)),
            simNao(celula(row, col.elegivel)),
            simNao(celula(row, col.reserva)),
            txt(celula(row, col.fabricante)),
            txt(celula(row, col.modelo)),
            txt(celula(row, col.serie)),
            num(celula(row, col.ano)),
            txt(celula(row, col.bay)),
            txt(celula(row, col.codOp)),
            txt(celula(row, col.projeto)),
            txt(celula(row, col.obs)),
            num(celula(row, col.cm))
        ]);

        if (!seMap[codSE]) {
            seMap[codSE] = novaSe();
        }
        seMap[codSE].qtd = seMap[codSE].qtd + 1;
        bump(seMap[codSE].nome, nomeSE);
        bump(seMap[codSE].ti, txt(celula(row, col.ti)));
        bump(seMap[codSE].local, txt(celula(row, col.local)));
        bump(seMap[codSE].arranjo, txt(celula(row, col.arranjo)));
    }

    if (itens.length === 0) {
        return saida("Nenhuma SE: a coluna CÓDIGO ODI veio vazia em todas as linhas", 0, 0, "");
    }

    const codigos = Object.keys(seMap);
    codigos.sort();
    const ses: (string | number)[][] = [];
    const nomes: string[] = [];
    for (let i = 0; i < codigos.length; i++) {
        const codSE = codigos[i];
        const agg = seMap[codSE];
        const nome = modo(agg.nome);
        nomes.push(codSE + " — " + (nome !== "" ? nome : "(sem nome)") + " (" + agg.qtd + ")");
        ses.push([
            codSE,
            nome,
            modo(agg.ti),
            num(modo(agg.local)),
            num(modo(agg.arranjo)),
            classeTensao(nome),
            agg.qtd
        ]);
    }

    gravarTabela(
        workbook,
        "_ImportSEs",
        "tblImportSEs",
        ["CodSE", "NomeSE", "TI", "LocalInstalacao", "ArranjoFisico", "ClasseTensao", "QtdItens"],
        ses
    );
    gravarTabela(
        workbook,
        "_ImportItens",
        "tblImportItens",
        [
            "CodSE", "NomeSE", "CodAsset", "IdItem", "Imobilizado", "IdUC", "CodTUC", "DescricaoTUC",
            "TI", "LocalInstalacao", "ArranjoFisico",
            "A1", "A2", "A3", "A4", "A5", "A6",
            "DescricaoBem", "Quantidade", "Unidade", "Elegivel", "Reserva",
            "Fabricante", "Modelo", "NumSerie", "Ano", "Bay",
            "CodOperacao", "Projeto", "Observacoes", "CM"
        ],
        itens
    );

    return saida("", ses.length, itens.length, nomes.join(" · "));
}

interface Colunas {
    // índice da coluna no cabeçalho (não o tipo do dado).
    // texto: txt(celula(...)) · número: num(...) / atr(...)
    asset: number;
    idItem: number;
    imobilizado: number;
    iduc: number;
    codOdi: number;
    nomeOdi: number;
    ti: number;
    local: number;
    cm: number;
    arranjo: number;
    tuc: number;
    tipoTuc: number;
    a1: number;
    a2: number;
    a3: number;
    a4: number;
    a5: number;
    a6: number;
    descricao: number;
    quant: number;
    unidade: number;
    elegivel: number;
    reserva: number;
    fabricante: number;
    modelo: number;
    serie: number;
    ano: number;
    bay: number;
    codOp: number;
    projeto: number;
    obs: number;
}

interface SeAgg {
    nome: { [k: string]: number };
    ti: { [k: string]: number };
    local: { [k: string]: number };
    arranjo: { [k: string]: number };
    qtd: number;
}

function colunasVazias(): Colunas {
    const c: Colunas = {
        asset: -1,
        idItem: -1,
        imobilizado: -1,
        iduc: -1,
        codOdi: -1,
        nomeOdi: -1,
        ti: -1,
        local: -1,
        cm: -1,
        arranjo: -1,
        tuc: -1,
        tipoTuc: -1,
        a1: -1,
        a2: -1,
        a3: -1,
        a4: -1,
        a5: -1,
        a6: -1,
        descricao: -1,
        quant: -1,
        unidade: -1,
        elegivel: -1,
        reserva: -1,
        fabricante: -1,
        modelo: -1,
        serie: -1,
        ano: -1,
        bay: -1,
        codOp: -1,
        projeto: -1,
        obs: -1
    };
    return c;
}

function novaSe(): SeAgg {
    const s: SeAgg = {
        nome: {},
        ti: {},
        local: {},
        arranjo: {},
        qtd: 0
    };
    return s;
}

function acharCabecalho(values: (string | number | boolean)[][]): { row: number; col: Colunas } {
    const vazio: { row: number; col: Colunas } = { row: -1, col: colunasVazias() };
    const max = Math.min(values.length, 12);
    for (let r = 0; r < max; r++) {
        const col = colunasVazias();
        const row = values[r];
        for (let c = 0; c < row.length; c++) {
            const k = norm(row[c]);
            if (k === "" || k === "..") {
                continue;
            }
            if (k.indexOf("asset experts") >= 0 || k === "n asset experts") {
                col.asset = c;
            } else if (k === "iduc" || k === "id uc") {
                col.iduc = c;
            } else if (
                k === "id"
                || k.indexOf("id item") >= 0
                || k === "id planilha"
            ) {
                col.idItem = c;
            } else if (k.indexOf("numero imobilizado") >= 0) {
                col.imobilizado = c;
            } else if (k === "codigo odi" || k === "cod odi") {
                col.codOdi = c;
            } else if (k.indexOf("descricao de odi") >= 0) {
                col.nomeOdi = c;
            } else if (k === "ti") {
                col.ti = c;
            } else if (k.indexOf("local instalacao") >= 0) {
                col.local = c;
            } else if (k.indexOf("centro modular") >= 0) {
                col.cm = c;
            } else if (k.indexOf("arranjo fisico") >= 0) {
                col.arranjo = c;
            } else if (k === "tuc") {
                col.tuc = c;
            } else if (k.indexOf("unidade de cadastro") >= 0 || k.indexOf("descricao tuc") >= 0) {
                col.tipoTuc = c;
            } else if (k === "a1") {
                col.a1 = c;
            } else if (k === "a2") {
                col.a2 = c;
            } else if (k === "a3") {
                col.a3 = c;
            } else if (k === "a4") {
                col.a4 = c;
            } else if (k === "a5") {
                col.a5 = c;
            } else if (k === "a6") {
                col.a6 = c;
            } else if (k.indexOf("descricao tecnica") >= 0) {
                col.descricao = c;
            } else if (k === "quant" || k === "quantidade") {
                col.quant = c;
            } else if (k === "unidade") {
                col.unidade = c;
            } else if (k.indexOf("elegivel") >= 0) {
                col.elegivel = c;
            } else if (k === "reserva") {
                col.reserva = c;
            } else if (k === "fabricante") {
                col.fabricante = c;
            } else if (k === "modelo") {
                col.modelo = c;
            } else if (k.indexOf("numero serie") >= 0) {
                col.serie = c;
            } else if (k === "ano") {
                col.ano = c;
            } else if (k === "bay") {
                col.bay = c;
            } else if (k.indexOf("codigo operacao") >= 0) {
                col.codOp = c;
            } else if (k === "projeto") {
                col.projeto = c;
            } else if (k.indexOf("observacao") >= 0) {
                col.obs = c;
            }
        }
        if (col.codOdi >= 0) {
            const ok: { row: number; col: Colunas } = { row: r, col: col };
            return ok;
        }
    }
    return vazio;
}

function gravarTabela(
    workbook: ExcelScript.Workbook,
    sheetName: string,
    tableName: string,
    headers: string[],
    data: (string | number)[][]
): void {
    const old = workbook.getWorksheet(sheetName);
    if (old) {
        old.delete();
    }
    const ws = workbook.addWorksheet(sheetName);
    const values: (string | number)[][] = [headers];
    if (data.length === 0) {
        const vazia: (string | number)[] = [];
        for (let i = 0; i < headers.length; i++) {
            vazia.push("");
        }
        values.push(vazia);
    } else {
        for (let i = 0; i < data.length; i++) {
            values.push(data[i]);
        }
    }
    ws.getRangeByIndexes(0, 0, values.length, headers.length).setValues(values);
    const tabelas = ws.getTables();
    for (let t = 0; t < tabelas.length; t++) {
        if (tabelas[t].getName() === tableName) {
            tabelas[t].delete();
        }
    }
    const faixa = ws.getRangeByIndexes(0, 0, values.length, headers.length);
    ws.addTable(faixa.getAddress(), true).setName(tableName);
}

function saida(erro: string, qtdSEs: number, qtdItens: number, listaSEs: string): string {
    return JSON.stringify({
        erro: erro,
        qtdSEs: qtdSEs,
        qtdItens: qtdItens,
        listaSEs: listaSEs
    });
}

function celula(row: (string | number | boolean)[], idx: number): string | number | boolean {
    if (idx < 0 || idx >= row.length) {
        return "";
    }
    return row[idx];
}

function norm(v: string | number | boolean): string {
    let s = String(v);
    s = s.trim();
    s = s.toLowerCase();
    s = s.replace(/[áàâãä]/g, "a");
    s = s.replace(/[éèêë]/g, "e");
    s = s.replace(/[íìîï]/g, "i");
    s = s.replace(/[óòôõö]/g, "o");
    s = s.replace(/[úùûü]/g, "u");
    s = s.replace(/ç/g, "c");
    s = s.replace(/º/g, "");
    s = s.replace(/[^a-z0-9]+/g, " ");
    s = s.replace(/\s+/g, " ");
    return s.trim();
}

function txt(v: string | number | boolean): string {
    if (v === null || v === undefined) {
        return "";
    }
    return String(v).trim();
}

function chaveSE(v: string | number | boolean): string {
    return txt(v).replace(/\s+/g, "").toUpperCase();
}

function atr(v: string | number | boolean): string {
    const s = txt(v);
    if (s === "") {
        return "00";
    }
    return s;
}

function num(v: string | number | boolean): number | string {
    if (v === null || v === undefined || v === "") {
        return "";
    }
    if (typeof v === "number") {
        return v;
    }
    const s = String(v).trim();
    if (s === "") {
        return "";
    }
    const n = parseFloat(s.replace(/\./g, "").replace(",", "."));
    if (isNaN(n)) {
        return "";
    }
    return n;
}

function simNao(v: string | number | boolean): string {
    const s = norm(v);
    if (s === "sim" || s === "s" || s === "1") {
        return "SIM";
    }
    if (s === "nao" || s === "n" || s === "0") {
        return "NÃO";
    }
    return txt(v).toUpperCase();
}

function bump(bag: { [k: string]: number }, value: string): void {
    if (value === "") {
        return;
    }
    if (bag[value]) {
        bag[value] = bag[value] + 1;
    } else {
        bag[value] = 1;
    }
}

function modo(bag: { [k: string]: number }): string {
    let best = "";
    let n = 0;
    const keys = Object.keys(bag);
    for (let i = 0; i < keys.length; i++) {
        const k = keys[i];
        if (bag[k] > n) {
            n = bag[k];
            best = k;
        }
    }
    return best;
}

function classeTensao(nome: string): string {
    const m = nome.match(/(\d+(?:[.,]\d+)?)\s*k\s*v/i);
    if (!m) {
        return "";
    }
    return m[1].replace(",", ".") + " kV";
}
