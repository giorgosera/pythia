'''
Created on 24 Mar 2012

@author: george
'''

from database.warehouse import WarehouseServer
from analysis.clustering.kmeans import OrangeKmeansClusterer
from analysis.clustering.dbscan import DBSCANClusterer
from database.model.tweets import *
from tools.utils import aggregate_data
from matplotlib.dates import num2date#!@UnresolvedImport
from visualizations.graphs import D3Timeline
from analysis.clustering.algorithms import cosine
from datetime import timedelta    

def rate_clusters(oc):
    clusters = []
    for cluster in oc.clusters:
        documents = cluster.get_documents().values()
        if len(documents) == 0 : continue
        dates = [doc.date for doc in documents]
        delta = max(dates) - min(dates)
        delta_seconds = delta.total_seconds()
        if delta_seconds == 0: delta_seconds = 0.01
        #if delta_seconds == 0: continue
        rate_growth = float(len(dates))/delta_seconds
        date = min(dates)

        #=======================================================================
        # while date in [c[1] for c in clusters]:
        #    date += timedelta(minutes=1)
        #=======================================================================
        clusters.append( (rate_growth, date, cluster) )
    return clusters

print '--------------------------------------'
print '--> Retrieving tweets...'
ws = WarehouseServer()
#items = [doc for doc in ws.get_all_documents(type=EvaluationTweet)]
from_date = datetime.datetime(2011, 1, 25, 0, 0, 0)
to_date = datetime.datetime(2011, 1, 27, 0, 0, 0) 
items = ws.get_documents_by_date(from_date, to_date, type=EgyptTweet)
size= len(items)

i=0
window=1500
top_clusters=[]
while i < size:
    print '-->Clustering batch',i,"/",size
    #oc = OrangeKmeansClusterer(k=200, ngram=1, distance=cosine)
    oc = DBSCANClusterer(epsilon=0.65, min_pts=5, distance=cosine)
    copy = list(items) #deep copy
    documents = copy[i:i+window]
    dates = [doc.date for doc in documents]
    print max(dates), min(dates)
    oc.add_documents(documents)
    print '--> Running clustering...'
    oc.run(pca=False)
    oc.dump_clusters_to_file("synthetic"+str(i))
    print '--> Identifying events...'
    clusters = rate_clusters(oc)
    #get the N top events
    N = int(len(clusters)*0.05) #take the top 5 percent clusters
    clusters = sorted(clusters, key=lambda x: -x[0])[:N]
    top_clusters += clusters
    i += window
   
print len(top_clusters)
print '--> Generating summaries...'
meta = []
top_clusters = sorted(top_clusters, key=lambda x: x[1])
for i, cluster in enumerate(top_clusters):
    print '----> Analysing cluster:', i+1, 'of', len(top_clusters)
    cluster_struct = cluster[2]
    cluster_struct.analyse()
    summary = cluster_struct.summarize()[:5]
    summ_docs = []
    for doc in summary:
        if len(doc.raw) > 50:
            doc.raw = doc.raw[:50] + '\n' + doc.raw[51:]
            
        summ_docs.append(doc.raw)
    docs =  list(summ_docs)
    
    locations = cluster_struct.get_locations()
    persons = cluster_struct.get_persons()
    meta.append({"title":"event"+str(i), 
                 "date":cluster[1].strftime('%Y-%m-%d %H:%M:%S'), 
                 "keywords":cluster_struct.get_most_frequent_terms(N=9),
                 "authors": len(cluster_struct.get_authors()),
                 "tweets": len(cluster_struct.document_dict.items()),
                 "locations": locations if len(locations) != 0 else [("No location detected.",0)] ,
                 "namedEntities": persons if len(persons) != 0 else [("No named entities detected.",0)],
                 "topTweets": docs})
  
print '--> Preparing timeline...'


# final_dates = []
# final_counts = []
# for cluster in top_clusters:
#    final_dates.append(cluster[1])
#    final_counts.append(len(cluster[2].document_dict.items()))
# 
# final_dates = [[date.strftime('%Y-%m-%d %H:%M:%S') for date in final_dates]]
# final_counts = [[float(count) for count in final_counts]]
#===============================================================================

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
print '--> Plotting timeline...'
t.plot(url='timeline_hackathon.html')
print '--> Done! Go to http://localhost:8000/templates/timeline_hackathon.html to see the result. First start the server by navigating to visualizations and running \'python -m SimpleHTTPServer\' '