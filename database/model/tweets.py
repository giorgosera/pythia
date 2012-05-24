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
    date = DateTimeField(required=True, default=datetime.datetime.utcnow)
    
    def construct_word_freq_list(self, items):
        for item in items:
            t = WordFrequencyTuple()
            t.word = item[0]
            t.count = item[1]
            self.word_frequencies.append(t)
            

class Tweet(Document):
    author_screen_name = StringField(required=True)
    author_name = StringField(required=False)
    date = DateTimeField(required=True, default=datetime.datetime.utcnow)
    content = EmbeddedDocumentField(Content)
    retweet_count = IntField(required=True, default=0)
    
class CambridgeTweet(Tweet):
    meta = {"collection": "CambridgeTweets"}    
    origin = StringField(required=True, default="Unknown")
    no_of_followers = IntField(required=True, default=0) 
    
class TwoGroupsTweet(Tweet):
    meta = {"collection": "TwoGroupsTweets"}
    url = StringField(required=True)
    
class CyprusTweet(Tweet):
    meta = {"collection": "CyprusTweets"}
    url = StringField(required=True)
            
class EgyptTweet(Tweet):
    meta = {"collection": "EgyptTweets", "indexes": [("date")]}
    url = StringField(required=True)
    
class PsychTweet(Tweet):
    meta = {"collection": "PsychTweets"}
    url = StringField(required=True)
    
class TestTweet(Tweet):
    meta = {"collection": "TestTweets"}
    url = StringField(required=True)
    
class EvaluationTweet(Tweet):
    meta = {"collection": "EvaluationTweets"}
    url = StringField(required=True)
    event_class = IntField(required=True, default=0)
    
    def set_event_class(self, event_class):
        '''
        Sets the event class of this tweet. If class doesn't exist it
        creates a new class.
        '''
        event_list = EventList.objects.get()
        if event_class in [event.event_class for event in event_list.event_list]:
            self.event_class = event_class
        else:
            new_event_class = event_class
            new_event_desc = raw_input("This is a new event with class #" + str(new_event_class) + "! What is the description of this event?")
            event_list.add_new_class(new_event_class, new_event_desc)
            self.event_class = new_event_class
        self.save()            
        
    def get_event_description(self, event_class):
        '''
        Based on event_class it returns a textual description
        of the event.
        '''
        for event in el.event_list:
            if event.event_class == event_class:
                return el.event_list
        return None
    
    def get_available_events(self):
        '''
        It returns a list with the available event classes and descriptions.
        '''
        return [event for event in EventList.objects.get().event_list]
        

class EventItem(EmbeddedDocument):
    event_class = IntField(required=True, default=0)
    event_desc = StringField(required=True)

class EventList(Document):
    '''
    A helper class for the evaluation of event detection
    '''
    meta = {"collection": "EventClasses"}
    event_list = ListField(EmbeddedDocumentField(EventItem), required=True, default=list)
    
    def add_new_class(self, event_class, event_desc):
        ei = EventItem()
        ei.event_class = event_class
        ei.event_desc = event_desc
        self.event_list.append(ei)
        self.save()

el = EventList()    