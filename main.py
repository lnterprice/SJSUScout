import requests
from info import info
import pdb
import json
import time
from Champion import ChampionMain

class SJSUScout:
    def __init__(self, debug=False):
        self.matchDict = {0: {}, 1: {}, 2: {}, 3: {}, 4: {}}
        if not debug:
            print("Enter the summoner line by line with tag in order top, jungle, mid, adc, and sup")
            self.summonerTags = []
            for i in range(1, 6):
                username = input(str(i) + ": ")
                username = username.split("#")
                self.summonerTags.append(username)
        else:
            self.summonerTags = [('Interprice', 'NA1'), ('Kevyi', 'NA1'), ('Evan', 'lai'), ('Sinvu', 'NA1'), ('stinky', 'joker')]


    def convertPuuid(self):
        self.puuids = []
        for i in range(0, 5):
            url = f"https://{info['REGIONV1']}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{self.summonerTags[i][0]}/{self.summonerTags[i][1]}"
            response = requests.get(url, headers=info['headers'])
            response = json.loads(response.text)
            self.puuids.append(response['puuid'])

    def getLane(self, string):
        if string == "top":
            return 0
        if string == "jg":
            return 1
        if string == "mid":
            return 2
        if string == "adc":
            return 3
        if string == "sup":
            return 4
        return "not a lane"

    def parseCurrentPatch(self, puuid, season, count):
        # get match ids from count to count + 100
        url = f"https://{info['REGIONV1']}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?type=ranked&start={count}&count=100"
        matches = json.loads(requests.get(url, headers=info['headers']).text)

        # for each match id, add to a list
        matchData = []
        for match in matches:
            time.sleep(1.2)
            url = f"https://{info['REGIONV1']}.api.riotgames.com/lol/match/v5/matches/{match}"
            response = json.loads(requests.get(url, headers=info['headers']).text)
            # base case is when the season version does not start with the target season
            print(response['info']['gameVersion'])
            if not response['info']['gameVersion'].startswith(season):
                return matchData
            # otherwise append to list
            if not response['info']['gameDuration'] <= 360:
                matchData.append(response)
        # append lists from recursive method
        matchData += self.parseCurrentPatch(puuid, season, count + 100)
        # return the final list
        return matchData

    # precondition that this will be run nearly on the same level as init
    def getAllMatches(self, lane, season):
        lane = self.getLane(lane)
        targetPuuid = self.puuids[lane]
        matches = self.parseCurrentPatch(targetPuuid, season, 0)
        self.matchDict[lane]['unparsedMatchInfo'] = matches

    # parsing champion mains not acutlaly chapmion poool (untested as of 02/09/2025 03:00AM)
    def parseChampionPool(self, lane):
        lane = self.getLane(lane)
        targetPuuid = self.puuids[lane]
        # list of championmain objects
        self.championPoolObjects = []
        data = self.matchDict[lane]['unparsedMatchInfo']
        #pdb.set_trace()
        for object in data:
            for participant in object['info']['participants']:
                if participant['puuid'] == targetPuuid:
                    tempObj = ChampionMain(participant)
                    exists = False
                    for championPoolObj in self.championPoolObjects:
                        if tempObj == championPoolObj:
                            championPoolObj.addStat(participant)
                            exists = True
                            break
                    if not exists:
                        self.championPoolObjects.append(tempObj)

        for champObj in self.championPoolObjects:
            print(champObj)
        
        
def main():
    scout = SJSUScout(True)
    scout.convertPuuid()
    scout.getAllMatches("top", "15")
    scout.parseChampionPool("top")
main()

# response = url = f"https://{info['REGIONV1']}.api.riotgames.com/lol/match/v5/matches/{matches[-1]}"
# response = json.loads(requests.get(url, headers=info['headers']).text)
#ex match url https://americas.api.riotgames.com/lol/match/v5/matches/NA1_5157651823
# match['metadata']['participants'] gets participants in puuid
# match['info']['gameVersion'] gets match patch version
# match['info']['gameDuration']
# match['info']['participants'][num]['challenges']['acesBefore15Minutes']
# match['info']['participants'][num]['riotIdGameName']
# match['info']['participants'][num]['riotIdTagline']
# match['info']['participants'][num]['spellf{num}Casts']
# match['info']['participants'][num]['teamEarlySurrender'] = remake?
# match['info']['participants'][num]['totalMinionsKilled']
# match['info']['participants'][num]['visionScore']
# match['info']['participants'][num]['goldEarned']
# match['info']['participants'][num]['gameEndedInSurrender']
# match['info']['participants'][num]['win'] done 
# match['info']['participants'][num]['damageDealtToBuildings']
# match['info']['participants'][num]['damageDealtToObjectives'] (participation in drag/baron is objectives-buildings)
# match['info']['participants'][num]['championName']
# match['info']['participants'][num]['kills'] done
# match['info']['participants'][num]['deaths'] done
# match['info']['participants'][num]['assists'] done
# match['info']['participants'][num]['longestTimeSpentLiving']
# match['info']['participants'][num]['totalDamageDealtToChampions']
# match['info']['participants'][num]['totalHealsOnTeammates']
# match['info']['participants'][num]['visionScore']
# match['info']['participants'][num]['wardsKilled']
# match['info']['participants'][num]['visionWardsBoughtInGame']
# match['info']['participants'][num]['wardsPlaced']
# match['info']['participants'][num]['challenges']['gameLength']
# match['info']['participants'][num]['challenges']['goldPerMinute']
# match['info']['participants'][num]['challenges']['maxCsAdvantageOnLaneOpponent']
# match['info']['participants'][num]['challenges']['maxLevelLeadLaneOpponent']
# match['info']['participants'][num]['firstBloodAssist']
# match['info']['participants'][num]['firstBloodKill']
# match['info']['participants'][num]['firstTowerAssist']
# match['info']['participants'][num]['firstTowerKill']
# match['info']['participants'][num]['challenges']['skillshotsDodged']
# match['info']['participants'][num]['challenges']['soloKills']
# match['info']['participants'][num]['challenges']["gameLength"]