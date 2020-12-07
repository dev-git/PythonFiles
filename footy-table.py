import requests
import json
#import apprise
import sys
import datetime

### fetch("http://www.oratiaunited.co.nz/api/1.0/competition/cometwidget/filteredstandings", {
#  "headers": {
#    "accept": "*/*",
#    "accept-language": "en-US,en;q=0.9",
#    "content-type": "application/json; charset=UTF-8",
#    "x-requested-with": "XMLHttpRequest"
#  },
 # "referrer": "http://www.oratiaunited.co.nz/Our-Teams/First-Team-Reserves",
#  "referrerPolicy": "no-referrer-when-downgrade",
#  "body": "{\"competitionId\":\"764315830\",\"phaseId\":null,\"orgIds\":\"44882\",\"from\":\"2020-07-05T00:00:00.000Z\",\"to\":\"2020-07-11T00:00:00.000Z\",\"sportId\":\"1\",\"seasonId\":\"2020\",\"gradeIds\":\"\",\"gradeId\":\"\",\"organisationId\":\"\",\"roundId\":null,\"roundsOn\":\"False\"}",
#  "method": "POST",
 # "mode": "cors",
 # "credentials": "include"
#});



headers = {
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "content-type": "application/json; charset=UTF-8",
    "x-requested-with": "XMLHttpRequest"
}

compId = "764315830"
#compId = "90494959"
body = "{\"competitionId\":\"" + compId + "\",\"phaseId\":null,\"orgIds\":\"44882\",\"from\":\"2020-06-05T00:00:00.000Z\",\"to\":\"2020-07-11T00:00:00.000Z\",\"sportId\":\"1\",\"seasonId\":\"2020\",\"gradeIds\":\"\",\"gradeId\":\"\",\"organisationId\":\"\",\"roundId\":null,\"roundsOn\":\"False\"}"
#body = "{\"competitionId\":\"764315830\",\"phaseId\":null,\"orgIds\":\"42566,44272,44294,44295,44492,44534,44625,44671,44788,44791,44830,44831,44832,44833,44834,44835,44837,44838,44839,44840,44841,44855,44860,44884,44887,44888,45040,45041,45043,45044,45045,45046,45047,45048,45049,45050,45051,45053,45054,45055,45056,45057,45058,45067,47004,47209,47225,47232,59187,59189,59190,59256,59269,60684,61110,61232,62097,65455,65458,65461,65465,65468,66772,66972,66973,67513,67713,67734,70013,70015,70017,70812,71352,71433,71434,71532,72214,72225,72392,72466,73018,73595,73712,73713,73714,73715,73716,73792,73872,75206,75208,75211,75216,75219,75592,76573,77075,77179,77812,79324,83114,86612,88319,90156,90492,90694,91787,91790,91868,94483,95493,96252,100772\",\"from\":\"2020-06-04T00:00:00.000Z\",\"to\":\"2020-07-10T00:00:00.000Z\",\"sportId\":\"1\",\"seasonId\":\"2020\",\"gradeIds\":\"\",\"gradeId\":\"\",\"organisationId\":\"\",\"roundsOn\":\"True\"}"

now = datetime.datetime.now()
query = "http://www.oratiaunited.co.nz/api/1.0/competition/cometwidget/filteredstandings"
#query = "http://www.oratiaunited.co.nz/api/1.0/competition/cometwidget/filteredfixtures"
#query = "http://www.nff.org.nz/api/1.0/competition/cometwidget/filteredfixtures"
    
response = requests.request("POST", query, headers=headers, data =body)
result = response.text.encode('utf8')
rows = json.loads(result)
#print(rows)
#sys.exit()

#for game in range(3):
#    match = rows["fixtures"][game]
#    print(match["HomeTeamName"] + ' ' + str(match["HomeScore"]) + ' - ' + str(match["AwayScore"]) + ' ' + match["AwayTeamName"])


#sys.exit()
teamCount = len(rows[0]["Sections"][0]["Standings"])
print(teamCount)
print("Team Name                        P   W   D   L   F   A   Pts")
print('-' * 60)
for count in range(teamCount):
    standing = rows[0]["Sections"][0]["Standings"][count]
    print(standing["TeamName"][:23] + '          ' + str(standing["Played"]) + '   ' + str(standing["Wins"]) + '   ' + str(standing["Draws"]) + '   ' + str(standing["Losses"]) + '   ' + str(standing["ForPoints"]) + '   ' + str(standing["AgainstPoints"]) + '   ' + str(standing["Total"]))
#rowCount = rows["tables"][0]["rows"][0][0]
#print(rowCount)
print('\n')

gameQuery = "http://www.nff.org.nz/api/1.0/competition/cometwidget/filteredfixtures"
for roundId in range(1, 8):
    gameBody = "{\"competitionId\":\"" + compId + "\",\"phaseId\":null,\"orgIds\":\"42566,44272,44294,44295,44492,44534,44625,44671,44830,44831,44832,44833,44834,44835,44837,44838,44839,44840,44841,44845,44853,44854,44855,44857,44882,45040,45041,45043,45044,45045,45046,45047,45048,45049,45050,45051,45053,45054,45055,45056,45057,45058,45067,47004,47209,47225,47232,59187,59189,59190,59256,59269,60684,61110,61232,65455,65458,65461,65465,65468,66772,66972,66973,67513,67713,67734,70013,70015,70017,70812,71352,71433,71434,71532,72214,72225,72392,72466,73018,73595,73712,73713,73714,73715,73716,73792,73872,75206,75208,75211,75216,75219,75592,76573,77075,77179,77812,79324,83114,86612,88319,90156,90492,90694,91787,91790,91868,94483,95493,96252,100772\",\"from\":\"2020-06-01T00:00:00.000Z\",\"to\":\"2020-07-06T00:00:00.000Z\",\"sportId\":\"1\",\"seasonId\":\"2020\",\"gradeIds\":\"\",\"gradeId\":\"\",\"organisationId\":\"\",\"roundId\":" + str(roundId) + ",\"roundsOn\":\"True\"}"
    
    response = requests.request("POST", gameQuery, headers=headers, data =gameBody)
    result = response.text.encode('utf8')
    gameRows = json.loads(result)

    games = len(gameRows["fixtures"])
    print('Round: ' + str(roundId))
    for game in range(games):
        match = gameRows["fixtures"][game]
        print(match["HomeTeamName"] + ' ' + str(match["HomeScore"]) + ' - ' + str(match["AwayScore"]) + ' ' + match["AwayTeamName"])