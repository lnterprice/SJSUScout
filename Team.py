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
                f.write(f"{self.summoners[i]}, Patch {self.patchNums[i]}\n")
                df.to_csv(f, index=True)
                f.write("\n\n\n")
        #pdb.set_trace()
        

    def processTeam(self):
        self.summoners = []
        self.patchNums = []
        self.teamDFS = []

        with open("Summoners.txt", "r") as file:
            for i, line in enumerate(file):
                line = line.rstrip("\n")
                summonerTag = line.split(",")[0]
                beginningPatch, endingPatch = line.split(",")[1].split("-")
                self.summoners.append(summonerTag)
                self.patchNums.append(f"{beginningPatch}-{endingPatch}")
                #pdb.set_trace()
                summoner = Summoner(summonerTag.split("#")[0], summonerTag.split("#")[1])
                summoner.getAllMatches(beginningPatch, endingPatch)
                summoner.parseChampionPool()
                while not summoner.getCObjects():
                    patch = input(f"[-] {summoner.getTag()} does not have match in that patch of {beginningPatch}-{endingPatch}, choose another patch in format (laterpatch-newpatch): ")
                    beginningPatch, endingPatch = patch.split("-")
                    self.patchNums[i] = f"{beginningPatch}-{endingPatch}"
                    summoner.getAllMatches(beginningPatch, endingPatch)
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