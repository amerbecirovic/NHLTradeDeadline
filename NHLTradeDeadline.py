from Team import Team
import ImportData

def introduction():
    print("\nChoose a team from the list to view their trade deadline performance: \n")
    all_teams = ImportData.print_all_teams()
    
    while True:
        try:
            team_name = input("\nEnter team name: ")
            if team_name not in all_teams:
                raise ValueError
            break
        except ValueError:
            print("Not a valid team name, try again.")

    return team_name

    
def get_rosters(team_name):

    '''gather all of the rosters of the last ten years. store them in a dictionary of the form: {Season: [Roster]}
    call analysis(rosters)'''

    #first create a new Team object for the team entered
    team = Team(team_name)
    start_year = 2011 #first year we're looking at
    end_year = 2021 #last year we're looking at

    rosters = {} #initialize roster dictionary

    #get all rosters of the last ten years using by creating Roster objects from the team object
    for i in range(start_year, end_year):
        rosters[str(i) + str(i+1)] = team.get_roster(str(i) + str(i+1))
    
    return rosters

def made_trade(rosters, season):

    '''compare rosters x and x-1 to determine if players were added to the team for each season.'''

    #compare current season to the previous season. see what the differences are.
    current_roster = rosters[season]
    #print(current_roster.roster)

    previous_season_x = season[:4]
    previous_season_y = season[4:]
    previous_season = str(int(previous_season_x) - 1) + str(int(previous_season_y) - 1)

    previous_roster = rosters[previous_season]

    set_difference = set(current_roster.get_players()) - set(previous_roster.get_players())
    list_difference = list(set_difference)

    #for each player added, check if they were traded that season to confirm the player was a trade and not a signing.
   
    for player in list_difference:
        player_id = current_roster.roster[player]
        if ImportData.was_traded(player_id, season):
            return True

    return False

def made_playoffs(team):
    pass

def won_1st_rnd(team):
    pass

def won_2nd_rnd(team):
    pass

def won_conf_final(team):
    pass

def won_cup(team):
    pass

def team_success(team):

    '''if the team made a trade, determine where they finished that season, for every season over the
    last ten years. Missed playoffs? Made playoffs? won 1st rnd? won 2nd rnd? won conf final? won cup? Break out each
    possibility and show a % of each.''' 

    pass


team = introduction()
rosters = get_rosters(team)

