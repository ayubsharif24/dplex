from typing import * 
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
from bokeh.models import AjaxDataSource, CustomJS
from bokeh.plotting import figure, show

app = FastAPI()

origins = ["*"] 
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


x = list(np.arange(0, 6, 0.1))
y = list(np.sin(x) + np.random.random(len(x)))

@app.get("/")
def read_root():
	return {"Hello": "World"}


# from fastapi.encoders import jsonable_encoder
# @app.get('/data')
# async def data():
# 	x.append(x[-1]+0.1)
# 	y.append(np.sin(x[-1])+np.random.random())
# 	return jsonable_encoder({'x': x, 'y': y})

from fastapi.encoders import jsonable_encoder
@app.post('/data')
async def data():
	x = list(np.arange(0, 6, 0.1)+np.random.uniform(size=60, high=0.10))
	y = list(np.sin(x)+np.random.uniform(size=60, high=0.10))
	return jsonable_encoder({'x': x, 'y': y})
	#return jsonify(points=list(zip(x,y)))


adapter = CustomJS(code="""
	const result = {x: [], y: []}
	const points = cb_data.response
	console.log(points)
	console.log(cb_data)
	result.x = points["x"]
	result.y = points["y"]
	return cb_data.response
""")

source = AjaxDataSource(
	data_url='http://localhost:8001/data',
	polling_interval=2000, 
	adapter=adapter,
	method='POST'
)

p = figure(height=300, width=800, background_fill_color="white",
           title="Streaming Noisy sin(x) via Ajax", 
					 output_backend="webgl")
#p.circle(x, y, radius = 0.10)
p.circle('x', 'y', source=source)
# p.x_range.follow = "end"
# p.x_range.follow_interval = 10


show(p)

# if __name__ == "__main__":
# 	import uvicorn
# 	uvicorn.run(app,host="localhost",port=8001)
# app.run(port=5050)