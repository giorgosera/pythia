'''
Created on 26 Jan 2012

@author: george
'''
import cProfile, datetime, time
from analysis.clustering.online import OnlineKmeansClusterer
from database.warehouse import WarehouseServer
###########################################
# GLOBALS                                #
###########################################
ws = WarehouseServer()

def online_clustering_with_tweets():
    from_date = datetime.datetime(2011, 1, 25, 0, 0, 0)
    to_date = datetime.datetime(2011, 1, 26, 0, 00, 0) 
    items = ws.get_documents_by_date(from_date, to_date, limit=500)             
    
    okc = OnlineKmeansClusterer(window=500)
    for doc in items:
        okc.cluster(k=50, document = doc)    
    
    for cluster in okc.clusters:
        print '------------------------------------------------'
        for document in cluster.documents:
            print document.raw

if __name__ == "__main__":
    cProfile.run('online_clustering_with_tweets()', 'kmeansonline.profile')