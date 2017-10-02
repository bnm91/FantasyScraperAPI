import os
import MatchupDetails
from flask import Flask
from flask import request


##TODO: add begin and end week params
##TODO: add number of teams
##TODO: add exception handling

app = Flask(__name__)

@app.route('/getMatchupDetails', methods=['GET'])
def get_matchup_details():
    error = None
    if request.method == 'POST':
            return 'Hi there post'
    else:
        print request.args
        if request.args.get('leagueId') == None:
            return 'error: leagueId not specified'
        elif request.args.get('leagueName') == None:
            return 'error: leagueName not specified'
        elif request.args.get('seasonId') == None:
            return 'error: seasonId not specified'
        elif request.args.get('leagueSize') == None:
            return 'error: leagueSize not sepcified'
        else:
            output_string = MatchupDetails.get_matchup_details(request.args.get('leagueId'), request.args.get('leagueName'), request.args.get('seasonId'), request.args.get('leagueSize'),  1, 1)
            return output_string
            # return {'text': 'testText'}
            # return 'text \r\n text'

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

