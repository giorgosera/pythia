'''
Created on 27 Nov 2011

@author: george
'''
import otter #!@UnresolvedImport
import time, datetime
from mongoengine import connect
from AbstractCrawler import AbstractCrawler
from analysis.text import TextAnalyser

PAGE_SIZE = 10
connect("pythia_db")

class TopsyCrawler(AbstractCrawler):
    '''
    A Topsy crawler.   
    '''
    def login(self):
        '''
        Connects to the database and sets the API key
        '''    
        pass
        
    def search_for(self, keywords):
        '''
        Sets the keywords which the retrieval will be based upon.
        '''
        self.keywords = keywords
        
    def search_between(self, from_date, to_date, granularity_days=0, granularity_hours=1, granularity_mins=0):
        '''
        Sets the time period we want to retrive the tweets for.
        '''
        self.from_date = from_date
        self.delta = datetime.timedelta(days=granularity_days, hours=granularity_hours, minutes=granularity_mins)
        self.maxtime = self.from_date + self.delta
        self.to_date = to_date 
        
    def retrieve_items_of_type(self, type):
        self.type = type
        
        
    def crawl(self):
        '''
        Performs the actual crawling. 
        '''
        text_analyser = TextAnalyser(ngram=1)
        exception_log = []
        kw = otter.loadrc() # load api key
        count = 0
        while self.maxtime != self.to_date:
            for page in range(PAGE_SIZE):        
                try:
                    search = otter.Resource('search', **kw)
                    #search(q='#jan25 OR #egypt OR #tahrir', mintime = time.mktime(mintime.timetuple()), maxtime = time.mktime(maxtime.timetuple()), type='tweet', offset=page*10)
                    search(q=self.keywords, mintime = time.mktime(self.from_date.timetuple()), maxtime = time.mktime(self.maxtime.timetuple()), type='tweet', perpage=100, page=page+1)
                    for item in search.response.list:
                        print "Storing tweet #",count, "for the period",self.from_date,"until",self.maxtime 
                        tt = self.type()
                        tt.url = item.url
                        #Maybe REMOVE id from text analyser when evrything is refactored
                        print item.content
                        id, content = text_analyser.add_document(0, item.content)
                        tt.content = content
                        print tt.content
                        tt.date = self.from_date
                        tt.screen_name = item.trackback_author_nick
                        tt.retweet_count = item.trackback_total
                        tt.author_screen_name = item.trackback_author_nick
                        tt.author_name = item.trackback_author_name
                        tt.save(safe=True)
                        count += 1     
                except Exception, e:
                    print e
                    exception_log.append(e)
                finally:
                    pass          
            print tt.url        
            print "Retrieving tweets for next three hours"         
            self.from_date = self.maxtime
            self.maxtime += self.delta
                
        print "Succesfully retrieved", count,"tweets!"    
        print "Exceptions:"    
        for e in exception_log:
            print e