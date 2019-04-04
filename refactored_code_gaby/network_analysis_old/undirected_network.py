class UndirectedNetwork:
    def __init__(self, df):
        """
        Create an undirected network of nodes and edges from a data frame
        Each row in the dataframe is an edge and each column is a node

        TODO: Implement more network properties from
            http://infolab.stanford.edu/~ullman/mmds/ch10.pdf
        """
        self.neighbours = {}
        self.edges = []
        self.set_neighbours(df)
        self.edge_count = len(df)
        self.node_count = len(self.neighbours)

    def set_neighbours(self, df):
        """ Create a dict where each key is a node and each value is the node's neighbours
        note: neighbours of a node are all the other nodes that are connected by edges to this node
        """
        for _, row in df.iterrows():
            self.insert_neighbour_in_dict(row[0], row[1])
            self.insert_neighbour_in_dict(row[1], row[0])
            self.edges.append((row[0], row[1]))

    def insert_neighbour_in_dict(self, node_1, node_2):
        """Insert an item into a dict where the value of the dict is a set"""
        if node_1 == node_2:
            return
        neighbour_list = self.neighbours.get(node_1)
        if neighbour_list:
            neighbour_list.add(node_2)
        else:
            neighbour_list = {node_2}
        self.neighbours[node_1] = neighbour_list

    def count_triangles(self):
        """ Count the number of triangles in a graph """
        num_triangles = 0
        for node_1, node_2 in self.edges:
            if node_1 == node_2:
                # do not count edge if it points to itself
                continue
            u = self.neighbours.get(node_1)
            v = self.neighbours.get(node_2)
            num_triangles += len(u & v)
        # divide by 3 because each triangle will appear once for each of its 3 edges
        return num_triangles / 3

    def count_triangles_expected(self):
        """ Calculated the expected number of triangles, according to laws of probability
        If there are more triangles than expected, the network is non random
        """
        return (4 / 3) * ((self.edge_count / self.node_count) ** 3)
