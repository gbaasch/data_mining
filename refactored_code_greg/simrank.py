from copy import deepcopy
from time import time, sleep
import os
import sys
import re

# inverse probability of jumping
taxVal = 0.5

# Struct for holding a directed graph.
# Holds links accessible both from the source and destination nodes, to improve traversals
class WeightedDirectedGraph:
	def __init__(self):
		self.forwardEdges = {}		# All edges leading away from a node, as a tuple
		self.backEdges = {}			# All edges leading towards a node, as a tuple
		self.weights = {}			# The weight of an edge, indexed by (fromNode, toNode)
		self.nodeOutWeightsTotal = {}		# The combined weights of all edges leading away from a node

	# Very simple output for debugging
	def __str__(self):
		output = ""
		for key in self.forwardEdges:
			output += str(key) + "->" + str(self.forwardEdges[key]) + ": " + str(weights) + "\n"
		return output

	# Adds an edge and associated nodes
	def add_edge(self, fromNode, toNode, weight):
		# Ensure both nodes are in our node list
		# Add to forward edge list
		try:
			# Check for duplicate edge.
			if toNode in self.forwardEdges[fromNode]:
				# sum weights, then return
				self.weights[(fromNode, toNode)] = self.weights[(fromNode, toNode)] + weight
				self.nodeOutWeightsTotal[fromNode] += weight
				return

			# attempt to add the edge
			prev = self.forwardEdges[fromNode]
			self.forwardEdges[fromNode] = prev + (toNode,)
			self.nodeOutWeightsTotal[fromNode] = self.nodeOutWeightsTotal[fromNode] + weight
		# fromNode is a new node. Add it to our dictionaries
		except KeyError:
			self.forwardEdges[fromNode] = (toNode,)
			self.backEdges[fromNode] = tuple([])
			self.nodeOutWeightsTotal[fromNode] = weight

		# Add to back edge list
		try:
			prev = self.backEdges[toNode]
			self.backEdges[toNode] = prev + (fromNode,)
		# toNode is a new node. Add it to our dictionaries
		except KeyError:
			self.backEdges[toNode] = (fromNode,)
			self.forwardEdges[toNode] = tuple([])
			self.nodeOutWeightsTotal[toNode] = 0
		self.weights[(fromNode, toNode)] = weight
		return

	# Recursively removes all dead ends in this graph
	# Bad worst-case running time, but should perform well except for on graphs deliberately designed to break it.
	# returns list of node ids that have been removed
	def remove_dead_ends(self):
		removed = []
		keys = tuple(self.forwardEdges.keys())
		# Go through entire graph once
		for key in keys:
			try:
				# remove if dead end, and check if this creates new dead ends
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
		self.nodeOutWeightsTotal.pop(key)

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

		# update weights
		weight = self.weights.pop((fromNode, toNode))
		self.nodeOutWeightsTotal[fromNode] = self.nodeOutWeightsTotal[fromNode] - weight
		if weight[fromNode] < 0:
			print("error")
			sleep(0.1)

	# Reads the export data from the wto dataset.
	def build_from_file(self, filename):
		self.__init__()
		with open(filename, 'r') as inFile:
			for line in inFile.readlines():
				split = line.split('","')
				# Ignore lines that don't follow the expected input format
				if len(split) != 14 or split[7] != "Exports":
					continue
				# parse the exporter, the partner, and the value traded
				self.add_edge(split[1], split[3], float(split[10]))


# Takes a ranks dictionary, sorts it into order by rank, and prints it to a .tsv
def print_sim_rank(filename, ranks):
	# Build and sort our list
	printList = []
	for key in ranks.keys():
		printList.append((ranks[key], key))
	printList.sort(reverse=True)

	# Write one page rank and id pair per line
	with open(filename, 'w+') as outfile:
		outfile.write("PageRank\tIds\n")
		for item in printList:
			outfile.write(str(item[0]) + "\t" + str(item[1]) + "\n")
	return printList


# Calculates the page rank for all nodes in a graph
def sim_rank(graphOrig, startNode):
	# Keep a copy
	graph = deepcopy(graphOrig)
	# Remove all dead ends before future processing
	removedNodes = graph.remove_dead_ends()

	# Initialize our values
	ranks = {}
	numKeys = len(graph.forwardEdges.keys())
	for key in graphOrig.forwardEdges.keys():
		ranks[key] = 0
	ranks[startNode] = 1

	# Iterate a certain number of times
	for i in range(10):
		ranks = run_markov(ranks, graph, graphOrig, numKeys, removedNodes, startNode)

	ranks.pop(startNode)
	return ranks


# Runs one pass for calculating our page rankings
def run_markov(ranks, graph, origGraph, numKeys, removed, startNode):
	newRanks = {}

	# Initialize our new ranks for easier traversal later. Also take care of jumping here
	# Note we only initialize those that are not dead-end nodes
	for key in graph.forwardEdges.keys():
		newRanks[key] = 0
	newRanks[startNode] = (1 - taxVal)

	# For each (non-dead-end) node:
	for key in graph.forwardEdges.keys():
		# Get list of places we could get to
		connections = graph.forwardEdges[key]
		# Calculate probability of going to one of these nodes (same probability for each)
		# probability = ranks[key] * taxVal / len(connections)
		# Add this probability to the chance of being at that node after this iteration
		for nodeKey in connections:
			newRanks[nodeKey] = newRanks[nodeKey] + ranks[key] * taxVal *\
								graph.weights[(key, nodeKey)] / graph.nodeOutWeightsTotal[key]

	# Update values for all our dead-end nodes
	rank_dead_ends(ranks, newRanks, origGraph, removed)

	return newRanks


# After a markov iteration, updates all our dead end nodes
def rank_dead_ends(ranks, newRanks, origGraph, removed):
	for node in removed:
		newRank = 0.0
		for key in origGraph.backEdges[node]:
			newRank += ranks[key] * origGraph.weights[(key, node)] / origGraph.nodeOutWeightsTotal[key]
		newRanks[node] = newRank


# Use this when importing to another file
# infile, outfile: paths (relative or absolute)
# startNode: name of entity to use as the primary node for simrank
# returns ordered list of ranks as tuples: (rank, nodeID)
def simrank_runner(infile, startNode, outfile="sim_rank.tsv"):
	graph = WeightedDirectedGraph()
	graph.build_from_file(infile)
	ranks = sim_rank(graph, startNode)
	readableRanks = print_sim_rank(outfile, ranks)
	return readableRanks


# Running simrank from the command line, accepting arguments for filenames
def main_simrank():
	# Parse files if provided
	infile = "..\data\merchandise_values_annual_dataset.csv"
	outfile = "similarity.tsv"
	if len(sys.argv) > 1:
		infile = sys.argv[1]
	else:
		print("defaulting input file")
	# Exit if we can't read our input file
	if not os.path.exists(infile):
		print("Cannot find/read input file. Exiting")
		sys.exit(0)

	if len(sys.argv) > 2:
		outfile = sys.argv[2]
	else:
		print("defaulting output file")

	# Read input file
	graph = WeightedDirectedGraph()
	graph.build_from_file(infile)
	print("number of nodes:", len(graph.forwardEdges))
	print("number of edges:", len(graph.weights))
	print("Done reading file and creating graph")

	# Calculate page rank
	#"United States of America" "Developing Asia"
	ranks = sim_rank(graph, "Japan")
	print(len(ranks))

	# Print results
	print_sim_rank(outfile, ranks)


if __name__ == '__main__':
	main_simrank()
