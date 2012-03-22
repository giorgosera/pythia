'''
Created on 21 Mar 2012

@author: george
'''

from database.warehouse import WarehouseServer
from database.model.tweets import EvaluationTweet
from analysis.clustering.kmeans import OrangeKmeansClusterer
from evaluation.events import EventDetectionEvaluator

ws = WarehouseServer()
documents = ws.get_all_documents(type=EvaluationTweet)

oc = OrangeKmeansClusterer(k=35, ngram=1)
oc.add_documents(documents)
oc.run("orange_clustering_test", pca=True)
#oc.plot_scatter()
#oc.dump_clusters_to_file("kmeans_with_tweets_orange")

#===============================================================================
# clusters = {}
# for cluster_no, cluster in enumerate(oc.clusters):
#    docs = cluster.get_documents()
#    classes = [] 
#    for doc_id, doc in docs.iteritems():
#        document = ws.get_document_by_id(doc_id, type=EvaluationTweet)
#        classes.append(document.event_class)
#    clusters[cluster_no] = classes
#===============================================================================
    
doc_labels_clusters = []
for document in documents:
    for cluster_no, cluster in enumerate(oc.clusters):
        if str(document.id) in cluster.get_documents().keys():
            doc_labels_clusters.append( (document.event_class, cluster_no) )
            break
        
ebe = EventDetectionEvaluator()
ebe.calculate_bcubed_measures(doc_labels_clusters)

    #===========================================================================
    # print classes
    # if len(classes) > 0:
    #    cluster_class = max(g(sorted(classes)), key=lambda(x, v):(len(list(v)),-classes.index(x)))[0]
    #===========================================================================