'''
Created on 18 Mar 2012

@author: george
'''
import nltk, numpy
from analysis.clustering.algorithms import cosine

class CentroidSummarizer(object):
    '''
    This class implements the summarizer which is based on the centroid similarity.
    '''


    def __init__(self, documents):
        '''
        It initialises the centroid summarizer structure.
        It receives a dict of documents.
        '''
        self.documents = documents
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
 