import ImportData

class Team:
    def __init__(self, team_name):
        self.team_name = team_name
        self.roster = self.Roster(self.team_name)

    def get_team_name(self):
        return self.team_name

    class Roster:
        def __init__(self, team_name):
            self.roster = ImportData.get_roster(team_name)

