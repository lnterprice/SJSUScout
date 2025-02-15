from info import info
import pandas as pd
from Summoner import Summoner
OUTPUT_PATH = "excel/"
import pdb
class Team:

    def __init__(self, teamName):
        self.teamName = teamName
        self.processTeam()

    def toCSV(self):
        with open(f"excel/{self.teamName}.csv", 'w') as f:
            for i, df in enumerate(self.teamDFS):
                f.write(f"{self.summoners[i][0]}#{self.summoners[i][1]}, Patch {self.patchNums[i]}\n")
                df.to_csv(f, index=False)
                f.write("\n\n\n")
        #pdb.set_trace()
        

    def processTeam(self):
        self.summoners = []
        self.patchNums = []
        self.teamDFS = []
        for i in range(0, 5):
            summonerTag = input("Enter Summoner Tag (Example#NA1): ")
            summonerTag = (summonerTag.split("#")[0], summonerTag.split("#")[1])
            self.summoners.append(summonerTag)
            patchNum = input("Enter Patch Num that you want to get the match history of (Ex: 15.3, 15.2, 14.23): ")
            self.patchNums.append(patchNum)
        
        for i in range(0, 5):
            summoner = Summoner(self.summoners[i][0], self.summoners[i][1])
            summoner.getAllMatches(self.patchNums[i])
            summoner.parseChampionPool()
            #pdb.set_trace()
            while not summoner.getCObjects():
                patch = input(f"[-] {summoner.getTag()} does not have match in that patch, choose another patch: ")
                self.patchNums[i] = patch
                summoner.getAllMatches(self.patchNums[i])
                summoner.parseChampionPool()
            self.teamDFS.append(self.toDF(summoner.getCObjects()))

        

    def toDF(self, championObj):
        championList = {}
        for cObj in championObj:
            cObjDict = cObj.getDict()
            championName, id = list(cObjDict.keys())[0]
            info = list(cObjDict.values())[0]
            championList[championName] = info
        df = pd.DataFrame.from_dict(championList, orient="index")
        df['winRate'] = ((df['winRate']+0.005) * 100).apply(int).apply(str) + "%"
        df['KP'] = ((df['KP']+0.005) * 100).apply(int).apply(str) + "%"
        df = df.map(lambda x: int(x) if isinstance(x, float) and not pd.isna(x) else x)
        df = df.sort_values(by="numGames", ascending=False)
        return df