'''
Created on 20 Dec 2011

@author: george
'''

class AbstractParser(object):
    '''
    Defines the interface for an abstract parser. 
    '''
    
    def __init__(self, url):
        '''
        Constructor
        '''
        self.url = url
        
    def parse(self):
        '''
        Performs the parsing. Child classes must implement it.
        '''    
        raise NotImplementedError("parse() is not implemented.") 
        
        