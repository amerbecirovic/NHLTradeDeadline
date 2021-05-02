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
