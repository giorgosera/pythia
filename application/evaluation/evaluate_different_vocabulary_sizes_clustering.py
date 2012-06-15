'''
Created on 21 Mar 2012

@author: george
'''
import random
import pylab#!@UnresolvedImport 
import numpy, time
from matplotlib.font_manager import FontProperties#!@UnresolvedImport 
fontP = FontProperties()
fontP.set_size(45)
from database.model.tweets import *
from database.warehouse import WarehouseServer
from analysis.clustering.kmeans import OrangeKmeansClusterer
from analysis.clustering.dbscan import DBSCANClusterer
from analysis.clustering.nmf import NMFClusterer
from analysis.clustering.online import OnlineClusterer
from evaluation.evaluators import ExtrinsicClusteringEvaluator
from analysis.clustering.algorithms import euclidean, cosine, jaccard 
from analysis.dataset_analysis import DatasetAnalyser
from analysis.text import TextAnalyser
random.seed(time.clock())
####################HELPER METHODS###########################
    
def get_words_starting_with(letter):
    '''
    It returns all the words in the dictionary starting with "letter".
    '''
    words = []
    for word in open("/usr/share/dict/words"):
                    if word.startswith(letter):
                            words.append(unicode(word.rstrip()))
    return words

def pick_letters(N, with_replacement=False):
    '''
    Randomly selects a letter from the alphabet. N is the number of letters to be
    retrieved. If with_replacement is true then a letter can be selected more than once. 
    '''
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p' ,'q' ,'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    used = []
    i = 0
    while i<N:
        if not with_replacement:
            letter = random.choice([x for x in alphabet if x not in used])
        else:
            letter = random.choice([x for x in alphabet])
        used.append(letter)
        i += 1 
    return used

def increase_vocabulary(document, dictionary, i=5):
    '''
    Takes as input a document and concatenates on it a random word from
    the dictionary.
    '''
    extending_words = []
    for k in range(i):
        randint = random.randint(0, len(dictionary)-1)
        random_word = dictionary[randint]
        extending_words.append(random_word)
        
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
distances = [
             euclidean,
             cosine,
             jaccard
             ]

ws = WarehouseServer()
def run_evaluation():
    clusterers = [
                  OnlineClusterer(N=40, window = 50),
                  OrangeKmeansClusterer(k=40, ngram=1),
                  DBSCANClusterer(epsilon=0.5, min_pts=2, distance=euclidean),
                  NMFClusterer(rank=40, max_iter=65, display_N_tokens = 5, display_N_documents = 20)                  
                  ] 
    
    diversity = [1, 2, 5, 10, 26]#How many different letters to pick from the alphabet each time
    dictionaries = []
    
    #Create different diversities
    for d in diversity:
        letters = pick_letters(d)
        words = []
        for letter in letters:
            words.append(get_words_starting_with(letter))
        l = [word for sublist in words for word in sublist]
        random.shuffle(l)
        dictionaries.append(l)
    
    #Create different document datasets based on the diversities
    datasets = []
    datasets.append([doc for doc in ws.get_all_documents(type=EvaluationTweet)])#Append the original dataset
    for ind, dictionary in enumerate(dictionaries):        
        documents = [doc for doc in ws.get_all_documents(type=EvaluationTweet)]
        size = len(dictionary)

        augmented_dataset = []
        for document in documents:
            augmented_document = increase_vocabulary(document, dictionary[:int(size*0.01)])
            augmented_dataset.append(augmented_document)

        da = DatasetAnalyser(augmented_dataset)
        datasets.append(augmented_dataset)
    
    qualities_different_distances = []
    for distance in distances:
        print '------------------------------------------'
        q_different_clusterers = [] 
        for clusterer in clusterers:
            print 'Evaluating', clusterer, 'for', distance
            oc = clusterer
            oc.distance = distance
            q = []
            for ind, dataset in enumerate(datasets):
                print 'dataset ', ind
                da = DatasetAnalyser(dataset)
                print 'with vocabulary size: ', da.avg_vocabulary_size()
                print 'with average document length: ', da.avg_document_length()
                print da.vocabulary_size()
                
                #Special case for online clustering
                if type(oc) == OnlineClusterer:
                    oc.window = len(dataset) #no the window is the whole data set
                    for item in dataset:
                        oc.cluster(item)
                    ebe = ExtrinsicClusteringEvaluator(dataset)
                    bcubed_precision, bcubed_recall, bcubed_f = ebe.evaluate(clusterer=oc)
                    q.append(bcubed_f)  
                    continue
                
                ebe = ExtrinsicClusteringEvaluator(dataset)
                bcubed_precision, bcubed_recall, bcubed_f = ebe.evaluate(clusterer=oc)
                q.append(bcubed_f)
            q_different_clusterers.append(q)
        qualities_different_distances.append(q_different_clusterers)
    
    vocabulary_sizes = []
    for dataset in datasets:       
        da = DatasetAnalyser(dataset) 
        vocabulary_sizes.append(da.avg_vocabulary_size())
    
    t = numpy.linspace(vocabulary_sizes[0], vocabulary_sizes[-1], num=len(datasets))
    plots = []
    pylab.figure(1)
    
    dist_names = ["Euclidean", "Cosine", "Jaccard"]    
    for i, distance in enumerate(qualities_different_distances):
        pylab.subplot(2,2,i+1)
        for q_clusterer in distance:
            plots.append(pylab.plot(t, q_clusterer, marker='o'))
        pylab.title(dist_names[i])
        pylab.xlabel('Average vocabulary size')
        pylab.ylabel('BCubed F metric')
    pylab.legend(('online', 'kmeans', 'dbscan', 'nmf'), bbox_to_anchor=(2,0) , loc='lower right', shadow=True, prop=fontP)
    
    pylab.show()

import cProfile    
cProfile.run('run_evaluation()', 'different_vocabulary.profile')
        