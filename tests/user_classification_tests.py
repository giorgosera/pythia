'''
Created on 26 Jan 2012

@author: george
'''
import unittest, numpy
from mongoengine import connect
from tools.orange_utils import construct_orange_table
from database.model.agents import *
connect("pythia_db")
import orngTree, Orange#!@UnresolvedImport

class Test(unittest.TestCase):

    def test_author_classification_dummy_dataset(self):
        train_set = numpy.array([[0.2, 0.5, 0.2,  0.2, 0.1,  10.,  0],
                                [0.2, 0.3, 0.12, 0.1, 0.1,  10.,  0],
                                [0.2, 0.2, 0.08, 0.2, 0.01, 20.,  0],
                                [0.2, 0.5, 0.1,  0.1, 0.2,  5.,   0],
                                [0.2, 0.1, 0.2,  0.2, 0.3,  20.,  0],
                                [0.7, 0.5, 0.2,  0.8, 0.3,  0.1, 1],
                                [0.6, 0.8, 5.2,  0.2, 0.6,  0.3, 1],
                                [0.2, 0.6, 8.2,  0.9, 0.9,  0.1, 1],
                                [0.5, 0.9, 1.2,  0.1, 0.1,  0.2, 1],
                                [0.9, 0.1, 0.9,  0.6, 0.3,  0.6, 1]])
        
        attributes = ["retweets", "links", "retweeted", "replies", "mentions", "ff-ratio", "class"]
        
        table = construct_orange_table(attributes, train_set, classed=True)
        treeLearner = orngTree.TreeLearner()        
        treeClassifier = treeLearner(table)    
        example = Orange.data.Instance(table.domain, [0.2, 0.5, 0.2,  0.2, 0.1,  100,  0])    
        prediction = treeClassifier(example)
        self.assertEquals(0, prediction.value)
        
if __name__ == "__main__":
    unittest.main()