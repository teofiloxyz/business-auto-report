from typing import Optional

from .charts import Charts
from .data_manager import DataManager
from .pdf_report import PDFReport


class BusinessAutoReport:
    def __init__(self) -> None:
        self.ch = Charts()
        self.dm = DataManager()

    def generate_report(self, year_month: Optional[str] = None) -> None:
        if not year_month:
            year_month = self._choose_year_month()

        print(f"Generating report for {year_month}...")
        pdf_rep = PDFReport(year_month)

        month_ovr = self.dm.get_month_overview(year_month)
        pdf_rep.add_month_overview(month_ovr)
        homologous_pf = self.dm.get_homologous_performance(year_month)
        pdf_rep.add_homologous_performance(homologous_pf)
        in_chain_pf = self.dm.get_in_chain_performance(year_month)
        pdf_rep.add_in_chain_performance(in_chain_pf)

        charts_paths = []
        df_hom = self.dm.get_homologous_df(year_month)
        charts_paths.append(self.ch.get_homologous_daily_sales_chart(df_hom))
        charts_paths.append(self.ch.get_homologous_daily_expenses_chart(df_hom))
        charts_paths.append(self.ch.get_homologous_daily_ibt_chart(df_hom))

        df_12m = self.dm.get_12_months_df(year_month)
        charts_paths.append(self.ch.get_12_months_daily_sales_chart(df_12m))
        charts_paths.append(self.ch.get_12_months_daily_expenses_chart(df_12m))
        charts_paths.append(self.ch.get_12_months_daily_ibt_chart(df_12m))

        df_hom_ytd = self.dm.get_homologous_ytd_df(year_month)
        charts_paths.append(self.ch.get_homologous_ytd_chart(df_hom_ytd))

        df_by_pro = self.dm.get_total_sales_by_product_df(year_month)
        charts_paths.append(self.ch.get_total_sales_by_product_chart(df_by_pro))

        pdf_rep.generate_report(charts_paths)

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
