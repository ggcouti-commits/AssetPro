"""Gera Base Fisica teste: 12 SEs, 200 itens. Cabecalho na linha 2 (igual Andre)."""
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

DIR = Path(__file__).resolve().parent
DIR_TESTE = Path(
    r"C:\Users\Asus\OneDrive\Desktop\Power Apps\AssetPro\Arquivos para teste"
)

HEADERS = [
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

# 12 SEs, soma 200. TI pela maior tensao (urbana 30-33 / rural 51-53).
SES = [
    ("7SEGU001", "SE Guará II 138 kV", 33, 0, 2, 28),
    ("7SEAS001", "SE Asa Sul 138 kV", 33, 0, 1, 24),
    ("7SETA001", "SE Taguatinga 138 kV", 33, 0, 4, 22),
    ("7SECE001", "SE Ceilândia 69 kV", 32, 0, 1, 18),
    ("7SESO001", "SE Sobradinho 69 kV", 32, 0, 1, 17),
    ("7SEGA001", "SE Gama 69 kV", 52, 0, 1, 16),
    ("7SEBR001", "SE Brazlândia 69 kV", 53, 0, 1, 15),
    ("7SEPL001", "SE Planaltina 34,5 kV", 31, 0, 1, 14),
    ("7SESA001", "SE Samambaia 34,5 kV", 31, 0, 2, 13),
    ("7SENC001", "SE Núcleo Bandeirante 34,5 kV", 31, 0, 1, 12),
    ("7SEPA001", "SE Paranoá 34,5 kV", 51, 0, 1, 11),
    ("7SEVI001", "SE Vicente Pires 13,8 kV", 30, 0, 1, 10),
]

# 12 SEs, soma 500.
SES_500 = [
    ("7SEGU001", "SE Guará II 138 kV", 33, 0, 2, 62),
    ("7SEAS001", "SE Asa Sul 138 kV", 33, 0, 1, 55),
    ("7SETA001", "SE Taguatinga 138 kV", 33, 0, 4, 50),
    ("7SECE001", "SE Ceilândia 69 kV", 32, 0, 1, 48),
    ("7SESO001", "SE Sobradinho 69 kV", 32, 0, 1, 45),
    ("7SEGA001", "SE Gama 69 kV", 52, 0, 1, 42),
    ("7SEBR001", "SE Brazlândia 69 kV", 53, 0, 1, 40),
    ("7SEPL001", "SE Planaltina 34,5 kV", 31, 0, 1, 38),
    ("7SESA001", "SE Samambaia 34,5 kV", 31, 0, 2, 35),
    ("7SENC001", "SE Núcleo Bandeirante 34,5 kV", 31, 0, 1, 32),
    ("7SEPA001", "SE Paranoá 34,5 kV", 51, 0, 1, 28),
    ("7SEVI001", "SE Vicente Pires 13,8 kV", 30, 0, 1, 25),
]

# 20 SEs, soma 1000.
SES_1000 = [
    ("7SEGU001", "SE Guará II 138 kV", 33, 0, 2, 80),
    ("7SEAS001", "SE Asa Sul 138 kV", 33, 0, 1, 75),
    ("7SETA001", "SE Taguatinga 138 kV", 33, 0, 4, 70),
    ("7SECE001", "SE Ceilândia 69 kV", 32, 0, 1, 65),
    ("7SESO001", "SE Sobradinho 69 kV", 32, 0, 1, 60),
    ("7SEGA001", "SE Gama 69 kV", 52, 0, 1, 58),
    ("7SEBR001", "SE Brazlândia 69 kV", 53, 0, 1, 55),
    ("7SEPL001", "SE Planaltina 34,5 kV", 31, 0, 1, 52),
    ("7SESA001", "SE Samambaia 34,5 kV", 31, 0, 2, 50),
    ("7SENC001", "SE Núcleo Bandeirante 34,5 kV", 31, 0, 1, 48),
    ("7SEPA001", "SE Paranoá 34,5 kV", 51, 0, 1, 46),
    ("7SEVI001", "SE Vicente Pires 13,8 kV", 30, 0, 1, 44),
    ("7SERE001", "SE Recanto das Emas 69 kV", 32, 0, 1, 42),
    ("7SESM001", "SE Santa Maria 69 kV", 32, 0, 1, 40),
    ("7SESS001", "SE São Sebastião 34,5 kV", 31, 0, 1, 38),
    ("7SEJB001", "SE Jardim Botânico 34,5 kV", 31, 0, 2, 36),
    ("7SECR001", "SE Cruzeiro 13,8 kV", 30, 0, 1, 34),
    ("7SELS001", "SE Lago Sul 138 kV", 33, 0, 2, 32),
    ("7SEPP001", "SE Pipiripau 69 kV", 52, 0, 1, 30),
    ("7SEAL001", "SE Alexânia 34,5 kV", 51, 0, 1, 45),
]

# (tuc, nome tuc, cm, descricao, a1..a6, un, bay, fab, modelo, cod_op)
TIPOS = [
    ("155", "TRANSFORMADOR DE POTÊNCIA", 1, "TRANSFORMADOR DE POTÊNCIA TRIFÁSICO",
     "01", "02", "03", "", "", "", "UN", "T1", "ABB", "ONAN 40 MVA", "T1"),
    ("235", "DISJUNTOR", 1, "DISJUNTOR SF6",
     "01", "01", "", "", "", "", "UN", "DJ", "SIEMENS", "3AP1-FG", "DJ01"),
    ("240", "SECCIONADOR", 1, "SECCIONADOR TRIPOLAR",
     "01", "02", "", "", "", "", "UN", "SC", "SIEMENS", "3DC", "SC01"),
    ("245", "TRANSFORMADOR DE CORRENTE", 1, "TRANSFORMADOR DE CORRENTE",
     "01", "01", "02", "", "", "", "UN", "TC", "ARTECHE", "CA-145", "TC01"),
    ("250", "TRANSFORMADOR DE POTENCIAL", 1, "TRANSFORMADOR DE POTENCIAL INDUTIVO",
     "01", "01", "", "", "", "", "UN", "TP", "ARTECHE", "UTF-145", "TP01"),
    ("255", "PARA-RAIOS", 1, "PARA-RAIOS ÓXIDO DE ZINCO",
     "01", "02", "", "", "", "", "UN", "PR", "ABB", "POLIMEX", "PR01"),
    ("265", "PAINEL DE COMANDO E PROTEÇÃO", 1, "PAINEL DE PROTEÇÃO E CONTROLE",
     "01", "", "", "", "", "", "UN", "PN", "SCHNEIDER", "SEPAM", "PN01"),
    ("230", "RELÉ", 1, "RELÉ DE PROTEÇÃO NUMÉRICO",
     "01", "02", "", "", "", "", "UN", "RL", "SEL", "411L", "RL01"),
    ("275", "BANCO DE CAPACITORES", 5, "BANCO DE CAPACITORES SHUNT",
     "01", "01", "", "", "", "", "UN", "BC", "GE", "CAPBANK", "BC01"),
    ("220", "CABO ISOLADO", 9, "CABO DE POTÊNCIA ISOLADO",
     "01", "02", "03", "", "", "", "M", "CB", "PRYSMIAN", "EPR 15kV", "CB01"),
    ("210", "ESTRUTURA METÁLICA", 0, "ESTRUTURA METÁLICA DE PÁTIO",
     "01", "", "", "", "", "", "UN", "ES", "Usiminas", "TRELIÇA", "ES01"),
    ("205", "MALHA DE TERRA", 0, "MALHA DE TERRA DA SUBESTAÇÃO",
     "01", "", "", "", "", "", "UN", "MT", "Cobreazul", "Cu 70mm²", "MT01"),
    ("235", "DISJUNTOR", 2, "DISJUNTOR DE ENTRADA DE LINHA",
     "01", "01", "", "", "", "", "UN", "EL", "SIEMENS", "3AP1-FG", "EL01"),
    ("155", "TRANSFORMADOR DE POTÊNCIA", 4, "TRANSFORMADOR DE CONEXÃO",
     "01", "02", "03", "", "", "", "UN", "CT", "WEG", "ONAN 25 MVA", "CT01"),
    ("240", "SECCIONADOR", 9, "SECCIONADOR DE ALIMENTADOR",
     "01", "02", "", "", "", "", "UN", "AL", "SIEMENS", "3DC", "AL01"),
]


def gerar(ses: list, stem: str) -> None:
    total = sum(s[5] for s in ses)
    wb = Workbook()
    ws = wb.active
    ws.title = "Base"

    ws["A1"] = (
        f"BASE FÍSICA PADRÃO ELÉTRICA — TESTE · {len(ses)} subestações · {total} itens"
    )
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=len(HEADERS))
    ws["A1"].font = Font(name="Calibri", size=14, bold=True, color="FFFFFF")
    ws["A1"].fill = PatternFill("solid", fgColor="123B6E")
    ws["A1"].alignment = Alignment(horizontal="left", vertical="center")
    ws.row_dimensions[1].height = 22

    fill_h = PatternFill("solid", fgColor="1B4C86")
    font_h = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
    for c, h in enumerate(HEADERS, 1):
        cell = ws.cell(2, c, h)
        cell.font = font_h
        cell.fill = fill_h
        cell.alignment = Alignment(wrap_text=True, vertical="center")
    ws.row_dimensions[2].height = 32
    ws.freeze_panes = "A3"
    ultima = 2 + total
    ws.auto_filter.ref = f"A2:{get_column_letter(len(HEADERS))}{ultima}"

    n = 0
    for cod, nome, ti, local, arranjo, qtd in ses:
        for i in range(qtd):
            n += 1
            t = TIPOS[(n - 1) % len(TIPOS)]
            bay = f"{t[11]}-{i + 1:02d}"
            row = [
                n,
                f"ASSET-{cod}-{n:06d}",
                f"{20000000 + n}",
                cod,
                nome,
                ti,
                local,
                t[2],
                arranjo,
                t[0],
                t[1],
                t[4], t[5], t[6], t[7], t[8], t[9],
                f"{t[3]} — {nome}",
                1,
                t[10],
                "SIM",
                "NÃO" if n % 17 else "SIM",
                t[12],
                t[13],
                f"SN{cod[-3:]}{n:05d}",
                2010 + (n % 15),
                bay,
                t[14],
                "",
                "Base de teste AssetPro",
            ]
            ws.append(row)

    widths = [10, 26, 18, 14, 34, 8, 16, 16, 14, 10, 32, 8, 8, 8, 8, 8, 8,
              48, 10, 10, 12, 10, 14, 16, 16, 8, 10, 14, 12, 22]
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w

    out = DIR / f"{stem}.xlsx"
    DIR.mkdir(parents=True, exist_ok=True)
    wb.save(out)
    print(f"OK {out} · {n} itens · {len(ses)} SEs")

    if DIR_TESTE.exists():
        dest = DIR_TESTE / f"{stem}.xlsx"
        wb.save(dest)
        print(f"OK {dest}")


if __name__ == "__main__":
    assert sum(s[5] for s in SES) == 200
    assert sum(s[5] for s in SES_500) == 500
    assert sum(s[5] for s in SES_1000) == 1000
    gerar(SES_1000, "base-teste-20se-1000itens")
