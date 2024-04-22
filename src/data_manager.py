import os
import sqlite3
import sys
from typing import Any, Dict

import pandas as pd

from .date_utils import DateUtils

SCR_PATH = os.path.dirname(sys.argv[0])


class Database:
    def __init__(self) -> None:
        self.db_path = os.path.join(SCR_PATH, "database.db")

    def connect(self) -> None:
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def disconnect(self) -> None:
        self.conn.close()

    def fetch_result(self, query: str) -> Any:
        self.connect()
        result = self.conn.execute(query).fetchone()
        self.disconnect()
        return result

    def fetch_df_from_db(self, query: str) -> pd.DataFrame:
        self.connect()
        df = pd.read_sql_query(query, self.conn)
        self.disconnect()
        return df


class DataManager:
    def __init__(self) -> None:
        self.db = Database()
        self.date_utils = DateUtils()

    def get_first_db_year_month(self) -> str:
        query = f"""
            SELECT strftime('%Y-%m', MIN(date)) AS year_month
            FROM sales_fact
        """
        return self.db.fetch_result(query)[0]

    def get_latest_db_year_month(self) -> str:
        query = f"""
            SELECT strftime('%Y-%m', MAX(date)) AS year_month
            FROM sales_fact
        """
        return self.db.fetch_result(query)[0]

    def get_month_overview(self, year_month: str) -> Dict[str, float]:
        sales = self._get_total_sales(year_month)
        expenses = self._get_total_expenses(year_month)
        income_before_taxes = sales - expenses
        return {
            "sales": sales,
            "expenses": expenses,
            "IBT": income_before_taxes,
        }

    def _get_total_sales(self, year_month: str) -> float:
        query = f"""
            SELECT SUM(sales_fact.quantity * products_dim.unit_price) AS total_sales
            FROM sales_fact
            LEFT JOIN products_dim ON sales_fact.product_id = products_dim.product_id
            WHERE strftime('%Y-%m', sales_fact.date) = '{year_month}'
        """
        return self.db.fetch_result(query)[0]

    def _get_total_expenses(self, year_month: str) -> float:
        query = f"""
            SELECT SUM(amount) AS total_expenses
            FROM expenses_fact
            WHERE strftime('%Y-%m', date) = '{year_month}'
        """
        return self.db.fetch_result(query)[0]

    def get_homologous_performance(self, year_month: str) -> Dict[str, float]:
        """Didn't refactor the SQL queries for readability reasons"""

        df = self.get_homologous_df(year_month)
        return {
            "sales": self._get_perf_percentage(df, "average_daily_sales"),
            "expenses": self._get_perf_percentage(df, "average_daily_expenses"),
            "IBT": self._get_perf_percentage(df, "average_daily_ibt"),
        }

    def get_homologous_df(self, year_month: str) -> pd.DataFrame:
        year, month = self.date_utils.decompose_year_month(year_month)
        df_sales = self._get_homologous_sales_df(year, month)
        df_expenses = self._get_homologous_expenses_df(year, month)
        return self._get_daily_averages_df(df_sales, df_expenses)

    def _get_homologous_sales_df(self, year: int, month: int) -> pd.DataFrame:
        query = f"""
            SELECT strftime('%Y-%m', date) AS year_month,
            SUM(unit_price * quantity) AS total_sales
            FROM sales_fact
            LEFT JOIN products_dim ON sales_fact.product_id = products_dim.product_id
            WHERE strftime('%Y', date) >= '{year-3}'
            AND strftime('%Y', date) <= '{year}'
            AND strftime('%m', date) = '{month:02d}'
            GROUP by year_month
        """
        return self.db.fetch_df_from_db(query)

    def _get_homologous_expenses_df(
        self, year: int, month: int
    ) -> pd.DataFrame:
        query = f"""
            SELECT strftime('%Y-%m', date) AS year_month,
            SUM(amount) AS total_expenses
            FROM expenses_fact
            WHERE strftime('%Y', date) >= '{year-3}'
            AND strftime('%Y', date) <= '{year}'
            AND strftime('%m', date) = '{month:02d}'
            GROUP by year_month
        """
        return self.db.fetch_df_from_db(query)

    def _get_daily_averages_df(
        self, df_sales: pd.DataFrame, df_expenses: pd.DataFrame
    ) -> pd.DataFrame:
        df = pd.merge(df_sales, df_expenses, on="year_month", how="left")
        df["num_days"] = df["year_month"].apply(
            lambda x: self.date_utils.get_num_days(x)
        )
        df["average_daily_sales"] = df["total_sales"] / df["num_days"]
        df["average_daily_expenses"] = df["total_expenses"] / df["num_days"]
        df["average_daily_ibt"] = (
            df["average_daily_sales"] - df["average_daily_expenses"]
        )
        return df

    def _get_perf_percentage(self, df: pd.DataFrame, column: str) -> float:
        current = df.iloc[-1][column]
        previous = df.iloc[:-1][column].mean()
        return ((current - previous) / previous) * 100

    def get_in_chain_performance(self, year_month: str) -> Dict[str, float]:
        df = self.get_12_months_df(year_month).tail(2).copy()
        return {
            "sales": self._get_perf_percentage(df, "average_daily_sales"),
            "expenses": self._get_perf_percentage(df, "average_daily_expenses"),
            "IBT": self._get_perf_percentage(df, "average_daily_ibt"),
        }

    def get_12_months_df(self, year_month: str) -> pd.DataFrame:
        year, month = self.date_utils.decompose_year_month(year_month)
        df_sales = self._get_12_months_sales_df(year, month)
        df_expenses = self._get_12_months_expenses_df(year, month)
        return self._get_daily_averages_df(df_sales, df_expenses)

    def _get_12_months_sales_df(self, year: int, month: int) -> pd.DataFrame:
        query = f"""
            SELECT strftime('%Y-%m', date) AS year_month,
            SUM(unit_price * quantity) AS total_sales
            FROM sales_fact
            LEFT JOIN products_dim ON sales_fact.product_id = products_dim.product_id
            WHERE strftime('%Y-%m', date) > '{year-1}-{month:02d}'
            AND strftime('%Y-%m', date) <= '{year}-{month:02d}'
            GROUP by year_month
        """
        return self.db.fetch_df_from_db(query)

    def _get_12_months_expenses_df(self, year: int, month: int) -> pd.DataFrame:
        query = f"""
            SELECT strftime('%Y-%m', date) AS year_month,
            SUM(amount) AS total_expenses
            FROM expenses_fact
            WHERE strftime('%Y-%m', date) > '{year-1}-{month:02d}'
            AND strftime('%Y-%m', date) <= '{year}-{month:02d}'
            GROUP by year_month
        """
        return self.db.fetch_df_from_db(query)

    def get_homologous_ytd_df(self, year_month: str) -> pd.DataFrame:
        _, month = self.date_utils.decompose_year_month(year_month)
        df_sales = self._get_homologous_ytd_sales_df(month)
        df_expenses = self._get_homologous_ytd_expenses_df(month)
        return pd.merge(df_sales, df_expenses, on="year", how="left")

    def _get_homologous_ytd_sales_df(self, month: int) -> pd.DataFrame:
        query = f"""
            SELECT strftime('%Y', date) AS year,
            SUM(unit_price * quantity) AS ytd_total_sales
            FROM sales_fact
            LEFT JOIN products_dim ON sales_fact.product_id = products_dim.product_id
            WHERE strftime('%m', date) <= '{month:02d}'
            AND strftime('%m', date) >= '01'
            GROUP by year
        """
        return self.db.fetch_df_from_db(query)

    def _get_homologous_ytd_expenses_df(self, month: int) -> pd.DataFrame:
        query = f"""
            SELECT strftime('%Y', date) AS year,
            SUM(amount) AS ytd_total_expenses
            FROM expenses_fact
            WHERE strftime('%m', date) <= '{month:02d}'
            AND strftime('%m', date) >= '01'
            GROUP by year
        """
        return self.db.fetch_df_from_db(query)

    def get_total_sales_by_product_df(self, year_month: str) -> pd.DataFrame:
        query = f"""
            SELECT SUM(unit_price * quantity) AS total_sales,
            name as product
            FROM sales_fact
            LEFT JOIN products_dim ON sales_fact.product_id = products_dim.product_id
            WHERE strftime('%Y-%m', date) = '{year_month}'
            GROUP by product
            ORDER BY total_sales DESC
        """
        return self.db.fetch_df_from_db(query)

    def _get_total_expenses_by_category_df(
        self, year_month: str
    ) -> pd.DataFrame:
        query = f"""
            SELECT SUM(amount) AS total_expenses,
            name as category
            FROM expenses_fact
            LEFT JOIN expenses_categories_dim ON expenses_fact.category_id = expenses_categories_dim.category_id
            WHERE strftime('%Y-%m', date) = '{year_month}'
            GROUP by category
            ORDER BY total_expenses DESC
        """
        return self.db.fetch_df_from_db(query)
