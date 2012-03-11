'''
Created on 8 Feb 2012

@author: george

This module contains functions which perform housekeeping or other 
applications of Orange.
'''
import Orange, orange #!@UnresolvedImport

def construct_orange_table(variables, matrix=None, classed=False):
    '''
    Constructs an ExampleTable for Orange. It takes a
    list of variables and the corresponding feature vectors along
    with row identifiers i.e if this is a tweet table rowname would be
    the tweet id.
    '''
    #First construct the domain object (top row)
    vars = []
    for var in variables:
        vars.append(Orange.data.variable.Continuous(str(var)))
    domain = Orange.data.Domain(vars, classed) #The second argument indicated that the last attr must not be a class
    
    #Add data rows 
    if matrix != None:
        t = Orange.data.Table(domain, matrix)        
    else:
        t = Orange.data.Table(domain)        
    return t

def add_metas_to_table(table, rownames=None, meta_col_name="id"):
    '''
    Add meta attributes to the samples i.e. the id of the document
    '''
    doc_id = Orange.data.variable.String(meta_col_name)
    id = Orange.data.new_meta_id()
    table.add_meta_attribute(id)
    table.domain.add_meta(id, doc_id)
    
    if rownames!=None: 
        for i, id in enumerate(rownames):
            table[i][meta_col_name] = str(id)
        
    return table

def orange_pca(data):
    '''
    Projects the data points on the Principal Components
    '''
    pca = Orange.projection.pca.Pca(data, max_components=2)
    #See Orange documentation to find out what is ignore and ignore 
    projection = pca(data)
    matrix, ignore, ignore = projection.toNumpy()
    return matrix

def construct_distance_matrix(data):
    '''
    Constructs a distance matrix using Euclidean distance
    '''
    euclidean = orange.ExamplesDistanceConstructor_Euclidean(data)
    distance = orange.SymMatrix(len(data))
    for i in range(len(data)):
        for j in range(i+1):
            distance[i, j] = euclidean(data[i], data[j])
    return distance
        
def orange_mds(distance):
    '''
    It takes as input a distance matrix (see function above)
    and projects the data points using MDS
    '''
    mds = Orange.projection.mds.MDS(distance, dim=2)
    mds.run(100)
    return mds

