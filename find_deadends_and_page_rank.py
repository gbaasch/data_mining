from collections import OrderedDict
from operator import itemgetter

from link_analysis.question_1 import get_deadends
from link_analysis.question_2 import compute_page_rank

filename_ie = 'output-data/imports_exports.tsv'
filename_e = 'output-data/exports-2000-2000.tsv'
filename_i = 'output-data/imports.tsv'

if __name__ == '__main__':
    deadends_e, _, _ = get_deadends(filename_e, encoding="ISO-8859-1")
    print("\n\nexports: ", deadends_e)
    page_rank_vec = compute_page_rank(filename_e, encoding="ISO-8859-1")
    page_rank_vec_ordered = OrderedDict(sorted(page_rank_vec.items(), key=itemgetter(1), reverse=True))
    print("\n\npage rank: ", page_rank_vec_ordered)
