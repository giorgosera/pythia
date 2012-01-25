'''
Created on 23 Jan 2012

@author: george
'''

from database.warehouse import WarehouseServer

def output_clusters_to_file(clusters, rownames, filename):
    '''
    This method takes as input a set of clusters and generates 
    a very simplistic representation of these clusters in text form
    in a file. 
    '''
    
    ws = WarehouseServer()
    out = file(filename, 'w')
    out.write("Clustering results")
    out.write('\n')
    i = 0 
    for cluster in clusters:
        out.write('\n')
        out.write('***********************************************************')
        out.write('\n')
        out.write("Cluster"+str(i))
        out.write('\n')
        for document in cluster:
            out.write( ws.get_document_by_id(rownames[document]).text)
            out.write('\n')
        i += 1
        
def output_clusters_to_file_translated(clusters, rownames, analyser, filename):
    '''
    This method takes as input a set of clusters and generates 
    a very simplistic representation of these clusters in text form
    in a file. It differs from the above method in that the translated
    text appears in the file and not the original. 
    '''
    out = file(filename, 'w')
    out.write("Clustering results")
    out.write('\n')
    i = 0 
    for cluster in clusters:
        out.write('\n')
        out.write('***********************************************************')
        out.write('\n')
        out.write("Cluster"+str(i))
        out.write('\n')
        for document in cluster:
            out.write( analyser.get_document_by_id(rownames[document])["raw"])
            out.write('\n')
        i += 1        
            
        