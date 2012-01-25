'''
Created on 13 Nov 2011

@author: george

This module boots the application.
'''
import bingtrans
from mongoengine import connect
from calais import Calais #!@UnresolvedImport

class PythiaApp(object):
    
    def __init__(self):    
        self.db_name = "pythia_db"
        
        self.connections = {"db": connect(self.db_name),
                            "calais": Calais("av536xwvy4mgmcbw9cancqmd", submitter="pythia-application")
                            }
        
    def get_connections(self):
        '''
        Returns the collections dictionary
        '''
        return self.connections
    
    
    
