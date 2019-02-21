from link_analysis.question_1 import get_deadends

filename_ie = 'output-data/imports_exports.tsv'
filename_e = 'output-data/exports.tsv'
filename_i = 'output-data/imports.tsv'

if __name__ == '__main__':
    deadends_ie, _, _ = get_deadends(filename_ie, encoding="ISO-8859-1")
    deadends_e, _, _ = get_deadends(filename_e, encoding="ISO-8859-1")
    deadends_i, _, _ = get_deadends(filename_i, encoding="ISO-8859-1")
    print("imports and exports: ", deadends_ie)
    print("\n\nexports: ", deadends_e)
    print("\n\nimports: ", deadends_i)
