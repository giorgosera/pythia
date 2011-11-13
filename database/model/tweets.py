'''
The models represent entities in the database 
@author: Giorgos Eracleous
'''

import pymongo, datetime
from mongoengine import Document, StringField, DateTimeField, IntField


class Tweet(Document):
    username = StringField(required=True)
    date = DateTimeField(required=True, default=datetime.datetime.utcnow)
    text = StringField(required=True)
    
class CambridgeTweet(Tweet):
    meta = {"collection": "CambridgeTweets"}
    
    origin = StringField(required=True, default="Unknown")
    no_of_followers = IntField(required=True, default=0) 
    
class TopsyTweet(Tweet):
    meta = {"collection": "TopsyTweets"}
    
    hits = IntField(required=True, default=0)
    title = StringField(required=True)
    #The url of the original author
    url = StringField(required=True)
    trackback_total = IntField(required=True, default=0)
    highlight = StringField(required=True)
    #The url of the author trackbacked tweet
    trackback_author_url = StringField(required=True)
    trackback_permalink = StringField(required=True)
    topsy_author_url = StringField(required=True)  

