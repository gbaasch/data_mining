import pandas as pd
# data_exports[['Reporter_description', 'Indicator_description']].to_dict()


def compute_jaccard_similarity(s1, s2):
    intersection = s1 & s2
    union = s1 | s2
    return len(intersection) / len(union)


def add_item_to_set_dict(dict, key, item):
    items_set = dict.get(key)
    if items_set is None:
        dict[key] = {item}
    else:
        items_set.add(item)
        dict[key] = items_set


def create_itemsets(data):
    items_dict = {}
    for reporter, item in data:
        items_list = items_dict.get(reporter)
        if items_list is None:
            items_dict[reporter] = {item}
        else:
            items_list.add(item)
            items_dict[reporter] = items_list
    return items_dict


def create_itemsets_with_partner(data):
    items_dict = {}
    for reporter, item, partner in data:
        items_list = items_dict.get(reporter)
        if items_list is None:
            items_dict[reporter] = {(item, partner)}
        else:
            items_list.add((item, partner))
            items_dict[reporter] = items_list
    return items_dict


def create_sims_dict(data):
    sims_dict = {}
    items_dict = create_itemsets(list(data.index))
    similar_reporters = []
    dissimilar_reporters = []
    identical_reporters = []

    for reporter_1, indicators_1 in items_dict.items():
        for reporter_2, indicators_2 in items_dict.items():
            if not reporter_1 == reporter_2:
                sim = compute_jaccard_similarity(indicators_1, indicators_2)
                add_item_to_set_dict(sims_dict, sim, reporter_1)
                add_item_to_set_dict(sims_dict, sim, reporter_2)

                if 1 > sim >= 0.6:
                    similar_reporters.append((reporter_1, reporter_2, sim))
                elif sim < 0.6:
                    dissimilar_reporters.append((reporter_1, reporter_2, sim))
                elif sim == 1:
                    identical_reporters.append((reporter_1, reporter_2, sim))

    return similar_reporters, dissimilar_reporters, identical_reporters


if __name__ == '__main__':
    data = pd.read_csv('../data/merchandise_values_annual_dataset.csv', encoding="ISO-8859-1")
    data_exports = data[data['Flow_Description'] == 'Exports']

    outfile = '../output-data/item_sets.tsv'

    x = data_exports.groupby(['Reporter_description', 'Indicator_description']).sum()
    sims_dict = create_sims_dict(data_exports)

    # print(len(similar_reporters))
    # print(len(dissimilar_reporters))
    # print(len(identical_reporters))
    print(sims_dict)

    # print(similar_reporters)


    # for i in range(len(items_dict)):
    #     reporter_1, indicators_1 = items_dict[i]
        # for j in range(len(items_dict)):
        #     # do not want to compare a set to itself
        #     if not i == j:
        #         index_2, question_2 = items_dict[j]
        #         # Computes the Jaccard similarity and then outputs the qids if they are above or equal to 0.6
        #         sim = compute_jaccard_similarity(question_1, question_2)
        #         if sim >= 0.6:
        #             temp_qids = temp_qids + index_2 + ','
        # temp_qids = temp_qids.strip(',')
        # f.write(temp_qids + '\n')