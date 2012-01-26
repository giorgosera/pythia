'''
Created on 13 Nov 2011

@author: george

This module performs text analysis of the feeds
'''

import tools.utils, numpy, HTMLParser
import Orange, orange, nltk #!@UnresolvedImport
from application.boot import PythiaApp

class TextAnalyser(object):
    '''
    This class contains and implements all the methods responsible for 
    text analysis.
    '''
    def __init__(self, only_english = False):
        self.document_list = []
        self.frequency_matrix_data = None
        self.only_english = only_english
        
        #Keeps the number of times a word appears in all the docs in the corpus
        #For example if the word 'hello' appears in three documents then token_list['hello']= 3
        self.token_list = {}
        
        self.app = PythiaApp()
        self.ignorewords = set(['(' , ')', '<', '>', '#', '@', '?', '!', '.', ',', '=', '|', '&', ':', '+', '\'', '\'ve','\'m' ])
        
    def _tokenize(self, document):
        '''
        Distinguishes the tokens of a document. Strips out HTML,
        split alphanumreric and then turns the text to lowercase.
        It's supposed to be a private method.
        '''     
        clean_text = nltk.clean_html(document)
        clean_text = tools.utils.strip_url(clean_text)
        tokens = nltk.word_tokenize(clean_text)
        tokens = tools.utils.turn_lowercase(tokens)
        return tokens
    
    def _preprocess(self, text):
        '''
        It preprocess the input text by checking for encoding and also
        tokenizes the text. Finally it creates the word frequency vector.
        '''
        text = HTMLParser.HTMLParser().unescape(text)
        encoding = tools.utils.detect_encoding(text)
        if encoding == 'unicode':
            text = tools.utils.translate_text(text)
            
        tokens = self._tokenize(text)
        tokens = self._filter_tokens(tokens)
        tokens = [tools.utils.text_stemming(token) for token in tokens]
        word_frequencies = nltk.FreqDist(tokens).items()
        return text, tokens, word_frequencies
    
    
    def add_document(self, id, document):
        '''
        Inserts a new document in the list of documents. Note that it 
        deals with unicode strings which are automatically translated to 
        English.
        '''
        text, tokens, word_frequencies = self._preprocess(document)
        self.document_list.append({"id": id, "raw": text, "tokens": tokens, "word_frequencies": word_frequencies})
        #Update global frequncies count
        for token, count in word_frequencies:
            self.token_list.setdefault(token, 0)
            if count > 0:
                self.token_list[token] += 1
        
    def get_documents(self):
        return self.document_list   
    
    def get_document_by_id(self, id):
        result = None
        for document in self.document_list:
            if str(document["id"]) == id:
                result = document
        
        if result:
            return result 
        else:    
            raise Exception()       
        
    def get_global_token_frequencies(self):
        return self.token_list    
    
    def _filter_tokens(self, tokens):
        filtered = []
        for token in tokens:
            not_stop_word = token not in nltk.corpus.stopwords.words('english')
            not_ignore_word = token not in self.ignorewords
            ascii = tools.utils.detect_encoding(token) == "ascii"
            if not_stop_word and not_ignore_word and ascii:
                filtered.append(token)
        return filtered   

    def _filter_token_list(self, lower=0.1, higher=0.5, ignorewords=True):
        '''
        Filters tokens which appear either too often (i.e the, a) or very rarely (i.e flim flam).
        The lower and higher percentages indicate the tolerance. Also filters out common ignorewords.
        '''
        dict = {}
        filtered = []
        for token in self.token_list:
            fraction = float(self.token_list[token])/len(self.document_list)
            if fraction > lower and fraction < higher:
                filtered.append(token)
        return filtered        
    
    def save_frequency_matrix(self, filename):
        '''
        Creates a file containing a matrix of word counts and documents
        i.e
        
        ########################################################################
        #            "hello" | "this" | "is" | "a" | "word" | "count" | "matrix"
        # George        1    |  0     |   5  |  6  |    1   |   6     |   6
        # Chuck         3    |  1     |   3  |  3  |    0   |   0     |   4
        # .....................................................................
        #########################################################################  
        '''
        out = file(filename, 'w')
        out.write("Frequency matrix")
        token_list = self._filter_token_list(lower=0.0, higher=1.0)
        for token in token_list:
            out.write('\t%s' % token)
        out.write('\n')
        for i, document in enumerate(self.document_list):
            out.write(str(document["id"]))
            tf = document["word_frequencies"]
            for token in token_list:
                if token in tf:
                    out.write('\t%d' % tf[token])
                else:
                    out.write('\t0')
            out.write('\n')
            
    def save_frequency_matrix_as_tab(self, filename):
        '''
        It stores the frequency matrix as a tab delimited file
        which is supported by Orange. 
        '''
        token_list = self._filter_token_list(lower=0.0, higher=1.0)
        
        #First construct the domain object (top row)
        vars = []
        for token in token_list:
            if token == "&amp;":print 'un'
            vars.append(Orange.data.variable.Continuous(str(token)))
        domain = Orange.data.Domain(vars, False) #The second argument indicated that the last attr must not be a class
        
        #Add data rows 
        data = numpy.empty([len(self.document_list), len(token_list)])
        for i, document in enumerate(self.document_list):
            tokens = document["word_frequencies"]
            new_frequencies_row = numpy.zeros([1, len(token_list)])
            for j, token in enumerate(token_list):
                if token in tokens:
                    tfidf = tools.utils.tfidf(tokens[token], len(tokens), len(self.document_list), self.token_list[token])
                    print i, token, tfidf
                    new_frequencies_row[0][j] = tfidf#tokens[token]
            data[i] = new_frequencies_row    
        #Construct the table with the domain and the data
        t = Orange.data.Table(domain, data)
        
        #Add meta attributes to the samples i.e. the id of the document
        doc_id = Orange.data.variable.String("id")
        id = Orange.data.new_meta_id()
        t.add_meta_attribute(id)
        t.domain.add_meta(id, doc_id)
        for i, inst in enumerate(t):
            inst[id] = str(self.document_list[i]["id"])
             
        orange.saveTabDelimited (filename+".tab", t)
                    
    
    def read_frequency_matrix(self, filename): 
        '''
        Reads the frequency matrix from a file and returns the row names, col names
        and the actual frequencies. 
        '''
        lines=[line for line in file(filename)]
        
        colnames=lines[0].strip().split('\t')[1:]
        rownames=[]
        data=[]
        for line in lines[1:]:
            p=line.strip().split('\t')
            rownames.append(p[0])
            data.append([float(x) for x in p[1:]])
        self.frequency_matrix_data = data    
        return rownames,colnames,data

    def rotate_frequency_matrix(self):
        '''
        It rotates the frequency matrix. This is useful when we perfrom column clustering.
        '''
        #First we have to read the data using read_frequency_matrix(filename)
        if self.frequency_matrix_data:
            rotated = []
            data = self.frequency_matrix_data
            for i in range(len(data[0])):
                newrow = [data[j][i] for j in range(len(data))]
                rotated.append(newrow)
            return rotated    
        else:
            raise Exception("Oops, no data to rotate. Maybe you didn't call read_frequency_matrix(filename)")
  
#    def retweets_patterns(self):
#        '''
#        A regular expression is used to identify retweets. Note that 
#        Twitter identifies retweets either with "RT" followed by username
#        or "via" followed by username. 
#        It returns a list of dictionaries containing the origin and the user 
#        who retweeted.
#        
#        #TODO: Refactor regex generation to the tools package
#        '''
#        rt_patterns = re.compile(r"(RT|via)((?:\b\W*@\w+)+)", re.IGNORECASE)
#        rt_origins = []
#        for t in self.tweets:
#            rt_origins += rt_patterns.findall(t)
#              
#        return rt_origins
