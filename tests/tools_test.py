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
        
if __name__ == "__main__":
    unittest.main()