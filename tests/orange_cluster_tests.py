'''
Created on 26 Jan 2012

@author: george
'''
import unittest, numpy
from analysis.clustering.kmeans import OrangeKmeansClusterer
from tests.test_document import get_test_documents
###########################################
# GLOBALS                                #
###########################################
ignore, ignore, samples  =  get_test_documents()

oc = OrangeKmeansClusterer(k=4)        
for sample in samples:
    oc.add_document(sample)

class Test(unittest.TestCase):

    def test_orange_cluster_term_document_matrix(self):
        oc.construct_term_doc_matrix()
        calculated = oc.td_matrix
        expected = numpy.array([[ 0.31388923,  0.11584717,  0,           0,           0,           0,           0.47083384], 
                                [ 0,           0.13515504,  0.3662041,   0,           0.3662041,   0,           0         ],      
                                [ 0,           0,           0,           0.54930614,  0,           0.549306140, 0        ]])

        self.assertEqual(expected.all(), calculated.all())
        
    def test_orange_save_matrix_to_tab_file(self):
        oc.construct_term_doc_matrix()
        oc.save_table("sample_table_orange")
        
    def test_matrix_rotation(self):
        oc.construct_term_doc_matrix()
        rtd = oc.rotate_td_matrix()
        expected = [[0.31388922533374564, 0.0, 0.0], 
                    [0.11584717374518982, 0.13515503603605478, 0.0], 
                    [0.0, 0.36620409622270322, 0.0], 
                    [0.0, 0.0, 0.54930614433405489], 
                    [0.0, 0.36620409622270322, 0.0], 
                    [0.0, 0.0, 0.54930614433405489], 
                    [0.47083383800061845, 0.0, 0.0]]
        
        self.assertEqual(expected, rtd)
        
    def test_split_into_clusters(self):

        oc.run("orange_clustering_test")
        expected_clusters = [ ['0', '2'],['1']]
        self.assertEqual(expected_clusters, [c.get_documents().keys() for c in oc.clusters])
        oc.dump_clusters_to_file("test_orange_with_samples")
        
        
if __name__ == "__main__":
    unittest.main()