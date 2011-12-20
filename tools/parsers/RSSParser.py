'''
Created on 20 Dec 2011

@author: george
'''
from AbstractParser import AbstractParser
import feedparser#!@UnresolvedImport
from tools.utils import strip_html

class RSSParser(AbstractParser):
    '''
    Concrete implementation of AbstractParser for parsing RSS urls.
    '''
    def __init__(self, url):
        '''
        Constructor
        '''
        super(RSSParser,self).__init__(url)

    def parse(self, url):
        '''
        Parses feed and returns the title and the text found
        in the summary or description
        '''
        d=feedparser.parse(url)
        text = ""
        for e in d.entries:
            if 'summary' in e: summary=e.summary
            else: summary=e.description
        
            words = strip_html(e.title+' '+summary)
            text = text + ' ' + words
            
        return d.feed.title, text
    
    
           
        
        
        