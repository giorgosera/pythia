'''
Created on 13 Nov 2011

@author: george

Unit tests for the analysis.clustering package.
'''
import datetime
import unittest
from analysis.text import TextAnalyser
from analysis.clustering.algorithms.algorithms import hierarchical, kmeans, cosine, tanimoto
from visualizations.dendrogram import Dendrogram
from visualizations.Cluster2DPlot import Cluster2DPlot
from visualizations.outputfile import output_clusters_to_file 
from database.warehouse import WarehouseServer

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
id = 0
for s in sample_docs:
    analyser.add_document(id, s)
    id += 1


class TestHierarchicalClustering(unittest.TestCase):
    
    def test_hierarchical(self):        
        analyser.save_frequency_matrix("test.txt")
        rownames, colnames, data = analyser.read_frequency_matrix("test.txt")
        
        cluster = hierarchical(data, similarity=cosine)
        cluster.print_it(rownames)
        
        dendro = Dendrogram(cluster, rownames, "cluster.jpg", cluster.get_height(), cluster.get_depth())
        dendro.draw_node(10, cluster.get_height()/2)
        
    def test_kmeans(self):
        analyser.save_frequency_matrix("test.txt")
        rownames, colnames, data = analyser.read_frequency_matrix("test.txt")
        
        clusters = kmeans(data=data, similarity=cosine, k=2)
        c2dp = Cluster2DPlot(data=data, labels=rownames, filename="2dclusters.jpg")
        c2dp.draw()
        

    def test_tweet_hierarchical_clustering(self):        

        from_date = datetime.datetime(2011, 1, 25, 0, 0, 0)
        to_date = datetime.datetime(2011, 1, 25, 3, 0, 0) 
        items = ws.get_documents_by_date(from_date, to_date)
        
        t = TextAnalyser()
        for i in items:
            print i.date
            t.add_document(i.id, i.text)
        
        t.save_frequency_matrix("tweet_clusters.txt")
        rownames, colnames, data = t.read_frequency_matrix("tweet_clusters.txt")

        cluster = hierarchical(data)
        
        dendro = Dendrogram(cluster, rownames, "tweet_cluster.jpg", cluster.get_height(), cluster.get_depth())
        dendro.draw_node(10, cluster.get_height()/2)
        
    def test_tweet_kmeans_clustering(self):        

        from_date = datetime.datetime(2011, 1, 25, 0, 0, 0)
        to_date = datetime.datetime(2011, 1, 25, 3, 0, 0) 
        items = ws.get_documents_by_date(from_date, to_date)
        
        t = TextAnalyser()
        for i in items:
            print i.date
            t.add_document(i.id, i.text)
        
        t.save_frequency_matrix("tweet_clusters.txt")
        rownames, colnames, data = t.read_frequency_matrix("tweet_clusters.txt")

        clusters = kmeans(data, k=30)
        output_clusters_to_file(clusters, rownames, "kmeans_with_tweets")
        
if __name__ == "__main__":
    unittest.main()