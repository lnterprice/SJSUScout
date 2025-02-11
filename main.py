import requests
from info import info
import pdb
import json
import time
import pandas as pd
from Summoner import Summoner

if __name__ == "__main__":
    lnterprice = Summoner("Sinvu", "NA1")
    lnterprice.getAllMatches("15.3")
    lnterprice.parseChampionPool()
    championObj = lnterprice.getCObjects()
    championObj = [i.getDict() for i in championObj]
    df = pd.DataFrame(championObj)
    df.to_excel("excel/output.xlsx", index=False, engine="openpyxl")