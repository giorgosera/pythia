'''
Created on 27 Nov 2011

@author: george
'''
import sys
import time
from urllib2 import URLError
import twitter #!@UnresolvedImport
from twitter.oauth_dance import oauth_dance #!@UnresolvedImport
from AbstractCrawler import AbstractCrawler

class TwitterCrawler(AbstractCrawler):
    '''
    Not a crawler per se since we can access twitter's API and retrieve the tweets.
    It provides a wrapper class for commonly used API methods and of course for 
    the infamous OAuth dance.
    It also deals with the two main exceptions caused by Twitter 410 (not authorized)
    and 503 (OverCapacity) thanks to 'Mining Social Web' by Mathew Russell. 
    '''
    
    def login(self):
        '''
        Performs the OAuth dance and returns a Twitter API object. 
        '''    
        #TODO: Add these keys to a config file instead of having them hardcoded.
        consumer_key = "nAy4J74aqtxxOASxOb8pPQ"
        consumer_secret = "JOapiSE9hTcCjwTAk8DoHUYKOeRGtaFZwK1IcxBjxJQ"
        app_name = "TestGeorge"
        
        (oauth_token, oauth_token_secret) = oauth_dance(app_name, consumer_key, consumer_secret)
        self.twitter_object_handle =  twitter.Twitter(domain='api.twitter.com', api_version='1', 
                                      auth=twitter.oauth.OAuth(oauth_token, oauth_token_secret,
                                      consumer_key, consumer_secret))
        return self.twitter_object_handle
    
    def _make_twitter_request(self, twitter_function, max_errors=3, *args, **kwargs ): 
        '''
        A wrapper method for executing a twitter API request. It is supposed to be a private
        method.
        '''
        wait_period = 2
        error_count = 0
        while True:
            try:
                return twitter_function(*args, **kwargs)
            except twitter.api.TwitterHTTPError, e:
                error_count = 0
                wait_period = self.handle_twitter_http_error(e, wait_period)
                if wait_period is None:
                    return
            except URLError, e:
                error_count += 1
                print >> sys.stderr, "URLError encountered. Continuing."
                if error_count > max_errors:
                    print >> sys.stderr, "Too many consecutive errors...bailing out."
                    raise
        
    def handle_twitter_http_error(self, e, wait_period=2):
        '''
        A method for handling common HTTP errors.
        '''
        if wait_period > 3600: #Seconds
            print >> sys.stderr, "Too many retries. Quitting."
            raise e
        if e.e.code == 401:
            print >> sys.stderr, "Encountered 401 Error (Not Authorized)"
            return None
        elif e.e.code == (502, 503):
            print >> sys.stderr, "Encountered %i Error. Will retry in %i seconds" %(e.e.code, wait_period)
            time.sleep(wait_period)
            wait_period *= 1.5
            return wait_period
        elif self.twitter_object_handle.account.rate_limit_status()['remaining_hits'] == 0:
            status = self.twitter_object_handle.account.rate_limit_status()
            now = time.time() # UTC
            when_rate_limit_resets = status['reset_time_in_seconds'] # UTC
            sleep_time = when_rate_limit_resets - now
            print >> sys.stderr, 'Rate limit reached: sleeping for %i secs' % \
                    (sleep_time, )
            time.sleep(sleep_time)
            return 2
        else:
            raise e
        
    def get_user_info_by_screenname(self, screen_name):
        '''
        Returns a user's info given their screen name.
        The API's response is a JSON object stored as a list element.
        That's why it returns the first element of a list  
        '''     
        info = self._make_twitter_request(self.twitter_object_handle.users.lookup, 
                                              screen_name = screen_name)
        
        return info[0] 
    
    def get_user_followers(self, screen_name=None, limit=10000):
        '''
        Returns the followers of the given user
        '''
        cursor = -1
        result = []
        while cursor != 0:
            response = self._make_twitter_request(self.twitter_object_handle.followers.ids, 
                                                  screen_name=screen_name, 
                                                  cursor=cursor)
            for id in response['ids']:
                result.append(id)    
            cursor = response['next_cursor']
         
        return result
    
    def get_user_friends(self, screen_name=None, limit=10000):
        '''
        Returns the friends of the given user
        '''
        cursor = -1
        result = []
        while cursor != 0:
            response = self._make_twitter_request(self.twitter_object_handle.friends.ids, 
                                                  screen_name=screen_name, 
                                                  cursor=cursor)
            for id in response['ids']:
                result.append(id)    
            cursor = response['next_cursor']
         
        return result
            
        
        
       
    
