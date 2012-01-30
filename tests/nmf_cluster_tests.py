'''
Created on 26 Jan 2012

@author: george
'''
import unittest, numpy
from analysis.clustering.nmf import NMFClusterer

###########################################
# GLOBALS                                #
###########################################
doc1 = 'frequent FrEquEnt frequent <li>word</li> word sentence sentence' 
doc2 = 'sentence <a href="www.google.com">arab</a> spring'
doc3 = 'a is not a toKENIzed document'
samples = [doc1, doc2, doc3] 

nmfc = NMFClusterer(ngram=1)        
i = 0
for sample in samples:
    nmfc.add_document(i, sample)
    i += 1
    
class Test(unittest.TestCase):

    def test_nmf_cluster(self):
        nmfc.run(seed = 'random_vcol', method='nmf', rank=2, max_iter=65, display_N_tokens = 6, display_N_documents =3)
        nmfc.dump_clusters_to_file("nmf_with_tweets")
        
if __name__ == "__main__":
    unittest.main()