'''
Created on 26 Jan 2012

@author: george
'''
import cProfile, datetime
from analysis.clustering.dbscan import DBSCANClusterer
from database.warehouse import WarehouseServer
from analysis.clustering.algorithms import cosine, euclidean 

###########################################
# GLOBALS                                #
###########################################
ws = WarehouseServer()
    
def dbscan_clustering_with_tweets():
    from_date = datetime.datetime(2011, 1, 25, 12, 0, 0)
    to_date = datetime.datetime(2011, 1, 26, 12, 30, 0) 
    items = ws.get_documents_by_date(from_date, to_date, limit=100)             
    
    epsilon = 0.02
    min_pts = 2
    dbscan = DBSCANClusterer(epsilon=epsilon, min_pts=min_pts, distance=euclidean)
    dbscan.add_documents(items)
    clusters = dbscan.run(pca=True)
    dbscan.dump_clusters_to_file("dbscan_with_tweets")
    dbscan.plot_scatter()
         
if __name__ == "__main__":
    cProfile.run('dbscan_clustering_with_tweets()', 'dbscan.profile')    