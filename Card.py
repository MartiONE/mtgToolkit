import json

class Card:
    """
    Card class for Magic The Gathering
    
    """
    def __init__(self, **kwargs):
        self.ID = kwargs.get("id")
        self.layout = kwargs.get("layout")
        self.name = kwargs.get("name")
        self.names = kwargs.get("names")
        self.manaCost = kwargs.get("manaCost")
        self.cmc = kwargs.get("cmc")
        self.colors = kwargs.get("colors")
        self.colorIdentity = kwargs.get("colorIdentity")
        self._type = kwargs.get("type")
        self.supertypes = kwargs.get("supertypes")
        self.types = kwargs.get("types")
        self.subtypes = kwargs.get("subtypes")
        self.rarity = kwargs.get("rarity")
        self.text = kwargs.get("text")
        self.flavor = kwargs.get("flavor")
        self.artist = kwargs.get("artist")
        self.number = kwargs.get("number")
        self.power = kwargs.get("power")
        self.toughness = kwargs.get("toughness")
        self.loyalty = kwargs.get("loyalty")
        self.multiverseid = kwargs.get("multiverseid")
        self.variations = kwargs.get("variations")
        self.imageName = kwargs.get("imageName")
        self.watermark = kwargs.get("watermark")
        self.border = kwargs.get("border")
        self.timeshifter = kwargs.get("timeshifted")
        self.hand = kwargs.get("hand")
        self.life = kwargs.get("life")
        self.reserved = kwargs.get("reserverd")
        self.releaseDate = kwargs.get("releaseDate")
        self.starter = kwargs.get("starter")
        
    def __str__(self):
        return(self.name)