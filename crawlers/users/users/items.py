# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field#!@UnresolvedImport

class UserStatsItem(Item):
    screen_name = Field()
    total_tweets = Field()
    retweets = Field()
    retweeted = Field()
    links = Field()
    replies = Field()
    mentions = Field()
    followers = Field()
    friends = Field()
    
