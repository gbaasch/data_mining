from simrank import WeightedDirectedGraph

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
inpath = "data/merchandise_values_annual_dataset.csv"


def weighted_jaccard():
	global inpath, categories

	countryCatTrades = {}		# indexed by (country, commodity), holds revenue for that pair
	countryTotalRevenues = {}	# indexed by country, holds total revenue

	with open(inpath, "r") as infile:
		for line in infile.readlines():
			split = line.split('","')
			if not len(split) == 14 or not split[7].startswith("Exports"):
				continue

			val = float(split[10])
			country = split[1]
			if country in countryTotalRevenues:
				countryTotalRevenues[country] = countryTotalRevenues[country] + val
			else:
				countryTotalRevenues[country] = val

			key = (split[1], split[5])
			if key in countryCatTrades:
				countryCatTrades[key] = countryCatTrades[key] + val
			else:
				countryCatTrades[key] = val

	# normalize country incomes
	countryNormalizedRevenues = {}
	for key in countryCatTrades.keys():
		country, _ = key
		revenue = countryCatTrades[key]
		totalRevenue = countryTotalRevenues[country]
		countryNormalizedRevenues[key] = revenue / totalRevenue
	print("normalized revenues check:", len(countryNormalizedRevenues.keys()), "=", len(countryCatTrades.keys()))

	# keysCounted = 0
	# for country in countryTotalRevenues.keys():
	# 	subtotal = 0
	# 	for cat in categories:
	# 		key = (country, cat)
	# 		if key in countryNormalizedRevenues:
	# 			subtotal += countryNormalizedRevenues[key]
	# 			keysCounted += 1
	# 	print(country, subtotal)
	# print("keys counted:", keysCounted)
	# return

	# initialize "matrix" for similarities
	countrySims = []
	countryList = countryTotalRevenues.keys()
	for i in range(len(countryTotalRevenues.keys())):
		li = []
		for j in range(len(countryTotalRevenues.keys())):
			li.append(0.0)
		countrySims.append(li)

	for i, icountry in enumerate(countryTotalRevenues.keys()):
		for j, jcountry in enumerate(countryTotalRevenues.keys()):
			for cat in categories:
				ikey = (icountry, cat)
				jkey = (jcountry, cat)
				if ikey in countryNormalizedRevenues and jkey in countryNormalizedRevenues:
					ival, jval = countryNormalizedRevenues[ikey], countryNormalizedRevenues[jkey]
					if ival == 0 or jval == 0:
						continue
					countrySims[i][j] += min(ival, jval) / max(ival, jval)

	for i, country in enumerate(countryList):
		if country == "North America":
			ranks = []
			for c, sim in zip(countryList, countrySims[i]):
				ranks.append((sim / 31, c))
			ranks.sort(reverse=True)
			for j in range(30):
				print(ranks[j])


if __name__ == '__main__':
	weighted_jaccard()
