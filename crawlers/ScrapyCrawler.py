'''
Created on 27 Nov 2011

@author: george
'''
import os, json
from mongoengine import connect
from AbstractCrawler import AbstractCrawler

PAGE_SIZE = 10
connect("pythia_db")
type_dict = {0: "Celebrity", 1: "Media", 2: "Journalist", 3: "Activist", 4: "Commoner" }

from mongoengine import connect
connect("pythia_db")

class UserCrawler(AbstractCrawler):
    '''
    A Scrapy crawler.   
    '''             
    def setup(self, user_type):
        '''
        Sets up the crawler
        Training indicates if this crawler will retrieve training data
        '''
        self.user_type = user_type
        os.chdir("/home/george/virtualenvfyp/pythia/src/crawlers/users/")
        if os.path.exists('/home/george/virtualenvfyp/pythia/src/crawlers/users/items.json'):
            os.remove('/home/george/virtualenvfyp/pythia/src/crawlers/users/items.json')
           
    def crawl(self, url=None, store=False):
        '''
        Performs the actual crawling. If no url is passed then the crawler
        parses the default ones. If store is True then we user is prompted to input
        the user type. Otherwise we just return the results. The return type is a list of 
        item structs. 
        '''
        if url !=None:
            os.system('scrapy crawl user_stats -o items.json -t json -a user_url='+ url)
        else:
            os.system('scrapy crawl user_stats -o items.json -t json')
            
        json_data=open("/home/george/virtualenvfyp/pythia/src/crawlers/users/items.json")
        data = json.load(json_data)
        
        #Store training data in the database
        if store:
            for d in data:
                if len(self.user_type.objects(screen_name = d['screen_name'])) == 0:
                    type = raw_input("What type of user " + d["screen_name"] + " is?")
                    ta = self.user_type()
                    ta.screen_name = d["screen_name"]
                    ta.tweets_count = d['total_tweets'] 
                    ta.type = type
                    items = [d['retweets'], d['links'], d['retweeted'], d['replies'], d['mentions'], d['followers'], d['friends']]
                    ta.create_feature_vector(items)
                    print 'You have stored ' + ta.screen_name + " as " + type_dict[int(ta.type)]
                    print "Their feature vector from twtrland:"
                    print [d['retweets'], d['links'], d['retweeted'], d['replies'], d['mentions'], float(d['followers'])/d['friends']]
                    print "Their stored feature vector"
                    print ta.feature_vector
                else:
                    print d['screen_name'] + " already exists in the database"
                print '---------------------------------------------------------------'
        else:
            return data
