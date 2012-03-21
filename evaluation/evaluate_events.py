'''
Created on 21 Mar 2012

@author: george
'''

from database.warehouse import WarehouseServer
from database.model.tweets import EvaluationTweet
from analysis.clustering.kmeans import OrangeKmeansClusterer

ws = WarehouseServer()
documents = ws.get_all_documents(type=EvaluationTweet)

oc = OrangeKmeansClusterer(k=20, ngram=1)
oc.add_documents(documents)
oc.run("orange_clustering_test", pca=True)
oc.plot_scatter()
oc.dump_clusters_to_file("kmeans_with_tweets_orange")