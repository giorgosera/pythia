'''
Created on 3 Feb 2012

@author: george
'''

from database.warehouse import WarehouseServer
from analysis.clustering.kmeans import OrangeKmeansClusterer
from analysis.clustering.nmf import NMFClusterer

class Clustering(object):
    '''
    This class deals with the clustering procedure
    '''
    
    def __init__(self, from_date, 
                       to_date, 
                       limit, 
                       method='kmeans',
                       k = 3, 
                       ngram = 1,
                       db_collection="TopsyTweets", 
                       high_quality=False, 
                       quality_threshold=1):
        '''
        Initializes the system parameters.
        '''
        self.from_date = from_date
        self.to_date = to_date
        self.limit = limit
        self.method = method
        self.k = k
        self.ngram = ngram
        self.db_collection = db_collection
        self.high_quality = high_quality
        self.quality_threshold  = quality_threshold
        self.ws = WarehouseServer()
        self.data = None
        self.clusterer = None
        
    def retrieve_data(self):
        '''
        This method retrieves the data from the database according to the params 
        given. Quality refers to the kind of tweets we will retrieve friom the db.
        For example highly rated tweets are the ones whuch have been retweeted many times (quality_threshold)
        '''
        if self.high_quality:   
            data = self.ws.get_top_documents_by_date(self.from_date, self.to_date, self.quality_threshold)
        else:
            data = self.ws.get_documents_by_date(self.from_date, self.to_date)
            
        self.data = data
        
    def run(self):
        '''
        Initialises the clusterer to be used
        '''
        #First get the data from the db.
        self.retrieve_data()
        
        #And then initialise the clusterer
        if self.method == "kmeans":
            self.cluster = OrangeKmeansClusterer(self.k, self.ngram)
        elif self.method == "nmf":
            self.cluster = NMFClusterer(self.ngram)
        
        #Analyse data
        for item in self.data:
            self.clusterer.add_document(item.id, item.content)
        
        #Run the actual algorithm
        if self.method == "kmeans":
            self.clusterer.run("orange_clustering_test")
        else:    
            self.clusterer.run(seed = 'random_vcol', method='nmf', rank=self.k, max_iter=65, display_N_tokens = 6, display_N_documents =10)  
        