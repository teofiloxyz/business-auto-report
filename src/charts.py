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
            data=df,
            x="year_month",
            y="average_daily_sales",
            hue="year_month",
            palette="winter",
            legend=False,
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
            hue="year_month",
            palette="spring",
            legend=False,
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

    def get_homologous_daily_ebt_chart(self, df: pd.DataFrame) -> str:
        self._config_chart_theme()
        sns.barplot(
            data=df,
            x="year_month",
            y="average_daily_EBT",
            hue="year_month",
            palette="summer",
            legend=False,
        )
        past_3_months_average = df["average_daily_EBT"][:-1].mean()
        plt.axhline(
            y=past_3_months_average,
            color="cyan",
            label=f"Past 3 months average: € {past_3_months_average:,.2f}",
        )
        title = "Month + Previous 3 Homologous Months of Daily Earnings Before Taxes Average"
        self._config_chart_tags(title=title)
        return self._save_chart()

    def get_12_months_daily_sales_chart(self, df: pd.DataFrame) -> str:
        self._config_chart_theme()
        sns.barplot(
            data=df,
            x="year_month",
            y="average_daily_sales",
            hue="year_month",
            palette="winter",
            legend=False,
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
            hue="year_month",
            palette="spring",
            legend=False,
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

    def get_12_months_daily_ebt_chart(self, df: pd.DataFrame) -> str:
        self._config_chart_theme()
        sns.barplot(
            data=df,
            x="year_month",
            y="average_daily_EBT",
            hue="year_month",
            palette="summer",
            legend=False,
        )
        past_11_months_average = df["average_daily_EBT"][:-1].mean()
        plt.axhline(
            y=past_11_months_average,
            color="cyan",
            label=f"Past 11 months average: € {past_11_months_average:,.2f}",
        )
        title = (
            "Month + Previous 11 Months of Daily Earnings Before Taxes Average"
        )
        self._config_chart_tags(title=title)
        return self._save_chart()

    def get_homologous_ytd_gross_chart(self, df: pd.DataFrame) -> str:
        self._config_chart_theme(soft_grid=True)
        sns.lineplot(
            data=df, x="year", y="ytd_total_sales", label="YTD Total Sales"
        )
        sns.lineplot(
            data=df, x="year", y="ytd_total_COGS", label="YTD Total COGS"
        )
        plt.fill_between(
            df["year"], df["ytd_total_sales"], color="orange", alpha=0.5
        )
        plt.fill_between(
            df["year"], df["ytd_total_COGS"], color="blue", alpha=0.5
        )
        title = (
            "Homologous YTD of Total Sales and Cost of Sold Goods of All Years"
        )
        self._config_chart_tags(title=title, xlabel="Year")
        return self._save_chart()

    def get_homologous_ytd_chart(self, df: pd.DataFrame) -> str:
        self._config_chart_theme(soft_grid=True)
        sns.lineplot(
            data=df, x="year", y="ytd_total_sales", label="YTD Total Sales"
        )
        sns.lineplot(
            data=df,
            x="year",
            y="ytd_total_expenses",
            label="YTD Total Expenses",
        )
        plt.fill_between(
            df["year"], df["ytd_total_sales"], color="orange", alpha=0.5
        )
        plt.fill_between(
            df["year"], df["ytd_total_expenses"], color="blue", alpha=0.5
        )
        title = "Homologous YTD of Total Sales and Expenses of All Years"
        self._config_chart_tags(title=title, xlabel="Year")
        return self._save_chart()

    def get_total_sales_by_product_chart(self, df: pd.DataFrame) -> str:
        self._config_chart_theme()
        sns.barplot(
            data=df,
            x="total_sales",
            y="product",
            hue="total_sales",
            palette="Blues",
            legend=False,
        )
        title = "Total Revenue of the Month Decomposed By Product"
        self._config_chart_tags(
            title=title, xlabel="Amount", ylabel="Product", legend=False
        )
        return self._save_chart()

    def get_total_expenses_by_category_chart(self, df: pd.DataFrame) -> str:
        self._config_chart_theme()
        sns.barplot(
            data=df,
            x="total_expenses",
            y="category",
            hue="total_expenses",
            palette="Reds",
            legend=False,
        )
        title = "Total Expenses of the Month Decomposed By Category"
        self._config_chart_tags(
            title=title, xlabel="Amount", ylabel="Category", legend=False
        )
        return self._save_chart()

    def _config_chart_theme(self, soft_grid: bool = False) -> None:
        plt.figure(figsize=(11, 8.5))
        rc = {"grid.alpha": 0.2 if soft_grid else 1}
        sns.set_theme(style="darkgrid", rc=rc)
        plt.style.use("dark_background")

    def _config_chart_tags(
        self,
        title: str,
        xlabel: str = "Year-Month",
        ylabel: str = "Amount",
        legend: bool = True,
    ) -> None:
        plt.title(title)
        plt.xlabel(xlabel)
        plt.xticks(rotation=45)
        plt.ylabel(ylabel)
        if legend:
            plt.legend(title="Legend")

    def _save_chart(self) -> str:
        ch_path = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False).name
        plt.savefig(ch_path, format="pdf", dpi=300, orientation="landscape")
        plt.close()
        return ch_path
