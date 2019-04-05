try:
	from simrank import WeightedDirectedGraph
except ModuleNotFoundError:
	from refactored_code_greg.simrank import WeightedDirectedGraph

# Computes the weighted jaccard similarity of all countries to the one specified by "startNode"
def weighted_jaccard(startNode="North America", numToConsole=10, outpath = None, inpath="../data/merchandise_values_annual_dataset.csv"):
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

	countryCatTrades = {}			# indexed by (country, commodity), holds revenue for that pair
	countryTotalRevenues = {}		# indexed by country, holds total revenue

	# Parse data
	with open(inpath, "r") as infile:
		for line in infile.readlines():
			split = line.split('","')
			# skip lines that aren't exports
			if not len(split) == 14 or not split[7].startswith("Exports"):
				continue

			# Add to a country's total revenue
			val = float(split[10])
			country = split[1]
			if country in countryTotalRevenues:
				countryTotalRevenues[country] = countryTotalRevenues[country] + val
			else:
				countryTotalRevenues[country] = val

			# Add to a country's revenue by commodity
			key = (split[1], split[5])
			if key in countryCatTrades:
				countryCatTrades[key] = countryCatTrades[key] + val
			else:
				countryCatTrades[key] = val

	# normalize country incomes.
	# Also count how many commodities each country exports, for use in normalizing later
	countryNormalizedRevenues = {}
	countryCommodityCounts = {}
	for key in countryCatTrades.keys():
		# for each trade, divide by that country's total revenue and store in normalized dictionary
		country, _ = key
		revenue = countryCatTrades[key]
		totalRevenue = countryTotalRevenues[country]
		countryNormalizedRevenues[key] = revenue / totalRevenue

		# increment counters for how many commodities each country exports
		if country in countryCommodityCounts:
			countryCommodityCounts[country] = countryCommodityCounts[country] + 1
		else:
			countryCommodityCounts[country] = 1

	# initialize "matrix" (list of lists of floats) for similarities
	countrySims = []
	countryList = countryTotalRevenues.keys()
	for i in range(len(countryTotalRevenues.keys())):
		li = []
		for j in range(len(countryTotalRevenues.keys())):
			li.append(0.0)
		countrySims.append(li)

	# for each pair of countries, compute Jaccard similarity
	for i, icountry in enumerate(countryTotalRevenues.keys()):
		for j, jcountry in enumerate(countryTotalRevenues.keys()):
			for cat in categories:
				# Build normalized revenue keys from country and category
				ikey = (icountry, cat)
				jkey = (jcountry, cat)
				# Check if both countries trade that commodity
				if ikey in countryNormalizedRevenues and jkey in countryNormalizedRevenues:
					ival, jval = countryNormalizedRevenues[ikey], countryNormalizedRevenues[jkey]
					if ival == 0 or jval == 0:
						continue
					# Weighted Jaccard
					countrySims[i][j] += pow(min(ival, jval) / max(ival, jval), 2)

	for i, country in enumerate(countryList):
		if country == startNode:
			ranks = []
			for c, sim in zip(countryList, countrySims[i]):
				rank = pow(sim / max(countryCommodityCounts[country], countryCommodityCounts[startNode]), 0.5)
				ranks.append((rank, c))

			# Sort the data, and then remove the top one (which will always be the entity with itself)
			ranks.sort(reverse=True)
			ranks.pop(0)

			# Print the requested number to console (or at least as many as we can)
			for j in range(min(numToConsole, len(ranks))):
				print(ranks[j])

			# Print complete results to a file if outpath is provided
			if outpath:
				with open(outpath, "w+") as outFile:
					for rank in ranks:
						outFile.write(str(rank[0]) + "\t" + str(rank[1]) + "\n")

			return ranks


if __name__ == '__main__':
	weighted_jaccard("North America")
