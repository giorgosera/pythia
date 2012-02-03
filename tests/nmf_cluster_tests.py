'''
Created on 26 Jan 2012

@author: george
'''
import unittest, numpy
from analysis.clustering.nmf import NMFClusterer

###########################################
# GLOBALS                                #
###########################################
doc1_raw = 'frequent FrEquEnt frequent <li>word</li> word sentence sentence' 
doc2_raw = 'sentence <a href="www.google.com">arab</a> spring'
doc3_raw = 'a is not a toKENIzed document'               

doc1_tokens = ['frequent', 'frequent', 'frequent', 'word', 'word', 'sentenc', 'sentenc']
doc2_tokens = ['sentenc', 'arab', 'spring']
doc3_tokens = ['token', 'document']

freq1 = [('frequent', 3), ('sentenc', 2), ('word', 2)]
freq2 = [('arab', 1), ('sentenc', 1), ('spring', 1)]
freq3 = [('document', 1), ('token', 1)]


entry1 = {"tokens":doc1_tokens, "raw": doc1_raw, "word_frequencies":freq1}
entry2 = {"tokens":doc2_tokens, "raw": doc2_raw, "word_frequencies":freq2}
entry3 = {"tokens":doc3_tokens, "raw": doc3_raw, "word_frequencies":freq3}
samples = [entry1, entry2, entry3] 

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