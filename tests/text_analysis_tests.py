# -*- coding: utf-8 -*-
'''
Created on 13 Nov 2011

@author: george

Unit tests for the analysis package.
'''
import unittest, tools.utils
from analysis.text import TextAnalyser

class TestTextAnalyserFunctions(unittest.TestCase):
    
    def test_tokenization(self):
        doc1_raw = 'frequent FrEquEnt frequent <li>word</li> word sentence sentence' 
        doc2_raw = 'sentence <a href="www.google.com">arab</a> spring'
        doc3_raw = 'a is not a toKENIzed document'               
        
        doc1_tokens = ['frequent', 'frequent', 'frequent', 'word', 'word', 'sentenc', 'sentenc']
        doc2_tokens = ['sentenc', 'arab', 'spring']
        doc3_tokens = ['token', 'document']
        
        freq1 = [('frequent', 3), ('sentenc', 2), ('word', 2)]
        freq2 = [('arab', 1), ('sentenc', 1), ('spring', 1)]
        freq3 = [('document', 1), ('token', 1)]
        
        
        entry1 = {"raw": doc1_raw, "tokens":doc1_tokens, "word_frequencies":freq1}
        entry2 = {"raw": doc2_raw, "tokens":doc2_tokens, "word_frequencies":freq2}
        entry3 = {"raw": doc3_raw, "tokens":doc3_tokens, "word_frequencies":freq3}
        
        global_freqs_expected = {'word': 1, 'sentenc': 2, 'arab': 1, 'token': 1, 'spring': 1, 'document': 1, 'frequent': 1}
        
        expected = {'1': entry1, '2': entry2, '3': entry3}
        
        sample_docs = [doc1_raw, doc2_raw, doc3_raw]

        analyser = TextAnalyser()
        i = 1
        for s in sample_docs:
            analyser.add_document(i, s)
            i += 1
        
        self.assertEqual(expected, analyser.get_documents())
        self.assertEqual(global_freqs_expected, analyser.get_global_token_frequencies())
        
    def test_unicode_doc_translation(self):
        document = 'هذا اختبار' 
        analyser = TextAnalyser()
        id, document = analyser.add_document(1, document)
        
        expected = "This is a test"
        
        self.assertEqual(expected, document["raw"])
        
    def test_text_preprocessing(self):
        text = "This is a sample text. # ! . "
        analyser = TextAnalyser()
        processed = analyser._preprocess(text)
        expected = ('This is a sample text. # ! . ', ['sampl', 'text.'], [('sampl', 1), ('text.', 1)])
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