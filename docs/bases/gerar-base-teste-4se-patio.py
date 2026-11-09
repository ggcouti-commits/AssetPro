"""Base de teste: 4 SEs x 5 equipamentos de patio (mesmo cabecalho da Base Fisica Padrao)."""
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

DIR = Path(__file__).resolve().parent
DIR_TESTE = Path(
    r"C:\Users\Asus\OneDrive\Desktop\Power Apps\AssetPro\Arquivos para teste"
)

# Linha 2 = cabecalho real da planilha do Andre (inclui .. e ID ITEM).
HEADERS = [
    "..",
    "ID ITEM",
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
]

# TI pela maior tensao. Local 0 = RD. Arranjo 1 BS / 2 BD / 4 BPT.
SES = [
    {
        "cod": "7SEGU001",
        "nome": "SE U 138KV GUARA II CONSTR",
        "ti": 33,
        "local": 0,
        "arranjo": 2,
        "kv": "138KV",
        "itens": [
            {
                "tuc": "570",
                "tipo": "TRANSFORMADOR DE FORÇA",
                "cm": 4,
                "a": ("01", "82", "13", "91", "03", "01"),
                "desc": "TRAFO POT 25/33,3MVA 138/13,8KV DYN1 ONAN",
                "fab": "WEG",
                "mod": "TTR-40MVA",
                "serie": "TRG-18241982",
                "ano": 2018,
                "bay": "138KV",
                "op": "T1",
                "res": "NÃO",
            },
            {
                "tuc": "210",
                "tipo": "DISJUNTOR",
                "cm": 2,
                "a": ("03", "83", "71", "04", "02", "40"),
                "desc": "DISJUNTOR 3P 145KV 2500A 40KA SF6",
                "fab": "SIEMENS",
                "mod": "3AP1-FG",
                "serie": "DJG-3AP1001",
                "ano": 2019,
                "bay": "138KV",
                "op": "6025",
                "res": "NÃO",
            },
            {
                "tuc": "160",
                "tipo": "CHAVE",
                "cm": 2,
                "a": ("01", "82", "65", "03", "05", "01"),
                "desc": "CH SECCIONADORA 3P 145KV 2000A 40KA MOT",
                "fab": "HUBBELL",
                "mod": "GRMS",
                "serie": "SCG-82420",
                "ano": 2019,
                "bay": "138KV",
                "op": "6013",
                "res": "NÃO",
            },
            {
                "tuc": "575",
                "tipo": "TRANSFORMADOR DE MEDIDA",
                "cm": 2,
                "a": ("02", "82", "35", "01", "09", "02"),
                "desc": "TC/TP EXT 138KV 324VA OLEO",
                "fab": "ARTECHE",
                "mod": "CA-145",
                "serie": "TCG-1318760",
                "ano": 2020,
                "bay": "138KV",
                "op": "P61",
                "res": "NÃO",
            },
            {
                "tuc": "310",
                "tipo": "PÁRA-RAIOS",
                "cm": 2,
                "a": ("01", "02", "80", "02", "10", "00"),
                "desc": "PARA-RAIOS ZnO 120KV 10KA PATIO",
                "fab": "ABB",
                "mod": "POLIMEX-120",
                "serie": "PRG-120001",
                "ano": 2020,
                "bay": "138KV",
                "op": "P61",
                "res": "NÃO",
            },
        ],
    },
    {
        "cod": "7SEVA001",
        "nome": "SE U 69KV VALE DO AMANHECER",
        "ti": 32,
        "local": 0,
        "arranjo": 1,
        "kv": "69KV",
        "itens": [
            {
                "tuc": "570",
                "tipo": "TRANSFORMADOR DE FORÇA",
                "cm": 4,
                "a": ("01", "72", "13", "91", "03", "01"),
                "desc": "TRAFO POT 25MVA 69/13,8KV DYN1 ONAN",
                "fab": "TUSA",
                "mod": "T-25MVA",
                "serie": "TRV-2601",
                "ano": 2016,
                "bay": "69KV",
                "op": "T1",
                "res": "NÃO",
            },
            {
                "tuc": "210",
                "tipo": "DISJUNTOR",
                "cm": 2,
                "a": ("03", "73", "71", "04", "02", "40"),
                "desc": "DISJUNTOR 3P 72,5KV 2000A 31,5KA SF6",
                "fab": "ABB",
                "mod": "HPL-72",
                "serie": "DJV-2101",
                "ano": 2017,
                "bay": "69KV",
                "op": "6025",
                "res": "NÃO",
            },
            {
                "tuc": "160",
                "tipo": "CHAVE",
                "cm": 2,
                "a": ("01", "72", "65", "03", "05", "01"),
                "desc": "CH SECCIONADORA 3P 72,5KV 1250A MOT",
                "fab": "SIEMENS",
                "mod": "3CG",
                "serie": "SCV-2201",
                "ano": 2017,
                "bay": "69KV",
                "op": "6013",
                "res": "NÃO",
            },
            {
                "tuc": "575",
                "tipo": "TRANSFORMADOR DE MEDIDA",
                "cm": 2,
                "a": ("02", "72", "35", "01", "09", "02"),
                "desc": "TC EXT 69KV 200VA OLEO",
                "fab": "ARTECHE",
                "mod": "CA-72",
                "serie": "TCV-2301",
                "ano": 2016,
                "bay": "69KV",
                "op": "P61",
                "res": "NÃO",
            },
            {
                "tuc": "310",
                "tipo": "PÁRA-RAIOS",
                "cm": 2,
                "a": ("01", "02", "70", "02", "10", "00"),
                "desc": "PARA-RAIOS ZnO 60KV 10KA PATIO",
                "fab": "SIEMENS",
                "mod": "3EH4",
                "serie": "PRV-2501",
                "ano": 2016,
                "bay": "69KV",
                "op": "P61",
                "res": "SIM",
            },
        ],
    },
    {
        "cod": "7SETA001",
        "nome": "SE U 138KV TAGUATINGA",
        "ti": 33,
        "local": 0,
        "arranjo": 4,
        "kv": "138KV",
        "itens": [
            {
                "tuc": "570",
                "tipo": "TRANSFORMADOR DE FORÇA",
                "cm": 4,
                "a": ("01", "82", "13", "91", "03", "01"),
                "desc": "TRAFO POT 40MVA 138/13,8KV YND1 ONAF",
                "fab": "SIEMENS",
                "mod": "T-40MVA",
                "serie": "TRT-3601",
                "ano": 2014,
                "bay": "138KV",
                "op": "T1",
                "res": "NÃO",
            },
            {
                "tuc": "210",
                "tipo": "DISJUNTOR",
                "cm": 2,
                "a": ("03", "83", "71", "04", "02", "40"),
                "desc": "DISJUNTOR 3P 145KV 3150A 40KA SF6",
                "fab": "GE",
                "mod": "GL312",
                "serie": "DJT-3101",
                "ano": 2015,
                "bay": "138KV",
                "op": "6025",
                "res": "NÃO",
            },
            {
                "tuc": "160",
                "tipo": "CHAVE",
                "cm": 4,
                "a": ("01", "82", "65", "03", "05", "01"),
                "desc": "CH SECCIONADORA 3P 145KV 2000A PANT",
                "fab": "COELME",
                "mod": "S3C",
                "serie": "SCT-3201",
                "ano": 2015,
                "bay": "138KV",
                "op": "6013",
                "res": "NÃO",
            },
            {
                "tuc": "575",
                "tipo": "TRANSFORMADOR DE MEDIDA",
                "cm": 2,
                "a": ("02", "82", "35", "01", "09", "02"),
                "desc": "TP INDUTIVO EXT 138KV 400VA",
                "fab": "RITZ",
                "mod": "VEOT-145",
                "serie": "TPT-3401",
                "ano": 2015,
                "bay": "138KV",
                "op": "P62",
                "res": "NÃO",
            },
            {
                "tuc": "310",
                "tipo": "PÁRA-RAIOS",
                "cm": 2,
                "a": ("01", "02", "80", "02", "10", "00"),
                "desc": "PARA-RAIOS ZnO 120KV 10KA PATIO",
                "fab": "OHIO BRASS",
                "mod": "PVN-120",
                "serie": "PRT-3501",
                "ano": 2014,
                "bay": "138KV",
                "op": "P61",
                "res": "NÃO",
            },
        ],
    },
    {
        "cod": "7SESO001",
        "nome": "SE R 69KV SOBRADINHO",
        "ti": 53,
        "local": 0,
        "arranjo": 1,
        "kv": "69KV",
        "itens": [
            {
                "tuc": "570",
                "tipo": "TRANSFORMADOR DE FORÇA",
                "cm": 4,
                "a": ("01", "72", "13", "91", "03", "01"),
                "desc": "TRAFO POT 20MVA 69/13,8KV DYN1 ONAN",
                "fab": "WEG",
                "mod": "T-20MVA",
                "serie": "TRS-5601",
                "ano": 2012,
                "bay": "69KV",
                "op": "T1",
                "res": "NÃO",
            },
            {
                "tuc": "210",
                "tipo": "DISJUNTOR",
                "cm": 2,
                "a": ("03", "73", "71", "04", "02", "40"),
                "desc": "DISJUNTOR 3P 72,5KV 1600A 31,5KA SF6",
                "fab": "ABB",
                "mod": "HPL-72",
                "serie": "DJS-5101",
                "ano": 2013,
                "bay": "69KV",
                "op": "6025",
                "res": "NÃO",
            },
            {
                "tuc": "160",
                "tipo": "CHAVE",
                "cm": 2,
                "a": ("01", "72", "65", "03", "05", "01"),
                "desc": "CH SECCIONADORA 3P 72,5KV 1250A MOT",
                "fab": "ABB",
                "mod": "S9C",
                "serie": "SCS-5201",
                "ano": 2013,
                "bay": "69KV",
                "op": "6013",
                "res": "NÃO",
            },
            {
                "tuc": "575",
                "tipo": "TRANSFORMADOR DE MEDIDA",
                "cm": 2,
                "a": ("02", "72", "35", "01", "09", "02"),
                "desc": "TC EXT 69KV 200VA OLEO",
                "fab": "ARTECHE",
                "mod": "CA-72",
                "serie": "TCS-5301",
                "ano": 2013,
                "bay": "69KV",
                "op": "P61",
                "res": "NÃO",
            },
            {
                "tuc": "310",
                "tipo": "PÁRA-RAIOS",
                "cm": 2,
                "a": ("01", "02", "70", "02", "10", "00"),
                "desc": "PARA-RAIOS ZnO 60KV 10KA PATIO",
                "fab": "OHIO BRASS",
                "mod": "PVN-60",
                "serie": "PRS-5501",
                "ano": 2012,
                "bay": "69KV",
                "op": "P61",
                "res": "NÃO",
            },
        ],
    },
]


def gerar() -> Path:
    wb = Workbook()
    ws = wb.active
    ws.title = "BASE FÍSICA"

    ws.append(
        ["BASE FÍSICA PADRÃO ELÉTRICA — TESTE · 4 subestações · 20 itens de pátio"]
    )
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=len(HEADERS))
    ws["A1"].font = Font(name="Calibri", size=14, bold=True, color="FFFFFF")
    ws["A1"].fill = PatternFill("solid", fgColor="123B6E")
    ws["A1"].alignment = Alignment(horizontal="left", vertical="center")
    ws.row_dimensions[1].height = 22

    ws.append(HEADERS)
    fill_h = PatternFill("solid", fgColor="1B4C86")
    font_h = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
    for cell in ws[2]:
        cell.font = font_h
        cell.fill = fill_h
        cell.alignment = Alignment(wrap_text=True, vertical="center")
    ws.row_dimensions[2].height = 32
    ws.freeze_panes = "A3"

    n = 0
    for se in SES:
        for item in se["itens"]:
            n += 1
            ws.append(
                [
                    None,
                    n,
                    f"ASSET-{se['cod']}-{200000 + n}",
                    f"10000000{n:04d}-0",
                    se["cod"],
                    se["nome"],
                    str(se["ti"]),
                    str(se["local"]),
                    item["cm"],
                    se["arranjo"],
                    item["tuc"],
                    item["tipo"],
                    *item["a"],
                    item["desc"],
                    1,
                    "UN",
                    "SIM",
                    item["res"],
                    item["fab"],
                    item["mod"],
                    item["serie"],
                    item["ano"],
                    item["bay"],
                    item["op"],
                    "",
                    "Base de teste AssetPro — pátio",
                ]
            )

    widths = [
        4, 10, 26, 18, 14, 36, 8, 16, 16, 14, 10, 32,
        8, 8, 8, 8, 8, 8, 48, 10, 10, 12, 10, 14, 16, 16, 8, 10, 14, 12, 28,
    ]
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.auto_filter.ref = f"A2:{get_column_letter(len(HEADERS))}{2 + n}"

    stem = "base-teste-4se-20itens-patio"
    out = DIR / f"{stem}.xlsx"
    wb.save(out)
    print(f"OK {out} · {n} itens · {len(SES)} SEs")
    if DIR_TESTE.exists():
        dest = DIR_TESTE / f"{stem}.xlsx"
        wb.save(dest)
        print(f"OK {dest}")
    return out


if __name__ == "__main__":
    assert sum(len(s["itens"]) for s in SES) == 20
    gerar()
