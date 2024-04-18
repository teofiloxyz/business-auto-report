import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

from date_utils import DateUtils


class Charts:
    def __init__(self, chart_path: str) -> None:
        self.date_utils = DateUtils()
        self.chart_path = chart_path

    def get_daily_sales_homologous_month_chart(self, df: pd.DataFrame) -> None:
        self._config_chart_theme()
        sns.barplot(
            data=df, x="year_month", y="daily_sales_average", palette="winter"
        )
        past_3_months_average = round(df["daily_sales_average"][:-1].mean(), 2)
        plt.axhline(
            y=past_3_months_average,
            color="cyan",
            label=f"Past 3 months average: {past_3_months_average}",
        )
        title = "Month + Previous 3 Homologous Months of Daily Sales Average"
        self._config_chart_tags(title=title)
        self._save_chart()

    def _config_chart_theme(self, soft_grid: bool = False) -> None:
        plt.figure(figsize=(11, 8.5))
        rc = {"grid.alpha": 0.2 if soft_grid else 1}
        sns.set_theme(style="darkgrid", rc=rc)
        plt.style.use("dark_background")

    def _config_chart_tags(
        self, title: str, xlabel: str = "Year-Month", ylabel: str = "Amount"
    ) -> None:
        plt.title(title)
        plt.xlabel(xlabel)
        plt.xticks(rotation=45)
        plt.ylabel(ylabel)
        plt.legend(title="Legend")

    def _save_chart(self) -> None:
        plt.savefig(
            self.chart_path, format="pdf", dpi=300, orientation="landscape"
        )
        plt.close()
