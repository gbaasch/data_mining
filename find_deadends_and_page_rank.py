import os
from collections import OrderedDict
from operator import itemgetter

from link_analysis.deadends import get_deadends
from link_analysis.page_rank import compute_page_rank, print_page_ranks
from parse_data import categories

infile = 'output-data/{}/categorical/exports-{}-{}-category-{}.tsv'
outfile = 'output-data/page_ranks/by_year/{}/{}-{}.tsv'


def test_weighted_page_rank(weighted):
    infile = './link_analysis/test-page_rank.tsv'
    test_vec = compute_page_rank(infile, weighted=weighted, tax=None)
    print(test_vec)


if __name__ == '__main__':
    test = False
    weighted = True
    if not test:
        directory = 'weighted' if weighted else 'unweighted'
        # deadends, _, _ = get_deadends(infile, encoding="ISO-8859-1", weighted=weighted)
        # print("\ndeadends: ", deadends)

        for year in range(2000, 2018):
            for category in categories:
                print("year: {}, category: {}".format(year, category))

                # format files
                category = category.replace(" ", "_")
                outfile_formatted = outfile.format(directory, year, category)
                infile_formatted = infile.format(year, year, year, category)

                if not os.path.isfile(infile_formatted):
                    print("COULD NOT FIND FILE ", infile_formatted)
                    continue

                # calculate page rank
                page_rank_vec = compute_page_rank(infile_formatted, encoding="ISO-8859-1", weighted=weighted, tax=None)

                # print page rank
                page_rank_vec_ordered = OrderedDict(sorted(page_rank_vec.items(), key=itemgetter(1), reverse=True))
                print_page_ranks(page_rank_vec_ordered, outfile_formatted)
    else:
        test_weighted_page_rank(weighted)
