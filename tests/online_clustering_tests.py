'''
Created on 26 Jan 2012

@author: george
'''
import unittest, datetime
from analysis.clustering.online import OnlineClusterer
from database.warehouse import WarehouseServer
import pylab#!@UnresolvedImport
###########################################
# GLOBALS                                #
###########################################
ws = WarehouseServer()
    
class Test_online_clustering(unittest.TestCase):

    def test_online_clustering_with_tweets(self):
        from_date = datetime.datetime(2011, 1, 25, 0, 0, 0)
        to_date = datetime.datetime(2011, 1, 26, 0, 00, 0) 
        items = ws.get_top_documents_by_date(from_date, to_date, threshold=1000)             
        
        window = 300
        oc = OnlineClusterer(N=50, window = window)
        for item in items:
            oc.cluster(item)

        clusters=oc.trimclusters()            
        oc.dump_clusters_to_file("online_with_tweets")
        oc.plot_scatter()
        oc.plot_growth_timeline(cumulative=True)

        for cluster in oc.clusters:
            print cluster.id
            print cluster.get_size()
            print '-----------------'

if __name__ == "__main__":
    unittest.main()