# -*- coding: utf-8 -*-
'''
Created on 13 Nov 2011

@author: george

Unit tests for the analysis.clustering package.
'''
import datetime, unittest, Orange, orange, orngClustering #!@UnresolvedImport
from database.warehouse import WarehouseServer
from analysis.clustering.datastructures.clusters import OrangeKmeansClusterer, CustomClusterer
from analysis.clustering.algorithms.algorithms import hierarchical, kmeans, cosine
from visualizations.dendrogram import Dendrogram
from visualizations.Cluster2DPlot import Cluster2DPlot

import nimfa, numpy#!@UnresolvedImport
from scipy.sparse import csr_matrix#!@UnresolvedImport
from scipy import array#!@UnresolvedImport
from numpy import dot

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

oc = OrangeKmeansClusterer(k=2)
id = 0
for s in sample_docs:
    oc.add_document(id, s)
    id += 1 
   
cc = CustomClusterer()
id = 0
for s in sample_docs:
    cc.add_document(id, s)
    id += 1
    
cc.construct_term_doc_matrix()
cc.save_table("custom_clustering_test.txt")
    
class TestOrangeClustering(unittest.TestCase):
    
    ###########################################
    # ORANGE TESTS                            #
    ###########################################       
    def test_orange_sample_doc_kmeans(self):
        km = oc.run("orange_clustering_test")

        expected = [0, 0, 0, 1, 1, 1]
        self.assertEqual(expected, km.clusters)

    def test_orange_with_tweets_kmeans(self):    
        from_date = datetime.datetime(2011, 1, 23, 0, 0, 0)
        to_date = datetime.datetime(2011, 1, 25, 0, 0, 0) 
        items = ws.get_documents_by_date(from_date, to_date, 30)
 
        oc = OrangeKmeansClusterer(k=10)
        for item in items:
            oc.add_document(item.id, item.text)
            
        oc.run("orange_clustering_test")
        oc.dump_clusters_to_file("kmeans_with_tweets_orange")
        
        #Experiments
        max = (0, 0)
        for i, cluster in enumerate(oc.clusters):
            if cluster.get_size() > max[1]:
                max = (i, cluster.get_size())

        oc_new = OrangeKmeansClusterer(k=5)
        for doc_id in oc.clusters[max[0]].get_documents().keys():
            oc_new.add_document(doc_id, ws.get_document_by_id(doc_id).text)         
        
        oc_new.run("orange_clustering_test")
        oc_new.dump_clusters_to_file("re-kmeans_with_tweets_orange")
        #End of experiments
                
        def showfeatures(w,h,titles,wordvec,out='features.txt'): 
            outfile=file(out,'w')  
            pc,wc=numpy.shape(h)
            toppatterns=[[] for i in range(len(titles))]
            patternnames=[]
            
            # Loop over all the features
            for i in range(pc):
              slist=[]
              # Create a list of words and their weights
              for j in range(wc):
                slist.append((h[i,j],wordvec[j]))
              # Reverse sort the word list
              slist.sort()
              slist.reverse()
              
              # Print the first six elements
              n=[s[1] for s in slist[0:6]]
              outfile.write(str(n)+'\n')
              patternnames.append(n)
              
              # Create a list of articles for this feature
              flist=[]
              for j in range(len(titles)):
                # Add the article with its weight
                flist.append((w[j,i],titles[j]))
                toppatterns[j].append((w[j,i],i,titles[j]))
              
              # Reverse sort the list
              flist.sort()
              flist.reverse()
              
              # Show the top 3 articles
              for f in flist[0:3]:
                outfile.write(str(f)+'\n')
              outfile.write('\n')
            
            outfile.close()
            # Return the pattern names for later use
            return toppatterns,patternnames
        
        V = oc.td_matrix

        model = nimfa.mf(V, seed = 'random_vcol', method = 'nmf', rank = 10, max_iter = 65)
        fitted = nimfa.mf_run(model)
        w = fitted.basis() 
        h = fitted.coef()
        print numpy.shape(w)
        print numpy.shape(h)

        showfeatures(w,h, [doc["raw"] for doc in oc.document_dict.values()], oc.attributes)
        
    #===========================================================================
    # def test_orange_with_tweets_hierarchical(self):
    #    data = oc.load_table()
    #    sample = data.selectref(orange.MakeRandomIndices2(data), 0)
    #    root = orngClustering.hierarchicalClustering(sample)
    #    orngClustering.dendrogram_draw("hclust-dendrogram.png", root, data=sample, labels=[str(d["id"]) for d in sample]) 
    #===========================================================================
        
    ##########################################
    # CUSTOM TESTS                            #
    ##########################################       
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
        items = ws.get_documents_by_date(from_date, to_date, 5)
        
        cc = CustomClusterer()
        for i in items:
            cc.add_document(i.id, i.text)
        
        cc.construct_term_doc_matrix()
        cc.save_table("custom_cluster_with_tweets.txt")
        rownames, colnames, data = cc.load_table()
        cluster = hierarchical(data)
        
        rownames = [cc.get_document_by_id(id)["raw"][:140] for id in rownames]
        
        dendro = Dendrogram(cluster, rownames, "hierarchical_custom_cluster_with_tweets.jpg", cluster.get_height(), cluster.get_depth())
        dendro.draw_node(10, cluster.get_height()/2)
       
    def test_tweet_kmeans_clustering(self):        
        from_date = datetime.datetime(2011, 1, 24, 0, 0, 0)
        to_date = datetime.datetime(2011, 1, 25, 0, 0, 0) 
        items = ws.get_documents_by_date(from_date, to_date, 5)
        
        cc = CustomClusterer()
        for i in items:
            cc.add_document(i.id, i.text)
        
        cc.construct_term_doc_matrix()
        cc.save_table("custom_cluster_with_tweets.txt")
        rownames, colnames, data = cc.load_table()
        k=5
        km = kmeans(data, similarity=cosine, k=5)
        cc.split_documents(km, k)
        cc.dump_clusters_to_file("kmeans_with_tweets_custom")
        
            
if __name__ == "__main__":
    unittest.main()