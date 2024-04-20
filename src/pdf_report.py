import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
import sys
from typing import Dict

from .date_utils import DateUtils

SCR_PATH = os.path.dirname(sys.argv[0])


class PDFReport:
    def __init__(self, year_month: str) -> None:
        self.date_utils = DateUtils()
        filename = f"generated_report_{year_month}.pdf"
        self.pdf_path = os.path.join(SCR_PATH, f"docs/{filename}")
        self.text = TextReport(self.pdf_path)
        title = self._get_title(year_month)
        self.text.add_title(title)

    def add_month_overview(self, month_ovr: Dict[str, float]) -> None:
        paragraph = (
            f"The business made € {month_ovr['sales']:,.2f} in sales this month, "
            f"and incurred € {month_ovr['expenses']:,.2f} in expenses."
        )
        self.text.add_paragraph(paragraph)

    def add_homologous_performance(self, homologous_pf: float) -> None:
        paragraph = (
            f"The total sales this month performed {homologous_pf:.2f}% "
            "compared to the average of the previous three years."
        )
        self.text.add_paragraph(paragraph)

    def add_in_chain_performance(self, in_chain_pf: float) -> None:
        paragraph = (
            "The total sales' in-chain performance this month "
            f"was {in_chain_pf:.2f}%."
        )
        self.text.add_paragraph(paragraph)

    def generate(self) -> None:
        self.text.generate()

    def _get_title(self, year_month: str) -> str:
        year, month = self.date_utils.decompose_year_month(year_month)
        month_name = self.date_utils.get_month_name(month)
        return f"Report for {month_name} of {year}"


class TextReport:
    def __init__(self, first_page_path: str) -> None:
        page_width, page_height = letter
        page_width_pixels = page_width * 230 / 72
        page_height_pixels = page_height * 230 / 72
        self.doc = SimpleDocTemplate(
            first_page_path,
            title="Business Report",
            pagesize=(page_width_pixels, page_height_pixels),
        )
        self._load_carlito_font()
        self.text_styles = self._get_text_styles()
        self.flowables = []

    def add_title(self, title_text: str) -> None:
        title = Paragraph(title_text, self.text_styles["title"])
        self.flowables.append(title)
        self.flowables.append(Spacer(1, 200))

    def add_paragraph(self, paragraph_text: str) -> None:
        paragraph = Paragraph(paragraph_text, self.text_styles["paragraph"])
        self.flowables.append(paragraph)
        self.flowables.append(Spacer(1, 35))

    def generate(self) -> None:
        self.doc.build(self.flowables)

    def _load_carlito_font(self) -> None:
        carlito_path = "/usr/share/fonts/carlito/Carlito-Regular.ttf"
        carlitob_path = "/usr/share/fonts/carlito/Carlito-Bold.ttf"
        pdfmetrics.registerFont(TTFont("Carlito", carlito_path))
        pdfmetrics.registerFont(TTFont("Carlito Bold", carlitob_path))

    def _get_text_styles(self) -> Dict[str, ParagraphStyle]:
        return {
            "title": ParagraphStyle(
                name="Title", fontSize=120, fontName="Carlito Bold", alignment=1
            ),
            "paragraph": ParagraphStyle(
                name="Paragraph", fontSize=70, fontName="Carlito", leading=75
            ),
        }
