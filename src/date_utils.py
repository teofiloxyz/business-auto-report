import calendar
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from typing import Tuple, List


class DateUtils:
    def decompose_year_month(self, year_month: str) -> Tuple[int, int]:
        year, month = map(int, year_month.split("-"))
        return year, month

    def get_previous_year_month(self, year_month: str) -> str:
        current_ym = datetime.strptime(year_month, "%Y-%m")
        previous_ym = current_ym - relativedelta(months=1)
        return previous_ym.strftime("%Y-%m")

    def get_next_year_month(self, year_month: str) -> str:
        current_ym = datetime.strptime(year_month, "%Y-%m")
        next_ym = current_ym + relativedelta(months=1)
        return next_ym.strftime("%Y-%m")

    def get_num_days(self, year_month: str) -> int:
        year, month = self.decompose_year_month(year_month)
        return calendar.monthrange(year, month)[1]

    def get_month_name(self, month_num: int) -> str:
        try:
            return calendar.month_name[month_num]
        except (IndexError, KeyError):
            return "Invalid month number..."
