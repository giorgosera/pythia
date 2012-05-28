'''
Created on 26 Jan 2012

@author: george
'''
import datetime, cProfile
from analysis.clustering.nmf import NMFClusterer
from database.warehouse import WarehouseServer

###########################################
# GLOBALS                                 #
###########################################
ws = WarehouseServer()

def nmf_clustering_with_tweets():
    from_date = datetime.datetime(2011, 1, 23, 0, 0, 0)
    to_date = datetime.datetime(2011, 1, 27, 0, 0, 0) 
    items = ws.get_documents_by_date(from_date, to_date, limit=100)
    nmfc = NMFClusterer(seed = 'random_vcol', method='nmf', rank=30, max_iter=65, display_N_tokens = 6, display_N_documents =10)
    nmfc.add_documents(items)
    
    nmfc.run()
    nmfc.dump_clusters_to_file("nmf_with_tweets")
        
if __name__ == "__main__":
    cProfile.run('nmf_clustering_with_tweets()', 'nmf.profile')    