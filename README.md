# FantasyScraperAPI



### Base URL

https://espn-fantasy-api.herokuapp.com/



### CSV 
*For all GET requests, you can add /csv to the URL to return data as a CSV instead of JSON*

Example:
https://espn-fantasy-api.herokuapp.com/LeagueScoreboard/csv?leagueId=1234&seasonId=2017&leagueName=XXXX&beginWeek=1&endWeek=4


### Matchup Details

*Week by week, player by player scoring*

###### GET MatchupDetails

Example:
https://espn-fantasy-api.herokuapp.com/MatchupDetails?leagueId=1234&seasonId=2017&leagueSize=10&leagueName=PanthersFanLeague

###### Parameters

* leagueID
  * integer
  * League's ID number. Found in URL for league office. Example: http://games.espn.com/ffl/leagueoffice?leagueId=######&seasonId=2017
* seasonID
  * integer (year)
  * The calendar year the season began in
* leagueSize
  * integer
  * The number of teams in the league
* leagueName - optional
  * string (no quotation marks)
  * API user defined name of the league. Useful if dealing with multiple leagues
* beginWeek - optional
  * integer
  * First week of the range of weeks to be retrieved
* endWeek - optional
  * integer
  * Last week of the range of weeks to be retrieved


### League Scoreboard

*Week by week, matchup by matchup scores from the league

###### GET LeagueScoreboard

Example:
https://espn-fantasy-api.herokuapp.com/LeagueScoreboard?leagueId=1234&seasonId=2017&leagueName=XXXX&beginWeek=1&endWeek=4

###### Parameters

* leagueID
  * integer
  * League's ID number. Found in URL for league office. Example: http://games.espn.com/ffl/leagueoffice?leagueId=######&seasonId=2017
* seasonID
  * integer (year)
  * The calendar year the season began in
* leagueName - optional
  * string (no quotation marks)
  * API user defined name of the league. Useful if dealing with multiple leagues
* beginWeek - optional
  * integer
  * First week of the range of weeks to be retrieved
* endWeek - optional
  * integer
  * Last week of the range of weeks to be retrieved
