'''
The models represent entities in the database 
@author: Giorgos Eracleous
'''

import datetime
from mongoengine import Document, StringField, DateTimeField, IntField, DictField


class Tweet(Document):
    author_screen_name = StringField(required=True)
    author_name = StringField(required=True)
    date = DateTimeField(required=True, default=datetime.datetime.utcnow)
    content = DictField(required=True)
    
    
class CambridgeTweet(Tweet):
    meta = {"collection": "CambridgeTweets"}    
    origin = StringField(required=True, default="Unknown")
    no_of_followers = IntField(required=True, default=0) 
    
class TwoGroupsTweet(Tweet):
    meta = {"collection": "TwoGroupsTweets"}
    url = StringField(required=True)
    retweet_count = IntField(required=True, default=0)
    
class CyprusTweet(Tweet):
    meta = {"collection": "CyprusTweets"}
    url = StringField(required=True)
    retweet_count = IntField(required=True, default=0)
            
class EgyptTweet(Tweet):
    meta = {"collection": "EgyptTweets"}
    url = StringField(required=True)
    retweet_count = IntField(required=True, default=0)
    
class PsychTweet(Tweet):
    meta = {"collection": "PsychTweets"}
    url = StringField(required=True)
    retweet_count = IntField(required=True, default=0)