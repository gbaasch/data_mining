from itertools import combinations


class FindFrequentItems:
    """
    Finding frequent items or sets of frequent items can help reveal hidden relationships in the data
    """
    def __init__(self, itemsets, support_threshold, max_frequent_set_size=1):
        """
        max_frequent_set_size specifies what set size to count support for.
        for example, a single item, pairs, triplets etc.

        """
        itemsets = itemsets.itemsets
        self.max_frequent_set_size = max_frequent_set_size
        self.support_threshold = support_threshold
        self.num_items = len(itemsets)
        self.frequent_supports_for_setsizes = {}
        self.find_frequent_sets(itemsets)

    @staticmethod
    def _items_are_in_set(items, set):
        """ Check if a set of items all exist in another set """
        for i in items:
            if i not in set:
                return False
        return True

    @staticmethod
    def _order_set(s):
        ordered_subset = list(s)
        ordered_subset.sort()
        return tuple(ordered_subset)

    def _get_subsets(self, itemset, num):
        """ Recursively find subsets from the frequent sets of smaller size
        This follows the monotonicity principle, which says a set will only be frequent if all its subsets are frequent
        """
        if num == 1:
            # stopping condition. When num is 1 just return all items in the set
            yield from combinations(itemset, num)
        else:
            subset_items = set()
            # recursion
            for subset in self._get_subsets(itemset, num-1):
                candidates = self.frequent_supports_for_setsizes.get(num-1)
                # order subsets or they won't always be found
                ordered_subset = self._order_set(subset)
                if candidates.get(ordered_subset):
                    # add each item to the set or tuples will be added as set items
                    for s in ordered_subset:
                        subset_items.add(s)
            yield from combinations(subset_items, num)

    def _add_support(self, item, supports, frequent_supports):
        """ Add 1 to the support count for an item """
        count = supports.get(item)
        count = count + 1 if count else 1
        supports[item] = count
        # if the item is frequent, add it to frequent support dict
        if count >= self.support_threshold:
            frequent_supports[item] = count

    def get_frequent_items(self, itemsets):
        """ Find frequent items. Similar to find frequent itemsets, but the setsize is just 1 """
        supports = {}
        frequent_supports = {}
        for object, itemset in itemsets.items():
            for item in itemset:
                self._add_support(item, supports, frequent_supports)
        self.frequent_supports_for_setsizes[1] = frequent_supports

    def find_frequent_sets(self, itemsets):
        """ Find frequent itemsets """
        for i in range(self.max_frequent_set_size):
            set_size = i+1
            supports = {}
            frequent_supports = {}
            # for each itemset, check all subsets of set_size if and only the subsets exist
            # the list of candidate pairs
            for object, items in itemsets.items():
                for subset in self._get_subsets(items, set_size):
                    # sets need to be ordered or else they will be considered to be different
                    subset = self._order_set(subset)
                    self._add_support(subset, supports, frequent_supports)
            self.frequent_supports_for_setsizes[set_size] = frequent_supports

    def find_association_rules(self, set_size):
        """ Set size is the size of the set to check rules against
        For example if set size is 2 a rule maybe be (Diapers, Milk) -> Beer
        """
        frequent_supports_item_removed = self.frequent_supports_for_setsizes[set_size]
        frequent_supports = self.frequent_supports_for_setsizes[set_size+1]
        rules = []
        for item_set, support in frequent_supports.items():
            for item in item_set:
                listset = list(item_set)
                listset.remove(item)
                listset.sort()
                item_support = frequent_supports_item_removed.get(tuple(listset))
                confidence = support / item_support
                rules.append((tuple(listset), item, confidence))
        return rules