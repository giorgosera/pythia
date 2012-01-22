'''
Created on 22 Jan 2012

@author: george
'''
from mongoengine import *
from database.model.tweets import *

class WarehouseServer(object):
    '''
    This is a class containing methods related to the warehouse and 
    provides getters for clients to retrieve data.
    '''
    
    def __init__(self):
        '''
        Constructs a Warehouse server object and initiates connection with the database.
        '''
        self.connection = connect("pythia_db")
        
    
    def get_documents_by_date(self, from_date, to_date, collection="TopsyTweets"):
        '''
        This is a getter which returns all the documents which were retrieved during
        the period from_date <--> to_date. 
        '''
        t = TopsyTweet.objects[:900]
        return t
        