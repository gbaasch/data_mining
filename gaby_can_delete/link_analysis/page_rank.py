from gaby_can_delete.link_analysis.deadends import get_deadends
from gaby_can_delete.link_analysis.utils import create_dicts
import operator


beta = 0.80
tepochs = 10


def sum_probabilities(key, previous_vec, out_links, in_links, weighted):
    total_sum = 0
    if not in_links.get(key):
        total_sum = 0
    else:
        if weighted:
            for link in in_links.get(key):
                out_links_from_here = out_links.get(link)
                weight_sum = sum(out_links_from_here.values())
                weights_indv = out_links_from_here.get(key)
                weight_sum = 1 if weight_sum == 0 else weight_sum
                weighted_prob = weights_indv / weight_sum
                total_sum += (previous_vec[link] * weighted_prob)
        else:
            for link in in_links.get(key):
                out_degree = len(out_links.get(link))
                total_sum += (previous_vec[link] / out_degree)
    return total_sum


def update_probabilities(out_links, in_links, previous_vec, tax=None, weighted=False):
    new_vec = {}
    for key, value in out_links.items():
        total_sum = sum_probabilities(key, previous_vec, out_links, in_links, weighted)
        if tax:
            new_vec[key] = beta*total_sum + tax
        else:
            new_vec[key] = total_sum
    # print(new_vec)
    return new_vec


def create_init_vec(out_links, num_nodes):
    vec = {}
    for node in out_links:
        vec[node] = 1/num_nodes
    return vec


def compute_page_rank(filename, weighted=False, encoding='utf-8', tax=None):
    deadends, in_links, out_links = get_deadends(filename, weighted, encoding=encoding)
    num_nodes = len(out_links)
    vec = create_init_vec(out_links, num_nodes)

    # decide whether or not to use taxation.
    if tax:
        taxation_value = (1 - beta) / num_nodes
    else:
        taxation_value = None

    # Compute Page Rank
    for i in range(tepochs):
        vec = update_probabilities(out_links, in_links, vec, taxation_value, weighted)

    sum_vec = 0
    for v, val in vec.items():
        sum_vec += val

    # print(sum_vec)

    # Page Rank with dead ends
    # if remove_deadends:
    in_links_with_deadends, out_links_with_deadends = create_dicts(filename, encoding)
    while deadends:
        deadend = deadends.pop()
        vec[deadend] = sum_probabilities(deadend, vec, out_links_with_deadends, in_links_with_deadends, weighted)
    return vec


def print_page_ranks(vec, filename):
    # Sort the vec in descending order based on page rank value
    vec = sorted(vec.items(), key=operator.itemgetter(1))
    vec.reverse()

    with open(filename, 'w+') as f:
        f.write('PageRank\tIds\n')
        for key, value in vec[:-1]:
            f.write(str(value)+'\t'+str(key)+'\n')
        f.write(str(vec[-1][1])+'\t'+str(vec[-1][0]))

