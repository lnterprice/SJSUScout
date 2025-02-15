import pdb
class ChampionMain:
    def __init__(self, unparsedMatchData):
        if type(unparsedMatchData) == list:
            self.championID = unparsedMatchData[0]['championId']
            self.uData = unparsedMatchData
            self.player = unparsedMatchData[0]['riotIdGameName'] + "#" + unparsedMatchData[0]['riotIdTagline']
            self.championName = unparsedMatchData[0]['championName']
            self.info = {(self.championName, self.championID): {}}
            self.mastery = unparsedMatchData[0]['champExperience']

        elif type(unparsedMatchData) == dict:
            self.championID = unparsedMatchData['championId']
            self.uData = [unparsedMatchData]
            self.player = unparsedMatchData['riotIdGameName'] + "#" + unparsedMatchData['riotIdTagline']
            self.championName = unparsedMatchData['championName']
            self.info = {(self.championName, self.championID): {}}
            self.mastery = unparsedMatchData['champExperience']
        else:
            raise ValueError("[-] Unparsed Match Data neither List or String type")

    # basic functions/methods

    def addStat(self, dataJSON):
        self.uData.append(dataJSON)

    def getChampionID(self):
        return self.championID
    
    def returnRaw(self):
        return self.uData
    
    def getDict(self):
        self.updateInfo()
        return self.info

    def getNumGames(self):
        self.info[(self.championName, self.championID)]['numGames'] = len(self.uData)

    def updateInfo(self):
        self.getAverageKDA()
        self.getAvgWinRate()
        self.getAvgCSMin()
        self.getGPM()
        self.getAvgKP()
        self.getAvgDPM()
        self.getAvgAbilityUsage()
        self.getAverageVisionScore()
        self.getNumGames()

    # statistics cranker

    def getAverageKDA(self):
        kills = 0
        deaths = 0
        assists = 0
        for stat in self.uData:
            kills += stat['kills']
            deaths += stat['deaths']
            assists += stat['assists']
        self.info[(self.championName, self.championID)]['Kills'] = kills/len(self.uData)
        self.info[(self.championName, self.championID)]['Deaths'] = deaths/len(self.uData)
        self.info[(self.championName, self.championID)]['Assists'] = assists/len(self.uData)
        return (self.info[(self.championName, self.championID)]['Kills'], self.info[(self.championName, self.championID)]['Deaths'], self.info[(self.championName, self.championID)]['Assists'])

    def getAvgWinRate(self):
        totalGames = 0
        wins = 0
        for stat in self.uData:
            if stat['win']:
                wins += 1
            totalGames += 1
        try:
            self.info[(self.championName, self.championID)]['winRate'] = wins/   totalGames
        except ZeroDivisionError:
            self.info[(self.championName, self.championID)]['winRate'] = 0
        return self.info[(self.championName, self.championID)]['winRate']
    

    def getAvgCSMin(self):
        totalCSMin = 0
        for stat in self.uData:
            totalCSMin += (stat['totalMinionsKilled']/(stat['challenges']['gameLength']/60))
        self.info[(self.championName, self.championID)]['avgCSPerMinute'] = totalCSMin/len(self.uData)
        return self.info[(self.championName, self.championID)]['avgCSPerMinute']

    def getGPM(self):
        totalGold = 0
        for stat in self.uData:
            totalGold += stat['challenges']['goldPerMinute']
        self.info[(self.championName, self.championID)]['GPM'] = totalGold/len(self.uData)
        return self.info[(self.championName, self.championID)]['GPM']

    def getAvgKP(self):
        totalKP = 0
        for stat in self.uData:
            totalKP += stat['challenges']['killParticipation']
        self.info[(self.championName, self.championID)]['KP'] = totalKP/len(self.uData)
        return self.info[(self.championName, self.championID)]['KP']
    
    def getAvgDPM(self):
        totalDPM = 0
        for stat in self.uData:
            totalDPM += stat['challenges']['damagePerMinute']
        self.info[(self.championName, self.championID)]['avgDPM'] = totalDPM/len(self.uData)
        return self.info[(self.championName, self.championID)]['avgDPM']
    
    def getAvgAbilityUsage(self):
        totalAbilityUsage = 0
        for stat in self.uData:
            totalAbilityUsage += stat['challenges']['abilityUses']
        self.info[(self.championName, self.championID)]['avgAbusage'] = totalAbilityUsage/len(self.uData)
        return self.info[(self.championName, self.championID)]['avgAbusage']
    
    def getAverageVisionScore(self):
        vScore = 0
        for stat in self.uData:
            vScore += stat['visionScore']
        self.info[(self.championName, self.championID)]['visionScore'] = vScore/len(self.uData)
        return self.info[(self.championName, self.championID)]['visionScore']

    def __eq__(self, championMainObj):
        return championMainObj.getChampionID() == self.getChampionID()
    
    def __str__(self):
        self.updateInfo()
        KDAStr = str(self.info[(self.championName, self.championID)]['Kills']) + " / " + str(self.info[(self.championName, self.championID)]['Deaths']) + " / " + str(self.info[(self.championName, self.championID)]['Assists'])
        WRStr = str(self.info[(self.championName, self.championID)]['winRate'] * 100)
        CSStr = str(self.info[(self.championName, self.championID)]['avgCSPerMinute'])
        string = f"Player {self.player} has KDA {KDAStr} with an average win rate of {WRStr} and average CS/Min per game {CSStr} on champion {self.championName} with a total amount of games at {len(self.uData)}"
        return string