
def insert_in_dict(key, value, dict):
    if key not in dict:
        dict[key] = [value]
    else:
        dict[key].append(value)


def insert_out_dict(key, value, weight, dict):
    if key not in dict:
        weight_dict = {}
        # weight_dict[value]
        # dict[key] = {value: weight}
    else:
        weight_dict = dict[key]
    weight_dict[value] = float(weight)
    dict[key] = weight_dict


def create_dicts(filename, encoding):
    with open(filename, encoding=encoding) as f:
        file = f.readlines()
    in_links = {}
    out_links = {}
    for line in file[4:]:
        # parse line
        line = line.split('\t')
        from_node = line[0]
        to_node = line[1]
        weight = line[2].split('\n')[0]
        insert_out_dict(to_node, from_node, weight, in_links)
        insert_out_dict(from_node, to_node, weight, out_links)
    return in_links, out_links
