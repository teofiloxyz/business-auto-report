from typing import Callable, List, Optional, Tuple

from tqdm import tqdm

from .charts import Charts
from .data_manager import DataManager
from .pdf_report import PDFReport


class BusinessAutoReport:
    def __init__(self) -> None:
        self.ch = Charts()
        self.dm = DataManager()

    def generate_report(self, year_month: Optional[str] = None) -> None:
        year_month = year_month or self._choose_year_month()
        pdf_rep = PDFReport(year_month)
        gen_steps = self._get_generation_steps(year_month, pdf_rep)

        print(f"Generating report for {year_month}.")
        self._execute_generation_steps(gen_steps)
        print(f"Report for {year_month} is complete.")

    def _choose_year_month(self) -> str:
        first_ym = self.dm.get_first_db_year_month()
        lastest_ym = self.dm.get_latest_db_year_month()
        while True:
            year_month = input(
                f"Enter the year-month (between {first_ym} & {lastest_ym}): "
            )
            try:
                year, month = map(int, year_month.split("-"))
            except ValueError:
                print("Invalid input...")
                continue
            year_month = f"{year}-{month:02d}"
            if first_ym <= year_month <= lastest_ym:
                return year_month
            print(f"Invalid year-month. Try between {first_ym} & {lastest_ym}")

    def _get_generation_steps(
        self, year_month: str, pdf_rep: PDFReport
    ) -> List[Tuple[str, Callable]]:
        return [
            (
                "Adding month overview",
                lambda: pdf_rep.add_month_overview(
                    self.dm.get_month_overview(year_month)
                ),
            ),
            (
                "Adding homologous performance",
                lambda: pdf_rep.add_homologous_performance(
                    self.dm.get_homologous_performance(year_month)
                ),
            ),
            (
                "Adding in-chain performance",
                lambda: pdf_rep.add_in_chain_performance(
                    self.dm.get_in_chain_performance(year_month)
                ),
            ),
            (
                "Getting homologous daily sales chart",
                lambda: self.ch.get_homologous_daily_sales_chart(
                    self.dm.get_homologous_df(year_month)
                ),
            ),
            (
                "Getting homologous daily expenses chart",
                lambda: self.ch.get_homologous_daily_expenses_chart(
                    self.dm.get_homologous_df(year_month)
                ),
            ),
            (
                "Getting homologous daily EBT chart",
                lambda: self.ch.get_homologous_daily_ebt_chart(
                    self.dm.get_homologous_df(year_month)
                ),
            ),
            (
                "Getting 12 months daily sales chart",
                lambda: self.ch.get_12_months_daily_sales_chart(
                    self.dm.get_12_months_df(year_month)
                ),
            ),
            (
                "Getting 12 months daily expenses chart",
                lambda: self.ch.get_12_months_daily_expenses_chart(
                    self.dm.get_12_months_df(year_month)
                ),
            ),
            (
                "Getting 12 months daily EBT chart",
                lambda: self.ch.get_12_months_daily_ebt_chart(
                    self.dm.get_12_months_df(year_month)
                ),
            ),
            (
                "Getting homologous YTD gross chart",
                lambda: self.ch.get_homologous_ytd_gross_chart(
                    self.dm.get_homologous_ytd_gross_df(year_month)
                ),
            ),
            (
                "Getting homologous YTD chart",
                lambda: self.ch.get_homologous_ytd_chart(
                    self.dm.get_homologous_ytd_df(year_month)
                ),
            ),
            (
                "Getting total sales by product chart",
                lambda: self.ch.get_total_sales_by_product_chart(
                    self.dm.get_total_sales_by_product_df(year_month)
                ),
            ),
            (
                "Getting total expenses by category chart",
                lambda: self.ch.get_total_expenses_by_category_chart(
                    self.dm.get_total_expenses_by_category_df(year_month)
                ),
            ),
            (
                "Appending charts into final PDF",
                lambda: pdf_rep.generate_report(self.charts_paths),
            ),
        ]

    def _execute_generation_steps(
        self, gen_steps: List[Tuple[str, Callable]]
    ) -> None:
        """Increment the progress bar while executing the steps"""

        self.charts_paths = []
        with tqdm(total=len(gen_steps), desc="Generating Report") as pbar:
            for description, step_func in gen_steps:
                pbar.set_description(description)
                output = step_func()
                if output:
                    self.charts_paths.append(output)
                pbar.update(1)
