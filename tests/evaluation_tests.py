# -*- coding: utf-8 -*-
'''
Created on 13 Nov 2011

@author: george

Unit tests for the evaluation package.
'''
import unittest, numpy
from evaluation.evaluators import ClusteringEvaluator, ClassificationEvaluator

class TestClusteringEvaluationClass(unittest.TestCase):
    
    def test_confusion_matrix_creation(self):
        ede = ClusteringEvaluator()
        targets = [1, 1, 1, 1, 1 , 1, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2]
        predictions = [1, 1, 1, 1, 1 , 1, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2]
        confusion_matrix = ede.create_confusion_matrix(targets, predictions, 3)
        expected = numpy.array([[ 6., 0., 0.],[ 0., 6., 0.],[ 0., 0., 6.]])

        self.assertTrue(numpy.in1d((numpy.sum(confusion_matrix-expected, axis=1)), [0., 0., 0.]).all())
        
    def test_precision_recall_and_f_calculation(self):
        ede = ClusteringEvaluator()
        targets = [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1 , 1, 2, 2, 2, 2, 2, 2]
        predictions = [0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1 , 2, 2, 2, 2, 2, 0, 2]
        confusion_matrix = ede.create_confusion_matrix(targets, predictions, 3)
        rp_rates = ede.calculate_precision_recall(confusion_matrix)
        fs = ede.calculate_f_measure(rp_rates)
        self.assertEquals(sum(fs), [2.5])
    
    def test_bcubed_calculation(self):
        ede = ClusteringEvaluator()
        documents_labels_clusters = [(0, 0), (0, 1), (0, 0), (0, 0), (0, 1), (0, 0), 
                                     (1, 1), (1, 1), (1, 2), (1, 1), (1, 1), (1, 1),
                                     (2, 1), (2, 0), (2, 2), (2, 0), (2, 2), (2, 2)]
                
        precision ,recall, f = ede.calculate_bcubed_measures(documents_labels_clusters)
        self.assertAlmostEqual(0.532407407407 - precision, 0, places=7)
        self.assertAlmostEqual(0.555555555556 - recall, 0, places=7)
        self.assertAlmostEqual(0.543735224586 - f, 0, places=7)

class TestClassificationEvaluationClass(unittest.TestCase):

    def test_dataset_split(self):
        X = [i for i in xrange(97)]
        ce = ClassificationEvaluator(X) 
        ce.evaluate(K=10)
        #TODO put a self assert
        
        
        
if __name__ == "__main__":
    unittest.main()