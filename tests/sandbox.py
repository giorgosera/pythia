# -*- coding: utf-8 -*-
'''
Created on 23 Jan 2012

@author: george

My playground!
'''
import unittest
import Orange, orange, numpy, bingtrans #!@UnresolvedImport
import chardet, nltk #!@UnresolvedImport
from mygengo import MyGengo #!@UnresolvedImport
from calais import Calais #!@UnresolvedImport
import HTMLParser, tools.utils

gengo = MyGengo(
    public_key = 'Br1#utdXkjX}w4SX92Vk(UOfQ05^mRkQgPRZ9e(A035(KvUdFQ9|_bdXMO|7(35m',
    private_key = 'kut$VBhbClg#]@WE]Jhmiz2^QqeRz$^Ydx3W~XNO|#6BvnCvWz73Bywa$c4FjFvZ',
    sandbox = False, # possibly False, depending on your dev needs
)

class TestPlayground(unittest.TestCase):
    
    def testGengoTranslate(self):
        translation = gengo.postTranslationJob(job = {
          'type': 'text', # REQUIRED. Type to translate, you'll probably always put 'text' here (for now ;)
          'slug': 'Translating Chinese to English with the myGengo API', # REQUIRED. For storing on the myGengo side
          'body_src': '我們今天要去那裏嗎', # REQUIRED. The text you're translating. ;P
          'lc_src': 'zh', # REQUIRED. source_language_code (see getServiceLanguages() for a list of codes)  
          'lc_tgt': 'en', # REQUIRED. target_language_code (see getServiceLanguages() for a list of codes)
          'tier': 'machine', # REQUIRED. tier type ("machine", "standard", "pro", or "ultra")
          })
        print translation['response']['job']['body_tgt']
        
    def testBingTranslate(self):   
        bingtrans.set_app_id('5521E4A630094D968D49B39B6511A0A76CB025E1')  # you can get your AppID at: http://www.bing.com/developers/
        result = bingtrans.translate("هذا هو الاختبار", 'ar', 'en') 
        self.assertEqual("This is a test", result)            
        
    def testOrangeTableCreation(self):
        x = Orange.data.variable.Continuous("word1")
        y = Orange.data.variable.Continuous("word2")
        z = Orange.data.variable.Continuous("word3")
        domain = Orange.data.Domain([x, y, z], False)

        #Data
        data = numpy.array([[1, 2, 3], [3, 2, 1]])
        t = Orange.data.Table(domain, data)
        
        #Meta
        tweet_id = Orange.data.variable.String("id")
        id = Orange.data.new_meta_id()
        t.add_meta_attribute(id)
        t.domain.add_meta(id, tweet_id)
        for inst in t:
            inst[id] = "hello_id"
             
        orange.saveTabDelimited ("test_table_creation.tab", t)
        
    def test_lang_detection(self):
        text_ar = "هذا هو الاختبار"
        text_en = "Hello" 
        encoding = chardet.detect(text_en)
        if encoding['encoding'] == 'ascii':
            result = 'string is in ascii'
        
        self.assertEqual('string is in ascii', result)
        
    def test_nltk_named_entity_extraction(self):
        text = "George is a student. He studies the events that took place in Cairo, Egypt."
        sentences = nltk.sent_tokenize(text)         
        sentences = [nltk.word_tokenize(sent) for sent in sentences]
        sentences = [nltk.pos_tag(sent) for sent in sentences]
        print nltk.ne_chunk(sentences[1])
        
    def test_calais_named_entity_extraction(self):
        text = "George Eracleous is a student. He studies the events that took place in Cairo, Egypt."
        API_KEY = "av536xwvy4mgmcbw9cancqmd"
        calais = Calais(API_KEY, submitter="python-calais demo")
        result = calais.analyze(text)
        print result.print_entities()
        
    def test_text_unquoting(self):
        result = HTMLParser.HTMLParser().unescape("@ReemAbdellatif We&#39;ve been so inspired by #Tunisia, it&#39;s intoxicating to think we&#39;ll witness something similar in #Egypt")
        expected = "@ReemAbdellatif We've been so inspired by #Tunisia, it's intoxicating to think we'll witness something similar in #Egypt"
        self.assertEqual(expected, result)
        
    def test_stemming(self):
        stem = tools.utils.text_stemming("factionally")
        self.assertEqual("faction", stem)
        
    def test_english_detection(self):
        english_text = "This"
        non_english_text = "Αυτό"
        must_be_true = tools.utils.detect_english(english_text)
        must_be_false = tools.utils.detect_english(non_english_text)
        self.assertEqual(True, must_be_true)
        self.assertEqual(False, must_be_false)
        
if __name__ == "__main__":
    unittest.main()




