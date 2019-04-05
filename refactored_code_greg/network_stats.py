import matplotlib.pyplot as plt
import os

try:
	from simrank import WeightedDirectedGraph
except ModuleNotFoundError:
	from refactored_code_greg.simrank import WeightedDirectedGraph


path = "C:/Workspace/data_mining/output-data"
categoriesNS = [
    'Total merchandise', 'Agricultural products', 'Manufactures',
    'Fuels and mining products', 'Food', 'Clothing', 'Textiles',
    'Office and telecom equipment', 'Chemicals',
    'Machinery and transport equipment', 'Iron and steel',
    'Automotive products', 'Fuels', 'Transport equipment',
    'Telecommunications equipment',
    'Electronic data processing and office equipment', 'Pharmaceuticals',
    'Integrated circuits and electronic components', 'Other food products',
    'Other semi-manufactures', 'Other chemicals', 'Other manufactures',
    'Raw materials', 'Scientific and controlling instruments',
    'Other machinery', 'Ores and other minerals',
    'Personal and household goods', 'Non-ferrous metals',
    'Miscellaneous manufactures', 'Other transport equipment', 'Fish'
]

# Struct for holding a directed graph.
# Holds links accessible both from the source and destination nodes, to improve traversals
class DirectedGraph:
	def __init__(self):
		self.forwardEdges = {}
		self.backEdges = {}

	def __str__(self):
		output = ""
		for key in self.forwardEdges:
			output += str(key) + ": " + str(self.forwardEdges[key]) + "\n"
		return output

	# Adds an edge and associated nodes
	def add_edge(self, fromNode, toNode):
		# Ensure both nodes are in our node list
		# Add to forward edge list
		try:
			# Check for duplicate edge. If so, return
			if toNode in self.forwardEdges[fromNode]:
				return False
			prev = self.forwardEdges[fromNode]
			self.forwardEdges[fromNode] = prev + (toNode,)
		# fromNode is a new node. Add it to our dictionaries
		except KeyError:
			self.forwardEdges[fromNode] = (toNode,)
			self.backEdges[fromNode] = tuple([])
		try:
			prev = self.backEdges[toNode]
			self.backEdges[toNode] = prev + (fromNode,)
		# toNode is a new node. Add it to our dictionaries
		except KeyError:
			self.backEdges[toNode] = (fromNode,)
			self.forwardEdges[toNode] = tuple([])
		return True

	# Recursively removes all dead ends in this graph
	# Bad worst-case running time, but should perform well except for on graphs deliberately
	# designed to break it.
	def remove_dead_ends(self):
		removed = []
		keys = tuple(self.forwardEdges.keys())
		for key in keys:
			try:
				if len(self.forwardEdges[key]) == 0:
					self._remove_dead_ends_recurse(key, removed)
			# Node has already been removed by recursion. Don't worry
			except:
				pass
		return removed

	# INTERNAL METHOD: DO NOT DIRECTLY CALL
	# Removes the designated node, and checks all nodes that previously connected to that node
	def _remove_dead_ends_recurse(self, key, removed):
		removed.append(key)
		# remove each edge that terminated on this node.
		# If this creates new dead ends, recurse on those nodes
		srcNodes = self.backEdges[key]
		for src in srcNodes:
			self.remove_edge(src, key)
			if len(self.forwardEdges[src]) == 0:
				self._remove_dead_ends_recurse(src, removed)
		# remove references to this node once done working with it.
		self.forwardEdges.pop(key)
		self.backEdges.pop(key)

	# Removes an edge from both dictionaries
	def remove_edge(self, fromNode, toNode):
		# remove forward edge
		edges = self.forwardEdges[fromNode]
		# handle if the edge doesn't exist
		if toNode not in edges:
			print("DirectedGraph key error: edge", fromNode, toNode, "to remove doesn't exist")
			return
		edges = list(edges)
		edges.remove(toNode)
		edges = tuple(edges)
		self.forwardEdges[fromNode] = edges

		# remove back edge
		edges = self.backEdges[toNode]
		edges = list(edges)
		edges.remove(fromNode)
		edges = tuple(edges)
		self.backEdges[toNode] = edges

	# Removes a node and all corresponding edges
	def remove_node(self, node):
		if self.nodes.pop(node, None):
			dstNodes = self.forwardEdges[node]
			srcNodes = self.backEdges[node]
			for dst in dstNodes:
				self.remove_edge(node, dst)

			for src in srcNodes:
				self.remove_edge(src, dst)

	def build_from_file(filename):
		with open(filename, 'r') as inFile:
			for line in inFile.readlines():
				split = line.split("\t")
				# Ignore lines that don't follow the expected input format
				if not len(split) == 3:
					continue
				self.add_edge(split[0], split[1])


# -------------------------------------------------------------------


# returns the degree of a provided graph
# input: either a DirectedGraph or a WeightedDirectedGraph
def calc_average_degree(graph):
	totalNodes = len(graph.forwardEdges.keys())
	# catch empty graph
	if totalNodes == 0:
		return 0

	# Calculate average degree
	totalDegree = 0
	for key in graph.forwardEdges.keys():
		totalDegree += len(graph.forwardEdges[key])
	return totalDegree / totalNodes


# Calculates and plots the degree of each country over time
def degree_by_country(inpath="../data/merchandise_values_annual_dataset.csv"):
	startIndex = 1948
	graphs = []
	# build an overall graph, and one for each year
	mainGraph = DirectedGraph()
	for i in range(1948, 2018):
		graphs.append(DirectedGraph())

	# Read the file
	with open(inpath, 'r') as inFile:
		for line in inFile.readlines():
			split = line.split('","')
			# Ignore lines that don't follow the expected input format
			if not len(split) == 14 or not split[7].startswith("Exports"):
				continue

			# Insert edge into both the yearly graph and the main graph
			year = int(split[8])
			graphs[year-startIndex].add_edge(split[1], split[3])
			mainGraph.add_edge(split[1], split[3])

	# Calculate the degree of each country over each year
	countries = mainGraph.forwardEdges.keys()
	years = range(1990, 2017)
	for country in countries:
		annualDegrees = []
		for year in years:
			degree = 0
			if country in graphs[year-startIndex].forwardEdges:
				degree = len(graphs[year-startIndex].forwardEdges[country])
			annualDegrees.append(degree)
		# Add each country's degree to the plot
		plt.plot(years, annualDegrees)

	# Add labels to the plot
	plt.suptitle("Degree by country")
	plt.xlabel("year")
	plt.ylabel("degree")

	# Set axis and display the plot
	plt.axis([2000, 2018, 0, 35])
	plt.show()


# Calculates and plots the average degree of all countries by commodity over time
def degree_by_commodity(inpath="../data/merchandise_values_annual_dataset.csv"):
	# grab data across years. We only have good data since 2000 for commodities
	years = range(2000, 2018)

	# build a graph for each commodity, for each year
	catGraphs = []
	for year in years:
		oneYearGraphs = []
		for cat in categoriesNS:
			oneYearGraphs.append(DirectedGraph())
		catGraphs.append(oneYearGraphs)

	# Read the file
	with open(inpath, 'r') as inFile:
		for line in inFile.readlines():
			split = line.split('","')
			# Ignore lines that don't follow the expected input format
			if not len(split) == 14 or not split[7].startswith("Exports"):
				continue

			year = int(split[8])
			# Skip years out of range
			if year < years[0] or year > years[-1]:
				continue
			# Insert edge into the correct year/commodity graph
			com_index = categoriesNS.index(split[5])
			catGraphs[year - years[0]][com_index].add_edge(split[1], split[3])

	# build a graph for each commodity, for each year
	catDegrees = []
	for j, cat in enumerate(categoriesNS):
		oneCatDegrees = []
		for i, year in enumerate(years):
			oneCatDegrees.append(calc_average_degree(catGraphs[i][j]))
		catDegrees.append(oneCatDegrees)
		plt.plot(years, oneCatDegrees)

	# Add labels to the plot
	plt.suptitle("Average degree by commodity")
	plt.xlabel("year")
	plt.ylabel("degree")

	# Set axis and display the plot
	plt.axis([2000, 2018, 0, 25])
	plt.show()


# Calculates and prints (to console) the relative values of all goods exported by each country
def totals_by_entity(inpath="../data/merchandise_values_annual_dataset.csv"):
	graph = WeightedDirectedGraph()
	total = 0.0

	# build graph, and track total exports recorded
	with open(inpath, 'r') as inFile:
		for line in inFile.readlines():
			split = line.split('","')
			# Ignore lines that don't follow the expected input format
			if not len(split) == 14 or not split[7].startswith("Exports") or int(split[8]) < 2000:
				continue

			graph.add_edge(split[1], split[3], float(split[10]))
			total += float(split[10])

	# Rank countries based on relative exports
	revenue_ranks = []
	for country in graph.forwardEdges.keys():
		revenue_ranks.append((graph.nodeOutWeightsTotal[country] / total, country))

	# Print countries and revenue proportions to console, in order
	revenue_ranks.sort(reverse=True)
	for rank in revenue_ranks:
		print(rank)



if __name__ == '__main__':
	degree_by_country()
	degree_by_commodity()
	totals_by_entity()
