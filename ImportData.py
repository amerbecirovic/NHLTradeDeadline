import requests
import json

#declare empty list for storing raw data retrieved from request, global variable so it can be used by other functions.
raw_data = []

#make the request, store the data in raw_data
response = requests.get("https://statsapi.web.nhl.com/api/v1/teams/")
raw_data_dict = json.loads(json.dumps(response.json()))
raw_data.append(raw_data_dict)

#function to print all teams in the league, sorted in order
def print_all_teams():

    #declare new dictionary to parse a list of unsorted teams
    unsorted_teams = {}

    #fill the unsorted teams dictionary with all of the teams in the league
    for i in range(0, 31):
        unsorted_teams[i] = raw_data[0]['teams'][i]['name']

    #sort the teams in alphabetical order
    sorted_teams_list = sorted(unsorted_teams.values())

    for team in sorted_teams_list:
        print(team)

    return sorted_teams_list

def get_team_id(team_name):

    for teams in raw_data[0]['teams']:
        if team_name in teams['name']:
            return teams['id']

#function to get team roster data
def get_roster(team_id, season):
    #make the API request, store the data
    raw_roster_data = []
    response = requests.get("https://statsapi.web.nhl.com/api/v1/teams/" + str(team_id) + "/?expand=team.roster&season=" + season)
    raw_data_dict = json.loads(json.dumps(response.json()))
    raw_roster_data.append(raw_data_dict)

    full_roster = {}

    for player in raw_roster_data[0]['teams'][0]['roster']['roster']:

        full_roster[player['person']['fullName']] = player['person']['id']

    return full_roster


def was_traded(player_id, season):

    traded = False

    raw_player_data = []
    response = requests.get("https://statsapi.web.nhl.com/api/v1/people/" + str(player_id) + "/stats?stats=gameLog&season=" + season)
    raw_data_dict = json.loads(json.dumps(response.json()))
    raw_player_data.append(raw_data_dict)

    for i in range(len(raw_player_data[0]['stats'][0]['splits'])):

        if i == len(raw_player_data[0]['stats'][0]['splits']) - 1:
            return False

        current_team = raw_player_data[0]['stats'][0]['splits'][i]['team']['name']
        next_team = raw_player_data[0]['stats'][0]['splits'][i+1]['team']['name']
        if current_team != next_team:
            return True

    return False

def cup_winner(season):

    raw_playoff_data = []
    response = requests.get("https://statsapi.web.nhl.com/api/v1/tournaments/playoffs?expand=round.series,schedule.game.seriesSummary&season=" + season)
    raw_data_dict = json.loads(json.dumps(response.json()))
    raw_playoff_data.append(raw_data_dict)
    
    winner_str = raw_playoff_data[0]['rounds'][3]['series'][0]['currentGame']['seriesSummary']['seriesStatus']
    winner = winner_str.split()[0]

    return winner



def playoff_success(team, season):
    #for given team and season entered, return the 6 boolean element status array.
    success = [False] * 6
    team_name = team.split()[-1]

    raw_playoff_data = []
    response = requests.get("https://statsapi.web.nhl.com/api/v1/tournaments/playoffs?expand=round.series,schedule.game.seriesSummary&season=" + season)
    raw_data_dict = json.loads(json.dumps(response.json()))
    raw_playoff_data.append(raw_data_dict)

    num_rounds = 4

    #get all matchups in a dictionary in the form of {round_number: [matchups]} for comparison
    matchups = {}
    for rounds in raw_playoff_data[0]['rounds']:
        round_number = rounds['number']
        series_list = []
        for series in rounds['series']:
            series_list.append(series['names']['matchupName'])
        matchups[round_number] = series_list

    for i in range(1, num_rounds + 1):

        if i == 1:
            for matchup in matchups[i]:
                if team_name in matchup:
                    success[0] = True

        elif i == 2:
            for matchup in matchups[i]:
                if team_name in matchup:
                    for k in range(0,2):
                        success[k] = True

        elif i == 3:
            for matchup in matchups[i]:
                if team_name in matchup:
                    for k in range(0,3):
                        success[k] = True

        elif i == 4 and team_name in matchups[i][0]:
            for k in range(0,5):
                success[k] = True
            if team_name == cup_winner(season):
                success[5] = True

    return success