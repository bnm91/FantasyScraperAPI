from bs4 import BeautifulSoup
import lxml
import requests
import os, csv
import json

HEADER_ROW = {'Owner': 'Owner', 'Player': 'Player', 'Week':'Week', 'Season':'Season', 'Player_Opponent':'Player_Opponent', 'Player_Home':'Player_Home', 'Points':'Points', 'Roster_Slot':'Roster_Slot', 'League':'League', 'nfl_team':'nfl_team', 'nfl_position': 'nfl_position'}


def get_matchup_details(league_id, league_name, season_id, league_size, begin_week=None, end_week=None):
    output_dict = scrape_matchup_details(league_id, league_name, season_id, league_size, begin_week, end_week)
    return json.dumps(output_dict)

def get_matchup_details_csv(league_id, league_name, season_id, league_size, begin_week=None, end_week=None):
    output_dict = scrape_matchup_details(league_id, league_name, season_id, league_size, begin_week, end_week)
    return create_csv_from_json(output_dict, HEADER_ROW)

#
#scrapes Fantasy results player by player
#
def scrape_matchup_details(league_id, league_name, season_id, league_size, begin_week=None, end_week=None):

    try:
        if begin_week is None:
            begin_week = 1
        if end_week is None:
            end_week = 17

        matchup_details_list = []
        output_dict = {}

        # HEADER_ROW = {'Owner': 'Owner', 'Player': 'Player', 'Week':'Week', 'Season':'Season', 'Player_Opponent':'Player_Opponent', 'Player_Home':'Player_Home', 'Points':'Points', 'Roster_Slot':'Roster_Slot', 'League':'League', 'nfl_team':'nfl_team', 'nfl_position': 'nfl_position'}
        # matchup_details_list.append(comma_separate_values(HEADER_ROW))

        for wk in range(int(begin_week), int(end_week) + 1):
            owners = []
        
            for team_id in range(1, int(league_size) + 1):
                #example http://games.espn.go.com/ffl/boxscorequick?leagueId=457631&teamId=1&scoringPeriodId=1&seasonId=2015&view=scoringperiod&version=quick

                response = requests.get('http://games.espn.go.com/ffl/boxscorequick?leagueId=' + str(league_id) + '&teamId=' + str(team_id) + '&scoringPeriodId=' + str(wk) + '&seasonId=' + str(season_id) + '&view=scoringperiod&version=quick')
                data = response.text
                soup = BeautifulSoup(data)
                owner_divs = soup.find_all('div', class_='teamInfoOwnerData')

                if len(owner_divs) > 0:
                
                    owner_home = owner_divs[0].get_text()
                    if len(owner_divs) == 1:
                        #print 'only 1 owner'
                        break
                    else:
                        owner_away = owner_divs[1].get_text()
                        
                        if owner_away not in owners and owner_home not in owners:
                            owners.append(owner_away)
                            owners.append(owner_home)
                            
                            team_tables = soup.find_all('table', class_='playerTableTable')
                            
                            home_team_starters_table = team_tables[0]
                            home_team_bench_table = team_tables[1]
                            
                            away_team_starters_table = team_tables[2]
                            away_team_bench_table = team_tables[3]
                            
                            home_team_player_rows = home_team_starters_table.find_all('tr', class_='pncPlayerRow')
                            
                            #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                            # Team 1 Starters
                            for row in home_team_player_rows:

                                player_data = get_player_row(row, 1)
                                matchup_details_list.append(create_row_object(player_data, owner_home, wk, season_id, league_name))
                            
                            #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                            # Team 1 Bench
                            home_team_bench_player_rows = home_team_bench_table.find_all('tr', class_='pncPlayerRow')
                            
                            for row in home_team_bench_player_rows:
                                player_data = get_player_row(row, 1)                                 
                                
                                matchup_details_list.append(create_row_object(player_data, owner_home, wk, season_id, league_name))
                            
                            #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                            # Team 2 Starters
                            away_team_player_rows = away_team_starters_table.find_all('tr', class_='pncPlayerRow')
                            
                            for row in away_team_player_rows:
                                player_data = get_player_row(row, 0)
                                matchup_details_list.append(create_row_object(player_data, owner_away, wk, season_id, league_name))
                            
                            #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                            # Team 2 Bench Players
                            away_team_bench_player_rows = away_team_bench_table.find_all('tr', class_='pncPlayerRow')
                            
                            for row in away_team_bench_player_rows:
                                player_data = get_player_row(row, 0)
                                
                                matchup_details_list.append(create_row_object(player_data, owner_away, wk, season_id, league_name))
        
        output_dict['matchup_details'] = matchup_details_list

        return output_dict          
    except Exception as ex:
        return 'Error occurred : ' + str(ex)


def get_player_row(row, home):

    return_row = {}
    columns = row.findChildren('td')
    
    player_anchors = columns[1].find_all('a')

    if not player_anchors:
        return_row['player_name'] = ''
    else:
        return_row['player_name'] = player_anchors[0].get_text()
    
    return_row['roster_slot'] = columns[0].get_text()
    return_row['player_opponent'] = columns[2].get_text()
    return_row['home'] = home

    if '@' in return_row['player_opponent']:
        return_row['home'] = 0
        return_row['player_opponent'] = return_row['player_opponent'][1:]
    
    if  'BYE' in columns[2].get_text():
        return_row['points'] = columns[3].get_text()
        return_row['home']  = 1
    else:
        return_row['points'] = columns[4].get_text()
        
    if '--' in return_row['points']:
        return_row['points'] = '0'
    
    if columns[1] is None:
        s=''
    else:
        s = columns[1].get_text()
        
        return_row['nfl_position'] = ''
        return_row['nfl_team'] = ''
        
        if 'D/ST' in s:
            return_row['nfl_position'] = 'D/ST'
            return_row['nfl_team'] = ''
        else:
            if ', ' in s:
                # print s
                start = s.rindex(', ') + len (', ')
                e = s.find(u'\xa0')
                # print s.split(u'\xa0')[1]
                return_row['nfl_team'] = s[start:e]
                return_row['nfl_position'] = s.split(u'\xa0')[1]

    return return_row


def create_csv_from_json(matchup_details_json, header_row):
    csv_list = []
    csv_list.append(comma_separate_values(header_row))

    for details in matchup_details_json['matchup_details']:
        csv_list.append(comma_separate_values(details))
    
    return csv_list_to_csv_string(csv_list)


def create_row_object(player_data, owner, week, season_id, league_name):
    csv_row = {'Owner': owner, 'Player': player_data['player_name'], 'Week':str(week), 'Season':str(season_id), 'Player_Opponent':player_data['player_opponent'], 'Player_Home':str(player_data['home']), 'Points':player_data['points'], 'Roster_Slot':player_data['roster_slot'], 'League':str(league_name), 'nfl_team': player_data['nfl_team'], 'nfl_position':player_data['nfl_position']}
    return csv_row


def comma_separate_values(row_dict):
    row_string = ''
    row_string += row_dict['Owner'] + ','
    row_string += row_dict['Player'] + ','
    row_string += row_dict['Week'] + ','
    row_string += row_dict['Season'] + ','
    row_string += row_dict['Player_Opponent'] + ','
    row_string += row_dict['Player_Home'] + ','
    row_string += row_dict['Points'] + ','
    row_string += row_dict['Roster_Slot'] + ','
    row_string += row_dict['League'] + ','
    row_string += row_dict['nfl_team'] + ','
    row_string += row_dict['nfl_position']

    return row_string

def csv_list_to_csv_string(csv_list):
    csv_string = ''
    for row in csv_list:
        csv_string += row
        csv_string += ' <br />'
    return csv_string


def find_between_r(s, first):
    try:
        start = s.rindex(first) + len(first)
        end = s.find(u'\xa0')
        return s[start:end]
    except ValueError:
        return ""




