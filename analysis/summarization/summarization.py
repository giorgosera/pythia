'''
Created on 18 Mar 2012

@author: george
'''
import nltk, numpy
from analysis.clustering.algorithms import cosine

class AbstractSummarizer(object):
     
    def __init__(self, documents):
        '''
        It initialises the centroid summarizer structure.
        It receives a dict of documents.
        '''   
        self.documents = documents
    
    def summarize(self):
        raise NotImplementedError("summarize() was not implemented by child class")
        
        
    def _attach_feature_vectors(self):
        '''
        Iterates over the summarizer documents and calculates a tf-idf
        weighted feature vector for each document. The feature vectors is
        attached to the document.
        '''
        corpus = nltk.TextCollection([document.tokens for document in self.documents.values()])
        terms = list(set(corpus))
        
        for id, document in self.documents.iteritems():
            text = nltk.Text(document.tokens)
            fv = numpy.zeros([len(set(corpus))])
            for item in document.word_frequencies:
                fv[terms.index(item.word)]= corpus.tf_idf(item.word, text)
            self.documents[id].fv = fv
                          
class LexRankSummarizer(AbstractSummarizer):
    '''
    This class implements the LexRank algorithm for automatic text summarization.
    The implementation is based on this paper: http://tangra.si.umich.edu/~radev/lexrank/lexrank.pdf
    Please note that a single tweet is considered as a "sentence" of the LexRank algorithm.
    '''
    
    def summarize(self, threshold=0.1, tolerance=0.00001):
        
        self._attach_feature_vectors()
        doc_list = [document for document in self.documents.values()]
        n = len(doc_list)
        #Initialises the adjacency matrix
        adjacency_matrix = numpy.zeros([n, n])
        
        degree = numpy.zeros([1, n])
        scores = numpy.zeros([1, n])
        
        for i, documenti in enumerate(doc_list):
            for j, documentj in enumerate(doc_list):
                if len(documenti.tokens) < 2 or len(documentj) < 2:
                    if j == i:
                        adjacency_matrix[i][j] = 1.0
                    else:
                        adjacency_matrix[i][j] = 0.0
                else:
                    adjacency_matrix[i][j] = cosine(documenti.fv, documentj.fv )
                
                if adjacency_matrix[i][j] > threshold:
                    adjacency_matrix[i][j] = 1.0
                    degree[0][i] += 1
                else:
                    adjacency_matrix[i][j] = 0
        
        for i in xrange(n):
            for j in xrange(n):
                adjacency_matrix[i][j] = adjacency_matrix[i][j] / degree[0][i]

        scores[0] = self.power_method(adjacency_matrix, tolerance)
        result = []
        for i in xrange( 0, n ):
            result.append( [scores[0][i], doc_list[i].raw] )
        return result
    
    def power_method(self, m, epsilon ):
        n = len( m )
        p = [1.0 / n] * n
        while True:
            new_p = [0] * n
            for i in xrange( n ):
                for j in xrange( n ):
                    new_p[i] += m[j][i] * p[j]
            total = 0
            for x in xrange( n ):
                total += ( new_p[i] - p[i] ) ** 2
            p = new_p
            if total < epsilon:
                break
        return p
    
class CentroidSummarizer(AbstractSummarizer):
    '''
    This class implements the summarizer which is based on the centroid similarity.
    '''

    def __init__(self, documents):
        '''
        It initialises the centroid summarizer structure.
        It receives a dict of documents.
        '''
        super( CentroidSummarizer, self).__init__(documents)
        self.centroid = None
        
    def summarize(self):
        '''
        It performs the actual task of summarization. Basically, it ranks each document
        based on its distance from the collection centroid. The closer the better the ranking.
        It return a sorted list of documents.
        '''
        self._attach_feature_vectors()
        self._calculate_centroid()
        self._calculate_document_scores()
        doc_list = [document for document in self.documents.values()]
        #the smaller the distance the better
        sorted_documents = sorted(doc_list, key=lambda document: document.dist)
        return sorted_documents

    def _calculate_centroid(self):
        '''
        It calculates the centroid of this collection of documents.
        '''
        corpus = nltk.TextCollection([document.tokens for document in self.documents.values()])
        terms = list(set(corpus))
        
        centroid = numpy.zeros([len(self.documents.items()),len(terms)])
        for i, document in enumerate(self.documents.values()):
            centroid[i] = document.fv
        
        self.centroid = numpy.mean(centroid, axis=0)
        
    def _calculate_document_scores(self):
        '''
        Calculates the cosine similarity between a document and the centroid.
        It attaches the calculated distance on the document.
        '''
        for id, document in self.documents.iteritems():
            dist = cosine(self.centroid, document.fv)
            self.documents[id].dist = dist
 