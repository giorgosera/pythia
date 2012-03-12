# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field#!@UnresolvedImport

class UserStatsItem(Item):
    retweets = Field()
    retweeted = Field()
    links = Field()
    replies = Field()
    mentions = Field()
    followers = Field()
    friends = Field()
    
