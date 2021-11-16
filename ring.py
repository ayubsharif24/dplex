
from bokeh.plotting import figure, show, output_notebook
from bokeh.layouts import column
from bokeh.models import Slider, ColumnDataSource, CustomJS

# https://docs.bokeh.org/en/latest/docs/user_guide/plotting.html#userguide-plotting-wedges-arcs
output_notebook()

import numpy as np

normalize = lambda x: (x - np.min(x))/(np.max(x) - np.min(x))
theta = np.random.uniform(size=101, low=0.0, high=2*np.pi)
theta = normalize(np.cumsum(theta / (2*np.pi)))*2*np.pi

inner_r = np.random.uniform(size=100, low=0.30, high=0.45)
outer_r = np.random.uniform(size=100, low=0.45, high=0.60)

from tallem.color import bin_color, linear_gradient, colors_to_hex
col_pal = linear_gradient(["blue", "red"], 15)['hex']
wedge_col = bin_color(outer_r, col_pal)


wedges = []

ring_plot = figure(width=400, height=400)
for i in range(len(inner_r)):
	wedge = ring_plot.annular_wedge(
		x=0, y=0, 
		inner_radius=inner_r[i], outer_radius=outer_r[i],
		start_angle=theta[i], end_angle=theta[i+1], color=wedge_col[i], alpha=0.50
	)
	g = wedge.glyph
	g.line_color = "blue"
	g.line_width = 0.5
	wedges.append(wedge)

# wedge.update(inner_radius=)

slider = Slider(start=1.0, end=3.0, step=0.05, value=1.0)
for w in wedges:
	slider.js_link('value', w.glyph, 'outer_radius')
show(column(p, slider))

from bokeh.layouts import gridplot

import networkx as nx
from bokeh.plotting import figure, from_networkx
G = nx.karate_club_graph()
network_plot = figure(title="Networkx Integration Demonstration", x_range=(-1.1,1.1), y_range=(-1.1,1.1),tools="", toolbar_location=None)
graph = from_networkx(G, nx.spring_layout, scale=2, center=(0,0))
network_plot.renderers.append(graph)

show(gridplot([[ring_plot, network_plot]]))

# %% Try streaming mode


# normalize = lambda x: (x - np.min(x))/(np.max(x) - np.min(x))
# theta = np.random.uniform(size=101, low=0.0, high=2*np.pi)
# theta = normalize(np.cumsum(theta / (2*np.pi)))*2*np.pi

# inner_r = np.random.uniform(size=100, low=0.30, high=0.45)
# outer_r = np.random.uniform(size=100, low=0.45, high=0.60)
import numpy as np
from bokeh.models import ColumnDataSource
source = ColumnDataSource(data=dict(x=x, y=y))


data = {'x_values': [1, 2, 3, 4, 5],
        'y_values': [6, 7, 2, 3, 6]}

source = ColumnDataSource(data=data)


def update():

    # update some items in the "typical" CDS column
    s = slice(100)
    new_x = source.data['x'][s] + np.random.uniform(-0.1, 0.1, size=100)
    new_y = source.data['y'][s] + np.random.uniform(-0.2, 0.2, size=100)
    source.patch({ 'x' : [(s, new_x)], 'y' : [(s, new_y)] })

    # update a single point of the 1d multi-line data
    i = np.random.randint(200)
    new_y = source1d.data['ys'][0][i] + (0.2 * np.random.random()-0.1)
    source1d.patch({ 'ys' : [([0, i], [new_y])]})

    # update five rows of the 2d image data at a time
    s1, s2 = slice(50, 151, 20), slice(None)
    index = [0, s1, s2]
    new_data = np.roll(source2d.data['img'][0][s1, s2], 2, axis=1).flatten()
    source2d.patch({ 'img' : [(index, new_data)] })

curdoc().add_periodic_callback(update, 50)

curdoc().add_root(gridplot([[p, p1d, p2d]]))

## TODO: use fastAPI for a simple and efficient REST w/o resolving to Node 
# from typing import Optional
# from fastapi import FastAPI
# app = FastAPI()

# @app.get("/")
# def read_root():
# 	return {"Hello": "World"}

# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Optional[str] = None):
# 	return {"item_id": item_id, "q": q}


