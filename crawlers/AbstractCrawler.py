'''
Created on 27 Nov 2011

@author: george
'''

class AbstractCrawler(object):
    '''
    All crawlers should inherit fromt this abstract crawler
    '''    
    
    def __init__(self, crawler_name):
        self.name = crawler_name

#========================================================================#

