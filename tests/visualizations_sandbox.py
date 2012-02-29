# -*- coding: utf-8 -*-
'''
Created on 23 Jan 2012

@author: george

My playground!
'''
import unittest
from visualizations.graphs import Timeline  
from database.warehouse import WarehouseServer
from database.model.tweets import EgyptTweet

import os
import sys
import webbrowser
import json
import datetime 
from string import Template

ws = WarehouseServer()

class TestPlayground(unittest.TestCase):
    
    #===========================================================================
    # def test_matpotlib_timeline(self):
    #    items = [item.date for item in ws.get_all_documents(type=EgyptTweet)]
    #    t = Timeline(items)
    #    t.plot()
    #    t.show()
    #===========================================================================
        
    def test_d3_timeline(self):
        items = [item.date for item in ws.get_all_documents(type=EgyptTweet)]
        json_data = {'items': items}
        dthandler = lambda obj: obj.isoformat() if isinstance(obj, datetime.datetime) else None
        template = '../visualizations/templates/timeline.html'
        
        html = Template(open(template).read())
        html = html.substitute(items=json.dumps(json_data, default=dthandler))
        f = open(os.path.join(os.getcwd(), '../visualizations/templates', os.path.basename(template)), 'w')
        f.write(html)
        f.close()

        print >> sys.stderr, 'Data file written to: %s' % f.name
        webbrowser.open('localhost:8888/' + f.name)
        
if __name__ == "__main__":
    unittest.main()