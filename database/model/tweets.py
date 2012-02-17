'''
The models represent entities in the database 
@author: Giorgos Eracleous
'''

import datetime
from mongoengine import Document, StringField, DateTimeField, IntField, DateTimeField, EmbeddedDocument, EmbeddedDocumentField, ListField

class WordFrequencyTuple(EmbeddedDocument):
    word = StringField(required=True, default="Unknown")
    count = IntField(required=True, default=0)

class Content(EmbeddedDocument):
    raw = StringField(required=True, default="Unknown")
    tokens = ListField(StringField(), required=True, default=list)
    word_frequencies = ListField(EmbeddedDocumentField(WordFrequencyTuple), required=True, default=list)
    date = DateTimeField(required=True)
    
    def construct_word_freq_list(self, items):
        for item in items:
            t = WordFrequencyTuple()
            t.word = item[0]
            t.count = item[1]
            self.word_frequencies.append(t)
            

class Tweet(Document):
    author_screen_name = StringField(required=True)
    author_name = StringField(required=True)
    date = DateTimeField(required=True, default=datetime.datetime.utcnow)
    #content = DictField(required=True)
    content = EmbeddedDocumentField(Content)
    
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