# -*- coding: utf-8 -*-
'''
Created on 23 Jan 2012

@author: george

My playground!
'''

import unittest, random
from mygengo import MyGengo #!@UnresolvedImport
import Orange, orange, numpy #!@UnresolvedImport

gengo = MyGengo(
    public_key = 'Br1#utdXkjX}w4SX92Vk(UOfQ05^mRkQgPRZ9e(A035(KvUdFQ9|_bdXMO|7(35m',
    private_key = 'kut$VBhbClg#]@WE]Jhmiz2^QqeRz$^Ydx3W~XNO|#6BvnCvWz73Bywa$c4FjFvZ',
    sandbox = False, # possibly False, depending on your dev needs
)

class TestPlayground(unittest.TestCase):
    
    #===========================================================================
    # def testtranslate(self):
    #    translation = gengo.postTranslationJob(job = {
    #        'type': 'text', # REQUIRED. Type to translate, you'll probably always put 'text' here (for now ;)
    #        'slug': 'Translating Chinese to English with the myGengo API', # REQUIRED. For storing on the myGengo side
    #        'body_src': '我們今天要去那裏嗎', # REQUIRED. The text you're translating. ;P
    #        'lc_src': 'zh', # REQUIRED. source_language_code (see getServiceLanguages() for a list of codes)  
    #        'lc_tgt': 'en', # REQUIRED. target_language_code (see getServiceLanguages() for a list of codes)
    #        'tier': 'machine', # REQUIRED. tier type ("machine", "standard", "pro", or "ultra")
    #    })
    #    
    #    # This will print out a machine translation; for your human translation, you can
    #    # poll and check often, or set up a URL for it to post the results to.
    #    print translation['response']['job']['body_tgt']
        
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
        
if __name__ == "__main__":
    unittest.main()




