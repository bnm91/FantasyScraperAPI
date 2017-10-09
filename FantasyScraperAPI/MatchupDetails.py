from bs4 import BeautifulSoup
import lxml
import requests
import os, csv
import json
import utils

HEADER_ROW = {'Owner': 'Owner', 'Player': 'Player', 'Week':'Week', 'Season':'Season', 'Player_Opponent':'Player_Opponent', 'Player_Home':'Player_Home', 'Points':'Points', 'Roster_Slot':'Roster_Slot', 'League':'League', 'nfl_team':'nfl_team', 'nfl_position': 'nfl_position'}


def get_matchup_details(league_id, league_name, season_id, league_size, begin_week=None, end_week=None):
    output_dict = {}
    output_dict['matchup_details'] = scrape_matchup_details(league_id, league_name, season_id, league_size, begin_week, end_week)
    return json.dumps(output_dict)

def get_matchup_details_csv(league_id, league_name, season_id, league_size, begin_week=None, end_week=None):
    row_list = scrape_matchup_details(league_id, league_name, season_id, league_size, begin_week, end_week)
    return utils.create_csv_from_list(row_list, HEADER_ROW)

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

                            #TODO: clean up this function and call so it's more readable
                            matchup_details_list.extend(get_matchup_details_from_table(home_team_starters_table, owner_home, wk, season_id, league_name))
                            matchup_details_list.extend(get_matchup_details_from_table(home_team_bench_table, owner_home, wk, season_id, league_name))
                            matchup_details_list.extend(get_matchup_details_from_table(away_team_starters_table, owner_away, wk, season_id, league_name))
                            matchup_details_list.extend(get_matchup_details_from_table(away_team_bench_table, owner_away, wk, season_id, league_name))
                        
        return matchup_details_list          
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
        s =''
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


def get_matchup_details_from_table(table, owner_name, wk, season_id, league_name):
    return_list = []
    matchup_detail_rows = table.find_all('tr', class_='pncPlayerRow')
    for row in matchup_detail_rows:
        player_data = get_player_row(row, 1)                                 
        return_list.append(create_row_object(player_data, owner_name, wk, season_id, league_name))
    
    return return_list


def create_row_object(player_data, owner, week, season_id, league_name):
    csv_row = {'Owner': owner, 'Player': player_data['player_name'], 'Week':str(week), 'Season':str(season_id), 'Player_Opponent':player_data['player_opponent'], 'Player_Home':str(player_data['home']), 'Points':player_data['points'], 'Roster_Slot':player_data['roster_slot'], 'League':str(league_name), 'nfl_team': player_data['nfl_team'], 'nfl_position':player_data['nfl_position']}
    return csv_row
