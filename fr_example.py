import networkx as nx 
import numpy as np
import random

random.seed(10)
G = nx.watts_strogatz_graph(20,5,0.05)
initial_pos = { n : np.random.uniform(size=(2,))  for n in G.nodes}
# nx.draw(G, pos=initial_pos)

## Simulate iterations
P = [nx.spring_layout(G, pos=initial_pos, iterations=i, scale=None, seed=10) for i in range(15)]

import matplotlib.pyplot as plt
fig = plt.figure(figsize=(12,4))
for i in range(15):
	plt.subplot(3, 5, i+1)
	nx.draw(G, pos=P[i], node_size=15, node_color="red")
plt.show()
