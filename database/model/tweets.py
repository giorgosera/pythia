'''
The models represent entities in the database 
@author: Giorgos Eracleous
'''

import datetime
from mongoengine import Document, StringField, DateTimeField, IntField


class Tweet(Document):
    screen_name = StringField(required=True)
    date = DateTimeField(required=True, default=datetime.datetime.utcnow)
    text = StringField(required=True)
    
class CambridgeTweet(Tweet):
    meta = {"collection": "CambridgeTweets"}
    
    origin = StringField(required=True, default="Unknown")
    no_of_followers = IntField(required=True, default=0) 
    
class TwoGroupsTweet(Tweet):
    meta = {"collection": "TwoGroupsTweets"}
    #The url of the original tweet
    url = StringField(required=True)

class CyprusTweet(Tweet):
    meta = {"collection": "CyprusTweets"}
    #The url of the original tweet
    url = StringField(required=True)
        
class TopsyTweet(Tweet):
    meta = {"collection": "TopsyTweets"}
    #The url of the original tweet
    url = StringField(required=True)

    #What else is available in response:
    #title = StringField()
    #hits = IntField(required=True, default=0)
    #trackback_total = IntField(required=True, default=0)
    #highlight = StringField()
    #The url of the author trackbacked tweet
    #trackback_author_url = StringField()
    #trackback_permalink = StringField()
    #topsy_author_url = StringField(required=True)  

