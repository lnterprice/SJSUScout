import requests
from info import info
import pdb
import json
import time
from Summoner import Summoner

if __name__ == "__main__":
    lnterprice = Summoner("mike sherm", "lean")
    lnterprice.getAllMatches("15.3")
    lnterprice.parseChampionPool()
    for champion in lnterprice.getCObjects():
        print(champion.getDict())