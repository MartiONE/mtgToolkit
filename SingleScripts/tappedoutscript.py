import requests
from lxml import html
import re

def getCardJSON(url):
    r = requests.get(url)
    if r.status_code == 200:
        tree = html.fromstring(r.text)
        result = {}
        for item in tree.xpath("//div[@class='col-sm-9']/div[@class='well'][1]/div[2]/div/ul/li"):
            result[item.xpath("span")[0].text_content()] = item.xpath("a/@data-quantity")[0]
        return result 
    

def getPrices(cards, collections):
    total = 0
    collections = ["+".join(x.split()) for x in collections]
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
    for card, amount in cards.items():
        if card not in ["Swamp", "Mountain", "Island", "Plains", "Forest"]:
            found = False
            for collection in collections:
                if not found:
                    req = requests.post("https://www.magiccardmarket.eu/Products/Singles/{}/{}".format(collection, "+".join(card.split()).replace("/", "%2F%2F").replace("'", "%27")), data = payload)
                    if (req.status_code == 200) and (card in req.text): found = True
            if not found:
                print("Error on card {}".format(card))
            else:
                tree = html.fromstring(req.text)
                a = tree.xpath("//tbody[@id='articlesTable']/tr/td[@class='st_price']")[0]
                total += float(re.match("\d{1,2}[\.,]\d+", a.text_content()).group().replace(",", "."))*int(amount)
    return round(total, 2)
print(getPrices(getCardJSON("http://tappedout.net/mtg-decks/dissension-azorius-ascendant/"), ["Ravnica%3A+City+of+Guilds", "Dissension", "Guildpact"]))
            