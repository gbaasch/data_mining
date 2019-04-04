import os
import pandas as pd

from refactored_code_gaby.network_analysis.directed_network import DirectedNetwork
from refactored_code_gaby.network_analysis.undirected_network import UndirectedNetwork
from refactored_code_gaby.network_analysis.page_rank import PageRank

"""
Run this file to see the link analysis code working in practice with a test network.
"""

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))  # This is your Project Root
DIRECTED_FILE_PATH = os.path.join(ROOT_DIR, 'test_directed_network.csv')
UNDIRECTED_FILE_PATH = os.path.join(ROOT_DIR, 'test_undirected_network.csv')


if __name__ == '__main__':
    # create directed network
    print("\nDirected Network ==========================")
    df = pd.read_csv(DIRECTED_FILE_PATH)
    network = DirectedNetwork(df)
    print("Created Directed Network with in_links:", network.in_links)
    print("Created Directed Network with out_links:", network.out_links)
    # find deadends
    network.set_and_remove_dead_ends()
    print("Found dead ends:", network.dead_ends)
    # find unweighted page rank
    pr_unweighted = PageRank(network)
    page_ranks = pr_unweighted.get_page_ranks()
    print("Calculated unweighted page rank:", page_ranks)
    # find weighted page rank
    pr_weighted = PageRank(network, weighted=True, beta=None, epochs=1)
    page_ranks = pr_weighted.get_page_ranks()
    print("Calculated unweighted page rank with no taxation and one epoch:", page_ranks)

    # create undirected network
    print("\nUnirected Network ==========================")
    df = pd.read_csv(UNDIRECTED_FILE_PATH)
    network = UndirectedNetwork(df)
    print("Created Undirected Network with edges:", network.neighbours)
    num_triangles = network.count_triangles()
    num_triangles_expected = network.count_triangles_expected()
    print("Number of expected triangles: {}, Number of actual triangles: {}".format(
        num_triangles_expected, num_triangles))
