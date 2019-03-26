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


def find_supports(items_dict, candidate_pairs, frequent_threshold, num, frequent):
    frequent_supports = []
    infrequent_supports = []

    items = set()

    for key, item in candidate_pairs.items():
        for i in item:
            items.add(i)

    # print(items)
    for i in subsets(items, num):
        support = 0
        for item, item_set in items_dict.items():
            if items_in_set(i, item_set):
                support += 1
        support = support/len(items_dict)
        support_item_tuple = (i, support)
        if frequent:
            if support >= frequent_threshold:
                frequent_supports.append(support_item_tuple)
        else:
            if support <= frequent_threshold:
                frequent_supports.append(support_item_tuple)

        if support <= 0.05:
            infrequent_supports.append(support_item_tuple)

    print('amnt frequent', len(frequent_supports))
    return frequent_supports, infrequent_supports


def find_frequent_items(items_dict, threshold):
    frequent_supports, _ = find_supports(items_dict, threshold, 2)
    frequent_items = []
    for (item), support in list(frequent_supports)[1:]:
        frequent_items.append(item[0])
    return frequent_items


def find_association_rules(items_dict, threshold, setsize, frequent):
    # frequent_supports, _ = find_supports(indicators, items_dict, threshold, 3)
    frequent_item_supports = find_frequent_itemsets(items_dict, items_dict, threshold, setsize, frequent)
    frequent_supports = find_frequent_itemsets(items_dict, items_dict, threshold, setsize+1, frequent)

    rules = []
    for item_set, support in frequent_supports.items():
        # print('looping')
        for item in item_set:
            listset = list(item_set)
            listset.remove(item)
            listset.sort()
            item_support = frequent_item_supports.get(tuple(listset))
            # print('suuport', support, 'item_support', item_support)
            confidence = support / item_support
            rules.append((listset, item, confidence))
    return rules


def find_frequent_itemsets(items_dict, candidate_pairs, threshold, setsize, frequent):
    for i in range(setsize):
        # print(candidate_pairs)
        frequent_supports, _ = find_supports(items_dict, candidate_pairs, threshold, i+2, frequent)
        # indicators = []
        frequent_sets = {}
        c_num = 0
        candidate_pairs = {}
        for (item), support in frequent_supports[1:]:
            # indicators.append(item[0])
            if len(item) == setsize:
                ordered_item = list(item)
                ordered_item.sort()
                frequent_sets[tuple(ordered_item)] = support
                # frequent_sets.add((item, support))
            candidate_pairs[c_num] = item
            c_num += 1
        # items_dict = frequent_sets
    return frequent_sets


if __name__ == '__main__':
    test = False
    frequent = True
    if test:
        items_dict = {
            1: {'Bread', 'Milk'},
            2: {'Bread', 'Diapers', 'Beer', 'Eggs'},
            3: {'Milk', 'Diapers', 'Beer', 'Cola'},
            4: {'Bread', 'Milk', 'Diapers', 'Beer'},
            5: {'Bread', 'Milk', 'Diapers', 'Cola'},
        }

        frequent_itemsets = find_frequent_itemsets(items_dict, items_dict, 0.4, 3)
        print('frequent_itemsets')
        print(frequent_itemsets)
        rules = find_association_rules(items_dict, 0.4, 2)
        print('rules')
        print(rules)
    else:
        use_partner = False
        if use_partner:
            # Create items including partner descriptions
            print("preparing data")
            print(len(data_exports))
            # data_exports = data_exports[data_exports['Partner_description'] != 'World']
            print(len(data_exports))
            x = data_exports.groupby(['Reporter_description', 'Indicator_description', 'Partner_description']).sum()
            x_index = x.index
            print(len(x_index))
            items_dict = create_itemsets_with_partner(list(x.index))
        else:
            # Create items just based on category
            x = data_exports.groupby(['Partner_description', 'Reporter_description']).sum()
            # x = data_exports.groupby(['Reporter_description', 'Partner_description']).sum()
            x_index = x.index
            items_dict = create_itemsets(list(x.index))

        print('finding frequesnts')
        # find_supports(items_dict, items_dict, 0.8, 3)
        frequent_itemsets = find_frequent_itemsets(items_dict, items_dict, 0.5, 2, frequent)
        print(frequent_itemsets)
        print('finding rules')
        # rules = find_association_rules(items_dict, 0.6, 1, frequent)
        # print(rules)
        # supports = find_supports(items_dict, 0.8, 3)

