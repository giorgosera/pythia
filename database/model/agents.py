'''
Created on 27 Nov 2011

@author: george
'''
from mongoengine import Document, StringField, DateTimeField, IntField

class Agent(Document):
    screen_name = StringField(required=True)
    followers_count = IntField(required=True, default=0)
    friends_count = IntField(required=True, default=0)
    statuses_count = IntField(required=True, default=0)
    location = StringField(required=True, default="Unkown")  
    
class Author(Agent):
    pass    