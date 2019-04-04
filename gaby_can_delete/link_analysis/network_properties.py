import pandas as pd

encoding = "ISO-8859-1"
data_file = 'data/merchandise_values_annual_dataset.csv'
data = pd.read_csv(data_file, '\t', encoding=encoding)


def size():
    pass


def density():
    pass


def planar_network_density():
    pass


def average_degree():
    pass


def average_shortest_path_length():
    pass


def diameter():
    pass


def cluster_coefficient():
    pass


def connectedness():
    pass


def node_centrality():
    pass


def node_influence():
    pass


def get_average_degree_separation(category=None):
    if category:
        category_data = data[data['Indicator_description'] == category]
    else:
        category_data = data

    print(category_data.head())
    return len(category_data['Reporter_description'].value_counts()) / len(category_data)


# def get_average_degree_separations():
#     for category in categories

if __name__ == '__main__':
    get_average_degree_separation()
