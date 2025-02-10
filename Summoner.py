import requests
from info import info
import pdb
import json
import time
from Champion import ChampionMain

class Summoner:
    def __init__(self, name, tag):
        self.matchDict = {}
        self.summonerTag = (name, tag)
        self.puuid = self.convertPuuid()

    def convertPuuid(self):
        url = f"https://{info['REGIONV1']}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{self.summonerTag[0]}/{self.summonerTag[1]}"
        response = requests.get(url, headers=info['headers'])
        response = json.loads(response.text)['puuid']
        return response

    def parseCurrentPatch(self, season, count):
        # get match ids from count to count + 100
        url = f"https://{info['REGIONV1']}.api.riotgames.com/lol/match/v5/matches/by-puuid/{self.puuid}/ids?type=ranked&start={count}&count=100"
        matches = json.loads(requests.get(url, headers=info['headers']).text)

        # for each match id, add to a list
        matchData = []
        for match in matches:
            time.sleep(1.2)
            url = f"https://{info['REGIONV1']}.api.riotgames.com/lol/match/v5/matches/{match}"
            response = json.loads(requests.get(url, headers=info['headers']).text)
            # base case is when the season version does not start with the target season
            #pdb.set_trace()
            print(response['info']['gameVersion'])
            if not response['info']['gameVersion'].startswith(season):
                return matchData
            # otherwise append to list and filter remade games
            if not response['info']['gameDuration'] <= 360:
                matchData.append(response)
        # append lists from recursive method
        matchData += self.parseCurrentPatch(season, count + 100)
        # return the final list
        return matchData

    # precondition that this will be run nearly on the same level as init
    def getAllMatches(self, season):
        matches = self.parseCurrentPatch(season, 0)
        self.matchDict['unparsedMatchInfo'] = matches

    # parsing champion mains not acutlaly chapmion pool (untested as of 02/09/2025 03:00AM)
    def parseChampionPool(self):
        # list of championmain objects
        self.championPoolObjects = []
        data = self.matchDict['unparsedMatchInfo']
        #pdb.set_trace()
        for object in data:
            for participant in object['info']['participants']:
                if participant['puuid'] == self.puuid:
                    tempObj = ChampionMain(participant)
                    exists = False
                    for championPoolObj in self.championPoolObjects:
                        if tempObj == championPoolObj:
                            championPoolObj.addStat(participant)
                            exists = True
                            break
                    if not exists:
                        self.championPoolObjects.append(tempObj)
    
    def getCObjects(self):
        return self.championPoolObjects

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