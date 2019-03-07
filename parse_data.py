encoding = "ISO-8859-1"
inpath = "data/merchandise_values_annual_dataset.csv"

""" Listed below are the CSV headers and their column number for reference.
I created these as variables for easier reference. """
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

""" Listed below are all categories in variables for easy reference
"""
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

def add_weighted_connection(line, connections, connections_with_weights):
    """ In this function we will create a dictionary that has the reporter_description and
    partner_description as the key, and the export value as the value

    :param line: the line in the csv
    :param connections: the list of connections
    :param connections_with_weights: the list of weights
    :return:
    """
    new_connection = (line[reporter_description], line[partner_description])
    weight = line[value]
    if new_connection not in connections:
        # if the reporter-partner pair is not present, create a value in the dictionary and set it
        # equal to the weight
        connections.append(new_connection)
        connections_with_weights[new_connection] = weight
    else:
        # if the reporter-partner pair is present, add the weight
        new_weight = float(connections_with_weights[new_connection]) + float(weight)
        connections_with_weights[new_connection] = new_weight


def write_connections_to_file(outpath, connections, connections_with_weights):
    with open(outpath, 'w+', encoding=encoding) as outfile:
        # we just have this to match the format from the homework
        for i in range(4):
            outfile.write("#this is an empty line\n")
        for conn in connections:
            # TODO just iterate over dict
            for item in conn:
                outfile.write(str(item) + "\t")

            outfile.write(str(connections_with_weights[conn]))
            outfile.write("\n")


def parse_exports(encoding='utf-8', start_year=1950, end_year=2017, category=None):
    """ This function transforms the dataset retrieved online from the WTO into the
     format that was given in our homework assignment. This make running page rank
     easier because we can reuse our work from the programming assignment.

    :param encoding: the file encoding. This is important to have if people are using
                    different operating systems
    :param start_year: the first year from which to extract data
    :param end_year:  the second year from which to extract data
    :param category:  specify the category
    :return: This does not return anything but it does create a file
    """
    # specify the outpath for the file that is created
    if category:
        outpath = 'output-data/categorical/exports-{}-{}-category-{}.tsv'
    else:
        outpath = 'output-data/exports-{}-{}-category-{}.tsv'
    outpath = outpath.format(start_year, end_year, category)

    connections = []
    connections_with_weights = {}
    with open(inpath, 'r', encoding=encoding) as infile:
        # this skips the CSV header
        lines = infile.readlines()[1:]
        for line in lines:
            line = line.split('","')
            # if the year is not within the range we specified, skip it
            if not start_year <= int(line[year]) <= end_year:
                continue
            # if a category is specified, skip all other categories
            if category:
                if line[indicator_description] != category:
                    continue
            if line[flow_Description] == 'Exports':
                # we are creating an output file with columns From, To
                add_weighted_connection(line, connections, connections_with_weights)

    write_connections_to_file(outpath, connections, connections_with_weights)


if __name__ == '__main__':
    # this specifies what to run if this file as ran as a script
    parse_exports(encoding)
    for category in categories:
        parse_exports(encoding, category=category)
    print("Done")

