'''
Created on 13 Nov 2011

@author: george

Unit tests for the analysis package.
'''
import unittest
from analysis.text import TextAnalyser

class TestTextAnalyserFunctions(unittest.TestCase):
    
    def test_tokenization(self):
        doc1_raw = 'frequent FrEquEnt frequent <li>word</li> word sentence sentence' 
        doc2_raw = 'sentence <a href="www.google.com">arab</a> spring'
        doc3_raw = 'a is not a toKENIzed document'               
        
        doc1_tokens = ['frequent', 'frequent', 'frequent', 'word', 'word', 'sentence', 'sentence'] 
        doc2_tokens = ['sentence', 'arab', 'spring'] 
        doc3_tokens = ['a', 'is', 'not', 'a', 'tokenized', 'document']
        
        freq1 = {'frequent': 3, 'sentence': 2, 'word':2}
        freq2 = {'arab': 1, 'sentence': 1, 'spring':1}
        freq3 = {'a': 2, 'document': 1, 'is':1, 'not': 1, 'tokenized':1}
        
        
        entry1 = {"id": 1, "raw": doc1_raw, "tokens":doc1_tokens, "word_frequencies":freq1}
        entry2 = {"id": 2, "raw": doc2_raw, "tokens":doc2_tokens, "word_frequencies":freq2}
        entry3 = {"id": 3, "raw": doc3_raw, "tokens":doc3_tokens, "word_frequencies":freq3}
        
        global_freqs_expected = {'a': 1, 'tokenized': 1, 'word': 1, 'sentence': 2, 'spring': 1, 'is': 1, 'arab': 1, 'not': 1, 'document': 1, 'frequent': 1}
        
        expected = [entry1, entry2, entry3]
        
        sample_docs = [doc1_raw, doc2_raw, doc3_raw]

        analyser = TextAnalyser()
        i = 1
        for s in sample_docs:
            analyser.add_document(i, s)
            i += 1
                 
        self.assertEqual(expected, analyser.get_documents())
        self.assertEqual(global_freqs_expected, analyser.get_global_token_frequencies())
        
        analyser.save_frequency_matrix("test.txt")
        analyser.read_frequency_matrix("test.txt")
        
if __name__ == "__main__":
    unittest.main()