from link_analysis.utils import create_dicts


def remove_deadend(deadend, in_links, out_links, deadends):
    if in_links.get(deadend):
        links_leaving_deadend = in_links.pop(deadend)
        for link in links_leaving_deadend:
            outlinks_to_remove = out_links.get(link)
            outlinks_to_remove.pop(deadend)
            if not outlinks_to_remove:
                out_links.pop(link)
                deadends.append(link)


def get_deadends(filename, weighted, encoding='utf-8'):
    print('ENCOINFDKSA;', encoding)
    # TODO its confusing that this is in get_deadends and returned by this function
    # move it outside the function
    in_links, out_links = create_dicts(filename, encoding)

    # Initial removal of deadends
    deadends = []
    for key in in_links:
        if not out_links.get(key):
            deadends.append(key)

    for deadend in deadends:
        remove_deadend(deadend, in_links, out_links, deadends)

    return deadends, in_links, out_links
