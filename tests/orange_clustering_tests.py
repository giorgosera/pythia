# -*- coding: utf-8 -*-
'''
Created on 13 Nov 2011

@author: george

Unit tests for the analysis.clustering package.
'''
import datetime, unittest, Orange #!@UnresolvedImport
from analysis.text import TextAnalyser
from visualizations.outputfile import output_clusters_to_file_translated  
from database.warehouse import WarehouseServer
from analysis.clustering.datastructures.clusters import OrangeCluster

###########################################
# GLOBALS                                #
###########################################
ws = WarehouseServer()

doc0 = 'This is a document related to sports : Football, basketball, tennis, golf etc.' 
doc1 = 'In this document we will be talking about basketball, football, tennis, golf and sports in general.'
doc2 = 'I like golf but football is really an amazing sport. I love it. But I love basketball too and tennis'
doc3 = 'This document is related to programming. More specifically Python and CPP. For more info check my blog.'
doc4 = 'I wrote a small Python script to run a clustering algorithm. I hope it works well . If not Ill try CPP' 
doc5 = 'This blog writes about Python and programming in general.'

sample_docs = [doc0, doc1, doc2, doc3, doc4, doc5]
analyser = TextAnalyser()
oc = OrangeCluster()
id = 0
for s in sample_docs:
    index, d = analyser.add_document(id, s)
    oc.add_document(index, d)
    id += 1
    
oc.construct_term_doc_matrix()
oc.save_table("orange_clustering_test")

###########################################
# TESTS                                   #
###########################################
class TestHierarchicalClustering(unittest.TestCase):
           
    def test_orange_sample_doc_kmeans(self):
        
        table = oc.load_table()
        k = 3
        km = Orange.clustering.kmeans.Clustering(table, k, initialization = Orange.clustering.kmeans.init_diversity)
  
        expected = [1, 1, 1, 2, 0, 2]
        self.assertEqual(expected, km.clusters)

    def test_orange_with_tweets_kmeans(self):    
        from_date = datetime.datetime(2011, 1, 25, 12, 0, 0)
        to_date = datetime.datetime(2011, 1, 26, 0, 0, 0) 
        items = ws.get_documents_by_date(from_date, to_date, 50)
 
        t = TextAnalyser()
        oc = OrangeCluster()
        for item in items:
            index, d = t.add_document(item.id, item.text)
            oc.add_document(index, d)
        
        oc.construct_term_doc_matrix()
        oc.save_table("orange_clustering_test")
        k = 3
        table = oc.load_table()
        km = Orange.clustering.kmeans.Clustering(table, k, initialization = Orange.clustering.kmeans.init_diversity, distance=Orange.distance.instances.PearsonRConstructor())
        
        rownames = []
        for inst in table:
            rownames.append(str(inst['id'].value))
        
        clusters = [[] for k in range(k)]
 
        for item_index, cluster in enumerate(km.clusters):
            clusters[cluster].append(item_index)
            
        output_clusters_to_file_translated(clusters, rownames, t, "kmeans_with_tweets_orange")
            
if __name__ == "__main__":
    unittest.main()