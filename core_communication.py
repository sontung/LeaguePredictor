import requests
import json
import time


class WebServerCommunication:
    """
    Web server communication using Riot API
    """
    def __init__(self):
        self.current_game = None
        pass

    def getInfo(self):
        info = self.current_game
        self.current_game = None
        return info

    def send_get(self, url):
        r = requests.get(url)
        j = r.content
        obj = json.loads(j)
        return obj, r.status_code

    def getPlayerNameById(self, playerId):
        time.sleep(1)
        result = self.send_get("https://euw.api.pvp.net/api/lol/euw/v1.4/summoner/"
                               "%s/name?api_key=e29122ef-7d29-4305-a990-2b1b5f52a222" % playerId)[0]
        return result[playerId]

    def getCurrentGame(self, playerID):
        time.sleep(1)
        result, code = self.send_get("https://euw.api.pvp.net/observer-mode/rest/"
                                     "consumer/getSpectatorGameInfo/EUW1/%s"
                                     "?api_key=e29122ef-7d29-4305-a990-2b1b5f52a222" % playerID)
        if code == 404:
            self.current_game = "not in game"
            return "not in game"
        ranked_stats = self.getRankedStats([str(p["summonerId"]) for p in result["participants"]])
        listOfPlayers = []
        for player in result["participants"]:
            listOfPlayers.append([player["teamId"], player["summonerName"], self.getChampById(player["championId"]),
                                  self.getStatsByChampion(player["summonerId"], player["championId"]),
                                  ranked_stats[str(player["summonerId"])]])
        self.current_game = listOfPlayers
        return listOfPlayers

    def getStatsByChampion(self, playerId, champId):
        time.sleep(1)
        result = self.send_get("https://euw.api.pvp.net/api/lol/euw/v1.3/stats/"
                               "by-summoner/%s/"
                               "ranked?season=SEASON2016&api_key=e29122ef-7d29-4305-a990-2b1b5f52a222" % playerId)[0]
        win_rate = 0
        kda = 0
        for champion in result["champions"]:
            if champion["id"] == champId:
                win_rate = champion["stats"]["totalSessionsWon"] / float(champion["stats"]["totalSessionsPlayed"])
                if int(champion["stats"]["totalDeathsPerSession"]) == 0:
                    kda = (champion["stats"]["totalChampionKills"] + champion["stats"]["totalAssists"])
                else:
                    kda = (champion["stats"]["totalChampionKills"] + champion["stats"]["totalAssists"])\
                          / float(champion["stats"]["totalDeathsPerSession"])
        return win_rate, kda

    def getChampById(self, champId):
        time.sleep(1)
        result = self.send_get("https://global.api.pvp.net/api/lol/static-dat"
                               "a/euw/v1.2/champion/%d?api_key=e29122ef-7d29-4305-a990-2b1b5f52a222" % champId)[0]
        return result["name"]

    def getPlayerIdByName(self, playerName):
        time.sleep(1)
        result, code = self.send_get("https://euw.api.pvp.net/api/lol/euw/v1.4/summoner/by-name/"
                                     "%s?api_key=e29122ef-7d29-4305-a990-2b1b5f52a222" % playerName)
        if code == 404:
            return "not found"
        return str(result.values()[0]["id"])

    def getRankedStats(self, playerIds):
        time.sleep(1)
        ids = ','.join(playerIds)
        leagues = {}
        result, code = self.send_get("https://euw.api.pvp.net/api/lol/euw/v2.5/league/"
                                     "by-summoner/%s/"
                                     "entry?api_key=e29122ef-7d29-4305-a990-2b1b5f52a222" % ids)
        for player in result:
            leagues[player] = "%s %s" % (result[player][0]["tier"], result[player][0]["entries"][0]["division"])
        for p in playerIds:
            if p not in leagues:
                leagues[p] = "placement"
        return leagues
