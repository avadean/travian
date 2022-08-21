from tools import assertListOfObj
from report import Report


class Database:
    def __init__(self, reports: list[Report] = None):
        assertListOfObj(reports, Report)

        self.reports = reports

    def __str__(self):
        return f'reports: {len(self.reports)}\n'

    def addReports(self, reports: list[Report] = None):
        assertListOfObj(reports, Report)

        self.reports += reports
