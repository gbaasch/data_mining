import os
from itertools import combinations
import pandas as pd

from similar_items.create_itemsets_file import create_itemsets, create_itemsets_with_partner

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

data = pd.read_csv(ROOT_DIR + '/../data/merchandise_values_annual_dataset.csv', encoding="ISO-8859-1")
data_exports = data[data['Flow_Description'] == 'Exports']

# print(list(data_exports.index))


def items_in_set(items, set):
    for i in items:
        if i not in set:
            return False
    return True


def subsets(s, num):
    for cardinality in range(num):
        yield from combinations(s, cardinality)


# def find_supports(indicators, items_dict, frequent_threshold, num):
#     frequent_supports = []
#     infrequent_supports = []
#
#     for i in subsets(indicators, num):
#         support = 0
#         for item, set in items_dict.items():
#             if items_in_set(i, set):
#                 support += 1
#         support = support/len(items_dict)
#         support_item_tuple = (i, support)
#         if support >= frequent_threshold:
#             frequent_supports.append(support_item_tuple)
#         elif support <= 0.05:
#             infrequent_supports.append(support_item_tuple)
#
#     return frequent_supports, infrequent_supports


def find_supports(items_dict, frequent_threshold, num):
    frequent_supports = []
    infrequent_supports = []

    items = set()

    for key, item in items_dict.items():
        for i in item:
            items.add(i)

    for i in subsets(items, num):
        support = 0
        for item, item_set in items_dict.items():
            if items_in_set(i, item_set):
                support += 1
        support = support/len(items_dict)
        support_item_tuple = (i, support)
        if support >= frequent_threshold:
            frequent_supports.append(support_item_tuple)
        elif support <= 0.05:
            infrequent_supports.append(support_item_tuple)

    return frequent_supports, infrequent_supports


def find_frequent_items(indicators, items_dict, threshold):
    frequent_supports, _ = find_supports(indicators, items_dict, threshold, 2)
    frequent_items = []
    for (item), support in list(frequent_supports)[1:]:
        frequent_items.append(item[0])
    return frequent_items


def find_association_rules(indicators, items_dict, threshold):
    # frequent_supports, _ = find_supports(indicators, items_dict, threshold, 3)
    frequent_item_supports = find_frequent_itemsets(indicators, items_dict, 0.8, 1)
    frequent_supports = find_frequent_itemsets(indicators, items_dict, 0.8, 2)

    rules = []
    for item_set, support in frequent_supports.items():
        for item in item_set:
            listset = list(item_set)
            listset.remove(item)
            item_support = frequent_item_supports.get(tuple(listset))
            # print('suuport', support, 'item_support', item_support)
            confidence = support / item_support
            rules.append((listset, item, confidence))
            # TODO - create text for rule
    return rules


def find_frequent_itemsets(indicators, items_dict, threshold, setsize):
    for i in range(setsize):
        frequent_supports, _ = find_supports(indicators, items_dict, threshold, i+2)
        indicators = []
        frequent_sets = {}
        for (item), support in frequent_supports[1:]:
            indicators.append(item[0])
            if len(item) == setsize:
                frequent_sets[item] = support
                # frequent_sets.add((item, support))
    return frequent_sets


if __name__ == '__main__':
    # x = data_exports.groupby(['Reporter_description', 'Indicator_description', 'Partner_description']).sum()
    # indicators = list(data_exports['Indicator_description'].value_counts().index)
    # x_index = x.index
    # items_dict = create_itemsets_with_partner(list(x.index))
    #
    #
    # frequent_itemsets = find_frequent_itemsets(indicators, items_dict, 0.8, 1)
    # print(frequent_itemsets)
    #
    # rules = find_association_rules(indicators, items_dict, 0.8)
    # print(rules)

    x = data_exports.groupby(['Reporter_description', 'Indicator_description']).sum()
    # indicators = list(data_exports['Indicator_description'].value_counts().index)
    x_index = x.index
    items_dict = create_itemsets(list(x.index))

    supports = find_supports(items_dict, 0.8, 2)

    # rules = find_association_rules(indicators, items_dict, 0.8)
    # print(rules)



