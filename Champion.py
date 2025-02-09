import pdb
class ChampionMain:
    def __init__(self, unparsedMatchData):
        if type(unparsedMatchData) == list:
            self.championID = unparsedMatchData[0]['championId']
            self.uData = unparsedMatchData
            self.info = {self.championID: {}}
            self.player = unparsedMatchData[0]['riotIdGameName'] + "#" + unparsedMatchData[0]['riotIdTagline']
            self.championName = unparsedMatchData[0]['championName']
            self.mastery = unparsedMatchData[0]['champExperience']

        elif type(unparsedMatchData) == dict:
            #pdb.set_trace()
            self.championID = unparsedMatchData['championId']
            self.uData = [unparsedMatchData]
            self.info = {self.championID: {}}
            self.player = unparsedMatchData['riotIdGameName'] + "#" + unparsedMatchData['riotIdTagline']
            self.championName = unparsedMatchData['championName']
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
    
    def updateInfo(self):
        self.getAverageKDA()
        self.getAvgWinRate()
        self.getAvgCS()

    # statistics cranker

    def getAverageKDA(self):
        kills = 0
        deaths = 0
        assists = 0
        #pdb.set_trace()
        for stat in self.uData:
            kills += stat['kills']
            deaths += stat['deaths']
            assists += stat['assists']
        self.info[self.championID]['KDA'] = (kills/len(self.uData), deaths/len(self.uData), assists/len(self.uData))
        return self.info[self.championID]['KDA']

    def getAvgWinRate(self):
        totalGames = 0
        wins = 0
        for stat in self.uData:
            if stat['win']:
                wins += 1
            totalGames += 1
        try:
            self.info[self.championID]['Winrate'] = wins/   totalGames
        except ZeroDivisionError:
            self.info[self.championID]['Winrate'] = 0
        return self.info[self.championID]['Winrate']
    
    def getAvgCS(self):
        totalCS = 0
        for stat in self.uData:
            totalCS += stat['totalMinionsKilled']
        self.info[self.championID]['AvgCS'] = totalCS/len(self.uData)
        return self.info[self.championID]['AvgCS']

    

    def __eq__(self, championMainObj):
        return championMainObj.getChampionID() == self.getChampionID()
    
    def __str__(self):
        self.updateInfo()
        KDAStr = str(self.info[self.championID]['KDA'][0]) + " / " + str(self.info[self.championID]['KDA'][1]) + " / " + str(self.info[self.championID]['KDA'][2])
        WRStr = str(self.info[self.championID]['Winrate'] * 100)
        CSStr = str(self.info[self.championID]['AvgCS'])
        string = f"Player {self.player} has KDA {KDAStr} with an average win rate of {WRStr} and average CSING per game {CSStr} on champion {self.championName} with a total amount of games at {len(self.uData )}"
        return string