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
ebe = ClusteringEvaluator(documents)
bcubed_precision, bcubed_recall, bcubed_f = ebe.evaluate(clusterer=oc)
print bcubed_precision, bcubed_recall, bcubed_f