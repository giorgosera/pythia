'''
Created on 28 Nov 2011

@author: george
'''
import AlchemyAPI#!@UnresolvedImport
from lxml import etree#!@UnresolvedImport
from StringIO import StringIO

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
    
    def parse_result(self, result, type):
        '''
        Parses the result returned from Alchemy and constructs
        and dict.
        '''
        context = etree.iterparse(StringIO(result))
        object_dict = {}
        objects = []
        for action, elem in context:
            if not elem.text:
                text = "None"
            else:
                text = elem.text
            object_dict[elem.tag] = text
            if elem.tag == type:
                objects.append(object_dict)
                object_dict = {}
        return objects
        
    
    def analyse_text(self, text):
        raise NotImplementedError('run is not implemented.')
    
class TwitterSemanticAnalyser(AbstractSemanticAnalyser):
    '''
    Deals with Twitter related semantic analysis. 
    '''    
    
    def analyse_text(self, text):
        entities = self.extract_entities(text)
    
    def extract_entities(self, text):
        '''
        Extracts the main entities in this text.
        '''
        result = self.alchemy.TextGetRankedNamedEntities(text)     
        entities = self.parse_result(result, "entity")
        return entities 
    
    def extract_sentiment(self, text):
        '''
        Extracts the sentiment of this text.
        '''
        result = self.alchemy.TextGetTextSentiment(text);  
        sentiment = self.parse_result(result, "docSentiment") 
        return sentiment