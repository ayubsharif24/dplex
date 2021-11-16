import numpy as np
from networkx.utils import np_random_state

def _process_params(G, center):
	if not isinstance(G, nx.Graph):
		empty_graph = nx.Graph()
		empty_graph.add_nodes_from(G)
		G = empty_graph
	center = np.zeros(2) if center is None else np.asarray(center)
	return G, center

def spring_layout(
	G,
	k=None,
	pos=None,
	fixed=None,
	iterations=50,
	threshold=1e-4,
	weight="weight",
	scale=1,
	center=None,
):
	"""Position nodes using Fruchterman-Reingold force-directed algorithm.
	The algorithm simulates a force-directed representation of the network
	treating edges as springs holding nodes close, while treating nodes
	as repelling objects, sometimes called an anti-gravity force.
	Simulation continues until the positions are close to an equilibrium.
	There are some hard-coded values: minimal distance between
	nodes (0.01) and "temperature" of 0.1 to ensure nodes don't fly away.
	During the simulation, `k` helps determine the distance between nodes,
	though `scale` and `center` determine the size and place after
	rescaling occurs at the end of the simulation.
	Fixing some nodes doesn't allow them to move in the simulation.
	It also turns off the rescaling feature at the simulation's end.
	In addition, setting `scale` to `None` turns off rescaling.
	Parameters
	----------
	G : NetworkX graph or list of nodes
			A position will be assigned to every node in G.
	k : float (default=None)
			Optimal distance between nodes.  If None the distance is set to
			1/sqrt(n) where n is the number of nodes.  Increase this value
			to move nodes farther apart.
	pos : dict or None  optional (default=None)
			Initial positions for nodes as a dictionary with node as keys
			and values as a coordinate list or tuple.  If None, then use
			random initial positions.
	fixed : list or None  optional (default=None)
			Nodes to keep fixed at initial position.
			Nodes not in ``G.nodes`` are ignored.
			ValueError raised if `fixed` specified and `pos` not.
	iterations : int  optional (default=50)
			Maximum number of iterations taken
	threshold: float optional (default = 1e-4)
			Threshold for relative error in node position changes.
			The iteration stops if the error is below this threshold.
	weight : string or None   optional (default='weight')
			The edge attribute that holds the numerical value used for
			the edge weight.  Larger means a stronger attractive force.
			If None, then all edge weights are 1.
	scale : number or None (default: 1)
			Scale factor for positions. Not used unless `fixed is None`.
			If scale is None, no rescaling is performed.
	center : array-like or None
			Coordinate pair around which to center the layout.
			Not used unless `fixed is None`.
	Returns
	-------
	pos : dict
			A dictionary of positions keyed by node
	Examples
	--------
	>>> G = nx.path_graph(4)
	>>> pos = nx.spring_layout(G)
	# The same using longer but equivalent function name
	>>> pos = nx.fruchterman_reingold_layout(G)
	"""
	G, center = _process_params(G, center)

	if fixed is not None:
		if pos is None:
			raise ValueError("nodes are fixed without positions given")
		for node in fixed:
			if node not in pos:
				raise ValueError("nodes are fixed without positions given")
		nfixed = {node: i for i, node in enumerate(G)}
		fixed = np.asarray([nfixed[node] for node in fixed if node in nfixed])

	if pos is not None:
		# Determine size of existing domain to adjust initial positions
		dom_size = max(coord for pos_tup in pos.values() for coord in pos_tup)
		if dom_size == 0:
			dom_size = 1
		pos_arr = seed.rand(len(G), 2) * dom_size + center

		for i, n in enumerate(G):
			if n in pos:
				pos_arr[i] = np.asarray(pos[n])
	else:
		pos_arr = None
		dom_size = 1

	if len(G) == 0:
		return {}
	if len(G) == 1:
		return {nx.utils.arbitrary_element(G.nodes()): center}

	A = nx.to_numpy_array(G, weight=weight) # adjacency matrix, weighted if edges have 'weight' attribute
	if k is None and fixed is not None:
		# We must adjust k by domain size for layouts not near 1x1
		nnodes, _ = A.shape
		k = dom_size / np.sqrt(nnodes)
	pos = _fruchterman_reingold(
		A, k, pos_arr, fixed, iterations, threshold, 2, 4
	)
	if fixed is None and scale is not None:
		pos = rescale_layout(pos, scale=scale) + center
	pos = dict(zip(G, pos))
	return pos

def rescale_layout(pos, scale=1):
	"""Returns scaled position array to (-scale, scale) in all axes.
	The function acts on NumPy arrays which hold position information.
	Each position is one row of the array. The dimension of the space
	equals the number of columns. Each coordinate in one column.
	To rescale, the mean (center) is subtracted from each axis separately.
	Then all values are scaled so that the largest magnitude value
	from all axes equals `scale` (thus, the aspect ratio is preserved).
	The resulting NumPy Array is returned (order of rows unchanged).
	Parameters
	----------
	pos : numpy array
			positions to be scaled. Each row is a position.
	scale : number (default: 1)
			The size of the resulting extent in all directions.
	Returns
	-------
	pos : numpy array
			scaled positions. Each row is a position.
	See Also
	--------
	rescale_layout_dict
	"""
	# Find max length over all dimensions
	lim = 0  # max coordinate for all axes
	for i in range(pos.shape[1]):
		pos[:, i] -= pos[:, i].mean()
		lim = max(abs(pos[:, i]).max(), lim)
	# rescale to (-scale, scale) in all directions, preserves aspect
	if lim > 0:
		for i in range(pos.shape[1]):
			pos[:,i] *= scale / lim
	return pos

# Position nodes in adjacency matrix A using Fruchterman-Reingold
# Entry point for NetworkX graph is fruchterman_reingold_layout()
@np_random_state(7)
def _fruchterman_reingold(
  A, k=None, pos=None, fixed=None, iterations=50, threshold=1e-4, dim=2, seed=None
):
	assert isinstance(A, np.ndarray), "fruchterman_reingold() takes an adjacency matrix as input"
	nnodes, _ = A.shape

	# random initial positions; make sure positions are of same type as matrix
	pos = np.asarray(seed.rand(nnodes, dim), dtype=A.dtype) if pos is None else pos.astype(A.dtype)

	# optimal distance between nodes
	if k is None:
		k = np.sqrt(1.0 / nnodes)
	# the initial "temperature"  is about .1 of domain area (=1x1) <=> the largest step allowed in the dynamics.
	# This is needed in case the fixed positions force our domain to be much bigger than 1x1
	t = max(max(pos.T[0]) - min(pos.T[0]), max(pos.T[1]) - min(pos.T[1])) * 0.1
	# simple cooling scheme.
	# linearly step down by dt on each iteration so last iteration is size dt.
	dt = t / float(iterations + 1)
	delta = np.zeros((pos.shape[0], pos.shape[0], pos.shape[1]), dtype=A.dtype)

	for iteration in range(iterations):
		# matrix of difference between points
		delta = pos[:, np.newaxis, :] - pos[np.newaxis, :, :]
		# distance between points
		distance = np.linalg.norm(delta, axis=-1)
		# enforce minimum distance of 0.01
		np.clip(distance, 0.01, None, out=distance)
		# displacement "force"
		displacement = np.einsum(
			"ijk,ij->ik", delta, (k * k / distance ** 2 - A * distance / k)
		)
		# update positions
		length = np.linalg.norm(displacement, axis=-1)
		length = np.where(length < 0.01, 0.1, length)
		delta_pos = np.einsum("ij,i->ij", displacement, t / length)
		if fixed is not None:
			# don't change positions of fixed nodes
			delta_pos[fixed] = 0.0
		pos += delta_pos
		# cool temperature
		t -= dt
		err = np.linalg.norm(delta_pos) / nnodes
		if err < threshold:
			break
	return pos


class ForceLayout():
	def __init__(self, graph, k = None, pos = None, fixed = None):
		assert isinstance(graph, nx.classes.graph.Graph)
		self.graph = graph
		self.nv = graph.number_of_nodes()
		self.fixed = fixed

		## Adjacency matrix, positions, and difference, preallocated
		self._A = nx.to_numpy_array(self.graph, weight='weight') # adjacency matrix
		self._pos = np.asarray(np.random.uniform(size=(self.nv, 2)), dtype=self._A.dtype) if pos is None else pos.astype(self._A.dtype)
		self._delta = np.zeros((self.nv, self.nv, 2), dtype=self._A.dtype)

		# # optimal distance between nodes
		self.k = np.sqrt(1.0 / self.nv) if k is None else k
		
		# the initial "temperature"  is about .1 of domain area (=1x1) <=> the largest step allowed in the dynamics.
		# This is needed in case the fixed positions force our domain to be much bigger than 1x1
		self.temp = max(max(self._pos.T[0]) - min(self._pos.T[0]), max(self._pos.T[1]) - min(self._pos.T[1])) * 0.1

		# Linear cooling scheme -- decrease temp by dt on each iteration so last iteration is size dt.
		self.dt = self.temp / float(51)

		# Informational
		self.error = np.inf
		
	def step_force(self, n_iter: int = 1):
		for iteration in range(n_iter):
			# matrix of difference between points
			delta = self._pos[:, np.newaxis, :] - self._pos[np.newaxis, :, :]

			# distance between points
			distance = np.linalg.norm(delta, axis=-1)
			np.clip(distance, 0.01, None, out=distance) # enforce minimum distance of 0.01
			
			# displacement "force"
			displacement = np.einsum(
				"ijk,ij->ik", delta, (self.k * self.k / distance ** 2 - self._A * distance / self.k)
			)

			# update positions
			length = np.linalg.norm(displacement, axis=-1)
			length = np.where(length < 0.01, 0.1, length)
			delta_pos = np.einsum("ij,i->ij", displacement, self.temp / length)
			if self.fixed is not None:
				delta_pos[self.fixed] = 0.0 # don't change positions of fixed nodes
			self._pos += delta_pos

			# cool temperature
			self.temp -= self.dt
			self.error = np.linalg.norm(delta_pos) / self.nv

