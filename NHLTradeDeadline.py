from Team import Team
import ImportData

start_year = 2010
end_year = 2020

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

    #gather all of the rosters of the last ten years. store them in a dictionary of the form: {Season: [Roster]}

    #first create a new Team object for the team entered
    team = Team(team_name)

    rosters = {} #initialize roster dictionary

    #get all rosters of the last ten years using by creating Roster objects from the team object
    for i in range(start_year - 1, end_year):
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

def team_success(team):

    '''if the team made a trade, determine where they finished that season, for every season over the
    last ten years. Missed playoffs? Made playoffs? won 1st rnd? won 2nd rnd? won conf final? won cup? Break out each
    possibility and show a % of each.''' 

    '''
    define a new dictionary, format {'Season': [Success]} where [Success] is a list of 6 boolean elements. 
    index 0 - made playoffs
    index 1 - won 1st rnd
    index 2 - won 2nd rnd
    index 3 - won conf final
    index 4 - made cup
    index 5 - won cup
    '''
    success = {}
    made_playoffs_count = 0
    won_1st_rnd_count = 0
    won_2nd_rnd_count = 0
    won_3rd_rnd_count = 0
    made_cup_count = 0
    won_cup_count = 0

    #fill all seasons with list of success data
    for i in range(start_year, end_year):
        success[str(i) + str(i+1)] = ImportData.playoff_success(team, str(i) + str(i+1))
    
    #get counts for all possibilities over the last 10 years
    for values in success.values():
        k = 0
        for value in values:
            if k == 0 and value == True:
                made_playoffs_count += 1
            elif k == 1 and value == True:
                won_1st_rnd_count += 1
            elif k == 2 and value == True:
                won_2nd_rnd_count += 1
            elif k == 3 and value == True:
                won_3rd_rnd_count += 1
            elif k == 4 and value == True:
                made_cup_count += 1
            elif k == 5 and value == True:
                won_cup_count += 1
            k += 1

    counts = [made_playoffs_count, won_1st_rnd_count, won_2nd_rnd_count, won_3rd_rnd_count, made_cup_count, won_cup_count]
    return counts

team = introduction()
rosters = get_rosters(team)
counts = team_success(team)

def print_data(team, counts, rosters):

    #get total trades count over the 10 years
    trade_count = 0
    for i in range(start_year, end_year):
        if made_trade(rosters, str(i) + str(i+1)):
            trade_count += 1
    
    print("\nThe {team_name} have made {trade_count} trades from {start_year} to {end_year}. Their playoff success is as follows:\n"
    .format(team_name=team, trade_count=trade_count, start_year=start_year, end_year=end_year))

    print("Made Playoffs: " + str(counts[0]))
    print("Won 1st Round: " + str(counts[1]))
    print("Won 2nd Round: " + str(counts[2]))
    print("Won Conference Final: " + str(counts[3]))
    print("Won Cup: " + str(counts[5]) + "\n")
    

   
    
print_data(team, counts, rosters)

