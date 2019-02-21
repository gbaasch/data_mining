from link_analysis.question_1 import get_deadends

filename = 'output.tsv'

if __name__ == '__main__':
    deadends, _, _ = get_deadends(filename, encoding="ISO-8859-1")
    print(deadends)
