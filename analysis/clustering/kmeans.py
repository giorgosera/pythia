'''
Created on 29 Jan 2012

@author: george
'''

import Orange, orange #!@UnresolvedImport
from analysis.clustering.abstract import AbstractKmeansClusterer
from analysis.clustering.structures import Cluster
from tools.orange_utils import construct_orange_table, add_metas_to_table
from analysis.clustering.algorithms import ExamplesDistanceConstructor_Cosine, ExamplesDistanceConstructor_Jaccard
from analysis.clustering.algorithms import euclidean, cosine, jaccard

distances = {cosine: ExamplesDistanceConstructor_Cosine(), 
             euclidean: Orange.distance.instances.EuclideanConstructor(),
             jaccard: ExamplesDistanceConstructor_Jaccard()
             }

class OrangeKmeansClusterer(AbstractKmeansClusterer):
    '''
    A clustering data structure that works with Orange
    '''            
    def run(self, pca=False, post_process=False):
        '''
        Runs the kmeans algorithm.
        '''
        #Re-initialise clusters
        if self.clusters != []:
            self.clusters = []
            
        vars = []
        self.construct_term_doc_matrix(pca=pca)

        for token in self.attributes:
            vars.append(Orange.data.variable.Continuous(str(token)))
        domain = Orange.data.Domain(vars, False) #The second argument indicated that the last attr must not be a class
        table = Orange.data.Table(domain, self.td_matrix)
            
        km = Orange.clustering.kmeans.Clustering(table, self.k, distance=distances[self.distance])        #initialization= Orange.clustering.kmeans.init_hclustering(n=100), distance =  Orange.distance.instances.PearsonRConstructor    

        self.split_documents(km)
        if post_process:
            self._post_processing()
        return km
    
    def split_documents(self, km):
        '''
        This method splits the whole collection of documents 
        of this data set into the different clusters. Of course
        the algorithm should have been run and then invoke this method.
        It takes as input an object handler for the result of kmeans.
        '''
        clusters = [{} for k in range(self.k)]
        for doc_index, cluster in enumerate(km.clusters):
            document = self.document_dict.popitem(last=False)
            doc_id = document[0]
            rest = document[1]
            clusters[cluster][doc_id] = rest
            self.document_dict[doc_id] = rest
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
            t = construct_orange_table(self.attributes, self.td_matrix)
            t = add_metas_to_table(t, self.document_dict.keys())
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
