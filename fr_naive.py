#!/usr/bin/env python

import networkx as nx
import matplotlib.pyplot as plt
import math
from random import random
from numpy import arange



# attractive force
def f_a(d,k):
		return d*d/k

# repulsive force
def f_r(d,k):
		return k*k/d

def fruchterman_reingold(G,iteration=50):
		W = 1
		L = 1
		area = W*L
		k = math.sqrt(area/nx.number_of_nodes(G))

		# initial position
		for v in nx.nodes(G):
				G.nodes[v]['x'] = W*random()
				G.nodes[v]['y'] = L*random()


		t = W/10
		dt = t/(iteration+1)

		for i in range(iteration):
				# print("iter {0}".format(i))

				pos = {}
				for v in G.nodes():
						pos[v] = [G.nodes[v]['x'],G.nodes[v]['y']]

				# calculate repulsive forces
				for v in G.nodes():
						G.nodes[v]['dx'] = 0
						G.nodes[v]['dy'] = 0
						for u in G.nodes():
								if v != u:
										dx = G.nodes[v]['x'] - G.nodes[u]['x']
										dy = G.nodes[v]['y'] - G.nodes[u]['y']
										delta = math.sqrt(dx*dx+dy*dy)
										if delta != 0:
												d = f_r(delta,k)/delta
												G.nodes[v]['dx'] += dx*d
												G.nodes[v]['dy'] += dy*d

				# calculate attractive forces
				for v,u in G.edges():
						dx = G.nodes[v]['x'] - G.nodes[u]['x']
						dy = G.nodes[v]['y'] - G.nodes[u]['y']
						delta = math.sqrt(dx*dx+dy*dy)
						if delta != 0:
								d = f_a(delta,k)/delta
								ddx = dx*d
								ddy = dy*d
								G.nodes[v]['dx'] += -ddx
								G.nodes[u]['dx'] += +ddx
								G.nodes[v]['dy'] += -ddy
								G.nodes[u]['dy'] += +ddy

				# limit the maximum displacement to the temperature t
				# and then prevent from being displace outside frame
				cnt = 0
				for v in G.nodes():
						dx = G.nodes[v]['dx']
						dy = G.nodes[v]['dy']
						disp = math.sqrt(dx*dx+dy*dy)
						if disp != 0:
								cnt += 1
								d = min(disp,t)/disp
								x = G.nodes[v]['x'] + dx*d
								y = G.nodes[v]['y'] + dy*d
								x =  min(W,max(0,x)) - W/2
								y =  min(L,max(0,y)) - L/2
								G.nodes[v]['x'] = min(math.sqrt(W*W/4-y*y),max(-math.sqrt(W*W/4-y*y),x)) + W/2
								G.nodes[v]['y'] = min(math.sqrt(L*L/4-x*x),max(-math.sqrt(L*L/4-x*x),y)) + L/2

				# cooling
				t -= dt

		pos = {}
		for v in G.nodes():
				pos[v] = [G.nodes[v]['x'],G.nodes[v]['y']]
		return pos