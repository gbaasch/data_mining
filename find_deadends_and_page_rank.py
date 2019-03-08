from collections import OrderedDict
from operator import itemgetter

from link_analysis.deadends import get_deadends
from link_analysis.page_rank import compute_page_rank, print_page_ranks
from parse_data import categories

infile = 'output-data/categorical/exports-1950-2017-category-{}.tsv'
outfile = 'output-data/page_ranks/{}/{}.tsv'


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

        for category in categories:
            # format files
            category = category.replace(" ", "_")
            outfile_formatted = outfile.format(directory, category)
            infile_formatted = infile.format(category)

            # calculate page rank
            page_rank_vec = compute_page_rank(infile_formatted, encoding="ISO-8859-1", weighted=weighted, tax=None)

            # print page rank
            page_rank_vec_ordered = OrderedDict(sorted(page_rank_vec.items(), key=itemgetter(1), reverse=True))
            print_page_ranks(page_rank_vec_ordered, outfile_formatted)
    else:
        test_weighted_page_rank(weighted)
