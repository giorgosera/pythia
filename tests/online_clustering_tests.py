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
        from_date = datetime.datetime(2011, 1, 25, 12, 0, 0)
        to_date = datetime.datetime(2011, 1, 26, 12, 30, 0) 
        items = ws.get_documents_by_date(from_date, to_date, limit=100)             
        
        window = 100
        oc = OnlineClusterer(N=10, window = window)
        for item in items:
            oc.cluster(item)

        clusters=oc.trimclusters()            
        oc.dump_clusters_to_file("online_with_tweets")
        oc.plot_scatter()

        for cluster in oc.clusters:
            print cluster.id
            print cluster.get_size()
            print '-----------------'

if __name__ == "__main__":
    unittest.main()