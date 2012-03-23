'''
Created on 22 Jan 2012

@author: george
'''
from database.model.agents import TrainingAuthor
from crawlers.CrawlerFactory import CrawlerFactory

f = CrawlerFactory()
crawler = f.get_crawler("scrapy")

crawler.setup(user_type=TrainingAuthor)
crawler.crawl(store=True)