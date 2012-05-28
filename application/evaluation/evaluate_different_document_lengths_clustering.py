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
from evaluation.evaluators import ExtrinsicClusteringEvaluator
from analysis.clustering.algorithms import euclidean 
from analysis.dataset_analysis import DatasetAnalyser

#####################################HELPER METHODS############################################
def increase_length(i, document):
    '''
    Takes as input a document and concatenates on it as many as i random documents.
    '''
    extending_documents = []
    for k in range(i):
        randint = random.randint(0, len(original_docs)-1)
        random_doc = original_docs[randint]
        extending_documents.append(random_doc)
        
    for random_doc in extending_documents:

        document.content.raw += ' ' + random_doc.content.raw
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

    return document

#####################################MAIN SCRIPT############################################

ws = WarehouseServer()
clusterers = [OrangeKmeansClusterer(k=39, ngram=1), 
              DBSCANClusterer(epsilon=0.02, min_pts=2, distance=euclidean), 
              NMFClusterer(rank=39, max_iter=65, display_N_tokens = 5, display_N_documents = 10)] 

original_docs = [doc for doc in ws.get_all_documents(type=EvaluationTweet)]

def run_evaluation():
    #Inside the loop we alter the original documents in order to increase their length. However, we should keep
    #the vocabulary size the same. Therefore, we increase the length by concatenating the original
    #documents with random ones from the same dataset. 
    
    iterations=8
    f_measures = []
    for clusterer in clusterers:
        oc = clusterer
        f_list = []
        for i in range(iterations):
            documents = [doc for doc in ws.get_all_documents(type=EvaluationTweet)]
            longer_dataset = []
    
            for document in documents:
                longer_dataset.append(increase_length(i, document))
                
            da = DatasetAnalyser(longer_dataset)
            print da.avg_document_length()
            
            ebe = ExtrinsicClusteringEvaluator(longer_dataset)
            bcubed_precision, bcubed_recall, bcubed_f = ebe.evaluate(clusterer=oc)
            f_list.append(bcubed_f)
        f_measures.append(f_list)
    
    da = DatasetAnalyser(original_docs)
    original_length = da.avg_document_length()
    t = numpy.arange(original_length, 10+original_length*iterations, original_length)
    plots = []
    
    for measures_list in f_measures:
        plots.append(pylab.plot(t, measures_list))
    
    pylab.xlabel('Document average length')
    pylab.ylabel('Bcubed F metric')
    pylab.legend(('kmeans', 'dbscan', 'nmf'), 'lower right', shadow=True)
    pylab.show()

    
import cProfile    
cProfile.run('run_evaluation()', 'different_document_lengths.profile')