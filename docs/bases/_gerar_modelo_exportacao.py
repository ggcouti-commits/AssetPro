"""Gera docs/bases/modelo-exportacao.xlsx (aba Itens, tabela tblItens)."""
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.table import Table, TableStyleInfo

out = Path(__file__).resolve().parent / "modelo-exportacao.xlsx"

headers = [
    "CodAsset",
    "Imobilizado",
    "CodSE",
    "NomeSE",
    "TI",
    "LocalInstalacao",
    "CM",
    "ArranjoFisico",
    "CodTUC",
    "DescricaoTUC",
    "A1",
    "A2",
    "A3",
    "A4",
    "A5",
    "A6",
    "DescricaoBem",
    "Quantidade",
    "QuantidadeCampo",
    "Unidade",
    "Elegivel",
    "Reserva",
    "Fabricante",
    "Modelo",
    "NumSerie",
    "Ano",
    "Bay",
    "CodOperacao",
    "Projeto",
    "Observacoes",
    "Status",
    "ValidadoPor",
    "Origem",
    "Sobra",
    "CoordX",
    "CoordY",
]

wb = Workbook()
ws = wb.active
ws.title = "Itens"
ws.append(headers)
ws.append([""] * len(headers))

header_fill = PatternFill("solid", fgColor="1B3E6F")
header_font = Font(color="FFFFFF", bold=True, name="Calibri", size=11)
left = Alignment(horizontal="left", vertical="center", wrap_text=False)
for col, name in enumerate(headers, 1):
    cell = ws.cell(1, col)
    cell.fill = header_fill
    cell.font = header_font
    cell.alignment = Alignment(horizontal="left", vertical="center")
    body = ws.cell(2, col)
    body.fill = PatternFill(fill_type=None)
    body.font = Font(color="000000", name="Calibri", size=11)
    body.alignment = left
    width = 36 if name in ("DescricaoBem", "DescricaoTUC", "NomeSE", "Observacoes") else 16
    ws.column_dimensions[get_column_letter(col)].width = width

ref = f"A1:{get_column_letter(len(headers))}2"
ws.add_table(
    Table(
        displayName="tblItens",
        ref=ref,
        tableStyleInfo=TableStyleInfo(
            name="TableStyleLight1",
            showRowStripes=True,
            showColumnStripes=False,
        ),
    )
)
ws.freeze_panes = "A2"
wb.save(out)
print(out, out.stat().st_size)
