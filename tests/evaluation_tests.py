# -*- coding: utf-8 -*-
'''
Created on 13 Nov 2011

@author: george

Unit tests for the evaluation package.
'''
import unittest, numpy
from evaluation.evaluators import *
from analysis.clustering.kmeans import OrangeKmeansClusterer

class TestClusteringEvaluationClass(unittest.TestCase):
    
    def test_confusion_matrix_creation(self):
        ede = ExtrinsicClusteringEvaluator()
        targets = [1, 1, 1, 1, 1 , 1, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2]
        predictions = [1, 1, 1, 1, 1 , 1, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2]
        confusion_matrix = ede.create_confusion_matrix(targets, predictions, 3)
        expected = numpy.array([[ 6., 0., 0.],[ 0., 6., 0.],[ 0., 0., 6.]])

        self.assertTrue(numpy.in1d((numpy.sum(confusion_matrix-expected, axis=1)), [0., 0., 0.]).all())
        
    def test_precision_recall_and_f_calculation(self):
        ede = ExtrinsicClusteringEvaluator()
        targets = [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1 , 1, 2, 2, 2, 2, 2, 2]
        predictions = [0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1 , 2, 2, 2, 2, 2, 0, 2]
        confusion_matrix = ede.create_confusion_matrix(targets, predictions, 3)
        rp_rates = ede.calculate_precision_recall(confusion_matrix)
        fs = ede.calculate_f_measure(rp_rates)
        self.assertEquals(sum(fs), [2.5])
    
    def test_bcubed_calculation(self):
        ede = ExtrinsicClusteringEvaluator()
        documents_labels_clusters = [(0, 0), (0, 1), (0, 0), (0, 0), (0, 1), (0, 0), 
                                     (1, 1), (1, 1), (1, 2), (1, 1), (1, 1), (1, 1),
                                     (2, 1), (2, 0), (2, 2), (2, 0), (2, 2), (2, 2)]
                
        precision ,recall, f = ede.calculate_bcubed_measures(documents_labels_clusters)
        self.assertAlmostEqual(0.532407407407 - precision, 0, places=7)
        self.assertAlmostEqual(0.555555555556 - recall, 0, places=7)
        self.assertAlmostEqual(0.543735224586 - f, 0, places=7)
        
    def test_intrinsic_measures(self):
        ice = IntrinsicClusteringEvaluator()
        own_vectors = [numpy.array([0.1, 1.2]), numpy.array([0.2, 1.0])]
        other_cluster_vectors = [ [numpy.array([10.1, 1.2]), numpy.array([10.24, 0.8])], 
                                  [numpy.array([5.1, 1.3]), numpy.array([5.24, 1.8])] ]
        sc1 = ice._calculate_shilouette_coefficients(own_vectors, other_cluster_vectors)
        
        own_vectors = [numpy.array([10.1, 1.2]), numpy.array([10.24, 0.8])]
        other_cluster_vectors = [ [numpy.array([0.1, 1.2]), numpy.array([0.2, 1.0])], 
                                  [numpy.array([5.1, 1.3]), numpy.array([5.24, 1.8])] ]
        sc2 = ice._calculate_shilouette_coefficients(own_vectors, other_cluster_vectors)
        
        own_vectors = [numpy.array([5.1, 1.3]), numpy.array([5.24, 1.8])]
        other_cluster_vectors = [ [numpy.array([0.1, 1.2]), numpy.array([0.2, 1.0])], 
                                   [numpy.array([10.1, 1.2]), numpy.array([10.24, 0.8])]]
        sc3 = ice._calculate_shilouette_coefficients(own_vectors, other_cluster_vectors)

        sc = [sc1, sc2, sc3]
        
        quality = ice._calculate_clustering_quality(sc)
        
        self.assertEqual(quality, 0.9224153975232596)
        self.assertAlmostEqual(quality, 0.922415397523, places=5)
        
#===============================================================================
# class TestClassificationEvaluationClass(unittest.TestCase):
# 
#    def test_dataset_split(self):
#        X = [i for i in xrange(97)]
#        ce = ClassificationEvaluator(X) 
#        ce.evaluate(K=10)
#        #TODO put a self assert
#===============================================================================
        
if __name__ == "__main__":
    unittest.main()