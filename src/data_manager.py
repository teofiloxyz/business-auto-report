import pandas as pd

import os
import sqlite3
import sys
from typing import Any, Dict

from date_utils import DateUtils

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
        return {"sales": sales, "expenses": expenses}

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

    def get_homologous_performance(self, year_month: str) -> float:
        # add expenses in the future
        year, month = self.date_utils.decompose_year_month(year_month)
        query = f"""
            SELECT SUM(unit_price * quantity) / COUNT(DISTINCT date) AS average_daily_sales
            FROM sales_fact
            LEFT JOIN products_dim ON sales_fact.product_id = products_dim.product_id
            WHERE strftime('%Y-%m', date) >= '{year-3}-{month:02d}'
            AND strftime('%Y-%m', date) <= '{year_month}'
            AND strftime('%Y-%m', date) = '{month:02d}'
        """
        df = self.db.fetch_df_from_db(query)
        previous = df.iloc[:-1].mean()
        current = df.iloc[-1]
        return (current - previous) / previous * 100
