from bs4 import BeautifulSoup
import lxml
import requests
import os, csv
import json
from fantasyScaperUtils import utils

HEADER_ROW = {'Week': 'Week', 'Season': 'Season', 'Home': 'Home_Team', 'Scoreboard_Points_Home':'Scoreboard_Points_Home', 'Away': 'Away', 'Scoreboard_Points_Away': 'Scoreboard_Points_Away'}


def get_league_scoreboard(league_id, league_name, season_id, begin_week=None, end_week=None):
    output_dict = {}
    output_dict['league_scoreboard'] = scrape_league_scoreboard(league_id, league_name, season_id, begin_week, end_week)
    return json.dumps(output_dict)
    

def get_league_scoreboard_csv(league_id, league_name, season_id, begin_week=None, end_week=None):
    row_list = scrape_league_scoreboard(league_id, league_name, season_id, begin_week, end_week)
    return utils.create_csv_from_list(row_list, HEADER_ROW)

#
#scrapes fantasy scoreboard results
# returns dict: week, season, home team, home team points, away team, away team points
def scrape_league_scoreboard(league_id, league_name, season_id, begin_week=None, end_week=None):
    if begin_week is None:
        begin_week = 1
    if end_week is None:
        end_week = 17

    league_scoreboard_list = [] #a list of strings of comma separated values


    for wk in range(int(begin_week), int(end_week) + 1):

        #URL form example: http://games.espn.go.com/ffl/scoreboard?leagueId=######&matchupPeriodId=1\
        url = 'http://games.espn.go.com/ffl/scoreboard?leagueId=' + league_id + '&matchupPeriodId=' + str(wk)

        #scraping the page
        response = requests.get(url) 
        data = response.text
        soup = BeautifulSoup(data)
        matchup_tables = soup.find_all('table', class_='ptsBased matchup') #narrowing down to only the tables on the page with scoreboard information

        scoreboard_data = {}

        for matchup in matchup_tables:
            scoreboard_data = get_scoreboard_data(matchup)
            league_scoreboard_list.append(create_row_object(scoreboard_data, wk, season_id, league_name))

    return league_scoreboard_list

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


def create_row_object(scoreboard_data, week, season_id, league_name):
    csv_row = {'Week': week, 'Season': season_id, 'Home': scoreboard_data['owner_home'], 'Scoreboard_Points_Home': scoreboard_data['score_home'], 'Away': scoreboard_data['owner_away'], 'Scoreboard_Points_Away': scoreboard_data['score_away'], 'League_Name': league_name}
    return csv_row
