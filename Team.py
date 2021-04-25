import ImportData

class Team:
    def __init__(self, team_name):
        self.team_name = team_name
        self.team_id = self.get_team_id()

    def get_team_name(self):
        return self.team_name

    def get_team_id(self):
        return ImportData.get_team_id(self.team_name)

    def get_roster(self, season):
        return self.Roster(self, season)

    #roster for season X
    class Roster:
        def __init__(self, team, season):
            self.team = team
            self.roster = ImportData.get_roster(self.team_id(), season)

        def team_id(self):
            return self.team.team_id

        def print_roster(self):
            for player in self.roster:
                print(player)
        



