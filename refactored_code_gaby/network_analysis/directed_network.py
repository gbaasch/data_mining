class DirectedNetwork:
    def __init__(self, df):
        """
        This class represents a directional network with nodes and directional weighted edges.
        It is created from a dataframe with columns from_node, to_node, weight.

        If the network is not weighetd set all weights to 1.

        Useful analysis of this network includes PageRank and some network properties
        """
        self.dead_ends = []
        self.in_links = {}  # for each node, list all nodes that point to it
        self.out_links = {}  # for each node, list all nodes it points to
        self.set_in_out_links(df)
        self.num_nodes = len(self.out_links)
        self.num_edges = len(df)

    def set_in_out_links(self, df):
        """
        Create dictionaries that represent the nodes and their associated edges
        """
        for _, row in df.iterrows():
            self.insert_link_in_dict(
                row[1], row[0], row[2], self.in_links)
            self.insert_link_in_dict(
                row[0], row[1], row[2], self.out_links)

    def set_and_remove_dead_ends(self):
        """
        A dead end is a node with in links but no out links, or a node that points only to another dead end.
        This function finds the dead ends and recursively removes them from the network.
        """
        # set dead ends
        for key in self.in_links:
            if not self.out_links.get(key):
                self.dead_ends.append(key)

        # recursively remove dead ends
        for dead_end in self.dead_ends:
            if self.in_links.get(dead_end):
                links_leaving_dead_end = self.in_links.pop(dead_end)
                for link in links_leaving_dead_end:
                    out_links_to_remove = self.out_links.get(link)
                    out_links_to_remove.pop(dead_end)
                    if not out_links_to_remove:
                        self.out_links.pop(link)
                        # add newly found dead ends to the list
                        self.dead_ends.append(link)


    @staticmethod
    def insert_link_in_dict(key, value, weight, dict):
        """
        Insert values into a dictionary. The key is a node and the value will be a dictionary of weighted edges
        """
        if key not in dict:
            weight_dict = {}
        else:
            weight_dict = dict[key]
        weight_dict[value] = float(weight)
        dict[key] = weight_dict
