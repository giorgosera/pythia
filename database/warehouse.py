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
        
    
    def get_documents_by_date(self, from_date, to_date, limit = 10000, collection="TopsyTweets"):
        '''
        This is a getter which returns all the documents which were retrieved during
        the period from_date <--> to_date. 
        '''
        t = TopsyTweet.objects(Q(date__gte=from_date) & Q(date__lte=to_date)).limit(limit)
        return t
    
    def get_all_documents(self, collection="TopsyTweets"):
        '''
        This is a getter which returns all the documents in the collection.
        '''
        t = TopsyTweet.objects
        return t
    
    def get_n_documents(self, n=0, collection="TopsyTweets"):
        '''
        This is a getter which returns the n first the documents in the collection.
        '''
        t = TopsyTweet.objects[:n]
        return t
    
    def get_document_by_id(self, id, collection="TopsyTweets"):
        '''
        Returns the document which corresponds to this id
        '''
        return TopsyTweet.objects(id=id).get()
    
    def save_topsy_document(self, document):
        '''
        Saves a tweet coming from Topsy
        '''
        pass