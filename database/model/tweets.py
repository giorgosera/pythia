'''
The models represent entities in the database 
@author: Giorgos Eracleous
'''

import pymongo, datetime
from mongoengine import Document, StringField, DateTimeField, IntField


class Tweet(Document):
    meta = {"collection": "Tweets"}

    username = StringField(required=True)
    date = DateTimeField(required=True, default=datetime.datetime.utcnow)
    origin = StringField(required=True, default="Unknown")
    no_of_followers = IntField(required=True, default=0)
    text = StringField(required=True)
    source = StringField(required=True)
    
    