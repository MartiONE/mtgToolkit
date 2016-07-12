import requests
import json
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
            
    def calculateSetPrice(self, language="English"):
        for card in self.cards:
            req = requests.get("https://www.magiccardmarket.eu/Products/Singles/{}/{}".format(self.setName, "+".join(card.name.split())))
            pass

