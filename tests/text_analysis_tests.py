# -*- coding: utf-8 -*-
'''
Created on 13 Nov 2011

@author: george

Unit tests for the analysis package.
'''
import unittest, tools.utils
from analysis.text import TextAnalyser
from tests.test_document import get_test_documents, get_unicode_document

class TestTextAnalyserFunctions(unittest.TestCase):
    
    def test_tokenization(self):
        expected, sample_docs, objects = get_test_documents()
        calculated = {}
        analyser = TextAnalyser()
        id=0
        for s in sample_docs:
            d = analyser.add_document(s)
            calculated[str(id)] = d
            id+=1
            
        self.assertEqual(expected, calculated)
        
    def test_unicode_doc_translation(self):
        expected, document = get_unicode_document()
        analyser = TextAnalyser()
        document = analyser.add_document(document)
        self.assertEqual(expected, document["raw"])
        
    def test_text_preprocessing(self):
        text = "This is a sample text. # ! . "
        analyser = TextAnalyser()
        processed = analyser._preprocess(text)
        expected = ('This is a sample text. # ! . ', ['sampl', 'text'], [('sampl', 1), ('text', 1)])
        self.assertEqual(expected, processed)
        
    def test_tfidf(self):
        token_occurences = 2 
        no_of_tokens = 10
        no_of_docs = 10
        token_appears_in = 3
        result = tools.utils.tfidf(token_occurences, no_of_tokens, no_of_docs, token_appears_in)
        self.assertAlmostEqual(0.24079, result, 4)

        
        
if __name__ == "__main__":
    unittest.main()