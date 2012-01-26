'''
Created on 26 Jan 2012

@author: george
'''
import unittest
from analysis.clustering.datastructures.clusters import OrangeCluster
from analysis.text import TextAnalyser
import numpy

###########################################
# GLOBALS                                #
###########################################
doc1 = 'frequent FrEquEnt frequent <li>word</li> word sentence sentence' 
doc2 = 'sentence <a href="www.google.com">arab</a> spring'
doc3 = 'a is not a toKENIzed document'
samples = [doc1, doc2, doc3] 

ta = TextAnalyser()
oc = OrangeCluster()        
i = 0
for sample in samples:
    index, d = ta.add_document(i, sample)
    oc.add_document(index, d)
    i += 1

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
        
    def test_most_frequent_terms(self):
        oc.construct_term_doc_matrix()
        top = oc.get_most_frequent_terms(N=5)
        expected = [('frequent', 3), ('sentenc', 3), ('word', 2), ('arab', 1), ('document', 1)]
        self.assertEqual(expected, top)
        
if __name__ == "__main__":
    unittest.main()