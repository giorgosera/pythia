'''
Created on 29 Jan 2012

@author: george
'''
import nltk, numpy, Orange#!@UnresolvedImport
from tools.orange_utils import construct_orange_table, orange_pca, add_metas_to_table
from collections import OrderedDict 
from visualizations.graphs import MatplotlibTimeline, D3Timeline
from visualizations.mds import MDS
from tools.utils import aggregate_data
from matplotlib.dates import num2date#!@UnresolvedImport
from analysis.index import Index
        
class AbstractClusterer(object):
    '''
    This is the abstract clusterer and specialized clusterers
    must be derived from it. 
    '''

    def __init__(self, ngram=1, filter_terms=False):
        '''
        Constructs a new cluster object
        '''
        self.db_documents = None
        self.document_dict = OrderedDict()
        self.attributes = None
        self.td_matrix = None
        self.table_name = None
        self.clusters = []
        self.filter_terms = filter_terms
        
    def add_documents(self, document_list):
        '''
        Adds a batch of new documents in the cluster structure.
        '''    
        self.db_documents = document_list
        for document in document_list:
            self.add_document(document)
        
    def add_document(self, document):
        '''
        Adds a new document in the cluster structure.
        It also returns the index of the new doc for future use.
        The index is N-1 where N is the length of the dict since 
        this is an OrderedDict structure.
        '''    
        self.document_dict[str(document.id)] = document.content
        return len(self.document_dict.keys())-1
    
    def get_documents(self):
        return self.document_dict
    
    def get_document_by_id(self, id):
        result = self.document_dict[id]

        if result:
            return result 
        else:    
            raise Exception("Oops. No document with this ID was found.")       
        
    def _filter_terms(self):
        '''
        Removes tokens that appear either too often or too rarely. It returns the corpus of 
        filtered tokens and also changes the token and word_frequencies lists of each document
        according to the filtered tokens.
        '''
        index = Index("kmeans_index")
        index.add_documents(self.db_documents)
        index.finalize()
        filtered_terms = index.get_filtered_terms(lowestf=0.1, highestf=0.2)
        corpus = []
        for id, document in self.document_dict.iteritems():
            filtered_tokens = []
            for token in document.tokens:
                if token in filtered_terms:
                    filtered_tokens.append(token)
            
            if len(filtered_tokens) == 0: #if all the tokens are removed then this document is worthless
                self.document_dict.pop(id)
            else: #if there are still tokens ammend the token list and the word frequencies list to include only the relevant tokens
                self.document_dict[id].tokens = filtered_tokens
                self.document_dict[id].word_frequencies = [item for item in self.document_dict[id].word_frequencies if item.word in filtered_tokens]
                
            corpus.append(filtered_tokens)
        return corpus
        
    def construct_term_doc_matrix(self, pca=False):
        '''
        Constructs a term-document matrix such that td_matrix[document][term] 
        contains the weighting score for the term in the document.
        '''
        if not self.filter_terms:    
            corpus = nltk.TextCollection([document.tokens for document in self.document_dict.values()])
        else:
            corpus = nltk.TextCollection(self._filter_terms())
            
        terms = list(set(corpus))
        data_rows = numpy.zeros([len(self.document_dict), len(set(corpus))])
        
        for i, document in enumerate(self.document_dict.values()):
            text = nltk.Text(document.tokens)
            for item in document.word_frequencies:
                data_rows[i][terms.index(item.word)] = corpus.tf_idf(item.word, text)
        
        
        #table = Orange.data.Table("iris.tab")
        self.attributes = terms#table.domain.features
        #a, c, w = table.to_numpy()        
        self.td_matrix = data_rows#a
                
        #If PCA is True then we project our points on their principal components
        #for dimensionality reduction
        if pca:
            t = construct_orange_table(self.attributes, self.td_matrix)
            self.td_matrix = orange_pca(t)
            #Attributes names have no meaning after dimensionality reduction
            self.attributes = [i for i in range(self.td_matrix.shape[1])]

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
                out.write(document.raw)
                out.write('\n')
            i += 1   
            
    def plot_growth_timeline(self, cumulative=True, plot_method="d3"):
        '''
        Plots a graph depicting the growth of each cluster's size as a 
        function of time.
        '''
        assert self.clusters != []
        if plot_method == "matplotlib":
            for cluster in self.clusters:
                documents =  cluster.get_documents()
                if len(documents) > 0:
                    dates, counts = aggregate_data([doc['date'] for doc in documents.values()], cumulative=cumulative)
                    t = MatplotlibTimeline(dates, counts, cumulative=cumulative)
                    t.plot()
            t.show()
        elif plot_method=="d3":        
            data = []; meta = []
            for cluster in self.clusters:
                documents = cluster.get_documents()
                cluster.analyse()
                if len(documents) > 0:
                    data.append([doc.date for doc in documents.values()])
                    meta.append({"Terms" :cluster.get_most_frequent_terms(N=8), 
                                 "Authors": [len(cluster.get_authors())], #should be wrapped in a list
                                 "Locations": cluster.get_locations(N=2),
                                 "Main entities": cluster.get_persons(N=2)})

            dates = []; counts = []
            for d in data:
                t_dates, t_counts = aggregate_data(d, cumulative)
                dates.append([num2date(date).strftime('%Y-%m-%d %H:%M:%S') for date in t_dates])
                counts.append(t_counts)
            final_dates = dates
            final_counts = [count.tolist() for count in counts]
            t = D3Timeline(final_dates, final_counts, meta, cumulative=cumulative)
            t.plot(url='timeline_growth.html')
            
    def plot_sentiment_timeline(self, cumulative=True, plot_method="d3"):
        '''
        Plots a graph depicting the sentiment variation of each cluster as a 
        function of time.
        '''
        assert self.clusters != []
        dates = []
        counts = []
        for i, cluster in enumerate(self.clusters):
            cluster_sentiment = cluster.get_sentiment()
            dates.append([sentiment[0] for sentiment in cluster_sentiment])
            counts.append([sentiment[1] for sentiment in cluster_sentiment])
        final_dates = dates 
        final_counts = counts 
            
        t = D3Timeline(final_dates, final_counts, cumulative=cumulative)
        t.plot(url='timeline_sentiment.html')

    def plot_scatter(self):
        '''
        Plots all the data points in 2D.
        '''
        assert self.attributes and self.td_matrix != None
        
        #Create a clusterer document list to get the index of a doc (horrible hack I know)
        clusterer_document_list = [key for key in self.document_dict.keys()] 
        table = construct_orange_table(self.attributes)
        meta_col_name="cluster_id"
        table = add_metas_to_table(table, meta_col_name=meta_col_name)

        instances = []
        for cluster in self.clusters:
            #A small hack for dbscan noise cluster. It's id is -1 and color scale is  wrong if -1
            if cluster.id == -1: cluster.id += len(self.clusters);
            for doc_id in cluster.document_dict.iterkeys():
                index = clusterer_document_list.index(doc_id)
                inst = Orange.data.Instance(table.domain, list(self.td_matrix[index]))
                inst[meta_col_name] = str(cluster.id)
                instances.insert(index, inst)

        #we have a table with the clusters ids as metas.                
        table.extend(instances)        
        mds = MDS(table)
        classes_list = []
        for c in self.clusters:
            classes_list.append(c.id)

        mds.plot(classes_list=classes_list, class_col_name="cluster_id")
        
    def _post_processing(self):
        '''
        Post processing takes place after the clustering algorithm has finished execution.
        It removes the clusters that are not important. 
        TODO: Find a way to define importance. For now remove clusters with either too much or too few docs.
        '''
        total_docs = len(self.document_dict.keys())
        filtered = []
        for cluster in self.clusters:
            size = cluster.get_size()
            if size > total_docs*0.01 and size < total_docs*0.05:
                filtered.append(cluster) 
        #Replace cluster list with the filtered ones
        self.clusters = filtered
        
    def run(self):
        raise NotImplementedError('run is not implemented.')

    def split_documents(self):
        raise NotImplementedError('split_documents is not implemented.')
    
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