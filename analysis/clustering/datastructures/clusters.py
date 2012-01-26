'''
Created on 21 Jan 2012

@author: george
'''
import Orange, orange #!@UnresolvedImport
import nltk, numpy

class AbstractCluster(object):
    '''
    This is the abstract clusterer and specialized clusterers
    must be derived from it. 
    '''

    def __init__(self):
        '''
        Constructs a new cluster object
        '''
        self.document_dict = {}
        self.attributes = None
        self.td_matrix = None
        self.table_name = None
    
    def add_document(self, id, document):
        '''
        Adds a new document in the cluster structure.
        '''    
        self.document_dict[id] = document
        
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
        if self.frequency_matrix_data:
            rotated = []
            for i in range(len(self.td_matrix[0])):
                newrow = [self.td_matrix[j][i] for j in range(len(self.td_matrix))]
                rotated.append(newrow)
            return rotated    
        else:
            raise Exception("Oops, no data to rotate. Maybe you didn't call read_frequency_matrix(filename)")

    def load_table(self):
        raise NotImplementedError('load_table is not implemented.')
    
    def save_table(self, filename):
        raise NotImplementedError('save_table is not implemented.')
    
    def print_it(self):
        raise NotImplementedError('print_it is not implemented.')
            
class OrangeCluster(AbstractCluster):
    '''
    A clustering data structure that works with Orange
    '''            
        
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
                   
class CustomCluster(AbstractCluster):
    '''
    A clustering data structure that works with Orange
    '''            
    
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
            self.frequency_matrix_data = data    
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
    

class Bicluster(AbstractCluster):
    '''
    A bicluster class. 
    '''

    def __init__(self, vector, left=None, right=None, similarity=0.0, id=None):
        '''
        Constructs a bicluster
        '''
        AbstractCluster.__init__(self)
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
        
        
        