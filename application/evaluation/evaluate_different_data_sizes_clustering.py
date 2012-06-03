'''
Created on 21 Mar 2012

@author: george
'''
import pylab#!@UnresolvedImport 
import numpy 

from database.warehouse import WarehouseServer
from database.model.tweets import EvaluationTweet
from analysis.clustering.kmeans import OrangeKmeansClusterer
from analysis.clustering.dbscan import DBSCANClusterer
from analysis.clustering.nmf import NMFClusterer
from analysis.clustering.online import OnlineClusterer
from evaluation.evaluators import ExtrinsicClusteringEvaluator
from analysis.clustering.algorithms import euclidean, cosine, jaccard 

distances = [euclidean, cosine, jaccard]

def run_evaluation():
    ws = WarehouseServer()
    documents = [doc for doc in ws.get_all_documents(type=EvaluationTweet)]
    clusterers = [
                  OnlineClusterer(N=40, window = 50),
                  OrangeKmeansClusterer(k=40, ngram=1), 
                  DBSCANClusterer(epsilon=0.5, min_pts=3, distance=euclidean), 
                  NMFClusterer(rank=40, max_iter=65, display_N_tokens = 5, display_N_documents = 200)
                  ] 
    
    dataset_size = len(documents)
    
    f_different_distances = []
    step = 50
    initial_document_size = 50
    for distance in distances:
        print '------------------------------------------'
        f_different_clusterers = [] 
        for clusterer in clusterers:
            print 'Evaluating', clusterer, 'for', distance
            oc = clusterer
            clusterer.distance = distance
            f_list = []
            i=initial_document_size
            while (i < dataset_size): 
                print 'with data size:', i
                
                #Special case for onlie clustering
                if type(oc) == OnlineClusterer:
                    oc.window = i #no the window is the whole data set
                    for item in documents[:i]:
                        oc.cluster(item)
                    ebe = ExtrinsicClusteringEvaluator(documents[:i])
                    bcubed_precision, bcubed_recall, bcubed_f = ebe.evaluate(clusterer=oc)  
                    f_list.append(bcubed_f)
                    i += step
                    continue
                
                ebe = ExtrinsicClusteringEvaluator(documents[:i])
                bcubed_precision, bcubed_recall, bcubed_f = ebe.evaluate(clusterer=oc)
                f_list.append(bcubed_f)
                i += step
            f_different_clusterers.append(f_list)
        f_different_distances.append(f_different_clusterers)
        
    t = numpy.arange(initial_document_size, dataset_size, step)
    plots = []
    pylab.figure(1)
    
    dist_names = ["Euclidean", "Cosine", "Jaccard"]
    for i, f_different_distance in enumerate(f_different_distances):
        pylab.subplot(2,2,i+1)
        for f_measure in f_different_distance:
            plots.append(pylab.plot(t, f_measure))
        pylab.title(dist_names[i])
        pylab.xlabel('Number of documents')
        pylab.ylabel('Bcubed F metric')
        pylab.legend(('online', 'kmeans', 'dbscan', 'nmf'), 'lower right', shadow=True)
    
    pylab.show()
    
import cProfile    
cProfile.run('run_evaluation()', 'different_data_sizes.profile')
