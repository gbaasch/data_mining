import os
import pandas as pd

from data_mining.itemsets.itemsets import Itemsets
from data_mining.itemsets.frequent_items.find_frequent_items import FindFrequentItems
from data_mining.itemsets.similar_items.find_similar_items import FindSimilarItems

"""
Run this file to see the link analysis code working in practice with a test network.
"""

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))  # This is your Project Root
FILE_PATH = os.path.join(ROOT_DIR, 'test_itemsets.csv')


if __name__ == '__main__':
    print("\nFind Similar Items ==========================")
    # create itemsets
    df = pd.read_csv(FILE_PATH)
    itemsets = Itemsets(df)
    print("Created item sets:", itemsets.itemsets)
    # find similar items without minihash
    threshold = 0.6
    find_similar = FindSimilarItems(use_mini_hash=False, similarity_threshold=threshold)
    similar_items = find_similar.find_similar_items(itemsets)
    print("Found similar itemsets with threshold {}: {}".format(threshold, similar_items))
    # TODO mini hash class has a bug right now. Fix.
    # find similar items with minihash
    # find_similar = FindSimilarItems(use_mini_hash=True)
    # similar_items = find_similar.find_similar_items(itemsets)
    # print("Found similar itemsets:", similar_items)

    print("\nFind Frequent Items ==========================")
    support_threshold = 3
    max_frequent_set_size = 3
    # Find frequent items
    find_frequent = FindFrequentItems(itemsets, support_threshold, max_frequent_set_size)
    print("Frequent supports with support threshold {} and max set size {}".format(
        support_threshold, 3
    ))
    for m in range(max_frequent_set_size):
        print(m+1, find_frequent.frequent_supports_for_setsizes.get(m+1))
    # Find association rules
    association_rules = find_frequent.find_association_rules(2)
    print("Found association rules:", association_rules)
