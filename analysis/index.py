'''
Created on 4 Feb 2012

@author: george
'''
import os, time, lucene#!@UnresolvedImport
from lucene import *

class Index(object):
    '''
    This class is responsible for using the Pylucene framework
    for building an index for the keywords appearing in the documents
    we want to analyse.
    '''
    
    def __init__(self, index_dir):
        '''
        Initialises index parameters
        '''
        lucene.initVM()
        self.index_dir = index_dir
        if not os.path.exists(self.index_dir):
            os.mkdir(self.index_dir)
        store = lucene.SimpleFSDirectory(lucene.File(self.index_dir))
        self.analyser = PorterStemmerAnalyzer()
        self.writer = lucene.IndexWriter(store, 
                                    self.analyser, 
                                    True, 
                                    lucene.IndexWriter.MaxFieldLength.LIMITED)
        self.writer.setMaxFieldLength(1048576)
        
    def add_document(self, document):
        '''
        Adds a new document in the index.
        '''
        doc = lucene.Document()
        try:
            #All fields are converted to string since Lucene accepts only textual fields (and binary)
            doc.add(lucene.Field("id", str(document.id),
                                lucene.Field.Store.YES,
                                lucene.Field.Index.NOT_ANALYZED))
            doc.add(lucene.Field("content", document.content['raw'],
                                lucene.Field.Store.YES,
                                lucene.Field.Index.ANALYZED))
            doc.add(lucene.Field("author", document.author_screen_name,
                                lucene.Field.Store.YES,
                                lucene.Field.Index.NOT_ANALYZED))
            doc.add(lucene.Field("timestamp", str(time.mktime(document.date.timetuple())),
                                lucene.Field.Store.YES,
                                lucene.Field.Index.NOT_ANALYZED))
            self.writer.addDocument(doc)
        except Exception, e:
            print "Failed in indexDocs:", e
            
    def finalize(self):
        '''
        Performs optimization on the index and closes writer
        '''
        self.writer.optimize()
        self.writer.close()
        
    def search(self, query):
        '''
        Searches the index based on the query supplied.
        '''
        directory = lucene.SimpleFSDirectory(lucene.File(self.index_dir))
        searcher = lucene.IndexSearcher(directory, True)    
        query = lucene.QueryParser(lucene.Version.LUCENE_CURRENT, "content",
                                self.analyser).parse(query)
        scoreDocs = searcher.search(query, 50).scoreDocs
        
        results = []
        for scoreDoc in scoreDocs:
                results.append(searcher.doc(scoreDoc.doc))
                
        searcher.close()
        return results
        
class PorterStemmerAnalyzer(lucene.PythonAnalyzer):
    '''
    This class extends the simple analyzer by adding a stemmer. 
    '''
    def tokenStream(self, fieldName, reader):
        result = lucene.StandardTokenizer(lucene.Version.LUCENE_CURRENT, reader)
        result = lucene.StandardFilter(result)
        result = lucene.LowerCaseFilter(result)
        result = lucene.PorterStemFilter(result)
        result = lucene.StopFilter(True, result, lucene.StopAnalyzer.ENGLISH_STOP_WORDS_SET)
        return result
        
        
        