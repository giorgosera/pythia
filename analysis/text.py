'''
Created on 13 Nov 2011

@author: george

This module performs text analysis of the feeds
'''

import tools.utils, HTMLParser
import nltk #!@UnresolvedImport
from application.boot import PythiaApp

class TextAnalyser(object):
    '''
    This class contains and implements all the methods responsible for 
    text analysis.
    '''
    def __init__(self, ngram=1):
        self.ngram = ngram
        self.app = PythiaApp()
        self.ignorewords = set(['rt', 'jan25', 'egypt', 'cairo', '25jan', "s", \
                                '(' , ')', '<', '>', '#', '@', '?', '!', '.', ',', '=', '|', \
                                '&', ':', '+', '\'', '\'ve',"m", 're', '-', '"', '."', '...', '..', '--', '[', ']' ])
        
    def _tokenize(self, document):
        '''
        Distinguishes the tokens of a document. Strips out HTML,
        split alphanumreric and then turns the text to lowercase.
        It's supposed to be a private method.
        '''     
        clean_text = nltk.clean_html(document)
        clean_text = tools.utils.strip_url(clean_text)
        clean_text = tools.utils.strip_mentions(clean_text)
        clean_text = tools.utils.strip_hashtags(clean_text)
                
        if self.ngram == 1:
            tokens = nltk.WordPunctTokenizer().tokenize(clean_text)#nltk.word_tokenize(clean_text)
            tokens = tools.utils.turn_lowercase(tokens)
            tokens = self._filter_tokens(tokens)
        else:
            tokens = nltk.WordPunctTokenizer().tokenize(clean_text)
            lower_tokens = tools.utils.turn_lowercase(tokens)
            filtered_tokens = self._filter_tokens(lower_tokens)
            text = nltk.Text(filtered_tokens)
            if self.ngram == 2:
                finder = nltk.BigramCollocationFinder.from_words(text)
                scorer = nltk.metrics.BigramAssocMeasures.jaccard   
            elif self.ngram == 3:
                finder = nltk.TrigramCollocationFinder.from_words(text)
                scorer = nltk.metrics.TrigramAssocMeasures.jaccard
            collocations = finder.nbest(scorer, 5)
            tokens = [' '.join(str(i) for i in collocation) for collocation in collocations]
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
        #tokens = self._filter_tokens(tokens)
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
        new_document= {"raw": text, "tokens": tokens, "word_frequencies": word_frequencies}
                
        return id, new_document
        
    def _filter_tokens(self, tokens):
        filtered = []
        for token in tokens:
            not_stop_word = token not in nltk.corpus.stopwords.words('english')
            not_ignore_word = token not in self.ignorewords
            ascii = tools.utils.detect_encoding(token) == "ascii"
            not_single_char = len(token) > 1 
            if not_stop_word and not_ignore_word and ascii and not_single_char:
                filtered.append(token)
        return filtered         
  
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
