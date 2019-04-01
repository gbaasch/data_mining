import matplotlib.pyplot as plt
import numpy as np
import os


def total_pagerank():
    filenames = ["output-data/page_ranks/by_year/Agricultural_products-1950-2017.tsv",
                 "output-data/page_ranks/by_year/Automotive_products-1950-2017.tsv",
                 "output-data/page_ranks/by_year/Chemicals-1950-2017.tsv",
                 'output-data/page_ranks/by_year/Clothing-1950-2017.tsv',
                 "output-data/page_ranks/by_year/Electronic_data_processing_and_office_equipment-1950-2017.tsv",
                 "output-data/page_ranks/by_year/Fish-1950-2017.tsv",
                 "output-data/page_ranks/by_year/Food-1950-2017.tsv",
                 "output-data/page_ranks/by_year/Fuels-1950-2017.tsv",
                 "output-data/page_ranks/by_year/Fuels_and_mining_products-1950-2017.tsv",
                 "output-data/page_ranks/by_year/Integrated_circuits_and_electronic_components-1950-2017.tsv",
                 "output-data/page_ranks/by_year/Iron_and_steel-1950-2017.tsv",
                 "output-data/page_ranks/by_year/Machinery_and_transport_equipment-1950-2017.tsv",
                 "output-data/page_ranks/by_year/Manufactures-1950-2017.tsv",
                 "output-data/page_ranks/by_year/Miscellaneous_manufactures-1950-2017.tsv",
                 "output-data/page_ranks/by_year/Non-ferrous_metals-1950-2017.tsv",
                 "output-data/page_ranks/by_year/Office_and_telecom_equipment-1950-2017.tsv",
                 "output-data/page_ranks/by_year/Ores_and_other_minerals-1950-2017.tsv",
                 "output-data/page_ranks/by_year/Other_chemicals-1950-2017.tsv",
                 "output-data/page_ranks/by_year/Other_food_products-1950-2017.tsv",
                 "output-data/page_ranks/by_year/Other_machinery-1950-2017.tsv",
                 "output-data/page_ranks/by_year/Other_manufactures-1950-2017.tsv",
                 "output-data/page_ranks/by_year/Other_semi-manufactures-1950-2017.tsv",
                 "output-data/page_ranks/by_year/Other_transport_equipment-1950-2017.tsv",
                 "output-data/page_ranks/by_year/Personal_and_household_goods-1950-2017.tsv",
                 "output-data/page_ranks/by_year/Pharmaceuticals-1950-2017.tsv",
                 "output-data/page_ranks/by_year/Raw_materials-1950-2017.tsv",
                 "output-data/page_ranks/by_year/Scientific_and_controlling_instruments-1950-2017.tsv",
                 "output-data/page_ranks/by_year/Telecommunications_equipment-1950-2017.tsv",
                 "output-data/page_ranks/by_year/Textiles-1950-2017.tsv",
                 "output-data/page_ranks/by_year/Total_merchandise-1950-2017.tsv",
                 "output-data/page_ranks/by_year/Transport_equipment-1950-2017.tsv"
                 ]

    # filenames = [c for a, b, c in os.walk("output-data/page_ranks/by_year")]

    contentDictionaries = []
    for filename in filenames:
        contentDictionary = {}
        with open(filename, "r") as fileObject:
            for line in fileObject.readlines():

                if line.startswith("#"):
                    continue
                line = line.strip()
                st = line.split("\t")
                contentDictionary[st[1]] = float(st[0])
        contentDictionaries.append(contentDictionary)
    return contentDictionaries


def total_revenue():
    filenames = ["output-data/categorical/exports-1950-2017-category-Agricultural_products.tsv",
                 "output-data/categorical/exports-1950-2017-category-Automotive_products.tsv",
                 "output-data/categorical/exports-1950-2017-category-Chemicals.tsv",
                 "output-data/categorical/exports-1950-2017-category-Clothing.tsv",
                 "output-data/categorical/exports-1950-2017-category-Electronic_data_processing_and_office_equipment.tsv",
                 "output-data/categorical/exports-1950-2017-category-Fish.tsv",
                 "output-data/categorical/exports-1950-2017-category-Food.tsv",
                 "output-data/categorical/exports-1950-2017-category-Fuels.tsv",
                 "output-data/categorical/exports-1950-2017-category-Fuels_and_mining_products.tsv",
                 "output-data/categorical/exports-1950-2017-category-Integrated_circuits_and_electronic_components.tsv",
                 "output-data/categorical/exports-1950-2017-category-Iron_and_steel.tsv",
                 "output-data/categorical/exports-1950-2017-category-Machinery_and_transport_equipment.tsv",
                 "output-data/categorical/exports-1950-2017-category-Manufactures.tsv",
                 "output-data/categorical/exports-1950-2017-category-Miscellaneous_manufactures.tsv",
                 "output-data/categorical/exports-1950-2017-category-Non-ferrous_metals.tsv",
                 "output-data/categorical/exports-1950-2017-category-Office_and_telecom_equipment.tsv",
                 "output-data/categorical/exports-1950-2017-category-Ores_and_other_minerals.tsv",
                 "output-data/categorical/exports-1950-2017-category-Other_chemicals.tsv",
                 "output-data/categorical/exports-1950-2017-category-Other_food_products.tsv",
                 "output-data/categorical/exports-1950-2017-category-Other_machinery.tsv",
                 "output-data/categorical/exports-1950-2017-category-Other_manufactures.tsv",
                 "output-data/categorical/exports-1950-2017-category-Other_semi-manufactures.tsv",
                 "output-data/categorical/exports-1950-2017-category-Other_transport_equipment.tsv",
                 "output-data/categorical/exports-1950-2017-category-Personal_and_household_goods.tsv",
                 "output-data/categorical/exports-1950-2017-category-Pharmaceuticals.tsv",
                 "output-data/categorical/exports-1950-2017-category-Raw_materials.tsv",
                 "output-data/categorical/exports-1950-2017-category-Scientific_and_controlling_instruments.tsv",
                 "output-data/categorical/exports-1950-2017-category-Telecommunications_equipment.tsv",
                 "output-data/categorical/exports-1950-2017-category-Textiles.tsv",
                 "output-data/categorical/exports-1950-2017-category-Total_merchandise.tsv",
                 "output-data/categorical/exports-1950-2017-category-Transport_equipment.tsv",
                 ]

    # filenames = [c for a, b, c in os.walk("output-data/categorical")]

    contentDictionaries = []
    countryList = []
    for filename in filenames:

        with open(filename, "r") as fileObject:
            rev_list = []
            for line in fileObject.readlines():

                if line.startswith("#"):
                    continue
                line = line.strip()
                line_sep = line.split("\t")
                rev_list.append(line_sep)

                unique_country_list = []

                for i in rev_list:
                    unique_country_list.append(i[0])

                unique_country_list = list(set(unique_country_list))
                unique_country_list.sort()

                country_dict = {}

                for country in unique_country_list:
                    country_dict[country] = 0

                for each_list in rev_list:
                    key = each_list[0]
                    value = country_dict[key]
                    new = float(each_list[2])

                    country_dict[key] = value + new
        contentDictionaries.append(country_dict)
        countryList.append(unique_country_list)

    return contentDictionaries, countryList


pageRank_dicts = total_pagerank()
country_revenues, allCountries = total_revenue()

revenue_list = []

for i, allCountriesperCommodity in enumerate(allCountries):
    list_of_revenues = []
    for eachcountry in allCountriesperCommodity:
        list_of_revenues.append(country_revenues[i][eachcountry])

    maxi = max(list_of_revenues)
    mini = min(list_of_revenues)

    normalized_list_of_rev = [(x - mini) / (maxi - mini) for x in list_of_revenues]
    revenue_list.append(normalized_list_of_rev)

y_pageRank1 = []
x_revenue1 = []

masterList = []
for i, countriesPerCommodities in enumerate(allCountries):
    y_pageRank = []
    x_revenue = []

    page_rev_dicts = {}
    for j, country in enumerate(countriesPerCommodities):
        page_rev_dicts[(country, i)] = (pageRank_dicts[i][country], revenue_list[i][j])

        y_pageRank.append(pageRank_dicts[i][country])
        x_revenue.append(revenue_list[i][j])

    y_pageRank1.append(y_pageRank)
    x_revenue1.append(x_revenue)

    masterList.append(page_rev_dicts)

print((y_pageRank1))
print((x_revenue1))

fig = plt.figure(figsize=(11, 6))

gs = plt.GridSpec(1, 1, wspace=0.5, hspace=0.5)

ax1 = fig.add_subplot(gs[0, 0])

ax1.set_ybound(-0.1, 0.2)
ax1.set_xlabel("Revenue")
ax1.set_ylabel("Page Rank")
ax1.set_xlim(left=-0.01, right=1.1)
ax1.grid(True)

colours = ["Amaranth", "Amber ", "Amethyst ", "Apricot ", "Aquamarine","Azure ","Baby blue ", "Crimson ","Cyan ","Desert sand ", "Emerald ",
           "Beige ", "Black ","Blue ","Blush ","Brown ","Burgundy ","Cerise ","Champagne ","Chartreuse green ","Cobalt blue","Coffee","Copper ","Coral "
           "Blue-green ", "Blue-violet ", "Bronze ", "Byzantium ", "Carmine ", "Cerulean ", "Chocolate "]
markers = [".",",","o","v", "^" ,"<", ">", "1" ,"2", "3","4", "8", "s", "p", "P", "*","h","H","+","x","X","D","d",
           "|","_", "tickleft","tickright","tickup","tickdown","caretleft","caretright"]
for index_dummy, dummy in enumerate(x_revenue1):
    for index, value in enumerate(dummy):
        ax1.scatter(value, y_pageRank1[index_dummy][index])
    # ax1.set_title(label="Success rate")


plt.plot(np.unique(x_revenue1), np.poly1d(np.polyfit(x_revenue1, y_pageRank1, 1))(np.unique(x_revenue1)))

plt.show()
