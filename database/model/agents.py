'''
Created on 27 Nov 2011

@author: george
'''
import datetime, tools.utils, numpy
from urlparse import urlparse
from database.model.tweets import *
from mongoengine import Document, StringField, ListField, IntField, DateTimeField, EmbeddedDocument, EmbeddedDocumentField, ReferenceField, GenericReferenceField, FloatField
from crawlers.CrawlerFactory import CrawlerFactory

#Initialises crawler
f = CrawlerFactory()
crawler = f.get_crawler("scrapy")


class History(EmbeddedDocument):
    date = DateTimeField(required=True, default=datetime.datetime.utcnow())
    count = IntField(required=True, default=0)
    
class Agent(Document):
    #twitter_id = IntField(required=True, default=0)
    screen_name = StringField(required=True)
    followers_count = IntField(required=True, default=-1)
    friends_count = IntField(required=True, default=-1)
    #statuses_count = IntField(required=True, default=0)
    
class Author(Agent):
    meta = {"collection": "Authors"}
    type =IntField(required=True, default=0)
    followers_ids = ListField(IntField(), required=True, default=list)
    friends_ids = ListField(IntField(), required=True, default=list)
    
    tweets = ListField(GenericReferenceField(Tweet), required=True, default=list) 
    tweets_count = IntField(required=True, default=0)
    retweets = IntField(required=True, default=0) 
    retweeted_tweets = IntField(required=True, default=0)
    links = IntField(required=True, default=0)
    replies_to_others = IntField(required=True, default=0)
    mentions_to_others = IntField(required=True, default=0)
    feature_vector = ListField(FloatField(), required=True, default=list)
    
    followers_history = ListField(EmbeddedDocumentField(History), required=True, default=list)
    friends_history = ListField(EmbeddedDocumentField(History), required=True, default=list)
    
    def update_feature_vector(self):
        '''
        Instead of calculating the stats from the stored tweets we get them 
        from the crawler.
        '''
        crawler.setup(user_type=self)
        d = crawler.crawl(url='http://twtrland.com/profile/'+self.screen_name, store=False)[0]
        if d: #if there was NOTHING wrong in crawling
            items = [d['retweets'], d['links'], d['retweeted'], d['replies'], d['mentions'], d['followers'], d['friends']]
            self.retweets = items[0]
            self.links = items[1]
            self.retweeted_tweets = items[2] 
            self.replies_to_others = items[3] 
            self.mentions_to_others = items[4]
            self.followers_count = items[5]
            self.friends_count = items[6]
            if self.friends_count == 0:
                self.friends_count = 1
            self.feature_vector = [self.retweets, self.links, self.retweeted_tweets, self.replies_to_others, self.mentions_to_others, float(self.followers_count)/self.friends_count]
            self.save()
        return self.feature_vector
    
    def get_feature_vector_with_type(self):
        '''
        Returns the feature vector with the type of the author in the end
        '''
        self.feature_vector.append(self.type)
        return self.feature_vector
        


class TestAuthor(Author):
    meta = {"collection": "TestAuthors"} 
                    
class TrainingAuthor(Author):
    meta = {"collection": "TrainingAuthors"} 
    
    def create_feature_vector(self, items):
        '''
        Instead of calculating the stats from the stored tweets we get them 
        from the crawler.
        '''
        self.retweets = items[0]
        self.links = items[1]
        self.retweeted_tweets = items[2] 
        self.replies_to_others = items[3] 
        self.mentions_to_others = items[4]
        self.followers_count = items[5]
        self.friends_count = items[6]
        self.feature_vector = [self.retweets, self.links, self.retweeted_tweets, self.replies_to_others, self.mentions_to_others, float(self.followers_count)/self.friends_count]
        self.save()