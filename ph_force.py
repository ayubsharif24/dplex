import numpy as np
import networkx as nx
from bokeh.plotting import figure, show, output_notebook
from bokeh.layouts import column
from bokeh.models import Slider, ColumnDataSource, CustomJS



## TODO: 
# 1. Calculate MST, determine two subsets each edge connects 
# 2. Given a drawn layout, filter opacity of nodes/edges based on persistence 
# 3. Draw bars of persistence 
# 4. Do regular F-R layout w/ Bokeh 


X = np.random.uniform(size=(25, 2))

def EMST(X):
	''' Calculates the Euclidean minimum spanning tree of points 'X' ''' 
	import networkx as nx
	from scipy.spatial.distance import pdist
	from itertools import combinations
	G, W = nx.Graph(), pdist(X)
	G.add_weighted_edges_from(
		(i,j,W[c]) for (c, (i,j)) in enumerate(combinations(range(X.shape[0]), 2))
	)
	return(G, nx.minimum_spanning_tree(G))

G, emst = EMST(X)

nx.draw(G, pos = X)

def components_cut(g, threshold):
	from networkx.utils import UnionFind
	assert 'weight' in g.edges[next(iter(g.edges))].keys()
	uf = UnionFind(g.nodes)
	for (u,v,a) in g.edges(data=True):
		if a['weight'] <= threshold:
			uf.union(u,v)
	return(list(uf.to_sets()))

def subgraph_cut(g, threshold):
	from networkx.utils import UnionFind
	assert 'weight' in g.edges[next(iter(g.edges))].keys()
	G = nx.Graph()
	G.add_nodes_from(g.nodes)
	G.add_weighted_edges_from((u,v,a['weight']) for (u, v, a) in g.edges(data=True) if a['weight'] <= threshold)
	return(G)

nx.draw(subgraph_cut(G, 0.40), pos = X)








