# -*- coding: utf-8 -*-
'''
Created on 13 Nov 2011

@author: george

Unit tests for the analysis.clustering package.
'''
import datetime, unittest, Orange #!@UnresolvedImport
from analysis.text import TextAnalyser 
from database.warehouse import WarehouseServer
from analysis.clustering.datastructures.clusters import OrangeKmeansClusterer, CustomClusterer
from analysis.clustering.algorithms.algorithms import hierarchical, kmeans, cosine, tanimoto
from visualizations.dendrogram import Dendrogram
from visualizations.Cluster2DPlot import Cluster2DPlot

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

analyser = TextAnalyser(ngram=1)
oc = OrangeKmeansClusterer()
id = 0
for s in sample_docs:
    index, d = analyser.add_document(id, s)
    oc.add_document(index, d)
    id += 1
oc.construct_term_doc_matrix()
oc.save_table("orange_clustering_test") 
   
cc = CustomClusterer()
id = 0
for s in sample_docs:
    index, d = analyser.add_document(id, s)
    cc.add_document(index, d)
    id += 1
    
cc.construct_term_doc_matrix()
cc.save_table("custom_clustering_test.txt")
    
class TestOrangeClustering(unittest.TestCase):
    
    ###########################################
    # ORANGE TESTS                            #
    ###########################################       
    def test_orange_sample_doc_kmeans(self):
        
        table = oc.load_table()
        k = 3
        km = Orange.clustering.kmeans.Clustering(table, k, initialization = Orange.clustering.kmeans.init_diversity)
  
        expected = [1, 1, 1, 2, 0, 2]
        self.assertEqual(expected, km.clusters)

    def test_orange_with_tweets_kmeans(self):    
        from_date = datetime.datetime(2011, 1, 24, 0, 0, 0)
        to_date = datetime.datetime(2011, 1, 25, 0, 0, 0) 
        items = ws.get_documents_by_date(from_date, to_date, 10)
 
        t = TextAnalyser()
        oc = OrangeKmeansClusterer()
        for item in items:
            index, d = t.add_document(item.id, item.text)
            oc.add_document(index, d)
        
        oc.construct_term_doc_matrix()
        oc.save_table("orange_clustering_test")
        
        k = 5
        table = oc.load_table()
        km = Orange.clustering.kmeans.Clustering(table, k, distance =  Orange.distance.instances.PearsonRConstructor)
           
        oc.split_documents(km, k)
        oc.dump_clusters_to_file("kmeans_with_tweets_orange")
        
        
    ###########################################
    # CUSTOM TESTS                            #
    ###########################################       
    def test_sample_doc_hierarchical(self):        
        rownames, colnames, data = cc.load_table()
        cluster = hierarchical(data, similarity=cosine)
        cluster.print_it(rownames)
        
        dendro = Dendrogram(cluster, rownames, "cluster.jpg", cluster.get_height(), cluster.get_depth())
        dendro.draw_node(10, cluster.get_height()/2)
        
    def test_sample_doc_kmeans(self):
        rownames, colnames, data = cc.load_table()
        
        clusters = kmeans(data=data, similarity=cosine, k=2)
        c2dp = Cluster2DPlot(data=data, labels=rownames, filename="2dclusters.jpg")
        c2dp.draw()
        
    def test_tweet_hierarchical_clustering(self):        
        from_date = datetime.datetime(2011, 1, 24, 0, 0, 0)
        to_date = datetime.datetime(2011, 1, 25, 0, 0, 0) 
        items = ws.get_documents_by_date(from_date, to_date, 10)
        
        t = TextAnalyser()
        cc = CustomClusterer()
        for i in items:
            index, d = t.add_document(i.id, i.text)
            cc.add_document(index, d)
        
        cc.construct_term_doc_matrix()
        cc.save_table("custom_cluster_with_tweets.txt")
        rownames, colnames, data = cc.load_table()
        cluster = hierarchical(data)
        
        dendro = Dendrogram(cluster, rownames, "hierarchical_custom_cluster_with_tweets.jpg", cluster.get_height(), cluster.get_depth())
        dendro.draw_node(10, cluster.get_height()/2)
        
    def test_tweet_kmeans_clustering(self):        
        from_date = datetime.datetime(2011, 1, 24, 0, 0, 0)
        to_date = datetime.datetime(2011, 1, 25, 0, 0, 0) 
        items = ws.get_documents_by_date(from_date, to_date, 10)
        
        t = TextAnalyser()
        cc = CustomClusterer()
        for i in items:
            index, d = t.add_document(i.id, i.text)
            cc.add_document(index, d)
        
        cc.construct_term_doc_matrix()
        cc.save_table("custom_cluster_with_tweets.txt")
        rownames, colnames, data = cc.load_table()
        k=5
        km = kmeans(data, k=5)
        cc.split_documents(km, k)
        cc.dump_clusters_to_file("kmeans_with_tweets_custom")
            
if __name__ == "__main__":
    unittest.main()