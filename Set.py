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
        languageCodes = {"English" : 1, "French" : 2, "German" : 3, "Spanish" : 4, "Italian" : 5, "S-Chinese" : 6, "Japanese" : 7, "Portuguese" : 8, "Russian" : 9, "Korean" : 10, "T-Chinese" : 11}
        # Initialize the payload for the filter
        payload = {"productFilter[sellerStatus0]":"on",
                   "productFilter[sellerStatus1]":"on",
                   "productFilter[sellerStatus2]":"on",
                   "productFilter[idLanguage][]":str(languageCodes[language]),
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
                # Getting the first 5 prices
                a = [float(re.match("\d{1,2}[\.,]\d+", a.text_content()).group().replace(",", ".")) 
                     for a in tree.xpath("//tbody[@id='articlesTable']/tr/td[@class='st_price']")[:5]]
                # Adding the average
                total += sum(a)/len(a)
            else:
                print("Error on card " + card.name)
        return round(total, 2)
    
    def calculateSetPrice(self, language):
        return self.calculateSumofPrices(self.cards, language=language)

    def calculateCommonsPrices(self, language):
        return self.calculateSumofPrices(self.commons, language=language)
    
    def calculateUncommonsPrices(self, language):
        return self.calculateSumofPrices(self.uncommons, language=language)
    
    def calculateRaresPrices(self, language):
        return self.calculateSumofPrices(self.rares, language=language)
    
    def calculateMythicsPrices(self):
        return self.calculateSumofPrices(self.mythics, language=language)
    
    def calculateAverageBoosterPackPrice(self, language):
        common = self.calculateCommonsPrices(language) / len(self.commons)
        uncommon = self.calculateUncommonsPrices(language) / len(self.uncommons)
        rare = self.calculateRaresPrices(language) / len(self.rares)
        #mythic = self.calculateMythicsPrices() / len(self.mythics)
        return({"BoosterValueNoFoil" : round((common * self.boosterStructure.count("common")) + (uncommon * self.boosterStructure.count("uncommon")) + rare, 2),
                "AverageCommon": common,
                "AverageUncommon" : uncommon,
                "AverageRare" : rare})

