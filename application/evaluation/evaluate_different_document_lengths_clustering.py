'''
Created on 21 Mar 2012

@author: george
'''
import pylab#!@UnresolvedImport 
import numpy 
import random
from matplotlib.font_manager import FontProperties#!@UnresolvedImport 
fontP = FontProperties()
fontP.set_size(45)
from database.warehouse import WarehouseServer
from database.model.tweets import EvaluationTweet
from analysis.clustering.kmeans import OrangeKmeansClusterer
from analysis.clustering.dbscan import DBSCANClusterer
from analysis.clustering.nmf import NMFClusterer
from analysis.clustering.online import OnlineClusterer
from evaluation.evaluators import ExtrinsicClusteringEvaluator
from analysis.clustering.algorithms import euclidean, cosine, jaccard 
from analysis.dataset_analysis import DatasetAnalyser
from database.model.tweets import WordFrequencyTuple

#####################################HELPER METHODS############################################

def create_dictionary(documents):
    '''
    Creates a dictionary from the words in the original
    dataset. These words will be appended randomly in documents 
    to increase their size but keep the vocabulary size the same.
    '''
    dictionary = set()
    for document in documents:
        dictionary = dictionary | set(document.content.tokens)
    return list(dictionary)

def increase_length(i, document):
    '''
    Takes as input a document and concatenates on it as many as i random words from
    the dictionary.
    '''
    extending_words = []
    for k in range(i):
        randint = random.randint(0, len(dictionary)-1)
        random_words = dictionary[randint]
        extending_words.append(random_words)
        
    for random_word in extending_words:
        document.content.raw += ' ' + random_word
        document.content.tokens.append(random_word)
        
        j = 0
        for t in document.content.word_frequencies:
            if t.word == random_word:
                document.content.word_frequencies[j].count += 1                        
                break
            j += 1            
        if j == len(document.content.word_frequencies):
            t = WordFrequencyTuple()
            t.word = random_word
            t.count = 1
            document.content.word_frequencies.append(t)
                
    return document

#####################################MAIN SCRIPT############################################

distances = [euclidean, cosine, jaccard]
ws = WarehouseServer()
clusterers = [
              OnlineClusterer(N=40, window = 50),
              OrangeKmeansClusterer(k=40, ngram=1), 
              DBSCANClusterer(epsilon=0.5, min_pts=2, distance=euclidean), 
              NMFClusterer(rank=40, max_iter=65, display_N_tokens = 5, display_N_documents = 200)] 

original_docs = [doc for doc in ws.get_all_documents(type=EvaluationTweet)][:250]
dictionary = create_dictionary(original_docs)

def run_evaluation():
    #Inside the loop we alter the original documents in order to increase their length. However, we should keep
    #the vocabulary size the same. Therefore, we increase the length by concatenating the original
    #documents with random ones from the same dataset. 

    iterations= 8
    f_different_distances = []
    for distance in distances:
        print '------------------------------------------'
        f_different_clusterers = [] 
        for clusterer in clusterers:
            print 'Evaluating', clusterer, 'for', distance
            oc = clusterer
            clusterer.distance = distance
            f_list = []
            for i in range(iterations):
                documents = [doc for doc in ws.get_all_documents(type=EvaluationTweet)]
                longer_dataset = []
        
                for document in documents:
                    longer_dataset.append(increase_length(i, document))
                    
                da = DatasetAnalyser(longer_dataset)
                print 'with average document length: ', da.avg_document_length()
                print 'with vocabulary size: ', da.avg_vocabulary_size()
                
                #Special case for onlie clustering
                if type(oc) == OnlineClusterer:
                    oc.window = len(longer_dataset) #no the window is the whole data set
                    for item in longer_dataset:
                        oc.cluster(item)
                    ebe = ExtrinsicClusteringEvaluator(longer_dataset)
                    bcubed_precision, bcubed_recall, bcubed_f = ebe.evaluate(clusterer=oc)  
                    f_list.append(bcubed_f)
                    continue
                
                ebe = ExtrinsicClusteringEvaluator(longer_dataset)
                bcubed_precision, bcubed_recall, bcubed_f = ebe.evaluate(clusterer=oc)
                f_list.append(bcubed_f)
            f_different_clusterers.append(f_list)
        f_different_distances.append(f_different_clusterers)
    
    da = DatasetAnalyser(original_docs)
    original_length = da.avg_document_length()
    t = numpy.arange(original_length, 10+original_length*iterations, original_length)
    plots = []
    pylab.figure(1)
    
    dist_names = ["Euclidean", "Cosine", "Jaccard"]
    for i, f_different_distance in enumerate(f_different_distances):
        pylab.subplot(2,2,i+1)
        for f_measure in f_different_distance:
            plots.append(pylab.plot(t, f_measure))
        pylab.title(dist_names[i])
        pylab.xlabel('Average document length')
        pylab.ylabel('Bcubed F metric')
    pylab.legend(('online', 'kmeans', 'dbscan', 'nmf'), bbox_to_anchor=(2,0) , loc='lower right', shadow=True, prop=fontP)
    
    pylab.show()

    
import cProfile    
cProfile.run('run_evaluation()', 'different_document_lengths.profile')