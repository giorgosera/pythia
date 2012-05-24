'''
Created on 24 Mar 2012

@author: george
'''

import datetime, unittest 
from database.warehouse import WarehouseServer
from analysis.clustering.kmeans import OrangeKmeansClusterer
from tools.utils import aggregate_data
from matplotlib.dates import num2date#!@UnresolvedImport
from visualizations.graphs import D3Timeline


ws = WarehouseServer()
from_date = datetime.datetime(2011, 1, 26, 0, 0, 0)
to_date = datetime.datetime(2011, 1, 27, 0, 0, 0) 
items = ws.get_documents_by_date(from_date, to_date, limit=3000)

oc = OrangeKmeansClusterer(k=100, ngram=1)
oc.add_documents(items)
oc.run("orange_clustering_test", pca=False)

top_clusters = []
for cluster in oc.clusters:
    documents = cluster.get_documents().values()
    if len(documents) == 0 : continue
    dates = [doc.date for doc in documents]
    delta = max(dates) - min(dates)
    delta_seconds = delta.total_seconds()
    if delta_seconds == 0: continue
    rate_growth = float(len(dates))/delta_seconds
    top_clusters.append( (rate_growth, max(dates), cluster) )
    
top_clusters = sorted(top_clusters, key=lambda x: -x[0])[:20]

meta = []
top_clusters = sorted(top_clusters, key=lambda x: x[1])
for i, cluster in enumerate(top_clusters):
    cluster_struct = cluster[2]
    cluster_struct.analyse()
    summary = cluster_struct.summarize()[:5]
    summ_docs = []
    for doc in summary:
        if len(doc.raw) > 50:
            doc.raw = doc.raw[:50] + '\n' + doc.raw[51:]
            
        summ_docs.append(doc.raw)
    docs =  list(set(summ_docs))
    print len(docs)
    meta.append({"title":"event"+str(i), 
                 "date":cluster[1].strftime('%Y-%m-%d %H:%M:%S'), 
                 "keywords":cluster_struct.get_most_frequent_terms(N=9),
                 "authors": len(cluster_struct.get_authors()),
                 "locations": cluster_struct.get_locations(),
                 "namedEntities": cluster_struct.get_persons(),
                 "topTweets": docs})

data = [[doc.date for doc in items]]

dates = []
counts = []
for d in data:
    t_dates, t_counts = aggregate_data(d, cumulative=False)
    dates.append([num2date(date).strftime('%Y-%m-%d %H:%M:%S') for date in t_dates])
    counts.append(t_counts)
   
final_dates = dates
final_counts = [count.tolist() for count in counts]

t = D3Timeline(final_dates, final_counts, meta=meta, cumulative=False)
t.plot(url='timeline_hackathon.html')
