'''
Created on 26 Jan 2012

@author: george
'''
import unittest
import datetime
from analysis.text import TextAnalyser
from analysis.clustering.algorithms.algorithms import hierarchical, kmeans, cosine, tanimoto
from visualizations.dendrogram import Dendrogram
from visualizations.Cluster2DPlot import Cluster2DPlot
from visualizations.outputfile import output_clusters_to_file_translated
from database.warehouse import WarehouseServer
from analysis.clustering.datastructures.clusters import CustomClusterer

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
cc = CustomClusterer()
id = 0
for s in sample_docs:
    index, d = analyser.add_document(id, s)
    cc.add_document(index, d)
    id += 1

cc.construct_term_doc_matrix()
cc.save_table("custom_clustering_test.txt")

class Test(unittest.TestCase):

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
        from_date = datetime.datetime(2011, 1, 25, 0, 0, 0)
        to_date = datetime.datetime(2011, 1, 25, 3, 0, 0) 
        items = ws.get_documents_by_date(from_date, to_date, 50)
        
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
        from_date = datetime.datetime(2011, 1, 25, 12, 0, 0)
        to_date = datetime.datetime(2011, 1, 26, 0, 0, 0) 
        items = ws.get_documents_by_date(from_date, to_date, 50)
        
        t = TextAnalyser()
        cc = CustomClusterer()
        for i in items:
            index, d = t.add_document(i.id, i.text)
            cc.add_document(index, d)
        
        cc.construct_term_doc_matrix()
        cc.save_table("custom_cluster_with_tweets.txt")
        rownames, colnames, data = cc.load_table()
  
        clusters = kmeans(data, k=5)
        output_clusters_to_file_translated(clusters, rownames, cc, "kmeans_with_tweets_custom")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()