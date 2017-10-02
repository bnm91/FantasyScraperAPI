
from bs4 import BeautifulSoup
import lxml
import requests
import os, csv


def commaSeparateValues(rowDict):
    rowString = ''
    rowString += rowDict['Owner'] + ','
    rowString += rowDict['Player'] + ','
    rowString += rowDict['Week'] + ','
    rowString += rowDict['Season'] + ','
    rowString += rowDict['Player_Opponent'] + ','
    rowString += rowDict['Player_Home'] + ','
    rowString += rowDict['Points'] + ','
    rowString += rowDict['Roster_Slot'] + ','
    rowString += rowDict['League'] + ','
    rowString += rowDict['NflTeam'] + ','
    rowString += rowDict['NflPosition']

    return rowString

def csvListToCsvString(csvList):
    csvString = ''
    for row in csvList:
        csvString += row
        csvString += ' <br />'
    return csvString


def find_between_r(s, first, last):
    try:
        start = s.rindex(first) + len(first)
        end = s.find(u'\xa0')
        return s[start:end]
    except ValueError:
        return ""


def getPlayerRow(row, home):

    returnRow = {}
    columns = row.findChildren('td')
    
    playerAnchors = columns[1].find_all('a')

    if not playerAnchors:
        returnRow['playerName'] = ''
    else:
        returnRow['playerName'] = playerAnchors[0].get_text()
    

    returnRow['rosterSlot'] = columns[0].get_text()
    returnRow['playerOpponent'] = columns[2].get_text()
    returnRow['home'] = home

    if '@' in returnRow['playerOpponent']:
        returnRow['home'] = 0
        returnRow['playerOpponent'] = returnRow['playerOpponent'][1:]
        
    if  'BYE' in columns[2].get_text():
        returnRow['points'] = columns[3].get_text()
        returnRow['home']  = 1
    else:
        returnRow['points'] = columns[4].get_text()
        
    if '--' in returnRow['points']:
        returnRow['points'] = '0'
    
    if columns[1] is None:
        s=''
    else:
        s = columns[1].get_text()
        #print  str(wk) +  owner2
        
        returnRow['nflPosition'] = ''
        returnRow['nflTeam'] = ''
        
        if 'D/ST' in s:
            returnRow['nflPosition'] = 'D/ST'
            returnRow['nflTeam'] = ''
        else:
            if ', ' in s:
                print s
                start = s.rindex(', ') + len (', ')
                e = s.find(u'\xa0')
                print s.split(u'\xa0')[1]
                returnRow['nflTeam'] = s[start:e]
                returnRow['nflPosition'] = s.split(u'\xa0')[1]

    return returnRow


def createCSVRow(playerData, owner, week, seasonId, leagueName):
    csvRow = {'Owner': owner, 'Player': playerData['playerName'], 'Week':str(week), 'Season':str(seasonId), 'Player_Opponent':playerData['playerOpponent'], 'Player_Home':str(playerData['home']), 'Points':playerData['points'], 'Roster_Slot':playerData['rosterSlot'], 'League':str(leagueName), 'NflTeam': playerData['nflTeam'], 'NflPosition':playerData['nflPosition']}
    return commaSeparateValues(csvRow)


#
#scrapes Fantasy results player by player
#for each week
#
def getMatchupDetails(leagueId, leagueName, seasonId, leagueSize, beginWeek=None, endWeek=None):

    try:
        if beginWeek == None:
            beginWeek = 1
        if endWeek == None:
            endWeek = 17

        csvList = []

        headerRow = {'Owner': 'Owner', 'Player': 'Player', 'Week':'Week', 'Season':'Season', 'Player_Opponent':'Player_Opponent', 'Player_Home':'Player_Home', 'Points':'Points', 'Roster_Slot':'Roster_Slot', 'League':'League', 'NflTeam':'NflTeam', 'NflPosition': 'NflPosition'}
        csvList.append(commaSeparateValues(headerRow))

        for wk in range(beginWeek, endWeek + 1):
            print wk
            owners = []
        
            for teamId in range(1, int(leagueSize) + 1):
                #http://games.espn.go.com/ffl/boxscorequick?leagueId=457631&teamId=1&scoringPeriodId=1&seasonId=2015&view=scoringperiod&version=quick

                r = requests.get('http://games.espn.go.com/ffl/boxscorequick?leagueId=' + str(leagueId) + '&teamId=' + str(teamId) + '&scoringPeriodId=' + str(wk) + '&seasonId=' + str(seasonId) + '&view=scoringperiod&version=quick')
                
                data = r.text

                soup = BeautifulSoup(data)
                
                ownerDivs = soup.find_all('div', class_='teamInfoOwnerData')
                
                
                if len(ownerDivs) > 0:
                
                    owner1 = ownerDivs[0].get_text()
                    if len(ownerDivs) == 1:
                        print 'only 1 owner'
                    else:
                        owner2 = ownerDivs[1].get_text()		
                        
                        if owner2 not in owners and owner1 not in owners:
                            owners.append(owner2)
                            owners.append(owner1)
                            
                            teamTables = soup.find_all('table', class_='playerTableTable')
                            
                            team1StartersTable = teamTables[0]
                            team1BenchTable = teamTables[1]
                            
                            team2StartersTable = teamTables[2]
                            team2BenchTable = teamTables[3]
                            
                            team1PlayerRows = team1StartersTable.find_all('tr', class_='pncPlayerRow')
                            
                            #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                            # Team 1 Starters
                            for row in team1PlayerRows:

                                playerData = getPlayerRow(row, 1)
                                csvList.append(createCSVRow(playerData, owner1, wk, seasonId, leagueName))
                            
                            #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                            # Team 1 Bench
                            team1BenchPlayerRows = team1BenchTable.find_all('tr', class_='pncPlayerRow')
                            
                            for row in team1BenchPlayerRows:
                                playerData = getPlayerRow(row, 1)                                 
                                
                                csvList.append(createCSVRow(playerData, owner1, wk, seasonId, leagueName))
                            
                            #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                            # Team 2 Starters
                            team2PlayerRows = team2StartersTable.find_all('tr', class_='pncPlayerRow')
                            
                            for row in team2PlayerRows:
                                playerData = getPlayerRow(row, 0)
                                csvList.append(createCSVRow(playerData, owner2, wk, seasonId, leagueName))
                            
                            #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                            # Team 2 Bench Players
                            team2BenchPlayerRows = team2BenchTable.find_all('tr', class_='pncPlayerRow')
                            
                            for row in team2BenchPlayerRows:
                                playerData = getPlayerRow(row, 0)                             
                                
                                csvList.append(createCSVRow(playerData, owner2, wk, seasonId, leagueName))

        return csvListToCsvString(csvList)            
    except Exception as e:
        return 'Error occurred : ' + str(e)