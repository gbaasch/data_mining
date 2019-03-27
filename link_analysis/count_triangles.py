import pandas as pd

# infile = '../output-data/test_count_triangles.tsv'
infile = '../output-data/exports.tsv'

reporter_code = 0
reporter_description = 1
partner_code = 2
partner_description = 3
indicator_code = 4
indicator_description = 5
flow_Code = 6
flow_Description = 7
year = 8
unit = 9
value = 10
flag = 11
source_Description = 12
note = 13


categories = [
    'Total merchandise', 'Agricultural products', 'Manufactures',
    'Fuels and mining products', 'Food', 'Clothing', 'Textiles',
    'Office and telecom equipment', 'Chemicals',
    'Machinery and transport equipment', 'Iron and steel',
    'Automotive products', 'Fuels', 'Transport equipment',
    'Telecommunications equipment',
    'Electronic data processing and office equipment', 'Pharmaceuticals',
    'Integrated circuits and electronic components', 'Other food products',
    'Other semi-manufactures', 'Other chemicals', 'Other manufactures',
    'Raw materials', 'Scientific and controlling instruments',
    'Other machinery', 'Ores and other minerals',
    'Personal and household goods', 'Non-ferrous metals',
    'Miscellaneous manufactures', 'Other transport equipment', 'Fish'
]


def add_set_to_dict(dict, key, value):
    if value == key:
        return
    value_list = dict.get(key)
    if value_list:
        value_list.add(value)
    else:
        value_list = {value}
    dict[key] = value_list


def compute_triangles(infile):
    neighbours = {}
    with open(infile, encoding="ISO-8859-1") as f:
        lines = f.readlines()
    m = len(lines[4:])

    for line in lines[4:]:
        line = line.strip()
        line = line.split('\t')
        add_set_to_dict(neighbours, line[0], line[1])
        add_set_to_dict(neighbours, line[1], line[0])
    # print(neighbours)

    n = len(neighbours)
    num_triangles = 0
    for line in lines[4:]:
        line = line.strip()
        line = line.split('\t')
        if line[0] == line[1]:
            continue
        u = neighbours.get(line[0])
        v = neighbours.get(line[1])
        num_triangles += len(u & v)
        # print(line)
        # if num_triangles % 3 != 0:
        # print(u & v)
        # print(num_triangles)
        # break

    # print("num edges", m)
    # print("num nodes", n)
    expected = (4/3) * (m/n)**3
    # print("actual: ", num_triangles/3)
    return num_triangles, expected, m, n


if __name__ == '__main__':
    triangle_data = []
    for year in range(2000, 2018):
        # get triangles all categories
        infile = '../output-data/all-categories/{}/exports-{}-{}-category-None.tsv'
        infile_year = infile.format(year, year, year)
        triangles, e, m, n = compute_triangles(infile_year)
        triangle_data.append([year, 'All', triangles, e, m, n])

        for category in categories:
            # get triangles sub categories
            category_path = category.replace(" ", "_")
            infile = '../output-data/{}/categorical/exports-{}-{}-category-{}.tsv'
            infile_category = infile.format(year, year, year, category_path)
            # print(infile_year)
            try:
                triangles, e, m, b = compute_triangles(infile_category)
            except FileNotFoundError:
                print('skipped file')
            triangle_data.append([year, category, triangles, e, m, n])
    # therefore, the network is totally not random
    df = pd.DataFrame(triangle_data, columns=[
        'year', 'category', 'num_triangles', 'expected_triangles', 'num_edges', 'num_nodes'])
    df.to_csv('../output-data/triangles.csv')
    # IS THE PAGE RANK RELATED TO THE NEIGHBOURHOOD
