import requests
import json

#function to create a Python dictionary out of NHL API json data
def create_dict(response):
    raw_data_dict = json.loads(json.dumps(response.json()))
    return raw_data_dict

#function to print all teams in the league, sorted in order
def print_all_teams():

    #declare list to get raw data from the request. declare new dictionary to parse a list of unsorted teams
    raw_data = []
    unsorted_teams = {}

    #make the request
    response = requests.get("https://statsapi.web.nhl.com/api/v1/teams/")
    raw_data.append(create_dict(response))

    #fill the unsorted teams dictionary with all of the teams in the league
    for i in range(0, 31):
        unsorted_teams[i] = raw_data[0]['teams'][i]['name']

    #sort the dictionary in alphabetical order
    sorted_teams_list = sorted(unsorted_teams.values())
    sorted_teams = {}

    for i in range(0, 31):
        sorted_teams[i] = sorted_teams_list[i]

    counter = 1
    for team in sorted_teams.values():
        print(str(counter) + " - " + team)
        counter += 1

#function to get team roster data
def get_roster(team_name):
    pass
