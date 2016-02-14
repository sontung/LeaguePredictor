import json
import requests
import time
import pandas

x=[[6.345767575322812, 5.166666666666667, 1.0, 4.775585130793942, 1.5396825396825398, 0.375, 5.925319488817891, 2.75, 1.0, 6.3442192192192195, 2.3529411764705883, 0.25, 5.934103260869565, 4.928571428571429, 1.0, None, None, None, 6.95536756126021, 3.5, 1.0, 7.135290127643831, 2.6956521739130435, 0.5, 6.1195808332629085, 2.7948717948717947, 0.5, None, None, None, 1],
[6.176497160557563, 2.5, 0.375, None, None, None, 5.4791938794551225, 3.9375, 0.375, 7.209788122948374, 2.923076923076923, 0.3333333333333333, None, None, None, 3.937283950617284, 2.0, 0.3333333333333333, None, None, None, None, None, None, 6.360356347438753, 3.204081632653061, 0.625, 4.779542349726776, 2.0, 0.3333333333333333, 0],
[6.140609874152952, 2.6, 1.0, None, None, None, None, None, None, 5.663401996714268, 1.7419354838709677, 0.25, None, None, None, 6.261486377559246, 4.416666666666667, 0.6666666666666666, None, None, None, 7.1530172413793105, 2.2142857142857144, 1.0, 7.186849379521261, 2.702127659574468, 0.375, 4.028639618138425, 1.3333333333333333, 0.0, 1],
[6.752270663033606, 2.625, 0.6666666666666666, None, None, None, None, None, None, None, None, None, 4.931703810208483, 2.111111111111111, 0.5, None, None, None, 5.862552249815589, 2.4285714285714284, 0.5, None, None, None, 6.697857860954296, 5.9411764705882355, 0.5714285714285714, 6.980990415335463, 1.7407407407407407, 0.6666666666666666, 1],
[None, None, None, 7.746328029375765, 2.6153846153846154, 0.5, None, None, None, 6.886026731470231, 3.1463414634146343, 0.625, None, None, None, None, None, None, 6.300844453039386, 2.652173913043478, 0.625, None, None, None, 4.6965626652564785, 2.7586206896551726, 0.4, None, None, None, 0],
[None, None, None, 4.976190476190476, 0.5, 0.0, 7.120276185192035, 3.357142857142857, 0.5, 4.500792493501553, 1.5774647887323943, 0.5, 6.85250999555753, 2.3, 1.0, 6.151859099804305, 4.75, 0.0, None, None, None, 6.2624, 6.0, 1.0, 6.502783400809717, 3.6, 0.6666666666666666, 5.22124128775307, 3.6551724137931036, 0.625, 0],
[6.445130274793756, 3.2641509433962264, 0.375, 6.300844453039386, 2.652173913043478, 0.625, 6.294383432695325, 4.0, 0.375, 5.934103260869565, 4.928571428571429, 1.0, None, None, None, 5.515299990755293, 2.9545454545454546, 0.16666666666666666, None, None, None, 3.7552083333333335, 0.6, 0.0, None, None, None, 6.619361084220716, 8.833333333333334, 0.6666666666666666, 0],
[4.642276422764228, 1.5714285714285714, 0.0, None, None, None, None, None, None, 5.4791938794551225, 3.9375, 0.375, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 1],
[4.483521156708484, 2.5714285714285716, 0.5, 8.357609195402299, 3.28125, 0.8333333333333334, None, None, None, None, None, None, 6.762448700410396, 2.9782608695652173, 0.5, 5.616223288268643, 5.25, 1.0, None, None, None, 6.610809799887788, 2.411764705882353, 0.5, 6.85250999555753, 2.3, 1.0, 5.275543226999537, 4.25, 1.0, 1]]
t= [[100, 'duckbike', 'Miss Fortune', (0.8, 3.347826086956522), 'SILVER IV'],
    [100, 'KNS Kaneki', 'Dr. Mundo', (1.0, 8.0), 'SILVER V'],
    [100, 'Asiat Mechanics', 'Elise', (0.0, 1.8), 'SILVER IV'],
    [100, 'LegendLuigi', 'Anivia', (0.0, 3.5), 'SILVER V'],
    [100, 'Darion MD', 'Nami', (1.0, 25.0), 'placement'],
    [200, 'Ahuca', 'Sivir', (0.8333333333333334, 4.145833333333333), 'BRONZE II'],
    [200, 'kitkat20', 'Morgana', (0.4, 2.25), 'SILVER V'],
    [200, 'KeshinX', 'Amumu', (0.5555555555555556, 2.7413793103448274), 'SILVER IV'],
    [200, 'RfaNeko', 'Twisted Fate', (0, 0), 'SILVER II'],
    [200, 'axer2000', 'Malphite', (0.6666666666666666, 6.0), 'BRONZE I']]


def writeToCSV(inp):
    a_dict = {"Result": [y[-1] for y in inp]}
    for count in range(len(inp[0])-1):
        key = "stat%d" % (count+1)
        a_dict[key] = [x[count] for x in inp]
    df = pandas.DataFrame(a_dict)
    cols = df.columns.tolist()
    cols.sort(key=lambda element: int(element[4:] if 'stat' in element else 1))
    df = df[cols]
    df.to_csv("data.csv", index=False)


def getChampById(champId):
    r = requests.get("https://global.api.pvp.net/api/lol/static-dat"
                         "a/euw/v1.2/champion/%d?api_key=e29122ef-7d29-4305-a990-2b1b5f52a222" % champId)
    j = json.loads(r.content)
    time.sleep(1)
    return j["name"]


def getPlayerById(playerId):
    r = requests.get("https://euw.api.pvp.net/api/lol/euw/v1.4/summoner/"
                     "%d?api_key=e29122ef-7d29-4305-a990-2b1b5f52a222" % playerId)
    j = json.loads(r.content)
    time.sleep(1)
    return j[str(playerId)]["name"]


def getStatsByChampAndPlayerId(champId, playerId):
    for i in range(2):
        r = requests.get("https://euw.api.pvp.net/api/lol/euw/v2.2"
                     "/matchlist/by-summoner/"
                     "%d?championIds=%d&rankedQueues=RANKED_SOLO_5x5&"
                     "seasons=SEASON2016,PRESEASON2016&api_key=e29122ef-7d29-4305-a990-2b1b5f52a222" %
                     (playerId, champId))
        j = json.loads(r.content)
        time.sleep(1)
    if j["totalGames"] == 0:
        return [None, None, None]
    totalGames = 0
    matchDuration = 0
    goldEarned = 0
    totalKills = 0
    totalDeaths = 0
    totalAssists = 0
    totalWins = 0
    matchIds = [str(x["matchId"]) for x in j["matches"]][0:8]
    for matchId in matchIds:
        totalGames += 1
        for i in range(2):
            r1 = requests.get("https://euw.api.pvp.net/api/lol/euw/v2.2/"
                          "match/%s?api_key=e29122ef-7d29-4305-a990-2b1b5f52a222" % matchId)
            j1 = json.loads(r1.content)
            time.sleep(1)
        try:
            matchDuration += j1["matchDuration"]
        except KeyError:
            if j1["status"]["status_code"] == 404:
                print "%s match not found" % matchId
                return [None, None, None]
        try:
            for player in j1["participants"]:
                if player["championId"] == champId:
                    totalWins += player["stats"]["winner"]
                    goldEarned += player["stats"]["goldEarned"]
                    totalKills += player["stats"]["kills"]
                    totalDeaths += player["stats"]["deaths"]
                    totalAssists += player["stats"]["assists"]
        except KeyError:
            print matchId
            return
    averageGPM = goldEarned / float(matchDuration)
    if totalDeaths == 0:
        totalDeaths = 1
    totalKDA = (totalKills + totalAssists) / float(totalDeaths)
    return [averageGPM, totalKDA, totalWins/float(totalGames)]


def gather_data(playerId):
    X = []
    stats1 = []
    stats2 = []
    for i in range(2):
        r = requests.get("https://euw.api.pvp.net/api/lol/euw/v1.3/game/by-summoner/%d/"
                     "recent?api_key=e29122ef-7d29-4305-a990-2b1b5f52a222" % playerId)
        j = r.content
        time.sleep(1)
    obj = json.loads(j)
    for game in obj["games"]:
        if game["teamId"] == 100:
            stats1.extend(getStatsByChampAndPlayerId(game["championId"], playerId))
            winner = int(game["stats"]["win"])
        else:
            stats2.extend(getStatsByChampAndPlayerId(game["championId"], playerId))
            winner = int(not game["stats"]["win"])
        for player in game["fellowPlayers"]:
            if player["teamId"] == 100:
                stats1.extend(getStatsByChampAndPlayerId(player["championId"], player["summonerId"]))
            else:
                stats2.extend(getStatsByChampAndPlayerId(player["championId"], player["summonerId"]))
        stats1.extend(stats2)
        stats1.append(winner)
        X.append(stats1)
        print stats1
        stats1 = []
        stats2 = []

writeToCSV(x)
#
# r = requests.get("https://euw.api.pvp.net/api/lol/euw/v1.3/game/by-summoner/57067299/recent?api_key=e29122ef-7d29-4305-a990-2b1b5f52a222")
# j = r.content
# obj = json.loads(j)
# playerID = 57067299
# gather_data(playerID)
# for game in obj["games"]:
#     print getPlayerById(playerID), getChampById(game["championId"]), \
#         getStatsByChampAndPlayerId(game["championId"], playerID)
#     for player in game["fellowPlayers"]:
#         print player["summonerId"], player["championId"], \
#             getStatsByChampAndPlayerId(player["championId"], player["summonerId"])