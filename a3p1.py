import re
from copy import deepcopy
import sys
import os

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


def main_a1():
	# Parse files if provided
	infile, outfile = "web-Google_10k.txt", "outfile-deadends.tsv"
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

	# Read file and process results
	graph = read_input(infile)
	print("number of nodes:", len(graph.forwardEdges.keys()))
	removed = graph.remove_dead_ends()
	print("number of nodes removed", len(removed))
	print_deadends(outfile, removed)


# Takes a list of nodes that are dead ends, and prints them to a .tsv, one per line
def print_deadends(filename, removed):
	with open(filename, 'w+') as outfile:
		for id in removed:
			outfile.write(str(id) + "\n")


# Returns a dictionary containing all edges. Keys are the origin node,
# and values are a tuple of the destination of all outgoing edges.
def read_input(filename):
	graph = DirectedGraph()
	with open(filename, 'r') as inFile:
		for line in inFile.readlines():
			m = re.search(r"^(\d+)\t(\d+)$", line.strip())
			# Ignore lines that don't follow the expected input format
			if not m:
				continue
			graph.add_edge(m.group(1), m.group(2))
	return graph


if __name__ == '__main__':
	main_a1()
