# -*- coding: utf-8 -*-
'''
Created on 13 Nov 2011

@author: george

Unit tests for the utils.tools package.
'''
import unittest, tools.utils

class TestToolsFunctions(unittest.TestCase):
    
    def test_strip_hashtags(self):
        text = "RT : RT : As #Egyptians prepare for #jan25 protests: #Mubarak has been president for 29 yrs, Emergency Law for every 1 of those yrs."
        calculated1 = tools.utils.strip_hashtags(text)
        text = "This # George <-- should be removed."
        calculated2 = tools.utils.strip_hashtags(text)
        text = "#jan25"
        calculated3 = tools.utils.strip_hashtags(text)
        expected1 = "RT : RT : As prepare for protests: has been president for 29 yrs, Emergency Law for every 1 of those yrs."
        expected2 = "This <-- should be removed."
        expected3 = ""        

        self.assertEqual(calculated1, expected1)
        self.assertEqual(calculated2, expected2)
        self.assertEqual(calculated3, expected3)
        
    def test_is_a_retweet_method(self):
        tweet_with_RT = "RT @monaeltahawy: RT @Gheblawi Beyond belief: religious history &amp; make-up of #Egypt interesting discussion #Copts http://www.bbc.co.uk/podcasts/series/belief"
        tweet_with_VIA= "Breaking News - Messi spotted outside the Etihad #transferdeadlineday http://twitpic.com/8dwcum (via @AndrewBloch )"
        not_a_retweet = "This is not a retweet #test"
        tweet_with_almost_RT = "RT Beyond belief: religious history &amp; make-up of #Egypt interesting discussion #Copts http://www.bbc.co.uk/podcasts/series/belief"
        result1 = tools.utils.is_a_retweet(tweet_with_RT)
        result2 = tools.utils.is_a_retweet(tweet_with_VIA)
        result3 = tools.utils.is_a_retweet(not_a_retweet)
        result4 = tools.utils.is_a_retweet(tweet_with_almost_RT)
        
        self.assertEqual(True, result1)
        self.assertEqual(True, result2)
        self.assertEqual(False, result3)
        self.assertEqual(False, result4)
        
    def test_translation(self):
        text = "تسجيل صوتي ل د.محمد البلتاجي يعلن مشاركة الاخوان بشكل رسمي في 25يناير http://www.palsharing.com/y5brwm1nrdio.html #Jan25"
        translated = tools.utils.translate_text(text)
        expected = 'Audio recording of Dr. Mohammed Al announces the participation of brothers officially in January 25, http://www.palsharing.com/y5brwm1nrdio.html # Jan25'
        self.assertEquals(expected, translated)
        text = 'Io sono Giorgos'
        translated = tools.utils.translate_text(text)
        self.assertEquals("I'm Giorgos", translated)
        
        
    def test_strip_url(self):
        text1 = 'Check out http://www.djamesuk.co.uk for the latest mixtape downloads and updates!'
        text2 = 'Check out www.djamesuk.co.uk for the latest mixtape downloads and updates!'
        text3 = 'http://www.djamesuk.co.uk Check out for the latest mixtape downloads and updates!'
        text4 = 'www.djamesuk.co.uk Check out for the latest mixtape downloads and updates!'
        text5 = 'Check out for the latest mixtape downloads and updates! www.djamesuk.co.uk'
        result1 =  tools.utils.strip_url(text1)
        result2 =  tools.utils.strip_url(text2)
        result3 = tools.utils.strip_url(text3)
        result4 = tools.utils.strip_url(text4)
        result5 = tools.utils.strip_url(text5)        
        expected = 'Check out for the latest mixtape downloads and updates!'
        
        self.assertEqual(expected, result1)
        self.assertEqual(expected, result2)
        self.assertEqual(expected, result3)
        self.assertEqual(expected, result4)
        self.assertEqual(expected, result5)
        
    def test_random(self):
        text = 'RT @S_Elhussieny: + 1 # egypt # elbaradei RT @ ZeinabSamir: @ shmpOngO if taken by Criss ElBaradei hamil revolution revolution'
        print tools.utils.strip_mentions(text)
        
    def test_encoding(self):
        text = 'RT @S_Elhussieny: + 1 # egypt # elbaradei RT @ ZeinabSamir: @ shmpOngO if taken by Criss ElBaradei hamil revolution revolution'
        
if __name__ == "__main__":
    unittest.main()