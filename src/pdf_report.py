import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
import sys
import tempfile
from typing import Dict, List

import fitz

from .date_utils import DateUtils

SCR_PATH = os.path.dirname(sys.argv[0])


class PDFReport:
    def __init__(self, year_month: str) -> None:
        self.date_utils = DateUtils()
        filename = f"generated_report_{year_month}.pdf"
        self.pdf_path = os.path.join(SCR_PATH, f"docs/{filename}")
        self.text_pdf_path = tempfile.NamedTemporaryFile(
            suffix=".pdf", delete=False
        ).name
        self.text_report = TextReport(self.text_pdf_path)
        title = self._get_title(year_month)
        self.text_report.add_title(title)

    def add_month_overview(self, month_ovr: Dict[str, float]) -> None:
        paragraph = (
            f"This month, the business achieved € {month_ovr['sales']:,.2f} "
            f"in sales and incurred € {month_ovr['expenses']:,.2f} in expenses. "
            f"With a gross profit of € {month_ovr['gross']:,.2f} "
            f"({month_ovr['gross_mg']:.2f}% of margin) "
            f"and EBITDA totaling € {month_ovr['EBITDA']:,.2f} "
            f"({month_ovr['EBITDA_mg']:.2f}% of margin), "
            f"the earnings before taxes amounted to € {month_ovr['EBT']:,.2f} "
            f"({month_ovr['EBT_mg']:.2f}% of margin). "
        )
        self.text_report.add_paragraph(paragraph)

    def add_homologous_performance(
        self, homologous_pf: Dict[str, float]
    ) -> None:
        paragraph = (
            f"This month, total sales performed {homologous_pf['sales']:.2f}%, "
            f"total expenses {homologous_pf['expenses']:.2f}%, "
            f"gross profit {homologous_pf['gross']:.2f}%, "
            f"EBITDA {homologous_pf['EBITDA']:.2f}%, "
            f"and earnings before taxes {homologous_pf['EBT']:.2f}%, "
            "compared to the average of the previous three years."
        )
        self.text_report.add_paragraph(paragraph)

    def add_in_chain_performance(self, in_chain_pf: Dict[str, float]) -> None:
        paragraph = (
            f"This month, total sales performed {in_chain_pf['sales']:.2f}%, "
            f"total expenses {in_chain_pf['expenses']:.2f}%, "
            f"gross profit {in_chain_pf['gross']:.2f}%, "
            f"EBITDA {in_chain_pf['EBITDA']:.2f}%, "
            f"and earnings before taxes {in_chain_pf['EBT']:.2f}%, "
            "compared to the previous month."
        )
        self.text_report.add_paragraph(paragraph)

    def generate_report(self, charts_paths: List[str]) -> None:
        paragraph = "Please, take a look at the charts in the next pages."
        self.text_report.add_paragraph(paragraph)
        self.text_report.generate()
        self._append_charts_to_report(charts_paths)

    def _get_title(self, year_month: str) -> str:
        year, month = self.date_utils.decompose_year_month(year_month)
        month_name = self.date_utils.get_month_name(month)
        return f"Report for {month_name} of {year}"

    def _append_charts_to_report(self, charts_paths: List[str]) -> None:
        text_pdf = fitz.open(self.text_pdf_path)
        for chart_path in charts_paths:
            chart_pdf = fitz.open(chart_path)
            text_pdf.insert_pdf(chart_pdf)
            chart_pdf.close()
            os.remove(chart_path)
        text_pdf.save(self.pdf_path)
        text_pdf.close()
        os.remove(self.text_pdf_path)


class TextReport:
    def __init__(self, text_pdf_path: str) -> None:
        self.doc = SimpleDocTemplate(
            text_pdf_path,
            title="Business Report",
            pagesize=letter,
        )
        self._load_carlito_font()
        self.text_styles = self._get_text_styles()
        self.flowables = []

    def add_title(self, title_text: str) -> None:
        title = Paragraph(title_text, self.text_styles["title"])
        self.flowables.append(title)
        self.flowables.append(Spacer(1, 60))

    def add_paragraph(self, paragraph_text: str) -> None:
        paragraph = Paragraph(paragraph_text, self.text_styles["paragraph"])
        self.flowables.append(paragraph)
        self.flowables.append(Spacer(1, 8))

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
                name="Title", fontSize=34, fontName="Carlito Bold", alignment=1
            ),
            "paragraph": ParagraphStyle(
                name="Paragraph", fontSize=20, fontName="Carlito", leading=22
            ),
        }
