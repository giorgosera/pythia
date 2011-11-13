'''
Created on 13 Nov 2011

@author: george

This module boots the application.
'''
import pymongo
from mongoengine import connect

class PythiaApp(object):
    
    def __init__(self):    
        self.db_name = "pythia_db"
        connect(self.db_name)
        
        
if __name__ == "__main__":
    pa = PythiaApp()
    
