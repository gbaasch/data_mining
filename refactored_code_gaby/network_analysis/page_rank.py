class PageRank:
    def __init__(self, directional_network, weighted=False, beta=0.8, epochs=10):
        """
        PageRank is used to evaluate the relative importance of a node in a network

        PageRank can be unweighted or weighted, and can use tax or not
        """
        self.network = directional_network
        self.weighted = weighted
        self.epochs = epochs  # the number of iterations the PageRank will run
        self.init_vec = self.create_init_vec()
        self.beta = beta
        # if beta is specified, use taxation
        self.taxation_value = (1 - self.beta) / self.network.num_nodes if self.beta else None

    def create_init_vec(self):
        """
        Create an initial probability vector
        """
        vec = {}
        for node in self.network.out_links:
            vec[node] = 1 / self.network.num_nodes
        return vec

    def get_page_ranks(self):
        """ Get the page ranks for the network """
        # save state of network before removing dead ends
        in_links_with_deadends = self.network.in_links
        out_links_with_deadends = self.network.out_links

        # remove dead ends
        self.network.set_and_remove_dead_ends()

        # iteratively update the probability of being at a certain node
        vec = self.init_vec
        for i in range(self.epochs):
            vec = self.update_probabilities(vec)

        # calculate the PageRank for the dead ends
        dead_ends = self.network.dead_ends.copy()
        while dead_ends:
            dead_end = dead_ends.pop()
            vec[dead_end] = self.sum_probabilities(
                dead_end, vec, in_links_with_deadends, out_links_with_deadends)
        return vec

    def update_probabilities(self, vec):
        """ Update the probability matrix """
        new_vec = {}
        for key, _ in self.network.out_links.items():
            total_sum = self.sum_probabilities(
                key, vec, self.network.in_links, self.network.out_links)
            if self.taxation_value:
                new_vec[key] = self.beta * total_sum + self.taxation_value
            else:
                new_vec[key] = total_sum
        return new_vec

    def sum_probabilities(self, key, previous_vec, in_links, out_links):
        total_sum = 0
        if not in_links.get(key):
            total_sum = 0
        else:
            if self.weighted:
                for link in in_links.get(key):
                    out_links_from_here = out_links.get(link)
                    weight_sum = sum(out_links_from_here.values())
                    weights_indv = out_links_from_here.get(key)
                    weight_sum = 1 if weight_sum == 0 else weight_sum
                    weighted_prob = weights_indv / weight_sum
                    total_sum += (previous_vec[link] * weighted_prob)
            else:
                for link in in_links.get(key):
                    out_degree = len(out_links.get(link))
                    total_sum += (previous_vec[link] / out_degree)
        return total_sum
