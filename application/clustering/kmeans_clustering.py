# -*- coding: utf-8 -*-
'''
Created on 13 Nov 2011

@author: george

'''
import datetime, cProfile
from database.warehouse import WarehouseServer
from database.model.tweets import EvaluationTweet
from analysis.clustering.kmeans import OrangeKmeansClusterer
from tests.test_document import get_orange_clustering_test_data
from analysis.clustering.algorithms import jaccard, euclidean
###########################################
# GLOBALS                                #
###########################################
ws = WarehouseServer()
sample_docs = get_orange_clustering_test_data()

def orange_with_tweets_kmeans():
        import time
        start = time.time()            
        from_date = datetime.datetime(2011, 1, 26, 0, 0, 0)
        to_date = datetime.datetime(2011, 1, 27, 0, 0, 0) 
        items = ws.get_documents_by_date(from_date, to_date, limit=10)
        oc = OrangeKmeansClusterer(distance=jaccard, k=4, ngram=1)
        oc.add_documents(items)
        oc.run(pca=False)
        print time.time() - start
        oc.plot_scatter()
        oc.dump_clusters_to_file("kmeans_with_tweets_orange")
            
if __name__ == "__main__":
    cProfile.run('orange_with_tweets_kmeans()', 'kmeans.profile')