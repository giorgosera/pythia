'''
Created on 28 Nov 2011

@author: george
'''
import tools.utils
from collections import OrderedDict

class AbstractSocialAnalyser(object):
    '''
    This an abstract class for social analysis classes. 
    '''

    def __init__(self, dataset):
        '''
        Constructs a social analyser. Dataset is a dict
        object which is the result of the text analyser
        processing.
        '''
        self.dataset = dataset
    
    
class TwitterSocialAnalyser(AbstractSocialAnalyser):
    '''
    Deals with Twitter related social analysis. 
    '''    
    
    def filter_retweets(self):
        '''
        Filters out all the tweet which are not retweets.
        In this function we assume that a retweet is a tweet which contains 
        either this pattern: RT @username or this pattern: (via @username).
        '''
        filtered = OrderedDict()
        for tweet_id in self.dataset.keys():
            tweet = self.dataset[tweet_id]
            if tools.utils.is_a_retweet(tweet["raw"]):
                filtered[tweet_id] = tweet
        
        return filtered
        
    def filter_mentions(self):
        '''
        Filters out all the tweet which are not mentions (contain the @ operator).
        '''
        filtered = OrderedDict()
        for tweet_id in self.dataset.keys():
            tweet = self.dataset[tweet_id]
            if tools.utils.is_a_retweet(tweet["raw"]):
                filtered[tweet_id] = tweet
        
        return filtered
            
                
            
                
    
    
        
        
        