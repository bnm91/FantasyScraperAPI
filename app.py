import os
import MatchupDetails
import LeagueScoreboard
from flask import Flask
from flask import request


##TODO: add begin and end week params
##TODO: add number of teams
##TODO: add exception handling

app = Flask(__name__)

@app.route('/getMatchupDetails', methods=['GET'])
def get_matchup_details():
    error = None
    begin_week = None
    end_week = None

    if request.method == 'POST':
            return 'Hi there post'
    else:
        if request.args.get('beginWeek') is not None:
            begin_week = request.args.get('beginWeek')
        if request.args.get('endWeek') is not None:
            end_week = request.args.get('endWeek')

        if request.args.get('leagueId') == None:
            return 'error: leagueId not specified'
        elif request.args.get('leagueName') == None:
            return 'error: leagueName not specified'
        elif request.args.get('seasonId') == None:
            return 'error: seasonId not specified'
        elif request.args.get('leagueSize') == None:
            return 'error: leagueSize not sepcified'
        else:
            output = MatchupDetails.get_matchup_details(request.args.get('leagueId'), request.args.get('leagueName'), request.args.get('seasonId'), request.args.get('leagueSize'), end_week, begin_week)
            return output


@app.route('/getMatchupDetails/csv', methods=['GET'])
def get_matchup_details_csv():
    error = None
    begin_week = None
    end_week = None

    if request.method == 'POST':
            return 'Hi there post'
    else:
        if request.args.get('beginWeek') is not None:
            begin_week = request.args.get('beginWeek')
        if request.args.get('endWeek') is not None:
            end_week = request.args.get('endWeek')

        if request.args.get('leagueId') == None:
            return 'error: leagueId not specified'
        elif request.args.get('leagueName') == None:
            return 'error: leagueName not specified'
        elif request.args.get('seasonId') == None:
            return 'error: seasonId not specified'
        elif request.args.get('leagueSize') == None:
            return 'error: leagueSize not sepcified'
        else:
            output = MatchupDetails.get_matchup_details_csv(request.args.get('leagueId'), request.args.get('leagueName'), request.args.get('seasonId'), request.args.get('leagueSize'), end_week, begin_week)
            return output


@app.route('/getLeagueScoreboard', methods=['GET'])
def get_league_scoreboard():
    error = None
    begin_week = None
    end_week = None
    
    if request.method == 'POST':
            return 'Hi there post'
    else:
        if request.args.get('beginWeek') is not None:
            begin_week = request.args.get('beginWeek')
        if request.args.get('endWeek') is not None:
            end_week = request.args.get('endWeek')
        
        if request.args.get('leagueId') == None:
            return 'error: leagueId not specified'
        elif request.args.get('leagueName') == None:
            return 'error: leagueName not specified'
        elif request.args.get('seasonId') == None:
            return 'error: seasonId not specified'
        else:
            output_string = LeagueScoreboard.get_league_scoreboard(request.args.get('leagueId'), request.args.get('leagueName'), request.args.get('seasonId'), begin_week, end_week)
            return output_string

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

