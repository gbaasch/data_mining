import pandas as pd

data_exports = pd.read_csv('./data/merchandise_values_annual_dataset.csv', encoding="ISO-8859-1")


# Import page rankds into a dateframe
def get_page_rank_df(weighted):
    if weighted:
        weighted_path = 'weighted'
    else:
        weighted_path = 'unweighted'
    data_list = []
    for year in range(2000, 2018):
        for category in list(data_exports.Indicator_description.value_counts().index):
            category_formatted = category.replace(' ', '_')
            filename = './output-data/page_ranks/by_year/{}/{}-{}.tsv'.format(
                weighted_path, year, category_formatted)
            try:
                df = pd.read_csv(filename, sep='\t')
                df['Year'] = year
                df['Indicator_description'] = category
                data_list.append(df)
            except FileNotFoundError:
                print("Could not find:", filename)

    page_ranks_df = pd.concat(data_list, axis=0)
    if weighted:
        page_ranks_df.rename(index=str, columns={"PageRank": "Weighted_PageRank"}, inplace=True)
    else:
        page_ranks_df.rename(index=str, columns={"PageRank": "Unweighted_PageRank"}, inplace=True)
    return page_ranks_df


weighted_pr_df = get_page_rank_df(weighted=True)
unweighted_pr_df = get_page_rank_df(weighted=False)


def join_dfs(data_exports, page_rank_df):
    data_exports_pr = data_exports.copy()
    #     data_exports_pr.merge(page_rank_df)
    data_exports_pr = data_exports_pr.join(
        page_rank_df.set_index(
            ['Ids', 'Year', 'Indicator_description']),
        on=['Reporter_description', 'Year', 'Indicator_description']
    )
    # data_exports_pr[(data_exports_pr['Year'] >= 2000) & (data_exports_pr['Indicator_description'] == 'Manufactures')]
    #     data_exports_pr[(data_exports_pr['Year'] >= 2000)].head()
    return data_exports_pr


weighted_pr_df.head()
unweighted_pr_df.head()

data_exports_pr = join_dfs(data_exports, weighted_pr_df)
data_exports_pr = join_dfs(data_exports_pr, unweighted_pr_df)
data_exports_pr.head()


data_exports_pr.to_csv('./data/merchandise_values_page_ranks_weighted_unweighted.csv')
