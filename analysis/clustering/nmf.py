'''
Created on 29 Jan 2012

@author: george
'''
import nimfa, numpy#!@UnresolvedImport
from analysis.clustering.abstract import AbstractClusterer
from analysis.clustering.structures import Cluster
from collections import OrderedDict
import pymf#!@UnresolvedImport
            
class NMFClusterer(AbstractClusterer):
    '''
    This clusterer uses non-negative matrix factorization to distinguish
    topics in tweets and then identify similar tweets.
    '''
    
    def __init__(self, seed = 'random_vcol', method='nmf', rank=3, max_iter=65, display_N_tokens = 5, display_N_documents = 8):
        """
        Constructor for NMF clusterer.
        """
        super(NMFClusterer, self).__init__(filter_terms=False)#Force filter terms to be false cz not yet supported
        self.seed=seed        
        self.method = method
        self.rank = rank
        self.max_iter = max_iter
        self.display_N_tokens = display_N_tokens
        self.display_N_documents = display_N_documents 
    
    def run(self):
        #Re-initialise clusters
        if self.clusters != []:
            self.clusters = []
 
        self.construct_term_doc_matrix(pca=False) #We cannot perform PCA with NMF because we only want non-negative vectors
        V = self.td_matrix
        
        nmf_mdl = pymf.NMF(V, num_bases=self.rank)
        nmf_mdl.factorize(niter=self.max_iter)
        w = nmf_mdl.W 
        h = nmf_mdl.H
                
        #model = nimfa.mf(V, seed = self.seed, method = self.method, rank = self.rank, max_iter = self.max_iter)
        #fitted = nimfa.mf_run(model)
        #w = fitted.basis() 
        #h = fitted.coef()
                
        self.split_documents(w,h, self.document_dict, self.attributes, display_N_tokens = self.display_N_tokens, display_N_documents = self.display_N_documents)

        #Just testing remove it    
        #self.showfeatures(w,h, [self.document_dict.values()[i]["raw"] for i in range(numpy.shape(w)[0])], self.attributes)
        
    def split_documents(self, w, h, documents, colnames, display_N_tokens, display_N_documents):
        pc, wc = numpy.shape(h)
        toppatterns = [[] for i in range(len(documents.keys()))]
        pattern_names = []
        top_documents = []
        
        # Loop over all the features
        for i in range(pc):
            slist=[]
            # Create a list of tokens and their weights
            #colname[j] is a token and h[i, j] is its weight
            for j in range(wc):
                slist.append((h[i,j],colnames[j]))
            # Reverse sort the word list 
            slist.sort()
            slist.reverse()
            
            # Print the first N tokens
            n=[s[1] for s in slist[0:display_N_tokens]]
            pattern_names.append(n)
            
            # Create a list of documents associated with this feature
            flist=[]

            for j, key in enumerate(documents.keys()):
                # Add the document with its weight
                document = documents.popitem(last=False)
                flist.append((w[j,i],document))
                #restores document after pop.
                documents[key] = document[1]
                toppatterns[j].append((w[j,i],i,documents[key]))
            # Reverse sort the list
            flist.sort()
            flist.reverse()
            
            top_docs = OrderedDict()            
            # Show the top N articles
            for f in flist[0:display_N_documents]:
                top_docs[f[1][0]] = f[1][1]
                top_docs[f[1][0]].weight = f[0]
            top_documents.append(top_docs)
            
        [self.clusters.append(Cluster(i, top_documents[i], pattern_names[i])) for i in range(pc)]
            
    def showfeatures(self, w,h,titles,wordvec,out='features.txt'): 
        outfile=file(out,'w')  
        pc,wc=numpy.shape(h)
        toppatterns=[[] for i in range(len(titles))]
        patternnames=[]
        
        # Loop over all the features
        for i in range(pc):
            outfile.write('\n')
            outfile.write('***********************************************************')
            outfile.write('\n')
            outfile.write('Cluster' + str(i) + '\n')
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
            for f in flist[0:10]:
                outfile.write(str(f)+'\n')
            outfile.write('\n')
        
        outfile.close()
        # Return the pattern names for later use
        return toppatterns,patternnames