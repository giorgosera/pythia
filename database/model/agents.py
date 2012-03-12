'''
Created on 27 Nov 2011

@author: george
'''
import datetime, tools.utils, numpy
from urlparse import urlparse
from database.model.tweets import *
from mongoengine import Document, StringField, ListField, IntField, DateTimeField, EmbeddedDocument, EmbeddedDocumentField, ReferenceField, GenericReferenceField, FloatField

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
    type = StringField(required=False)
    followers_ids = ListField(IntField(), required=True, default=list)
    friends_ids = ListField(IntField(), required=True, default=list)
    
    tweets = ListField(GenericReferenceField(Tweet), required=True, default=list) 
    retweets = IntField(required=True, default=0) 
    retweeted_tweets = IntField(required=True, default=0)
    links = IntField(required=True, default=0)
    replies_to_others = IntField(required=True, default=0)
    mentions_by_others = IntField(required=True, default=0)
    feature_vector = ListField(FloatField(), required=True, default=list)
    
    followers_history = ListField(EmbeddedDocumentField(History), required=True, default=list)
    friends_history = ListField(EmbeddedDocumentField(History), required=True, default=list)
    
    def update_feature_vector(self):
        '''
        Updates and returns the feature vector. If it doesn't exist it creates it.
        '''
        self.reset_stats()
        self.calculate_author_stats()
        total_tweets = len(self.tweets)
        vector = numpy.zeros(6, dtype=float)

        vector[0] = float(self.retweets)/float(total_tweets) #retweet ratio
        vector[1] = self.links/float(total_tweets) #links ratio
        
        if self.retweeted_tweets != 0:
            vector[2] = float(total_tweets)/self.retweeted_tweets #how often this author gets retweeted
        else:
            vector[2] = float(total_tweets)/(self.retweeted_tweets+1)
            
        vector[3] = self.replies_to_others / float(total_tweets) #how many of them are replies
        vector[4] = self.mentions_by_others
        
        if self.friends_count != 0:
            vector[5] = self.followers_count / float(self.friends_count)
        else:
            #Add 1 to friends count to avoid division by zero
            vector[5] = self.followers_count / (self.friends_count+1.0)
            
        self.feature_vector = vector.tolist()
        return self.feature_vector
    
    def reset_stats(self):
        '''
        Resets all the stats to allow for update
        '''
        self.retweets = 0
        self.retweeted_tweets = 0
        self.links = 0
        self.replies_to_others = 0
        self.mentions_by_others = 0
    
    def calculate_author_stats(self):
        '''
        Parses the entire list of this author's tweets and calculates stats
        '''
        for tweet in self.tweets:
            self.update_retweeted(tweet)
            self.update_links(tweet)
            is_a_retweet = self.update_retweets(tweet)
            if not is_a_retweet:
                self.update_mentions_and_replies(tweet)
            self.save(safe=True)
                
    def update_retweeted(self, tweet):
        '''
        Parses the tweet and if it belongs to this author and has been retweeted 
        then it updates the retweeted (another author retweeted this) count
        '''
        #If the url belongs to that user then this is their tweet so theri retweets as well
        if self.screen_name == urlparse(tweet.url).path.split('/')[1]:
            self.retweeted_tweets += tweet.retweet_count        
            
            
    def update_links(self, tweet):
        '''
        Parses the tweet and if it contains a url it updates the links count
        '''
        urls = tools.utils.extract_urls(tweet.content.raw)
        if len(urls) > 0 : #We just want to find out if this tweet has aurl not how many
            self.links += 1 
            
    def update_retweets(self, tweet):
        '''
        Parses the tweet and if it is a retweet it updates the retweet count
        '''
        #if this is a retweet increase counter
        is_a_retweet = tools.utils.is_a_retweet(tweet.content.raw)
        if is_a_retweet:    
            self.retweets += 1 
        return is_a_retweet
    
    def update_mentions_and_replies(self, tweet):
        '''
        If this is a mention to another user then increase replies
        counter and also update the mentioned user's mentions
        '''
        mentions = tools.utils.get_mentions(tweet.content.raw)
        if len(mentions) > 0:
            self.replies_to_others += 1 #No matter how many people are mentioned in the tweet we just increase by one cz we just want to know if this tweet is a reply 
            for mention in mentions:
                mentioned_author = Author.objects(screen_name=mention)                  
                if len(mentioned_author) > 0:
                    mentioned_author.update(inc__mentions_by_others=1)

class TestAuthor(Author):
    meta = {"collection": "TestAuthors"} 
    
    def update_mentions_and_replies(self, tweet):
        '''
        If this is a mention to another user then increase replies
        counter and also update the mentioned user's mentions
        '''
        mentions = tools.utils.get_mentions(tweet.content.raw)
        if len(mentions) > 0:
            self.replies_to_others += 1 #No matter how many people are mentioned in the tweet we just increase by one cz we just want to know if this tweet is a reply 
            for mention in mentions:
                mentioned_author = TestAuthor.objects(screen_name=mention)                   
                if len(mentioned_author) > 0:
                    mentioned_author.update(inc__mentions_by_others=1)