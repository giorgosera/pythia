# -*- coding: utf-8 -*-
'''
Created on 13 Nov 2011

@author: george

Unit tests for the evaluation package.
'''
import unittest, numpy
from evaluation.events import EventDetectionEvaluator

class TestEvaluationClass(unittest.TestCase):
    
    def test_confusion_matrix_creation(self):
        ede = EventDetectionEvaluator()
        targets = [1, 1, 1, 1, 1 , 1, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2]
        predictions = [1, 1, 1, 1, 1 , 1, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2]
        confusion_matrix = ede.create_confusion_matrix(targets, predictions, 3)
        expected = numpy.array([[ 6., 0., 0.],[ 0., 6., 0.],[ 0., 0., 6.]])

        self.assertTrue(numpy.in1d((numpy.sum(confusion_matrix-expected, axis=1)), [0., 0., 0.]).all())
        
    def test_precision_recall_and_f_calculation(self):
        ede = EventDetectionEvaluator()
        targets = [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1 , 1, 2, 2, 2, 2, 2, 2]
        predictions = [0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1 , 2, 2, 2, 2, 2, 0, 2]
        confusion_matrix = ede.create_confusion_matrix(targets, predictions, 3)
        rp_rates = ede.calculate_precision_recall(confusion_matrix)
        fs = ede.calculate_f_measure(rp_rates)
        self.assertEquals(sum(fs), [2.5])
if __name__ == "__main__":
    unittest.main()