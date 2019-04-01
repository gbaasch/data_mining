from data_mining import similarity_measures
from data_mining.itemsets.similar_items.mini_hash import MiniHashTable


class FindSimilarItems:
    """
    Given many sets, find which ones are similar above a certain threshold

    For large n use mini hash to speed up the runtime
    """
    def __init__(self, similarity_threshold=0.6, use_mini_hash=False, similarity_measure='jaccard'):
        self.similarity_threshold = similarity_threshold
        self.similarity_measure = similarity_measure
        self.use_mini_hash = use_mini_hash

    def find_similar_items(self, itemsets):
        """ Find the similarities of the provided itemsets """
        if not self.use_mini_hash:
            # find itemsets without mini hashing
            return self._find_similar_items_slow(itemsets)
        else:
            # find itemsets with mini hashing
            return self._find_similar_items_fast(itemsets)

    def _compute_similarity(self, itemset_1, itemset_2):
        """ Choose which similarity function to used based on the value passed on initialization """
        if self.similarity_measure == 'jaccard':
            return similarity_measures.jaccard_similarity(itemset_1, itemset_2)
        else:
            raise ValueError(self.similarity_measure + 'is not a valid similarity measure')

    def _find_similar_items_slow(self, itemsets):
        """ Find similarities just using a for loop. This will be slow for large n but is more simple """
        itemsets = itemsets.itemsets
        similar_items = {}
        for item_1, itemset_1 in itemsets.items():
            for item_2, itemset_2 in itemsets.items():
                # only compute similarity if it is not the same item
                if not item_1 == item_2:
                    sim = self._compute_similarity(itemset_1, itemset_2)
                    if sim >= self.similarity_threshold:
                        # TODO order items to prevent repeats
                        similar_items[(item_1, item_2)] = sim
        return similar_items

    def _find_similar_items_fast(self, itemsets, r=6, b=14):
        """ Find similarities with mini hashing. This will be much faster for large n """
        itemsets = itemsets.itemsets
        set_len = len(itemsets)

        # Create b mini hash tables of size r
        mini_hash_tables = []
        for _ in range(b):
            mini_hash = MiniHashTable(set_len, r)
            for item, itemset in itemsets.items():
                mini_hash[itemset] = item
            mini_hash_tables.append(mini_hash)

        # Create candidate pairs
        candidate_pairs = []
        for i in range(b):
            hash_table = mini_hash_tables[i]
            for data in hash_table.data:
                if len(data) > 1:
                    candidate_pairs.append(data)

            # Compute the Jaccard similarity on the candidate pairs to remove false positives
            similar_items = {}
            for pair in candidate_pairs:
                # for each combo in the candidate pairs
                for i in range(len(pair)):
                    for j in range(len(pair)):
                        # do not compare a questions with itself
                        if not i == j:
                            item_1 = pair[i]
                            item_2 = pair[j]
                            itemset_1 = itemsets.get(item_1)
                            itemset_2 = itemsets.get(item_2)
                            sim = self.compute_similarity(self.similarity_measure, itemset_1, itemset_2)
                            if sim >= self.similarity_threshold:
                                # TODO order items to prevent repeats
                                similar_items[(item_1, item_2)] = sim
            return similar_items
