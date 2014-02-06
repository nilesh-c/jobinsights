from scrapy.item import Item, Field


class Profile(Item):

    url = Field()
    workingat = Field()
