import tempfile

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from .date_utils import DateUtils


class Charts:
    def __init__(self) -> None:
        self.date_utils = DateUtils()

    def get_homologous_daily_sales_chart(self, df: pd.DataFrame) -> str:
        self._config_chart_theme()
        sns.barplot(
            data=df, x="year_month", y="average_daily_sales", palette="winter"
        )
        past_3_months_average = df["average_daily_sales"][:-1].mean()
        plt.axhline(
            y=past_3_months_average,
            color="cyan",
            label=f"Past 3 months average: € {past_3_months_average:,.2f}",
        )
        title = "Month + Previous 3 Homologous Months of Daily Sales Average"
        self._config_chart_tags(title=title)
        return self._save_chart()

    def get_homologous_daily_expenses_chart(self, df: pd.DataFrame) -> str:
        self._config_chart_theme()
        sns.barplot(
            data=df,
            x="year_month",
            y="average_daily_expenses",
            palette="spring",
        )
        past_3_months_average = df["average_daily_expenses"][:-1].mean()
        plt.axhline(
            y=past_3_months_average,
            color="cyan",
            label=f"Past 3 months average: € {past_3_months_average:,.2f}",
        )
        title = "Month + Previous 3 Homologous Months of Daily Expenses Average"
        self._config_chart_tags(title=title)
        return self._save_chart()

    def get_homologous_daily_ibt_chart(self, df: pd.DataFrame) -> str:
        self._config_chart_theme()
        sns.barplot(
            data=df,
            x="year_month",
            y="average_daily_ibt",
            palette="summer",
        )
        past_3_months_average = df["average_daily_ibt"][:-1].mean()
        plt.axhline(
            y=past_3_months_average,
            color="cyan",
            label=f"Past 3 months average: € {past_3_months_average:,.2f}",
        )
        title = "Month + Previous 3 Homologous Months of Daily Income Before Taxes Average"
        self._config_chart_tags(title=title)
        return self._save_chart()

    def get_12_months_daily_sales_chart(self, df: pd.DataFrame) -> str:
        self._config_chart_theme()
        sns.barplot(
            data=df, x="year_month", y="average_daily_sales", palette="winter"
        )
        past_11_months_average = df["average_daily_sales"][:-1].mean()
        plt.axhline(
            y=past_11_months_average,
            color="cyan",
            label=f"Past 11 months average: € {past_11_months_average:,.2f}",
        )
        title = "Month + Previous 11 Months of Daily Sales Average"
        self._config_chart_tags(title=title)
        return self._save_chart()

    def get_12_months_daily_expenses_chart(self, df: pd.DataFrame) -> str:
        self._config_chart_theme()
        sns.barplot(
            data=df,
            x="year_month",
            y="average_daily_expenses",
            palette="spring",
        )
        past_11_months_average = df["average_daily_expenses"][:-1].mean()
        plt.axhline(
            y=past_11_months_average,
            color="cyan",
            label=f"Past 11 months average: € {past_11_months_average:,.2f}",
        )
        title = "Month + Previous 11 Months of Daily Expenses Average"
        self._config_chart_tags(title=title)
        return self._save_chart()

    def get_12_months_daily_ibt_chart(self, df: pd.DataFrame) -> str:
        self._config_chart_theme()
        sns.barplot(
            data=df,
            x="year_month",
            y="average_daily_ibt",
            palette="summer",
        )
        past_11_months_average = df["average_daily_ibt"][:-1].mean()
        plt.axhline(
            y=past_11_months_average,
            color="cyan",
            label=f"Past 11 months average: € {past_11_months_average:,.2f}",
        )
        title = (
            "Month + Previous 11 Months of Daily Income Before Taxes Average"
        )
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
