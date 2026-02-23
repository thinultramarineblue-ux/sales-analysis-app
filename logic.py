# py logic.py



import csv
from datetime import datetime

class SalesLogic:

    def __init__(self, filename):
        self.filename = filename
        self.data = self._load_data()

    def _load_data(self):
        try:
            with open(self.filename, encoding="utf-8") as f:
                return list(csv.DictReader(f))
        except FileNotFoundError:
            return []

    def filter_by_period(self, start, end):
        try:
            start_date = datetime.strptime(start, "%Y-%m-%d")
            end_date = datetime.strptime(end, "%Y-%m-%d")
        except ValueError:
            return None

        filtered = []

        for row in self.data:
            try:
                row_date = datetime.strptime(row["日付"], "%Y-%m-%d")
            except ValueError:
                continue

            if start_date <= row_date <= end_date:
                filtered.append(row)

        return filtered

    def total_by_column(self, column, data=None):

        if data is None:
            data = self.data

        result = {}

        for row in data:
            key = row[column]
            try:
                total = int(row["単価"]) * int(row["数量"])
            except ValueError:
                continue

            result[key] = result.get(key, 0) + total

        return result
