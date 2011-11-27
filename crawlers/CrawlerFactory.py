'''
Created on 27 Nov 2011

@author: george
'''

from TwitterCrawler import TwitterCrawler

#Available crawlers
_crawlers_ = {"twitter": TwitterCrawler}

class CrawlerFactory(object):
    '''
    This class is responsible to provide handles to the supported
    crawlers.
    '''

    def __init__(self):
        '''
        The abstract constructor
        '''
        self.avail_crawlers = _crawlers_
    
    def get_crawler_types(self):
        '''
        Return all the valid crawler types
        '''
        return self.avail_crawlers
    
    def get_crawler(self, crawler_name):
        '''
        Method to return the desired crawler.
        If a valid crawler exists then it gets constructed and returned.
        '''
        crl = self.avail_crawlers.get(crawler_name, None)
        
        if not crl:
            raise Exception("No available crawler exists for " + crawler_name + "." )
        return crl(crawler_name)
    
    
    
    
    
                
    
    
    
