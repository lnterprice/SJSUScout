import requests
from info import info
import pdb
import json
import time
from Summoner import Summoner

if __name__ == "__main__":
    lnterprice = Summoner("Interprice", "NA1")
    lnterprice.getAllMatches("15.3")
    lnterprice.parseChampionPool()
    for champion in lnterprice.getCObjects():
        print(champion.getDict())