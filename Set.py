import requests
import json
from lxml import html
import re

from Card import Card

class Set:
    def __init__(self, url):
        req = requests.get(url)
        if req.status_code == 200:
            self.setName = req.json()["name"]
            self.boosterStructure = req.json()["booster"]
            self.cards = []
            self.commons = ()
            self.uncommons = ()
            self.rares = ()
            self.mythics = ()
        else:
            raise
        for card in req.json()["cards"]:
            # Storage of every card into its own place
            c = Card(**card)
            self.cards.append(c)
            if c.rarity == "Common": self.commons+=(c,)
            elif c.rarity == "Uncommon": self.uncommons+=(c,)
            elif c.rarity == "Rare": self.rares+=(c,)
            else: self.mythics+=c
            
    def calculateSumofPrices(self, _dict, language="English"):
        # Initialize the payload for the filter
        payload = {"productFilter[sellerStatus0]":"on",
                   "productFilter[sellerStatus1]":"on",
                   "productFilter[sellerStatus2]":"on",
                   "productFilter[idLanguage][]":"5",
                   "productFilter[condition][]":"MT",
                   "productFilter[condition][]":"NM",
                   "productFilter[isFoil]":"N",
                   "productFilter[isSigned]":"N",
                   "productFilter[isAltered]":"N",
                   "productFilter[minAmount]":"1"}
        total = 0
        for card in _dict:
            req = requests.post("https://www.magiccardmarket.eu/Products/Singles/{}/{}".format("+".join(self.setName.split()), "+".join(card.name.split()).replace("/", "%2F%2F").replace("'", "%27")), data = payload)
            if card.name in req.text:
                tree = html.fromstring(req.text)
                a = tree.xpath("//tbody[@id='articlesTable']/tr/td[@class='st_price']")[0]
                total += float(re.match("\d{1,2}[\.,]\d+", a.text_content()).group().replace(",", "."))
            else:
                print("Error on card " + card.name)
        return round(total, 2)
    
    def calculateSetPrice(self):
        return self.calculateSumofPrices(self.cards)

    def calculateCommonsPrices(self):
        return self.calculateSumofPrices(self.commons)
    
    def calculateUncommonsPrices(self):
        return self.calculateSumofPrices(self.uncommons)
    
    def calculateRaresPrices(self):
        return self.calculateSumofPrices(self.rares)
    
    def calculateMythicsPrices(self):
        return self.calculateSumofPrices(self.mythics)
    
    def calculateAverageBoosterPackPrice(self):
        common = self.calculateCommonsPrices() / len(self.commons)
        uncommon = self.calculateUncommonsPrices() / len(self.uncommons)
        rare = self.calculateRaresPrices() / len(self.rares)
        #mythic = self.calculateMythicsPrices() / len(self.mythics)
        return({"BoosterValue" : round((common * self.boosterStructure.count("common")) + (uncommon * self.boosterStructure.count("uncommon")) + rare, 2),
                "AverageCommon": common,
                "AverageUncommon" : uncommon,
                "AverageRare" : rare})

