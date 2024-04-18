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
    pass
