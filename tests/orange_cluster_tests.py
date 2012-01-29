'''
Created on 26 Jan 2012

@author: george
'''
import unittest, numpy
import nimfa#!@UnresolvedImport
from analysis.clustering.datastructures.clusters import OrangeKmeansClusterer

###########################################
# GLOBALS                                #
###########################################
doc1 = 'frequent FrEquEnt frequent <li>word</li> word sentence sentence' 
doc2 = 'sentence <a href="www.google.com">arab</a> spring'
doc3 = 'a is not a toKENIzed document'
samples = [doc1, doc2, doc3] 

oc = OrangeKmeansClusterer(k=2)        
i = 0
for sample in samples:
    oc.add_document(i, sample)
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
        
    def test_split_into_clusters(self):

        oc.run("orange_clustering_test")
        expected_clusters = [{'0': {'tokens': ['frequent', 'frequent', 'frequent', 'word', 'word', 'sentenc', 'sentenc'], 'raw': 'frequent FrEquEnt frequent <li>word</li> word sentence sentence', 'word_frequencies': [('frequent', 3), ('sentenc', 2), ('word', 2)]}, '2': {'tokens': ['token', 'document'], 'raw': 'a is not a toKENIzed document', 'word_frequencies': [('document', 1), ('token', 1)]}}
                             ,{'1': {'tokens': ['sentenc', 'arab', 'spring'], 'raw': 'sentence <a href="www.google.com">arab</a> spring', 'word_frequencies': [('arab', 1), ('sentenc', 1), ('spring', 1)]}}]
        
        self.assertEqual(expected_clusters, [c.get_documents() for c in oc.clusters])
        
        oc.dump_clusters_to_file("test_orange_with_samples")
        
        def showfeatures(w,h,titles,wordvec,out='features.txt'): 
            outfile=file(out,'w')  
            pc,wc=numpy.shape(h)
            toppatterns=[[] for i in range(len(titles))]
            patternnames=[]
            
            # Loop over all the features
            for i in range(pc):
              slist=[]
              # Create a list of words and their weights
              for j in range(wc):
                slist.append((h[i,j],wordvec[j]))
              # Reverse sort the word list
              slist.sort()
              slist.reverse()
              
              # Print the first six elements
              n=[s[1] for s in slist[0:6]]
              outfile.write(str(n)+'\n')
              patternnames.append(n)
              
              # Create a list of articles for this feature
              flist=[]
              for j in range(len(titles)):
                # Add the article with its weight
                flist.append((w[j,i],titles[j]))
                toppatterns[j].append((w[j,i],i,titles[j]))
              
              # Reverse sort the list
              flist.sort()
              flist.reverse()
              
              # Show the top 3 articles
              for f in flist[0:3]:
                outfile.write(str(f)+'\n')
              outfile.write('\n')
            
            outfile.close()
            # Return the pattern names for later use
            return toppatterns,patternnames
        
        V = oc.td_matrix

        model = nimfa.mf(V, seed = 'random_vcol', method = 'nmf', rank = 2, max_iter = 65)
        fitted = nimfa.mf_run(model)
        w = fitted.basis() 
        h = fitted.coef()

        showfeatures(w,h, oc.document_dict.keys(), oc.attributes)
        
        
if __name__ == "__main__":
    unittest.main()