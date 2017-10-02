# FantasyScraperAPI



### Base URL

https://fantasy-scraper-api.herokuapp.com/


### Matchup Details

*Week by week, player by player scoring*

###### GET getMatchupDetails

Example:
https://fantasy-scraper-api.herokuapp.com/getMatchupDetails?leagueId=1234&seasonId=2017&leagueSize=10&leagueName=PanthersFanLeague

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
