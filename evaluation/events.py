'''
Created on 19 Mar 2012

@author: george
'''
import datetime, numpy
from database.model.tweets import EvaluationTweet
from database.warehouse import WarehouseServer
from mongoengine import connect
from database.model.tweets import Content
from itertools import groupby as g
connect("pythia_db")

ws = WarehouseServer()

class EventDetectionEvaluator(object):
    '''
    This class is responsible for performing event detection
    evaluation.
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self.tweets = None
        
    def annotate_dataset(self):
        '''
        If the test dataset has not been annotated yet, then by calling this 
        function one can start annotating events manually.
        '''
        from_date=datetime.datetime(2011, 01, 25, 12, 0, 0)
        to_date=datetime.datetime(2011, 01, 25, 12, 5, 0)
        tweet_list = ws.get_documents_by_date(from_date, to_date)
        print 'Hey lucky guy...you have to annotate',len(tweet_list),"tweets!"
        for i, tweet in enumerate(tweet_list):
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
            if sum(confusion_matrix[:][i]) > 0:
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
            if rp_rates[i,0] != 0 or rp_rates(i,1) != 0:
                f_measures[i] = (1 + alpha) * (( rp_rates[i,0] * rp_rates[i,1]) / (alpha * rp_rates[i,1] + rp_rates[i,0]));
        return f_measures
    
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
            precision_average_sum += (correctness-1)/ (len(same_cluster)-1) if len(same_cluster) > 1 else 0
            correctness = 0.0
            for doc in same_label:
                if doci[1] == doc[1]: correctness += 1.0 
            recall_average_sum += (correctness-1)/ (len(same_label)-1) if len(same_label) > 1 else 0
        precision_bcubed = precision_average_sum/len(documents_labels_clusters)
        recall_bcubed = recall_average_sum/len(documents_labels_clusters) 

        print 'precision', precision_bcubed
        print 'recall', recall_bcubed            




#===============================================================================
#        average_sum = 0.0
# 
#        for doci in documents_labels_clusters:
#            correctness = 0.0
#            docs_in_cluster = len(clusters[doci[1]]) 
#            if docs_in_cluster != 1:
#                for label in clusters[doci[1]]: 
#                    if doci[0] == label: correctness += 1 #If the two docs have the same label
#                average_sum += (correctness-1)/(docs_in_cluster-1)
#        precision_bcubed = average_sum/len(documents_labels_clusters)
# 
# 
#        average_sum = 0.0
#        for doci in documents_labels_clusters:
#            correctness = 0.0
#            same_label_count = 0.0
#            for docj in documents_labels_clusters:
#                if doci[0] == docj[0]:
#                    same_label_count += 1
#                    if doci[1]==docj[1]: correctness+=1
#            average_sum += (correctness-1)/(same_label_count)
#        recall_bcubed = average_sum/len(documents_labels_clusters)
#===============================================================================

        
#===============================================================================
# if __name__ == "__main__":
#    ede = EventDetectionEvaluator()
#    ede.annotate_dataset()
#===============================================================================