'''
Created on 21 Mar 2012

@author: george
'''
import pylab#!@UnresolvedImport 
import numpy 
import random

from database.warehouse import WarehouseServer
from database.model.tweets import EvaluationTweet
from analysis.clustering.kmeans import OrangeKmeansClusterer
from analysis.clustering.dbscan import DBSCANClusterer
from analysis.clustering.nmf import NMFClusterer
from evaluation.evaluators import ClusteringEvaluator
from analysis.clustering.algorithms import euclidean 
from analysis.dataset_analysis import DatasetAnalyser

#####################################HELPER METHODS############################################
def increase_length(i, document):
    '''
    Takes as input a document and concatenates on it as many as i random documents.
    '''
    for k in range(i):
        randint = random.randint(0, len(documents)-1)
        random_doc = documents[randint]
        document.content.raw 
        
        document.content.tokens.append(",".join(random_doc.content.tokens))
        
        for tuple in random_doc.content.word_frequencies:
            j = 0
            for t in document.content.word_frequencies:
                if t.word == tuple.word:
                    document.content.word_frequencies[j].count += tuple.count                        
                    break
                j += 1            
            if j == len(document.content.word_frequencies):
                document.content.word_frequencies.append(tuple)
                
    print '3'
    return document

#####################################MAIN SCRIPT############################################
ws = WarehouseServer()
documents = [doc for doc in ws.get_all_documents(type=EvaluationTweet)]

clusterers = [OrangeKmeansClusterer(k=39, ngram=1), 
              DBSCANClusterer(epsilon=0.02, min_pts=3, distance=euclidean), 
              NMFClusterer(rank=39, max_iter=65, display_N_tokens = 5, display_N_documents = 10)] 

#Inside the loop we alter the original documents in order to increase their length. However, we should keep
#the vocabulary size the same. Therefore, we increase the length by concatenating the original
#documents with random ones from the same dataset. 
for clusterer in clusterers:
    oc = clusterer
    for i in range(4):
        longer_dataset = []
        for document in documents:
            print '1'
            longer_dataset.append(increase_length(i, document))
        ebe = ClusteringEvaluator(longer_dataset)
        bcubed_precision, bcubed_recall, bcubed_f = ebe.evaluate(clusterer=oc)
        print bcubed_precision, bcubed_recall, bcubed_f
        
    
