'''
Created on 13 Nov 2011

@author: george

This module performs analysis on a given dataset of documents
'''
import nltk
                
class DatasetAnalyser(object):
    '''
    This class contains and implements all the methods responsible for 
    dataset analysis.
    '''
    def __init__(self, dataset):
        self.dataset = dataset
        
        
    def avg_document_length(self):
        '''
        Calculates the average length of the documents in the dataset. The length
        is measured based on the characters. This method reminds me of my school years
        when writing methods to calculate avergae was a stanard procedure! 
        '''
        sum = 0 
        for document in self.dataset:
            sum += len(document.content.raw)
        return float(sum)/float(len(self.dataset))
    
    def vocabulary_size(self):
        '''
        It calculates how many different words appear in this dataset
        '''
        corpus = nltk.TextCollection([document.content.tokens for document in self.dataset])
        return len(set(corpus))
        
    def avg_vocabulary_size(self):
        '''
        Calculates the average vocabulary size. In plain English
        it calculates how many different words appear in each document on average.
        '''
        return float(self.vocabulary_size())/float(len(self.dataset))    

    def dataset_size(self):
        return len(self.dataset)