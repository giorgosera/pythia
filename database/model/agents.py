'''
Created on 27 Nov 2011

@author: george
'''
import datetime
from mongoengine import Document, StringField, ListField, IntField, DateTimeField, EmbeddedDocument, EmbeddedDocumentField

class History(EmbeddedDocument):
    date = DateTimeField(required=True, default=datetime.datetime.utcnow())
    count = IntField(required=True, default=0)
    
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
    followers_history = ListField(EmbeddedDocumentField(History), required=True, default=list)
    friends_history = ListField(EmbeddedDocumentField(History), required=True, default=list)
