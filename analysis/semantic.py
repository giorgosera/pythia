'''
Created on 28 Nov 2011

@author: george
'''
import AlchemyAPI#!@UnresolvedImport
import tools.utils

class AbstractSemanticAnalyser(object):
    '''
    This an abstract class for semantic analysis classes. 
    '''

    def __init__(self):
        '''
        Constructs a social analyser. Dataset is a dict
        object which is the result of the text analyser
        processing.
        '''
        alchemyObj = AlchemyAPI.AlchemyAPI()
        alchemyObj.setAPIKey("d7605e69dd3d2d7a032f11272d9b000e77d43545");
        self.alchemy = alchemyObj
        self.language = None       
    
    def analyse_text(self, text):
        raise NotImplementedError('run is not implemented.')
    
class TwitterSemanticAnalyser(AbstractSemanticAnalyser):
    '''
    Deals with Twitter related semantic analysis. 
    '''    
    
    def analyse_text(self, text):
        entities = self.extract_entities(text)
        sentiment = self.extract_sentiment(text)
        keywords = self.extract_keywords(text)
        return entities, sentiment, keywords
    
    def extract_entities(self, text):
        '''
        Extracts the main entities in this text.
        '''
        result = self.alchemy.TextGetRankedNamedEntities(text)     
        entities = tools.utils.parse_result(result, "entity")
        return entities 
    
    def extract_sentiment(self, text):
        '''
        Extracts the sentiment of this text.
        '''
        result = self.alchemy.TextGetTextSentiment(text);  
        sentiment = tools.utils.parse_result(result, "docSentiment") 
        return sentiment
    
    def extract_keywords(self, text):
        '''
        Extracts important keywords in this text.
        '''
        result = self.alchemy.TextGetRankedKeywords(text);  
        keywords = tools.utils.parse_result(result, "keyword")         
        return keywords
