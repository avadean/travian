from report import Report
from tools import assertListOfObj


class World:
    def __init__(self, name: str = None, reports: list[Report] = None):
        assert isinstance(name, str)
        assertListOfObj(reports, Report)

        self.name = name
        self.reports = reports

    def __str__(self):
        return f'reports: {len(self.reports)}\n'

    def addReports(self, reports: list[Report] = None):
        assertListOfObj(reports, Report)

        self.reports += reports

    def getPlayers(self):
        players = {report.attacker for report in self.reports}

        players.update({report.defender for report in self.reports})

        players = list(players)

        players = sorted(players)

        return players
