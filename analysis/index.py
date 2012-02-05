'''
Created on 4 Feb 2012

@author: george
'''
import os, time, lucene#!@UnresolvedImport
from lucene import *
from time import gmtime, strftime

class Index(object):
    '''
    This class is responsible for using the Pylucene framework
    to build an index for the keywords appearing in the documents
    we want to analyse. It also provides methods to search the index
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
            doc.add(lucene.Field("content", ' '.join(document.content['tokens']),
                                lucene.Field.Store.YES,
                                lucene.Field.Index.ANALYZED))
            doc.add(lucene.Field("author", document.author_screen_name,
                                lucene.Field.Store.YES,
                                lucene.Field.Index.NOT_ANALYZED))
            formatted_date = lucene.SimpleDateFormat("yyyyMMddHHmmss").parse(str(document.date))
            doc.add(lucene.Field("date", lucene.DateTools.dateToString(formatted_date, lucene.DateTools.Resolution.MINUTE),
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
        
    def search_by_term(self, query, limit=None):
        return self.search(query, "content", limit=limit)
    
    def search_by_author(self, query, limit=None):
        return self.search(query, field="author", limit=limit)
    
    def search_by_date(self, query, limit=None):
        return self.search(query, field="timestamp", limit=limit)
    
    def search_by_id(self, query, limit=None):
        return self.search(query, field="id", limit=limit)
        
    def search(self, query, field="content", limit=None):
        '''
        Searches the index based on the query supplied.
        '''
        directory = lucene.SimpleFSDirectory(lucene.File(self.index_dir))
        searcher = lucene.IndexSearcher(directory, True)  

        query = lucene.QueryParser(lucene.Version.LUCENE_CURRENT, field,
                                   self.analyser).parse(query)
        try:                           
            #if there's no limit then use a collector to retrieve them all
            if limit is None:
                collector = DocumentHitCollector(searcher)
                scoreDocs = searcher.search(query, collector)
                results = collector.get_collected_documents()
            else:
                scoreDocs = searcher.search(query, limit).scoreDocs
                results = []
                for scoreDoc in scoreDocs:
                        results.append(searcher.doc(scoreDoc.doc))
        except lucene.JavaError, e:
                print e
        searcher.close()
        return results
    
    def get_top_terms(self, limit=10):
        '''
        Returns the top keywords, in terms of documents mentioning them
        in the index. 
        '''
        directory = lucene.SimpleFSDirectory(lucene.File(self.index_dir))
        reader = lucene.FilterIndexReader.open(directory, True)
        terms = reader.terms()
        
        term_freqs = []
        while terms.next():
            term = terms.term();
            if term.field() == 'content':
                term_freqs.append( (reader.docFreq(term), term.text()) )
        return sorted(term_freqs, reverse=True)[:limit]
    
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
        
class DocumentHitCollector(lucene.PythonCollector):
    '''
    Overrides the PythonCollector method collect in order 
    to create a list with all the documents appearing in the 
    search results.
    '''
    def __init__(self, searcher):
        lucene.PythonCollector.__init__(self)
        self.documents = []
        self.searcher = searcher

    def collect(self, id, score):
        doc = self.searcher.doc(id)
        self.documents.append(doc);
        
    def get_collected_documents(self):
        return self.documents
    
    def setNextReader(self, reader, base):
        self.base = base
        
    def acceptsDocsOutOfOrder(self):
        return True