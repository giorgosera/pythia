'''
Created on 26 Jan 2012

@author: george
'''
import cProfile, datetime, time
from analysis.clustering.online import OnlineClusterer
from database.warehouse import WarehouseServer
###########################################
# GLOBALS                                #
###########################################
ws = WarehouseServer()

def online_clustering_with_tweets():
    from_date = datetime.datetime(2011, 1, 25, 12, 0, 0)
    to_date = datetime.datetime(2011, 1, 26, 12, 30, 0) 
    items = ws.get_documents_by_date(from_date, to_date, limit=300)             
    
    window = 100
    start = time.time() 
    oc = OnlineClusterer(N=50, window = window)
    for item in items:
        oc.cluster(item)
    print time.time() - start        
    clusters=oc.trimclusters()    

    oc.dump_clusters_to_file("online_with_tweets")
    oc.plot_scatter()

    #=======================================================================
    # for cluster in oc.clusters:
    #    print cluster.id
    #    print cluster.get_size()
    #    print '-----------------'
    #=======================================================================

if __name__ == "__main__":
    cProfile.run('online_clustering_with_tweets()', 'online.profile')