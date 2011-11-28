'''
Created on 27 Nov 2011

@author: george
'''
from mongoengine import Document, StringField, ListField, IntField

class Agent(Document):
    twitter_id = IntField(required=True, default=0)
    screen_name = StringField(required=True)
    followers_count = IntField(required=True, default=0)
    friends_count = IntField(required=True, default=0)
    statuses_count = IntField(required=True, default=0)
    location = StringField(required=True, default="Unkown")  
    
class Author(Agent):
    meta = {"collection": "Authors"}
    followers_ids = ListField(IntField(), required=True, default=list)
    friends_ids = ListField(IntField(), required=True, default=list)
    pass    