
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



#
#scrapes Fantasy results player by player
#
def getMatchupDetails(leagueId, leagueName, seasonId, leagueSize, beginWeek=None, endWeek=None):

    try:
        if beginWeek == None:
            beginWeek = 1
        if endWeek == None:
            endWeek = 17

        csvList = []

        headerRow = {'Owner': 'Owner', 'Player': 'Player', 'Week':'Week', 'Season':'Season', 'Player_Opponent':'Player_Opponent', 'Player_Home':'Player_Home', 'Points':'Points', 'Roster_Slot':'Roster_Slot', 'League':'League', 'NflTeam':'NflTeam', 'NflPosition': 'NflPosition'}
        #writer.writerow(["Owner", "Player", "Week", "Season", "Player_Opponent", "Player_Home", "Points", "Roster_Slot", "League"])
        csvList.append(commaSeparateValues(headerRow))

        for wk in range(beginWeek, endWeek + 1):
            # print wk
            owners = []
        
            for teamId in range(1, int(leagueSize) + 1):
                #print(teamId)
                #http://games.espn.go.com/ffl/boxscorequick?leagueId=457631&teamId=1&scoringPeriodId=1&seasonId=2015&view=scoringperiod&version=quick

                r = requests.get('http://games.espn.go.com/ffl/boxscorequick?leagueId=' + str(leagueId) + '&teamId=' + str(teamId) + '&scoringPeriodId=' + str(wk) + '&seasonId=' + str(seasonId) + '&view=scoringperiod&version=quick')
                
                data = r.text

                soup = BeautifulSoup(data)
                
                ownerDivs = soup.find_all('div', class_='teamInfoOwnerData')
                
                
                if len(ownerDivs) > 0:
                
                    owner1 = ownerDivs[0].get_text()
                    if len(ownerDivs) == 1:
                        raise ValueError("only 1 owner")
                    else:
                        owner2 = ownerDivs[1].get_text()		
                        
                        #print owner1
                        #print owner2
                        
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
                                columns = row.findChildren('td')
                                
                                playerAnchors = columns[1].find_all('a')

                                if not playerAnchors:
                                    playerName = ''
                                else:
                                    playerName = playerAnchors[0].get_text()
                                

                                playerOpponent = columns[2].get_text()
                                home = 1
                            
                                if '@' in playerOpponent:
                                    home = 0
                                    playerOpponent = playerOpponent[1:]
                            
                                #playerTeam = find_between_r(columns[1].get_text(), ', ', '\\')
                                    
                                    
                                    
                                    
                                if  'BYE' in columns[2].get_text():
                                    points = columns[3].get_text()
                                    home = 1
                                else:
                                    points = columns[4].get_text()
                                    
                                if '--' in points:
                                    points = '0'
                                
                                if columns[1] is None:
                                    s=''
                                else:
                                    s = columns[1].get_text()
                                    #print  str(wk) +  owner2
                                    
                                    
                                    nflPosition = ''
                                    nflTeam = ''
                                    
                                    if 'D/ST' in s:
                                        nflPosition = 'D/ST'
                                        nflTeam = ''
                                    else:
                                        if ', ' in s:
                                            # print s
                                            start = s.rindex(', ') + len (', ')
                                            e = s.find(u'\xa0')
                                            # print s.split(u'\xa0')[1]
                                            nflTeam = s[start:e]
                                            nflPosition = s.split(u'\xa0')[1]
                                
                                #print 'about to write'
                                #print owner1
                                #print playerName
                                #print str(wk)
                                #print str(seasonId)
                                #print playerOpponent
                                #print str(home)
                                #print columns[4].get_text()
                                #print columns[0].get_text()
                                #print str(leagueName)
                                
                                # writer.writerow([owner1, playerName, str(wk), str(seasonYear), playerOpponent, str(home), points, columns[0].get_text(), str(leagueName), nflTeam, nflPosition])
                                row = {'Owner': owner1, 'Player': playerName, 'Week':str(wk), 'Season':str(seasonId), 'Player_Opponent':playerOpponent, 'Player_Home':str(home), 'Points':points, 'Roster_Slot':columns[0].get_text(), 'League':str(leagueName), 'NflTeam': nflTeam, 'NflPosition':nflPosition}
                                csvList.append(commaSeparateValues(row))
                            
                            #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                            # Team 1 Bench
                            team1BenchPlayerRows = team1BenchTable.find_all('tr', class_='pncPlayerRow')
                            
                            for row in team1BenchPlayerRows:
                                columns = row.findChildren('td')
                                
                                playerAnchors = columns[1].find_all('a')

                                if not playerAnchors:
                                    playerName = ''
                                else:
                                    playerName = playerAnchors[0].get_text()
                                

                                playerOpponent = columns[2].get_text()
                                home = 1
                            
                                if '@' in playerOpponent:
                                    home = 0
                                    playerOpponent = playerOpponent[1:]
                            
                                #playerTeam = find_between_r(columns[1].get_text(), ', ', '\\')
                                    
                                if  'BYE' in columns[2].get_text():
                                    points = columns[3].get_text()
                                    home = 1
                                else:
                                    points = columns[4].get_text()
                                    
                                if '--' in points:
                                    points = '0'
                                
                                if columns[1] is None:
                                    s=''
                                else:
                                    s = columns[1].get_text()
                                    #print  str(wk) +  owner2
                                
                                    nflPosition = ''
                                    nflTeam = ''
                                    
                                    if 'D/ST' in s:
                                        nflPosition = 'D/ST'
                                        nflTeam = ''
                                    else:
                                        if ', ' in s:
                                            start = s.rindex(', ') + len (', ')
                                            e = s.find(u'\xa0')
                                            nflTeam = s[start:e]
                                            nflPosition = s.split(u'\xa0')[1]
                                        
                                    
                                
                                row = {'Owner': owner1, 'Player': playerName, 'Week':str(wk), 'Season':str(seasonId), 'Player_Opponent':playerOpponent, 'Player_Home':str(home), 'Points':points, 'Roster_Slot':columns[0].get_text(), 'League':str(leagueName), 'NflTeam': nflTeam, 'NflPosition':nflPosition}
                                csvList.append(commaSeparateValues(row))
                            
                            #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                            # Team 2 Starters
                            team2PlayerRows = team2StartersTable.find_all('tr', class_='pncPlayerRow')
                            
                            for row in team2PlayerRows:
                                
                                columns = row.findChildren('td')

                                playerAnchors = columns[1].find_all('a')

                                if not playerAnchors:
                                    playerName = ''
                                else:
                                    playerName = playerAnchors[0].get_text()
                                

                                playerOpponent = columns[2].get_text()
                                home = 1
                                
                                points = 0

                                if '@' in playerOpponent:
                                    home = 0
                                    playerOpponent = playerOpponent[1:]

                                #playerTeam = find_between_r(columns[1].get_text(), ', ', '\\')
                                
                                
                                if  'BYE' in columns[2].get_text():
                                    points = columns[3].get_text()
                                    home = 1
                                else:
                                    points = columns[4].get_text()
                                    
                                if '--' in points:
                                    points = '0'
                                
                                if columns[1] is None:
                                    #print 'null'
                                    s=''
                                else:
                                    s = columns[1].get_text()
                                    #print  str(wk) +  owner2
                                
                                    nflPosition = ''
                                    nflTeam = ''
                                    
                                    if 'D/ST' in s:
                                        nflPosition = 'D/ST'
                                        nflTeam = ''
                                    else:
                                        if ', ' in s:
                                            start = s.rindex(', ') + len (', ')
                                            e = s.find(u'\xa0')
                                            nflTeam = s[start:e]
                                            nflPosition = s.split(u'\xa0')[1]
                                        
                                    
                                
                                #print 'about to write'
                                #print owner2
                                #print playerName
                                #print str(wk)
                                #print str(seasonId)
                                #print playerOpponent
                                #print str(home)
                                #print points
                                #print columns[0].get_text()
                                #print str(leagueName)

                                row = {'Owner': owner2, 'Player': playerName, 'Week':str(wk), 'Season':str(seasonId), 'Player_Opponent':playerOpponent, 'Player_Home':str(home), 'Points':points, 'Roster_Slot':columns[0].get_text(), 'League':str(leagueName), 'NflTeam': nflTeam, 'NflPosition':nflPosition}
                                csvList.append(commaSeparateValues(row))
                            
                            #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                            # Team 2 Bench Players
                            team2BenchPlayerRows = team2BenchTable.find_all('tr', class_='pncPlayerRow')
                            
                            for row in team2BenchPlayerRows:
                                columns = row.findChildren('td')
                                
                                playerAnchors = columns[1].find_all('a')

                                if not playerAnchors:
                                    playerName = ''
                                else:
                                    playerName = playerAnchors[0].get_text()
                                

                                playerOpponent = columns[2].get_text()
                                home = 1
                            
                                if '@' in playerOpponent:
                                    home = 0
                                    playerOpponent = playerOpponent[1:]
                            
                                #playerTeam = find_between_r(columns[1].get_text(), ', ', '\\')
                                    
                                if  'BYE' in columns[2].get_text():
                                    points = columns[3].get_text()
                                    home = 1
                                else:
                                    points = columns[4].get_text()
                                    
                                if '--' in points:
                                    points = '0'
                                    
                                if columns[1] is None:
                                    s=''
                                else:
                                    s = columns[1].get_text()
                                    #print  str(wk) +  owner2
                                
                                    nflPosition = ''
                                    nflTeam = ''
                                    
                                    if 'D/ST' in s:
                                        nflPosition = 'D/ST'
                                        nflTeam = ''
                                    else:
                                        if ', ' in s:
                                            start = s.rindex(', ') + len (', ')
                                            e = s.find(u'\xa0')
                                            nflTeam = s[start:e]
                                            nflPosition = s.split(u'\xa0')[1]
                                
                                
                                row = {'Owner': owner2, 'Player': playerName, 'Week':str(wk), 'Season':str(seasonId), 'Player_Opponent':playerOpponent, 'Player_Home':str(home), 'Points':points, 'Roster_Slot':columns[0].get_text(), 'League':str(leagueName), 'NflTeam': nflTeam, 'NflPosition':nflPosition}
                                csvList.append(commaSeparateValues(row))

        return csvListToCsvString(csvList)            
    except Exception as e:
        return 'Error occurred : ' + str(e)

    # script_file = open('Insert_all_fantasy_week_results_data_' + str(begin) + '_' + str(end) + '.sql', 'w')

    # with open("Fantasy_Weekly_Scores_" + str(begin) + "_" + str(end) + ".csv", 'rb') as csvfileIn:
    #     resultReader = csv.reader(csvfileIn, delimiter=',')
    #     for row in resultReader:
    #         script_file.write('INSERT INTO Fantasy_Weekly_Score ([Owner], Player, [Week], Season, Player_Opponent, Player_Home, Points, Roster_Slot, Player_NFL_Team, Player_NFL_Position, Fantasy_League) VALUES ' 
    #             + '(' 
    #             + '\'' + row[0] + '\', ' 
    #             + '\'' + str(row[1]).replace('\'','\'\'') + '\', ' 
    #             + '\'' + row[2] + '\', ' 
    #             + '\'' + row[3] + '\', ' 
    #             + '\'' + row[4] + '\', ' 
    #             + '\'' + row[5] + '\', ' 
    #             + '' + row[6] + ', ' 
    #             + '\'' + row[7] + '\', ' 
    #             + '\'' + row[9] + '\', ' 
    #             + '\'' + row[10] + '\', ' 
    #             + '\'' + row[8] + '\''
    #             + ')\n')
            
        

# print getMatchupDetails('WPFL', '457631', 1, 2017, 1, 3)