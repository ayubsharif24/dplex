import os 
import networkx as nx
import timeit

G = nx.binomial_tree(8)
# G = nx.watts_strogatz_graph(100,8,0.15)
print(G)

## Write to file 
nx.write_gml(G, "input_graph.gml")
# os.system(r"/Users/mpiekenbrock/dplex/build/ogdf_layout")

## benchmark 
ogdf_fmm = timeit.timeit(lambda: os.system(r"/Users/mpiekenbrock/dplex/build/ogdf_layout"), number = 5)
print(ogdf_fmm/5)

## benchmark
fr_python = timeit.timeit(lambda: fruchterman_reingold(G, iteration=50), number = 1)
print(fr_python/1)


# nx.read_gml("output-energybased-graph-layout.gml")

pos2 = fruchterman_reingold(G, iteration=50)
nx.draw(G, pos=pos2, node_size=50)



# def fr_layout(file):
# 	G = nx.read_gml(file)
# 	return(nx.spring_layout(G))

# ## Test 
# nx_fr = timeit.timeit(lambda: fr_layout("build/input_graph.gml"), number = 5)