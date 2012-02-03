'''
Created on 29 Jan 2012

@author: george
'''
import nltk, numpy 
from collections import OrderedDict 
from analysis.text import TextAnalyser

class AbstractClusterer(object):
    '''
    This is the abstract clusterer and specialized clusterers
    must be derived from it. 
    '''

    def __init__(self, ngram=1):
        '''
        Constructs a new cluster object
        '''
        self.document_dict = OrderedDict()
        self.attributes = None
        self.td_matrix = None
        self.table_name = None
        self.clusters = []
        
    def add_document(self, id, document):
        '''
        Adds a new document in the cluster structure.
        '''    
        self.document_dict[str(id)] = document
    
    def get_documents(self):
        return self.document_dict
    
    def get_document_by_id(self, id):
        result = self.document_dict[id]

        if result:
            return result 
        else:    
            raise Exception("Oops. No document with this ID was found.")       
        
    def construct_term_doc_matrix(self):
        '''
        Constructs a term-document matrix such that td_matrix[document][term] 
        contains the weighting score for the term in the document.
        '''
        corpus = nltk.TextCollection([document['tokens'] for document in self.document_dict.values()])
        terms = list(set(corpus))
        data_rows = numpy.zeros([len(self.document_dict), len(set(corpus))])
        
        for i, document in enumerate(self.document_dict.values()):
            text = nltk.Text(document['tokens'])
            for term, count in document['word_frequencies']:
                data_rows[i][terms.index(term)] = corpus.tf_idf(term, text)
        
        self.attributes = terms
        self.td_matrix = data_rows 

    def rotate_td_matrix(self):
        '''
        It rotates the term-document matrix. This is useful when we perfrom column clustering.
        '''
        #First we have to read the data using read_frequency_matrix(filename)
        if self.td_matrix != None:
            rotated = []
            for i in range(self.td_matrix.shape[1]):
                newrow = [self.td_matrix[j][i] for j in range(self.td_matrix.shape[0])]
                rotated.append(newrow)
            return rotated    
        else:
            raise Exception("Oops, no matrix to rotate. Maybe you didn't call construct_term_doc_matrix()")
        
    def dump_clusters_to_file(self, filename):
        '''
        Dumps a simple representation of the clusters to a file.
        '''
        out = file(filename, 'w')
        out.write("Clustering results")
        out.write('\n')
        i = 0 
        for cluster in self.clusters:
            out.write('\n')
            out.write('***********************************************************')
            out.write('\n')
            out.write("Cluster" + str(cluster.id))
            out.write('\n')
            top_terms = ""
            for term in cluster.get_most_frequent_terms(N=10):
                top_terms += str(term) + " "
            out.write("Most frequent terms:" + top_terms)
            out.write('\n')
            for document in cluster.document_dict.values():
                #if document["weight"] != None:
                #    out.write(str(document["weight"]) + "-->")
                out.write(document["raw"])
                out.write('\n')
            i += 1   
    
    def run(self):
        raise NotImplementedError('run is not implemented.')

    def load_table(self):
        raise NotImplementedError('load_table is not implemented.')
    
    def save_table(self, filename):
        raise NotImplementedError('save_table is not implemented.')
    
    def print_it(self):
        raise NotImplementedError('print_it is not implemented.')

class AbstractKmeansClusterer(AbstractClusterer):
    '''
    This is the abstract clusterer and specialized clusterers
    must be derived from it. 
    '''

    def __init__(self, k=3, ngram=1):
        '''
        Constructs a new kmeans abstract cluster object
        '''
        AbstractClusterer.__init__(self, ngram=ngram)
        self.k = k