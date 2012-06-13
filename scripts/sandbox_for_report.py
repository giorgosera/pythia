# -*- coding: utf-8 -*-

from analysis.text import TextAnalyser
from tools.utils import text_stemming

text_analyser = TextAnalyser()

text = ['egyptians', 'prepare', 'jan25', 'protests', 'mumbarak', 'turned', 'egypt', 'police', 'state', 'torture', 'police', 'brutality', 'r', 'systematic' ]
for word in text:
    print text_stemming(word)
print 