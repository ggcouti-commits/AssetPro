from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter
from pathlib import Path

out = Path(__file__).with_name("amostra-importacao-5ses.xlsx")

wb = Workbook()
ws = wb.active
ws.title = "Base"

headers = [
    "Nº ASSET EXPERTS",
    "NÚMERO IMOBILIZADO",
    "CÓDIGO ODI",
    "DESCRIÇÃO DE ODI",
    "TI",
    "LOCAL INSTALAÇÃO",
    "CENTRO MODULAR",
    "ARRANJO FÍSICO",
    "TUC",
    "TIPO DE UNIDADE DE CADASTRO",
    "A1",
    "A2",
    "A3",
    "A4",
    "A5",
    "A6",
    "DESCRIÇÃO TÉCNICA DO ATIVO",
    "QUANT",
    "UNIDADE",
    "ELEGÍVEL",
    "RESERVA",
    "FABRICANTE",
    "MODELO",
    "NÚMERO SÉRIE",
    "ANO",
    "BAY",
    "CÓDIGO OPERAÇÃO",
    "PROJETO",
    "OBSERVAÇÃO",
    "..",
]

ws.append(["Base física padrão elétrica — amostra AssetPro (5 SEs)"])
ws.append(headers)

fill = PatternFill("solid", fgColor="1F4E79")
font = Font(bold=True, color="FFFFFF")
for c in ws[2]:
    c.fill = fill
    c.font = font
    c.alignment = Alignment(horizontal="center", wrap_text=True)

ses = [
    {
        "cod": "7SEGU001",
        "nome": "SE U 138KV GUARA II CONSTR",
        "ti": 33,
        "local": 0,
        "arranjo": 1,
        "itens": [
            (230, "01", "DISJUNTOR 138KV", "1,00", "UN", "SIM", "NÃO", "ABB", "HPL 245", "DJ-1001", 2012, "BAY 01", "T2", 1),
            (230, "01", "DISJUNTOR 138KV", "1,00", "UN", "SIM", "NÃO", "SIEMENS", "3AP1", "DJ-1002", 2014, "BAY 02", "T2", 2),
            (240, "01", "SECCIONADORA 138KV", "1,00", "UN", "SIM", "NÃO", "SIEMENS", "3CG", "SEC-2001", 2013, "BAY 01", "6025", 2),
            (240, "01", "SECCIONADORA 138KV", "1,00", "UN", "SIM", "NÃO", "ABB", "S9C", "SEC-2002", 2015, "BAY 02", "6025", 2),
            (250, "01", "TRANSFORMADOR DE CORRENTE 138KV", "1,00", "UN", "SIM", "NÃO", "ARTECHE", "CA-145", "TC-3001", 2011, "BAY 01", "T2", 1),
            (255, "01", "TRANSFORMADOR DE POTENCIAL 138KV", "1,00", "UN", "SIM", "NÃO", "ARTECHE", "UTF-145", "TP-4001", 2011, "BAY 01", "", 1),
            (215, "01", "PARA-RAIOS 138KV", "1,00", "UN", "SIM", "NÃO", "OHIO BRASS", "PVN", "PR-5001", 2010, "BAY 01", "", 2),
            (400, "01", "TRAFO POTENCIA 138/13.8KV", "1,00", "UN", "SIM", "NÃO", "WEG", "TTR-40MVA", "TR-6001", 2009, "BAY TRAFO", "T1", 4),
            (430, "01", "BACIA CONTENCAO TRAFO", "1,00", "UN", "SIM", "NÃO", "", "", "", 2009, "BAY TRAFO", "", 4),
            (160, "01", "PAINEL SERVICOS AUXILIARES", "1,00", "UN", "SIM", "NÃO", "SCHNEIDER", "Prisma", "PA-7001", 2016, "PAINEL", "", 8),
            (120, "01", "CABO FORCA 15KV", "120,00", "M", "SIM", "NÃO", "FURUKAWA", "XLPE 240", "", 2018, "PAINEL", "", 1),
            (555, "01", "PORTAO DE ACESSO", "1,00", "UN", "NÃO", "NÃO", "", "", "", 2008, "INFRA", "", 0),
        ],
    },
    {
        "cod": "7SEVA001",
        "nome": "SE U 69KV VALE DO AMANHECER",
        "ti": 31,
        "local": 0,
        "arranjo": 2,
        "itens": [
            (230, "01", "DISJUNTOR 69KV", "1,00", "UN", "SIM", "NÃO", "ABB", "HPL 72", "DJ-2101", 2016, "BAY 01", "T2", 2),
            (230, "01", "DISJUNTOR 69KV", "1,00", "UN", "SIM", "NÃO", "SIEMENS", "3AP1-FG", "DJ-2102", 2017, "BAY 02", "T2", 2),
            (240, "01", "SECCIONADORA 69KV", "1,00", "UN", "SIM", "NÃO", "SIEMENS", "3CG", "SEC-2201", 2016, "BAY 01", "6025", 3),
            (240, "01", "SECCIONADORA 69KV", "1,00", "UN", "SIM", "NÃO", "ABB", "S9C", "SEC-2202", 2016, "BAY 02", "6025", 3),
            (250, "01", "TRANSFORMADOR DE CORRENTE 69KV", "1,00", "UN", "SIM", "NÃO", "ARTECHE", "CA-72", "TC-2301", 2016, "BAY 01", "", 2),
            (255, "01", "TRANSFORMADOR DE POTENCIAL 69KV", "1,00", "UN", "SIM", "NÃO", "ARTECHE", "UTF-72", "TP-2401", 2016, "BAY 02", "", 3),
            (215, "01", "PARA-RAIOS 69KV", "1,00", "UN", "SIM", "NÃO", "SIEMENS", "3EH4", "PR-2501", 2015, "BAY 01", "", 2),
            (400, "01", "TRAFO POTENCIA 69/13.8KV", "1,00", "UN", "SIM", "NÃO", "TUSA", "T-25MVA", "TR-2601", 2014, "BAY TRAFO", "T1", 4),
            (400, "01", "TRAFO POTENCIA 69/13.8KV", "1,00", "UN", "SIM", "SIM", "TUSA", "T-25MVA", "TR-2602", 2014, "RESERVA", "T1", 4),
            (160, "02", "RELE PROTECAO", "1,00", "UN", "SIM", "NÃO", "SEL", "SEL-351", "RL-2701", 2018, "PAINEL", "", 1),
            (160, "02", "RELE PROTECAO", "1,00", "UN", "SIM", "NÃO", "SEL", "SEL-387", "RL-2702", 2018, "PAINEL", "", 1),
            (170, "01", "BANCO BATERIA 125VCC", "1,00", "UN", "SIM", "NÃO", "HOPPECKE", "OPzS", "BT-2801", 2017, "CC", "", 8),
            (555, "01", "CERCA PERIMETRAL", "180,00", "M", "NÃO", "NÃO", "", "", "", 2014, "INFRA", "", 0),
            (120, "01", "CABO CONTROLE", "80,00", "M", "SIM", "NÃO", "PRYSMIAN", "1,5mm", "", 2018, "PAINEL", "", 1),
        ],
    },
    {
        "cod": "7SEBRA001",
        "nome": "SE U 138KV BRASILIA LESTE",
        "ti": 33,
        "local": 0,
        "arranjo": 4,
        "itens": [
            (230, "01", "DISJUNTOR 138KV", "1,00", "UN", "SIM", "NÃO", "GE", "GL312", "DJ-3101", 2008, "BAY 01", "T2", 2),
            (240, "01", "SECCIONADORA 138KV", "1,00", "UN", "SIM", "NÃO", "COELME", "S3C", "SEC-3201", 2008, "BAY 01", "6025", 2),
            (250, "01", "TRANSFORMADOR DE CORRENTE 138KV", "1,00", "UN", "SIM", "NÃO", "RITZ", "ASG", "TC-3301", 2009, "BAY 01", "", 1),
            (255, "01", "TRANSFORMADOR DE POTENCIAL 138KV", "1,00", "UN", "SIM", "NÃO", "RITZ", "VEOT", "TP-3401", 2009, "BAY 01", "", 1),
            (215, "01", "PARA-RAIOS 138KV", "1,00", "UN", "SIM", "NÃO", "OHIO BRASS", "PVN", "PR-3501", 2007, "BAY 01", "", 2),
            (400, "01", "TRAFO POTENCIA 138/69KV", "1,00", "UN", "SIM", "NÃO", "SIEMENS", "T-80MVA", "TR-3601", 2005, "BAY TRAFO", "T1", 4),
            (430, "01", "BACIA CONTENCAO TRAFO", "1,00", "UN", "SIM", "NÃO", "", "", "", 2005, "BAY TRAFO", "", 4),
            (160, "01", "PAINEL COMANDO", "1,00", "UN", "SIM", "NÃO", "SCHNEIDER", "Blokset", "PA-3701", 2010, "PAINEL", "", 8),
            (170, "01", "RETIFICADOR 125VCC", "1,00", "UN", "SIM", "NÃO", "EATON", "SC200", "RT-3801", 2011, "CC", "", 8),
            (555, "01", "CASA DE COMANDO", "1,00", "UN", "NÃO", "NÃO", "", "", "", 2005, "INFRA", "", 0),
            (120, "01", "ELETRODUTO ACO", "45,00", "M", "SIM", "NÃO", "GERDAU", "", "", 2012, "INFRA", "", 0),
        ],
    },
    {
        "cod": "7SETAG001",
        "nome": "SE U 34.5KV TAGUATINGA",
        "ti": 32,
        "local": 0,
        "arranjo": 1,
        "itens": [
            (230, "01", "DISJUNTOR 34,5KV", "1,00", "UN", "SIM", "NÃO", "SCHNEIDER", "SF1", "DJ-4101", 2019, "BAY 01", "T2", 1),
            (230, "01", "DISJUNTOR 34,5KV", "1,00", "UN", "SIM", "NÃO", "SCHNEIDER", "SF1", "DJ-4102", 2019, "BAY 02", "T2", 1),
            (240, "01", "SECCIONADORA 34,5KV", "1,00", "UN", "SIM", "NÃO", "ROMAGNOLE", "ST-36", "SEC-4201", 2019, "BAY 01", "6025", 1),
            (250, "01", "TRANSFORMADOR DE CORRENTE 34,5KV", "1,00", "UN", "SIM", "NÃO", "ARTECHE", "CA-36", "TC-4301", 2019, "BAY 01", "", 1),
            (255, "01", "TRANSFORMADOR DE POTENCIAL 34,5KV", "1,00", "UN", "SIM", "NÃO", "ARTECHE", "UTF-36", "TP-4401", 2019, "BAY 02", "", 1),
            (215, "01", "PARA-RAIOS 34,5KV", "1,00", "UN", "SIM", "NÃO", "SIEMENS", "3EH5", "PR-4501", 2018, "BAY 01", "", 2),
            (400, "01", "TRAFO DISTRIBUICAO 34,5/13.8KV", "1,00", "UN", "SIM", "NÃO", "WEG", "T-10MVA", "TR-4601", 2018, "BAY TRAFO", "T1", 4),
            (160, "02", "RELE PROTECAO", "1,00", "UN", "SIM", "NÃO", "SEL", "SEL-751", "RL-4701", 2020, "PAINEL", "", 1),
            (160, "01", "PAINEL MEDICAO", "1,00", "UN", "SIM", "NÃO", "LANDIS", "E650", "PA-4801", 2020, "PAINEL", "", 8),
            (170, "01", "NO-BREAK 10KVA", "1,00", "UN", "SIM", "NÃO", "APC", "SRT10K", "NB-4901", 2021, "CC", "", 8),
            (120, "01", "CABO FORCA 35KV", "60,00", "M", "SIM", "NÃO", "NEXANS", "XLPE 95", "", 2019, "BAY 01", "", 1),
            (555, "01", "ILUMINACAO PATIO", "12,00", "UN", "NÃO", "NÃO", "", "", "", 2019, "INFRA", "", 0),
            (555, "01", "EXTINTOR PQS", "4,00", "UN", "NÃO", "NÃO", "", "", "", 2022, "INFRA", "", 0),
        ],
    },
    {
        "cod": "7SESOB001",
        "nome": "SE U 69KV SOBRADINHO",
        "ti": 53,
        "local": 0,
        "arranjo": 5,
        "itens": [
            (230, "01", "DISJUNTOR 69KV", "1,00", "UN", "SIM", "NÃO", "ABB", "HPL 72", "DJ-5101", 2013, "BAY 01", "T2", 2),
            (230, "01", "DISJUNTOR 69KV", "1,00", "UN", "SIM", "NÃO", "ABB", "HPL 72", "DJ-5102", 2013, "BAY 02", "T2", 3),
            (230, "01", "DISJUNTOR 69KV", "1,00", "UN", "SIM", "NÃO", "SIEMENS", "3AP1", "DJ-5103", 2014, "BAY 03", "T2", 5),
            (240, "01", "SECCIONADORA 69KV", "1,00", "UN", "SIM", "NÃO", "SIEMENS", "3CG", "SEC-5201", 2013, "BAY 01", "6025", 2),
            (240, "01", "SECCIONADORA 69KV", "1,00", "UN", "SIM", "NÃO", "ABB", "S9C", "SEC-5202", 2013, "BAY 02", "6025", 3),
            (250, "01", "TRANSFORMADOR DE CORRENTE 69KV", "1,00", "UN", "SIM", "NÃO", "ARTECHE", "CA-72", "TC-5301", 2013, "BAY 01", "", 2),
            (255, "01", "TRANSFORMADOR DE POTENCIAL 69KV", "1,00", "UN", "SIM", "NÃO", "ARTECHE", "UTF-72", "TP-5401", 2013, "BAY 02", "", 3),
            (215, "01", "PARA-RAIOS 69KV", "1,00", "UN", "SIM", "NÃO", "OHIO BRASS", "PVN", "PR-5501", 2012, "BAY 01", "", 2),
            (400, "01", "TRAFO POTENCIA 69/13.8KV", "1,00", "UN", "SIM", "NÃO", "WEG", "T-20MVA", "TR-5601", 2011, "BAY TRAFO", "T1", 4),
            (430, "01", "BACIA CONTENCAO TRAFO", "1,00", "UN", "SIM", "NÃO", "", "", "", 2011, "BAY TRAFO", "", 4),
            (160, "02", "RELE PROTECAO", "1,00", "UN", "SIM", "NÃO", "GE", "F60", "RL-5701", 2015, "PAINEL", "", 1),
            (160, "01", "PAINEL SERVICOS AUXILIARES", "1,00", "UN", "SIM", "NÃO", "WEG", "CCM", "PA-5801", 2015, "PAINEL", "", 8),
            (170, "01", "BANCO BATERIA 125VCC", "1,00", "UN", "SIM", "NÃO", "HOPPECKE", "OPzS", "BT-5901", 2014, "CC", "", 9),
            (120, "01", "CABO FORCA 15KV", "90,00", "M", "SIM", "NÃO", "FURUKAWA", "XLPE 185", "", 2016, "PAINEL", "", 1),
            (555, "01", "PORTAO DE ACESSO", "1,00", "UN", "NÃO", "NÃO", "", "", "", 2011, "INFRA", "", 0),
        ],
    },
]

seq = 0
for se in ses:
    for tuc, a1, desc, qtd, und, eleg, res, fab, mod, serie, ano, bay, cop, cm in se["itens"]:
        seq += 1
        imob = "10000000{:04d}-0".format(seq)
        asset = "ASSET-{}-{}".format(se["cod"], 200000 + seq)
        ws.append(
            [
                asset,
                imob,
                se["cod"],
                se["nome"],
                se["ti"],
                se["local"],
                cm,
                se["arranjo"],
                tuc,
                "UNIDADE DE CADASTRO",
                a1,
                "00",
                "00",
                "00",
                "00",
                "00",
                desc,
                qtd,
                und,
                eleg,
                res,
                fab,
                mod,
                serie,
                ano,
                bay,
                cop,
                "XOXOXOXOXO",
                "",
                "",
            ]
        )

ws.row_dimensions[1].height = 22
ws.row_dimensions[2].height = 32
ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=10)
ws["A1"].font = Font(bold=True, size=14, color="1F4E79")

widths = [
    22, 20, 14, 36, 8, 12, 12, 12, 10, 22,
    8, 8, 8, 8, 8, 8, 36, 10, 10, 12,
    10, 14, 14, 14, 8, 14, 12, 14, 14, 6,
]
for i, w in enumerate(widths, 1):
    ws.column_dimensions[get_column_letter(i)].width = w

ws.auto_filter.ref = "A2:{}{}".format(get_column_letter(len(headers)), ws.max_row)
ws.freeze_panes = "A3"

wb.save(out)
print("FILE", out)
print("ITENS", seq)
for se in ses:
    print(se["cod"], len(se["itens"]), se["nome"])
