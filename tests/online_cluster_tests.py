'''
Created on 26 Jan 2012

@author: george
'''
import unittest, numpy
from analysis.clustering.online import OnlineClusterer
from analysis.clustering.structures import OnlineCluster
from tests.test_document import get_test_documents, get_orange_clustering_test_data
###########################################
# GLOBALS                                #
###########################################
expected, sample_docs_raw, samples = get_test_documents()

class Test(unittest.TestCase):

#===============================================================================
#    def test_sample_doc_clustering_with_online(self):
#        oc = OnlineClusterer(N=2, window=3)        
#        samples = get_orange_clustering_test_data()
#        for document in samples:
#            index = oc.add_document(document)
#            oc.cluster(index, str(document.id), document.content)
#        expected = [0, 0, 0, 1, 1, 1]
#        
#    def test_cluster_term_document_matrix(self):
#        oc = OnlineClusterer(N=2, window=3)        
#        for document in samples:
#            index = oc.add_document(document)
#            oc.cluster(index, str(document.id), document.content)
# 
#            
#        calculated = oc.td_matrix
#        expected = numpy.array([[ 0.31388923,  0.11584717,  0,           0,           0,           0,           0.47083384], 
#                                [ 0,           0.13515504,  0.3662041,   0,           0.3662041,   0,           0         ],      
#                                [ 0,           0,           0,           0.54930614,  0,           0.549306140, 0        ]])
#        
#        self.assertEqual(expected.all(), calculated.all())
#===============================================================================
        
    def test_cluster_center_resize(self):
        center = numpy.array([0, 0, 1, 1, 0, 1])
        terms = ['test0', 'test1', 'test2', 'test3', 'test4', 'test5']
        cluster = OnlineCluster(center, 1, 1, "test", terms) 

        #'Test a longer term vector
        new_terms_longer_list = ['test0', 'test1', 'test2', 'test3', 'test4', 'test5', 'test6', 'test7'] 
        cluster.resize(new_terms_longer_list)
        expected_center = numpy.array([0, 0, 1, 1, 0, 1, 0, 0]) #2 zeroes in the end
        self.assertTrue(numpy.sum(expected_center - cluster.center) == 0)
        self.assertEquals(new_terms_longer_list, cluster.term_vector)
        
        #'Test a smaller term vector
        new_terms_smaller_list = ['test0', 'test1', 'test2', 'test3'] 
        cluster.resize(new_terms_smaller_list)
        expected_center = numpy.array([0, 0, 1, 1])
        self.assertTrue(numpy.sum(expected_center - cluster.center) == 0)
        self.assertEquals(new_terms_smaller_list, cluster.term_vector)

        #Test a longer term vector and shuffled
        new_terms_longer_listand_shuffled = ['test7', 'test0', 'test5', 'test2', 'test1', 'test3', 'test4', 'test6']  
        cluster.resize(new_terms_longer_listand_shuffled)
        expected_center = numpy.array([0, 0, 0, 1, 0, 1, 0, 0])
        self.assertTrue(numpy.sum(expected_center - cluster.center) == 0)
        self.assertEquals(new_terms_longer_listand_shuffled, cluster.term_vector)

if __name__ == "__main__":
    unittest.main()