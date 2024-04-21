import tempfile

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from .date_utils import DateUtils


class Charts:
    def __init__(self) -> None:
        self.date_utils = DateUtils()

    def get_daily_sales_homologous_chart(self, df: pd.DataFrame) -> str:
        self._config_chart_theme()
        sns.barplot(
            data=df, x="year_month", y="average_daily_sales", palette="winter"
        )
        past_3_months_average = round(df["average_daily_sales"][:-1].mean(), 2)
        plt.axhline(
            y=past_3_months_average,
            color="cyan",
            label=f"Past 3 months average: {past_3_months_average}",
        )
        title = "Month + Previous 3 Homologous Months of Daily Sales Average"
        self._config_chart_tags(title=title)
        return self._save_chart()

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

    def _save_chart(self) -> str:
        ch_path = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False).name
        plt.savefig(ch_path, format="pdf", dpi=300, orientation="landscape")
        plt.close()
        return ch_path
