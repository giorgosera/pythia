'''
Created on 26 Jan 2012

@author: george
'''
import unittest, numpy
from analysis.clustering.nmf import NMFClusterer
from tests.test_document import get_test_documents

expected, sample_docs_raw, samples = get_test_documents()

nmfc = NMFClusterer(seed = 'random_vcol', method='nmf', rank=2, max_iter=65, display_N_tokens = 6, display_N_documents =3)        
nmfc.add_documents(samples)
    
class Test(unittest.TestCase):

    def test_nmf_cluster(self):
        nmfc.run()
        nmfc.dump_clusters_to_file("nmf_with_samples")
        
if __name__ == "__main__":
    unittest.main()