'''
Created on 11 Mar 2012

@author: george
'''
import Orange#!@UnresolvedImport
from tools.orange_utils import construct_orange_table

class kNNClassifier(object):
    '''
    This class implements methods to construct a kNN learner and 
    classify new examples.
    '''

    def __init__(self):
        '''
        Constructs the classifier object
        '''
        self.classifer = None
        self.train_table = None
        
    def train(self, train_set, attributes):
        '''
        Gets the training data (numpy array) and the attribute list and constructs the tree
        '''
        self.train_table = construct_orange_table(attributes, train_set, classed=True)
        self.classifer = Orange.classification.knn.kNNLearner(self.train_table, k=10)       
        
    def classify(self, example):
        '''
        Gets a new example (a feature vector i.e list) and classifies it.
        '''
        example = Orange.data.Instance(self.train_table.domain, example) 
        return self.classifer(example)
    
    def evaluate(self, N=10):
        '''
        Performs N-fold cross validation to evaluate the classifier's performance
        '''
        pass