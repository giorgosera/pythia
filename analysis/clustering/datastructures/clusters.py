'''
Created on 21 Jan 2012

@author: george
'''
import Orange, orange #!@UnresolvedImport
import nltk, numpy
from collections import OrderedDict 
from analysis.text import TextAnalyser

class AbstractKmeansClusterer(object):
    '''
    This is the abstract clusterer and specialized clusterers
    must be derived from it. 
    '''

    def __init__(self):
        '''
        Constructs a new cluster object
        '''
        self.document_dict = OrderedDict()
        self.attributes = None
        self.td_matrix = None
        self.table_name = None
        self.clusters = []
        self.text_analyser = TextAnalyser()
    
    def add_document(self, id, document):
        '''
        Adds a new document in the cluster structure.
        '''    
        id, document = self.text_analyser.add_document(id, document)
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
                top_terms += str(term)
            out.write("Most frequent terms:" + top_terms)
            out.write('\n')
            for document in cluster.document_dict.values():
                out.write(document["raw"])
                out.write('\n')
            i += 1   

    def load_table(self):
        raise NotImplementedError('load_table is not implemented.')
    
    def save_table(self, filename):
        raise NotImplementedError('save_table is not implemented.')
    
    def print_it(self):
        raise NotImplementedError('print_it is not implemented.')
            
class OrangeKmeansClusterer(AbstractKmeansClusterer):
    '''
    A clustering data structure that works with Orange
    '''            
    
    def run(self, filename, k=3):
        '''
        Runs the kmeans algorithm.
        '''
        self.construct_term_doc_matrix()
        self.save_table(filename)
        table = self.load_table()
        #initialization= Orange.clustering.kmeans.init_hclustering(n=100), distance =  Orange.distance.instances.PearsonRConstructor
        km = Orange.clustering.kmeans.Clustering(table, k)
        self.split_documents(km, k)
    
    def split_documents(self, km, k):
        '''
        This method splits the whole collection of documents 
        of this data set into the different clusters. Of course
        the algorithm should have been run and then invoke this method.
        It takes as input an object handler for the result of kmeans.
        '''
        clusters = [{} for k in range(k)]
        for doc_index, cluster in enumerate(km.clusters):
            document = self.document_dict.popitem(last=False)
            doc_id = document[0]
            rest = document[1]
            clusters[cluster][doc_id] = rest
        
        #Finally create K cluster objects with their document dicts. 
        [self.clusters.append(Cluster(id, cluster)) for id, cluster in enumerate(clusters)]
            
    def find_optimal_k(self, lowestk, highestk):
        '''
        Calculates the silhuette for a range of ks and returns 
        the best k for this data set.
        '''
        table = self.load_table()
        for k in range(lowestk, highestk):
            km = Orange.clustering.kmeans.Clustering(table, k, initialization=Orange.clustering.kmeans.init_diversity)
            score = Orange.clustering.kmeans.score_silhouette(km)
            print k, score
        
    def load_table(self):
        '''
        Loads the data from a tab delimited file. 
        '''
        if self.table_name != None:
            return Orange.data.Table(self.table_name)
        else:
            raise Exception("Oops. It seems that you have not saved a term-document matrix. Use save_table(filename)")
        
    def save_table(self, filename):
        '''
        It stores the term-docuemtn matrix as a tab delimited file
        which is supported by Orange. 
        '''
        if self.td_matrix != None: 
            #First construct the domain object (top row)
            vars = []
            for token in self.attributes:
                vars.append(Orange.data.variable.Continuous(str(token)))
            domain = Orange.data.Domain(vars, False) #The second argument indicated that the last attr must not be a class
            
            #Add data rows 
            t = Orange.data.Table(domain, self.td_matrix)
            
            #Add meta attributes to the samples i.e. the id of the document
            doc_id = Orange.data.variable.String("id")
            id = Orange.data.new_meta_id()
            t.add_meta_attribute(id)
            t.domain.add_meta(id, doc_id)
            
            for i, id in enumerate(self.document_dict.keys()):
                t[i]['id'] = str(id)
            
            orange.saveTabDelimited (filename+".tab", t)
            self.table_name = filename
        else:
            raise Exception("Oops. It seems that you have not constructed a term-document matrix. Use construct_term_document_matrix()")
                   
class CustomClusterer(AbstractKmeansClusterer):
    '''
    A clustering data structure that works with Orange
    '''            
    
    def split_documents(self, km, k):
        '''
        This method splits the whole collection of documents 
        of this data set into the different clusters. Of course
        the algorithm should have been run and then invoke this method.
        It takes as input an object handler for the result of kmeans.
        '''
        clusters = [{} for k in range(k)]
        for cluster_id, cluster in enumerate(km):
            for doc_index in cluster:
                document = self.document_dict.popitem(doc_index)
                doc_id = document[0]
                rest = document[1]
                clusters[cluster_id][doc_id] = rest
        #Finally create K cluster objects with their document dicts. 
        [self.clusters.append(Cluster(id, cluster)) for id, cluster in enumerate(clusters)]
    
    def load_table(self):
        '''
        Loads the data from a table file. 
        '''
        if self.table_name != None:
            lines=[line for line in file(self.table_name)]
            colnames=lines[0].strip().split('\t')[1:]
            rownames=[]
            data=[]
            for line in lines[1:]:
                p=line.strip().split('\t')
                rownames.append(p[0])
                data.append([float(x) for x in p[1:]])
            return rownames,colnames,data
        else:
            raise Exception("Oops. It seems that you have not saved a term-document matrix. Use save_table(filename)")
        
    def save_table(self, filename):
        '''
        It stores the term-document matrix in a custom format.
        '''
        if self.td_matrix != None:  
            out = file(filename, 'w')
            out.write("Term-document matrix")

            for token in self.attributes:
                out.write('\t%s' % token)
            out.write('\n')
            for i, id in enumerate(self.document_dict.keys()):
                out.write(str(id))
                for token in self.attributes:
                    out.write('\t%f' % self.td_matrix[i][self.attributes.index(token)])
                out.write('\n') 
            self.table_name = filename
        else:
            raise Exception("Oops. It seems that you have not constructed a term-document matrix. Use construct_term_document_matrix()")    
    
class Cluster(object):
    '''
    This is a structure responsible for representing a cluster after the 
    clustering has been performed. This class is used by the clusterers.
    '''
    def __init__(self, id, document_dict):
        '''
        Id specifies the id of this cluster and document_dict 
        is a dictionary storing all the relevant documents for this
        cluster.
        '''
        self.id = id
        self.document_dict = document_dict
        
    def get_documents(self):
        '''
        Returns a dictionary of the documents in the cluster.
        '''
        return self.document_dict
    
    def get_most_frequent_terms(self, N=5):
        '''
        Returns the top N occuring terms in this cluster.
        '''
        corpus = nltk.TextCollection([document['tokens'] for document in self.document_dict.values()])
        return nltk.FreqDist(corpus).items()[:N]     
    
    def get_size(self):
        '''
        The size of the cluster is defined by the number of its documents.
        '''   
        return len(self.document_dict.keys())
    
    def get_collocations(self, n=2, N=5):
        '''
        Returns the top collocations of the cluster corpus 
        based on Jaccard index. The collocations correspond 
        to n-grams and more specifically we limited the options
        to bigrams (n=2) and trigrams (n=3) ( n defaults to 2 ). 
        '''
        corpus = nltk.TextCollection([document['tokens'] for document in self.document_dict.values()])
        finder = nltk.BigramCollocationFinder.from_words(corpus)
        scorer = nltk.metrics.BigramAssocMeasures.jaccard
        #finder.apply_freq_filter(3)
        finder.apply_word_filter(lambda w:w in nltk.corpus.stopwords.words('english'))
        collocations = finder.nbest(scorer, N)
        
        #print "Cluster",self.id,"collocations:"
        #for collocation in collocations:
            #print ' '.join(str(i) for i in collocation)

class Bicluster(AbstractKmeansClusterer):
    '''
    A bicluster class. 
    '''

    def __init__(self, vector, left=None, right=None, similarity=0.0, id=None):
        '''
        Constructs a bicluster
        '''
        AbstractKmeansClusterer.__init__(self)
        self.left = left
        self.right = right
        self.vector = vector
        self.similarity = similarity
        self.id = id 
        
    def get_height(self):
        '''
        Returns the height of a cluster. Endpoints have a height of 1 and 
        then all other points have height equal to the sum of all their branches.
        '''    
        if self.left == None and self.right == None:
            return 1
        
        return self.left.get_height() + self.right.get_height()
        
    def get_depth(self):
        '''
        Returns the depth of the error.
        '''
        if self.left == None and self.right == None:
            return 0 
        
        return max(self.left.get_depth(), self.right.get_depth()) + self.similarity

    def print_it(self, labels=None, n=0):
        '''
        This method outputs the clusters in a human readable form.
        '''
        # For each new cluster have a small indentation to make it look hierarchical  
        for i in range(n): 
            print ' ',
        if self.id<0:
            # This is a branch
            print '->'
        else:
            # This is an root node
            if labels==None: print self.id
            else: print labels[self.id]
            
        # Recursively traverse the left and right branches
        if self.left!=None: 
            self.left.print_it(labels=labels,n=n+1)
        if self.right!=None: 
            self.right.print_it(labels=labels,n=n+1)
        
        
        