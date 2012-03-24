# -*- coding: utf-8 -*-
'''
Created on 13 Nov 2011

@author: george

Unit tests for the analysis.clustering package.
'''
import datetime, unittest 
from database.warehouse import WarehouseServer
from analysis.clustering.kmeans import OrangeKmeansClusterer
from tests.test_document import get_orange_clustering_test_data

###########################################
# GLOBALS                                #
###########################################
ws = WarehouseServer()
sample_docs = get_orange_clustering_test_data()

oc = OrangeKmeansClusterer(k=2)
for s in sample_docs:
    oc.add_document(s)

class TestOrangeClustering(unittest.TestCase):
    
    ###########################################
    # ORANGE TESTS                            #
    ###########################################       
    def test_orange_sample_doc_kmeans(self):
        km = oc.run("orange_clustering_test")
        expected = [0, 0, 0, 1, 1, 1]
        self.assertEqual(expected, km.clusters)

    def test_orange_with_tweets_kmeans(self):
        import time
        start = time.time()            
        from_date = datetime.datetime(2011, 1, 26, 0, 0, 0)
        to_date = datetime.datetime(2011, 1, 27, 0, 0, 0) 
        items = ws.get_documents_by_date(from_date, to_date, limit=1000)
        
        oc = OrangeKmeansClusterer(k=34, ngram=1)
        oc.add_documents(items)
        oc.run("orange_clustering_test", pca=False)
        print time.time() - start
        oc.plot_growth_timeline(cumulative=False)
        oc.plot_scatter()
        oc.dump_clusters_to_file("kmeans_with_tweets_orange")
            
if __name__ == "__main__":
    unittest.main()