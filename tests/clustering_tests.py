# -*- coding: utf-8 -*-
'''
Created on 13 Nov 2011

@author: george

Unit tests for the analysis.clustering package.
'''
import datetime, unittest, Orange #!@UnresolvedImport
from analysis.text import TextAnalyser
from analysis.clustering.algorithms.algorithms import hierarchical, kmeans, cosine, tanimoto
from visualizations.dendrogram import Dendrogram
from visualizations.Cluster2DPlot import Cluster2DPlot
from visualizations.outputfile import output_clusters_to_file, output_clusters_to_file_translated  
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
    
tweet0 = "RT @ahramonline: #Egypt Breaking news: Explosion hits Egypt church, seven dead, fourteen wounded http://ht.ly/1aGhbH"
tweet1 = "RT @monaeltahawy: #Egypt -my heart aches for you. Regime &amp; radicals both hve long stoked fires of bigotry vs our Christian sisters and brothers. Shame, shame."
tweet2 = "RT @ThomReilly: #Egypt: #Reuters + #Al_Jazeera confirm #Alexandria church bomb attack: http://bit.ly/dIRoGl"
tweet3 = "RT @orthotox: حتى القنوات المصرية الخاصة تتعامل مع الحدث وكأنها لم تسمع عنه أصلاً  #Egypt #Media #Fail"
tweet4 = "RT @monaeltahawy: I condemn attacks vs Christian sisters&amp;brothers in #Egypt, #Nigeria, #Iraq. And I say big fuck you to fellow Muslims behind cowardly attacks"
tweet5 = "RT @halmustafa: مراسل الجزيرة: 10 قتلى ونحو 30 إصابة وقوات الامن تحاصر المنطقة ويتم الان حصر الاحتجاجات داخل الكنيسة #Egypt"
tweet6 = "RT @radicalahmad: يا أهلنا في الإسكندرية كونوا إخوانا ولا تجعلوا من ارتكب هذا الجرم القبيح يحقق هدفه في إشعال فتنة بينكم #Alexandria #Egypt"
tweets = [tweet0, tweet1,tweet2,tweet3,tweet4,tweet5,tweet6]

###########################################
# TESTS                                   #
###########################################
class TestHierarchicalClustering(unittest.TestCase):
    
 #==============================================================================
 #   def test_sample_doc_hierarchical(self):        
 #       analyser.save_frequency_matrix("test.txt")
 #       rownames, colnames, data = analyser.read_frequency_matrix("test.txt")
 #       
 #       cluster = hierarchical(data, similarity=cosine)
 #       cluster.print_it(rownames)
 #       
 #       dendro = Dendrogram(cluster, rownames, "cluster.jpg", cluster.get_height(), cluster.get_depth())
 #       dendro.draw_node(10, cluster.get_height()/2)
 #       
 #   def test_sample_doc_kmeans(self):
 #       analyser.save_frequency_matrix("test.txt")
 #       rownames, colnames, data = analyser.read_frequency_matrix("test.txt")
 #       
 #       clusters = kmeans(data=data, similarity=cosine, k=2)
 #       c2dp = Cluster2DPlot(data=data, labels=rownames, filename="2dclusters.jpg")
 #       c2dp.draw()
 #       
 # 
 #   def test_tweet_hierarchical_clustering(self):        
 # 
 #       from_date = datetime.datetime(2011, 1, 25, 0, 0, 0)
 #       to_date = datetime.datetime(2011, 1, 25, 3, 0, 0) 
 #       items = ws.get_documents_by_date(from_date, to_date, 50)
 #       
 #       t = TextAnalyser()
 #       for i in items:
 #           t.add_document(i.id, i.text)
 #           
 #       t.save_frequency_matrix("tweet_clusters.txt")
 #       rownames, colnames, data = t.read_frequency_matrix("tweet_clusters.txt")
 # 
 #       cluster = hierarchical(data)
 #       
 #       dendro = Dendrogram(cluster, rownames, "tweet_cluster.jpg", cluster.get_height(), cluster.get_depth())
 #       dendro.draw_node(10, cluster.get_height()/2)
 #       
 #   def test_tweet_kmeans_clustering(self):        
 # 
 #       from_date = datetime.datetime(2011, 1, 25, 0, 0, 0)
 #       to_date = datetime.datetime(2011, 1, 25, 3, 0, 0) 
 #       items = ws.get_documents_by_date(from_date, to_date, 50)
 #       
 #       t = TextAnalyser()
 #       for i in items:
 #           t.add_document(i.id, i.text)
 #       
 #       t.save_frequency_matrix("tweet_clusters.txt")
 #       rownames, colnames, data = t.read_frequency_matrix("tweet_clusters.txt")
 # 
 #       clusters = kmeans(data, k=5)
 #       output_clusters_to_file(clusters, rownames, "kmeans_with_tweets")
 #       
 #   def test_orange_sample_doc_kmeans(self):
 #       analyser.save_frequency_matrix_as_tab("test_orange_with_samples")
 #       table = Orange.data.Table("test_orange_with_samples")
 #       k = 3
 #       km = Orange.clustering.kmeans.Clustering(table, k)
 # 
 #       expected = [0, 1, 1, 2, 2, 2]
 #       self.assertEqual(expected, km.clusters)
 #==============================================================================

    def test_orange_with_tweets_kmeans(self):    
        from_date = datetime.datetime(2011, 1, 25, 12, 0, 0)
        to_date = datetime.datetime(2011, 1, 26, 0, 0, 0) 
        items = ws.get_documents_by_date(from_date, to_date, 100)

        t = TextAnalyser()
        for item in items:
            t.add_document(item.id, item.text)
            
        t.save_frequency_matrix_as_tab("test_with_tweets_orange")
        table = Orange.data.Table("test_with_tweets_orange")
        k = 5
        km = Orange.clustering.kmeans.Clustering(table, k, distance=Orange.distance.instances.PearsonRConstructor,initialization=Orange.clustering.kmeans.init_diversity)
        
        rownames = []
        
        for inst in table:
            rownames.append(str(inst['id'].value))
        
        clusters = [[] for k in range(k)]

        for item_index, cluster in enumerate(km.clusters):
            clusters[cluster].append(item_index)
            
        output_clusters_to_file_translated(clusters, rownames, t, "kmeans_with_tweets_orange")
            
if __name__ == "__main__":
    unittest.main()