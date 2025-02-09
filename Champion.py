class ChampionMain:
    def __init__(self, unparsedMatchData):
        if type(unparsedMatchData) == list:
            self.championID = unparsedMatchData[0]['championID']
            self.uData = unparsedMatchData
        elif type(unparsedMatchData) == dict:
            self.championID = unparsedMatchData['championID']
            self.uData = [unparsedMatchData]
        else:
            raise ValueError("[-] Unparsed Match Data neither List or String type")

    def addStat(self, dataJSON):
        self.uData.append(dataJSON)

    def getChampionID(self):
        return self.championID
    
    def __eq__(self, championMainObj):
        return championMainObj.getChampionID() == self.getChampionID()
    
    def __str__(self):
        print(self.championID)