'''
Created on 21 Mar 2012

@author: george
'''

from database.warehouse import WarehouseServer
from database.model.tweets import EvaluationTweet
from analysis.clustering.kmeans import OrangeKmeansClusterer
from evaluation.evaluators import ClusteringEvaluator

ws = WarehouseServer()
documents = ws.get_all_documents(type=EvaluationTweet)

oc = OrangeKmeansClusterer(k=35, ngram=1)
oc.add_documents(documents)
oc.run("orange_clustering_test", pca=True)
#oc.plot_scatter()
#oc.dump_clusters_to_file("kmeans_with_tweets_orange")
    
doc_labels_clusters = []
for document in documents:
    for cluster_no, cluster in enumerate(oc.clusters):
        if str(document.id) in cluster.get_documents().keys():
            doc_labels_clusters.append( (document.event_class, cluster_no) )
            break
        
ebe = ClusteringEvaluator()
p, r, f =ebe.calculate_bcubed_measures(doc_labels_clusters)
print p, r, f