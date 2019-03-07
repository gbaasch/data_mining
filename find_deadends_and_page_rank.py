from collections import OrderedDict
from operator import itemgetter

from link_analysis.deadends import get_deadends
from link_analysis.page_rank import compute_page_rank, print_page_ranks

infile = 'output-data/exports-1950-2017.tsv'
outfile = 'output-data/page_ranks/test-weighted.tsv'


def test_weighted_page_rank():
    infile = './link_analysis/test_page_rank.tsv'
    test_vec = compute_page_rank(infile, weighted=True, tax=None)
    print(test_vec)


if __name__ == '__main__':
    test = False
    if not test:
        # deadends, _, _ = get_deadends(infile, encoding="ISO-8859-1")
        # print("\ndeadends: ", deadends)
        page_rank_vec = compute_page_rank(infile, encoding="ISO-8859-1", weighted=True, tax=None)
        page_rank_vec_ordered = OrderedDict(sorted(page_rank_vec.items(), key=itemgetter(1), reverse=True))
        print_page_ranks(page_rank_vec_ordered, outfile)
    else:
        test_weighted_page_rank()
