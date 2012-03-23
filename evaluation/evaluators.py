'''
Created on 19 Mar 2012

@author: george
'''
import numpy
from database.model.tweets import EvaluationTweet
from database.model.tweets import Content
from itertools import groupby as g

class AbstractEvaluator(object):
    
    def __init__(self, dataset=None):
        '''
        Constructor
        '''
        self.dataset = dataset
    
    def evaluate(self):
        raise NotImplementedError("evaluate() was not implemented by child class")
        
    def annotate_dataset(self):
        '''
        If the test dataset has not been annotated yet, then by calling this 
        function one can start annotating events manually. This function should be
        implemented by the derived classes.
        '''
        raise NotImplementedError("annotate_dataset() was not implemented by child class")
    
    
    def create_confusion_matrix(self, targets, predictions, labels_range):
        '''
        It constructs a confusion matrix based on the known labels of the events and 
        the actual predictions
        '''
        assert len(targets)==len(predictions)
        confusion_matrix = numpy.zeros([labels_range, labels_range])

        for i in xrange(len(targets)):
            confusion_matrix[targets[i]][predictions[i]] += 1 

        return confusion_matrix
    
    def calculate_precision_recall(self, confusion_matrix):
        '''
        It takes as input a confusion matrix and calculates the precision and recall for
        each class.
        '''
        dim = confusion_matrix.shape[0]
        rp_rates = numpy.zeros([dim,2])
        for i in xrange(dim):
            if numpy.sum(confusion_matrix[i, :]) > 0:
                rp_rates[i, 0] = confusion_matrix[i, i] / numpy.sum(confusion_matrix[i, :])
            if sum(confusion_matrix[:, i]) > 0:
                rp_rates[i, 1] = confusion_matrix[i, i] / numpy.sum(confusion_matrix[:, i]) 
        
        return rp_rates
    
    def calculate_f_measure(self, rp_rates, alpha=1):
        '''
        It takes as input a matrix containing the precision and recall measures for a number of 
        classes and outputs the corresponding F measures.
        '''
        dim = rp_rates.shape[0]

        f_measures = numpy.zeros([dim,1])
        for i in xrange(dim):
            if rp_rates[i,0] != 0 or rp_rates[i,1] != 0:
                f_measures[i] = (1 + alpha) * (( rp_rates[i,0] * rp_rates[i,1]) / (alpha * rp_rates[i,1] + rp_rates[i,0]));
        return f_measures
    
class ClusteringEvaluator(AbstractEvaluator):
    '''
    This class is responsible for performing clustering
    evaluation.
    '''
        
    def annotate_dataset(self):
        '''
        If the test dataset has not been annotated yet, then by calling this 
        function one can start annotating events manually.
        '''

        print 'Hey lucky guy...you have to annotate',len(self.dataset),"tweets!"
        for i, tweet in enumerate(self.dataset):
            print '-------------------'+ 'Tweet ' + str(i) +'------------------------'
            print tweet.content.raw
            accept = raw_input("Accept? (Y or N)")
            if accept == "N": 
                continue
            elif accept == "Y":
                et = self.clone_document(tweet)
                avail_events = et.get_available_events()
                if len(avail_events) > 0:
                    print '========= Available events ========='
                    for event in avail_events:
                        print event.event_class, event.event_desc
                    print '===================================='
                    
                    #A loop to catch the stupid mistake of typing a string for an event class
                    is_not_int = True
                    while is_not_int:
                        event_class = raw_input("What is the class of this event?")
                        try:
                            int(event_class)
                            is_not_int = False
                        except ValueError:
                            is_not_int = True
                            
                    et.set_event_class(int(event_class))                        
                else:
                    print 'No events available yet.'
                    et.set_event_class(0)                        
    
    def clone_document(self, document):
        tt = EvaluationTweet()
        tt.url  = document.url
        content = Content()
        content.raw = document.content.raw
        content.tokens = document.content.tokens
        content.word_frequencies = document.content.word_frequencies
        content.date = document.date
        tt.content = content
        tt.date = document.date
        tt.retweet_count = document.retweet_count
        tt.author_screen_name = document.author_screen_name
        tt.author_name = document.author_name                        
        #tt.save(safe=True)
        return tt
    
    def evaluate(self, clusterer):
        '''
        Performs clustering evaluation
        '''
        clusterer.add_documents(self.dataset)
        clusterer.run("orange_clustering_test", pca=True)
            
        doc_labels_clusters = []
        for document in self.dataset:
            for cluster_no, cluster in enumerate(clusterer.clusters):
                if str(document.id) in cluster.get_documents().keys():
                    doc_labels_clusters.append( (document.event_class, cluster_no) )
                    break
        

        p, r, f =self.calculate_bcubed_measures(doc_labels_clusters)
        return p, r, f
    
    def calculate_bcubed_measures(self, documents_labels_clusters):
        '''
        This method calculates the BCubed precision, recall and F measures. 
        BCubed measures are extrinsic measures and require the presence of a ground
        truth.
        The function assumes that the clusters are in the range 0..Nc and the labels 0..Nl.
        For more details : http://www.cs.utsa.edu/~qitian/seminar/Spring11/03_11_11/IR2009.pdf
        '''
        grouped_by_label = [list(label[1]) for label in g(sorted(documents_labels_clusters), key=lambda(x):x[0])]
        grouped_by_cluster = {cluster[0] :list(cluster[1]) for cluster in g(sorted(documents_labels_clusters ,key=lambda(x):x[1]), key=lambda(x):x[1])}
        
        precision_average_sum = 0.0
        recall_average_sum = 0.0
        for i, doci in enumerate(documents_labels_clusters):
            same_label = grouped_by_label[doci[0]]
            same_cluster = grouped_by_cluster[doci[1]]
            correctness = 0.0
            for doc in same_cluster:
                if doci[0] == doc[0]: correctness += 1.0 
            precision_average_sum += correctness/ len(same_cluster)
            correctness = 0.0
            for doc in same_label:
                if doci[1] == doc[1]: correctness += 1.0 
            recall_average_sum += correctness/ len(same_label)
        precision_bcubed = precision_average_sum/len(documents_labels_clusters)
        recall_bcubed = recall_average_sum/len(documents_labels_clusters) 
        f_bcubed = (2*precision_bcubed*recall_bcubed)/(precision_bcubed+recall_bcubed)
        
        return precision_bcubed, recall_bcubed, f_bcubed
    
class ClassificationEvaluator(AbstractEvaluator):
    '''
    This class is responsible for performing classification
    evaluation.
    '''
    
    def __init__(self, dataset=None, classes_list=None):
        '''
        Constructor
        '''
        super( ClassificationEvaluator, self ).__init__(dataset)
        self.classes_list = classes_list
        
    def annotate_dataset(self):
        '''
        If the test dataset has not been annotated yet, then by calling this 
        function one can start annotating events manually.
        '''
        pass
    
    def evaluate(self, classifier, K=10):
        '''
        This method performs the actual task of evaluation. It takes as input
        k which determines the number of folds in k-fold cross validation and the type
        of the classifier. It return a numpy array which contains n rows and m columns where
        n is the number of different classes and m = 3 (precision ,recall and f measure).
        '''
        attributes = ["retweets", "links", "retweeted", "replies", "mentions", "ff-ratio", "class"]
        metrics = numpy.zeros([len(self.classes_list), 3])
        for training, validation in self.split_dataset(K=K, randomize=True):
            targets = [vector[1] for vector in validation]
            classifier.train([vector[0] for vector in training], attributes)
            fold_predictions = [int(classifier.classify(example[0]).value) for example in validation]
            confusion_matrix = self.create_confusion_matrix(targets, fold_predictions, len(self.classes_list))
            rp_rates = self.calculate_precision_recall(confusion_matrix)
            f_measures = self.calculate_f_measure(rp_rates)
            metrics += numpy.concatenate((rp_rates, f_measures), axis=1)
        
        return metrics/float(K)

            
    def split_dataset(self, K, randomize=False):
        '''
        Splits the dataset according to the number of folds.
        '''
        feature_vectors_type = [(datapoint.get_feature_vector_with_type(), datapoint.type) for datapoint in self.dataset]
        if randomize: from random import shuffle; X=list(feature_vectors_type); shuffle(X)
        for k in xrange(K):
            training = [x for i, x in enumerate(X) if i % K != k]
            validation = [x for i, x in enumerate(X) if i % K == k]
            yield training, validation
        
        
    