from bs4 import BeautifulSoup
import lxml
import requests
import os, csv


#
#scrapes fantasy scoreboard results
# returns: week, season, home team, home team points, away team, away team points
#
def get_league_scoreboard(league_id, league_name, season_id, begin_week=None, end_week=None):
    if begin_week is None:
        begin_week = 1
    if end_week is None:
        end_week = 17

    csv_list = [] #a list of strings of comma separated values

    HEADER_ROW = {'Week': 'Week', 'Season': 'Season', 'Home': 'Home_Team', 'Scoreboard_Points_Home':'Scoreboard_Points_Home', 'Away': 'Away', 'Scoreboard_Points_Away': 'Scoreboard_Points_Away'}
    csv_list.append(comma_separate_values(HEADER_ROW))

    for wk in range(int(begin_week), int(end_week) + 1):

        #URL form example: http://games.espn.go.com/ffl/scoreboard?leagueId=######&matchupPeriodId=1\
        url = 'http://games.espn.go.com/ffl/scoreboard?leagueId=' + league_id + '&matchupPeriodId=' + str(wk)

        #scraping the page
        response = requests.get(url) 
        data = response.text
        soup = BeautifulSoup(data)
        matchups = soup.find_all('table', class_='ptsBased matchup') #narrowing down to only the tables on the page with scoreboard information

        scoreboard_data = {}

        for matchup in matchups:
            scoreboard_data = get_scoreboard_data(matchup)
            csv_list.append(create_csv_row(scoreboard_data, wk, season_id, league_name))

    return csv_list_to_csv_string(csv_list)

#get the scoreboard data from a matchup table
def get_scoreboard_data(matchup):
    scoreboard_data = {}

    owners = matchup.find_all('span', class_='owners')
    scores = matchup.find_all('td', class_='score')
    scoreboard_data['owner_away'] = owners[0].get_text().split(",")[0] #teams can multiple owners, we only want the first one
    scoreboard_data['owner_home'] = owners[1].get_text().split(",")[0]
    scoreboard_data['score_away'] = scores[0].get_text()
    scoreboard_data['score_home'] = scores[1].get_text()
    return scoreboard_data

#creates a dictionary describing a League Scoreboard row and then breaks that into a csv row string
def create_csv_row(scoreboard_data, week, season_id, league_name):
    csv_row = {'Week': week, 'Season': season_id, 'Home': scoreboard_data['owner_home'], 'Scoreboard_Points_Home': scoreboard_data['score_home'], 'Away': scoreboard_data['owner_away'], 'Scoreboard_Points_Away': scoreboard_data['score_away'], 'League_Name': league_name}
    return comma_separate_values(csv_row)


# breaks dictionary describing a League Scoreboard row into a csv row
def comma_separate_values(row_dict):
    row_string = ''
    row_string += str(row_dict['Week']) + ','
    row_string += row_dict['Season'] + ','
    row_string += row_dict['Home'] + ','
    row_string += row_dict['Scoreboard_Points_Home'] + ','
    row_string += row_dict['Away'] + ','
    row_string += row_dict['Scoreboard_Points_Away']

    return row_string


# transforms list of rows of csv strings into a single "cvs file" string that is presentable on the web
def csv_list_to_csv_string(csv_list):
    csv_string = ''
    for row in csv_list:
        csv_string += row
        csv_string += ' <br />'
    return csv_string