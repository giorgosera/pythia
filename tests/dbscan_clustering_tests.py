'''
Created on 26 Jan 2012

@author: george
'''
import unittest, datetime
from analysis.clustering.dbscan import DBSCANClusterer
from database.warehouse import WarehouseServer

###########################################
# GLOBALS                                #
###########################################
ws = WarehouseServer()
    
class Test_Dbscan_clustering(unittest.TestCase):

    def test_dbscan_clustering_with_tweets(self):
        from_date = datetime.datetime(2011, 1, 25, 12, 0, 0)
        to_date = datetime.datetime(2011, 1, 26, 12, 30, 0) 
        items = ws.get_documents_by_date(from_date, to_date, limit=600)             
        
        epsilon = 0.01
        min_pts = 2
        dbscan = DBSCANClusterer(filter_terms=True)
        dbscan.add_documents(items)
        clusters = dbscan.run(epsilon, min_pts, pca=True)
        dbscan.dump_clusters_to_file("dbscan_with_tweets")
        #=======================================================================
        dbscan.plot_scatter()
        # dbscan.plot_growth_timeline(cumulative=True)
        dbscan.plot_growth_timeline(cumulative=True)
        # dbscan.plot_sentiment_timeline(cumulative=False)
        #=======================================================================
         
if __name__ == "__main__":
    unittest.main()