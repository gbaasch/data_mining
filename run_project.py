import pandas as pd
import os

from refactored_code_gaby.network_analysis.directed_network import DirectedNetwork
from refactored_code_gaby.network_analysis.undirected_network import UndirectedNetwork
from refactored_code_gaby.network_analysis.page_rank import PageRank

from refactored_code_gaby.itemsets.itemsets import Itemsets
from refactored_code_gaby.itemsets.frequent_items.find_frequent_items import FindFrequentItems

from refactored_code_greg.network_stats import degree_by_commodity, degree_by_country
from refactored_code_greg.weighted_jaccard import weighted_jaccard
from refactored_code_greg.simrank import simrank_runner

# Change these if you only want to run part of this script
RUN_PAGERANK = True
RUN_ASSOCIATION_RULES = True
RUN_COUNTING_TRIANGLES = True
RUN_DEGREES = True

RUN_JACCARD = True
JACCARD_NODEID = "Canada"       # Country to compare to for Jaccard similarity
RUN_SIMRANK = True
SIMRANK_NODEID = "Canada"       # Country to compare to for simRank similarity

# Constants
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(ROOT_DIR, 'data/merchandise_values_annual_dataset.csv')
CATEGORIES = [
    'Total Merchandise', 'Agricultural products', 'Manufactures',
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


if __name__ == '__main__':
    """ This is the main script file for our project code. """
    # =============
    # PARSE DATA
    # ================
    df_not_used = pd.read_csv(DATA_FILE, encoding="ISO-8859-1")
    df_exports = df_not_used[df_not_used['Flow_Description'] == 'Exports']  # we only look at reported exporters
    df_exports = df_not_used[df_not_used['Year'] >= 2000]  # we only look at reported exporters
    df_grouped = df_exports.groupby(['Reporter_description', 'Partner_description', 'Year']).sum()
    edges_no_categories = list(df_grouped.index)  # nodes and edges only, no categories included
    df_edges_no_categories = pd.DataFrame(data=edges_no_categories, columns=['Exporter', 'Importer', 'Year'])

    # =============
    # RUN PAGE RANK
    # ================
    if RUN_PAGERANK:
        print("Running PageRank for years 2000-2018, all categories...")
        df_list = []
        for year in range(2000, 2018):
            for category in CATEGORIES:
                # calculated page ranks
                df_year_cat = df_exports[(df_exports['Indicator_description'] == category) & (df_exports['Year'] == year)]
                directed_network = DirectedNetwork(df_year_cat[['Reporter_description', 'Partner_description', 'Value']])
                pr_weighted = PageRank(directed_network, weighted=True, beta=None, epochs=10)
                weighted_page_ranks = pr_weighted.get_page_ranks()
                pr_unweighted = PageRank(directed_network, weighted=False)
                unweighted_page_ranks = pr_unweighted.get_page_ranks()

                # create dataframes that will be printed to a file
                df_weighted = pd.DataFrame.from_dict(weighted_page_ranks, orient='index', columns=['Weighted_PageRank'])
                df_weighted['Year'] = year
                df_weighted['Indicator_description'] = category
                df_weighted['Reporter_description'] = df_weighted.index
                df_list.append(df_weighted)

                # only print example page ranks occasionally or they overwhelm the console
                if category == 'Ores and other minerals ':
                    w = 'Developing Asia'
                    print("Example PageRanks for {} in {}: \n\tWeighted: {}, Unweighted: {}".format(
                        w, year, weighted_page_ranks.get(w), unweighted_page_ranks.get(w)))

        print("Weighted and Unweighted PageRanks have been calculated for each commodity and each year.")
        print("Creating a new csv data file...")
        # append page ranks to data frame to create a new csv that can be used for visualization
        weighted_pr_df = pd.concat(df_list)
        data_exports_pr = df_exports.copy()
        data_exports_pr = data_exports_pr.join(
            weighted_pr_df.set_index(
                ['Reporter_description', 'Year', 'Indicator_description']),
            on=['Reporter_description', 'Year', 'Indicator_description']
        )
        data_exports_pr.to_csv(os.path.join(ROOT_DIR, 'data/merchandise_values_page_ranks_weighted_unweighted_new.csv'))

    # =============
    # EVALUATE NETWORK PROPERTIES
    # ================
    if RUN_COUNTING_TRIANGLES:
        print("Running Count Triangles for years 2000-2018...")
        triangle_data = []
        for year in range(2000, 2018):
            df_year = df_edges_no_categories[df_edges_no_categories['Year'] == year]
            # create network classes from dataset
            undirected_network = UndirectedNetwork(df_year)
            expected_triangles = undirected_network.count_triangles_expected()
            # count triangles
            triangles = undirected_network.count_triangles()
            nodes = undirected_network.node_count
            edges = undirected_network.edge_count
            print("Triangles for", year)
            print("\tExpected Triangles: {}, Actual Triangles: {}, Total Edges: {}, Total Vertices: {}".format(
                expected_triangles, triangles, edges, nodes))

    # =============
    # FREQUENT ITEMS AND ASSOCIATION RULE MINING
    # ================
    if RUN_ASSOCIATION_RULES:
        print("\nRunning Association Rule Mining....")
        print("Creating itemsets...")
        itemsets_partner_reporter = Itemsets(df_exports[['Partner_description', 'Reporter_description']])
        threshold = 0.6 * itemsets_partner_reporter.size
        print("Finding Frequent Itemsets...")
        association_rule_maker = FindFrequentItems(itemsets_partner_reporter, threshold, 2)
        print("Finding Association Rules...")
        rules = association_rule_maker.find_association_rules(1)
        for rule in rules:
            print("Any time someone imports from {}, they also import from {} with {} confidence.".format(
                rule[0][0], rule[1], rule[2]
            ))

    # =============
    # NETWORK DEGREE
    # ================
    if RUN_DEGREES:
        print("Calculating network degrees...")
        degree_by_country(DATA_FILE)
        degree_by_commodity(DATA_FILE)
        print("Done calculating degrees\n")

    # =============
    # JACCARD SIMILARITY FOR BAGS
    # ================
    if RUN_JACCARD:
        print("Running Jaccard similarity for", JACCARD_NODEID)
        print("This identifies whether two countries have a similar economic base")
        # Note: data is printed inside this call
        weighted_jaccard(SIMRANK_NODEID, 10, "jaccard_output.tsv", DATA_FILE)
        print("Complete data written to \"jaccard_output.tsv\"\n")

    # =============
    # WEIGHTED SIM RANK
    # ================
    if RUN_SIMRANK:
        print("Running simRank for", SIMRANK_NODEID)
        print("This identifies where a country depends on for exporting their merchandise to")
        ranks = simrank_runner(DATA_FILE, SIMRANK_NODEID, "simrank_output.tsv")
        if len(ranks) > 10:
            print("Top 10 entities by simRank:")
            for i in range(10):
                print(ranks[i])
            print("Complete data written to \"simrank_output.tsv\"\n")
        else:
            print("simRank output unexpectedly short. Verify provided nodeID and rerun\n")

    print('Done! We hope you enjoyed exploring the Global Trade Network with us!')
