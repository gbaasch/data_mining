from time import sleep

# A program for calculating various statistics of the Kaggle dataset
# Written by Gregory O'Hagan
# Notes:
# • "commodity_trade_statistics_data.csv" has data from 1988-2016 (not all years for all data)

# ********** INSERT GLOBAL VARIABLES REQUIRED HERE **********

# for min_max_year
minYear = 2000
maxYear = 2000

# for find_all_categories
categories = {}
catValues = {}

# for imports_vs_exports_by_cat:
catImports = {}
catExports = {}


def main():
	with open("data/commodity_trade_statistics_data.csv", "r") as kFile:
		# parse each line. Skip the first line
		line = kFile.readline()
		line = kFile.readline()
		while line:
			# handle text fields ending with a newline
			nextLine = kFile.readline()
			if nextLine.startswith('",'):
				line = line.strip() + nextLine
				nextLine = kFile.readline()

			# Parse out data. This is formatted to be able to read every line of the Kaggle file
			# m = re.match(r"(.+),(\d+),([\da-zA-Z]+),\"?(.+)\"?,(.+),(\d+),(\d*),(.+),([\d.E+]*),(.+)$", line)
			m = non_regex_kaggle_split(line)
			if m:
				# parse into labels
				# note that "quan" can be in scientific notation
				# country, year, comCode, comName, flow, usd, kg, quanName, quan, category = m
				# year = int(year)

				# ********** INSERT CODE HERE **********
				# Call work function(s) here:
				# find_min_max_year(m)
				# find_all_categories(m)
				find_imports_vs_exports_by_cat(m)

			# get next line if there is one
			line = nextLine

	# ********** INSERT CODE HERE **********
	# Call display function(s) here
	# print_min_max_year()
	# print_all_categories()
	print_imports_vs_exports_by_cat()


def find_min_max_year(m):
	global minYear, maxYear
	year = int(m[1])
	if year < minYear:
		minYear = year
	elif year > maxYear:
		maxYear = year


def print_min_max_year():
	global minYear, maxYear
	print("Minimum year:", minYear)
	print("Maximum year:", maxYear)


def find_all_categories(m):
	global categories, catValues
	cat = m[-1]
	val = int(m[5])
	try:
		categories[cat] = categories[cat] + 1
		catValues[cat] = catValues[cat] + val
	except KeyError:
		categories[cat] = 1
		catValues[cat] = val


def print_all_categories():
	global categories, catValues
	print("category occurrence count, category USD, category name")
	for key in categories.keys():
		print(categories[key], "\t", catValues[key], "\t", key)


def find_imports_vs_exports_by_cat(m):
	global catImports, catExports
	cat = m[-1]
	val = int(m[5])
	isImport = m[4].startswith("I")
	if isImport:
		try:
			catImports[cat] = catImports[cat] + val
		except KeyError:
			catImports[cat] = val
	else:
		try:
			catExports[cat] = catExports[cat] + val
		except KeyError:
			catExports[cat] = val


def print_imports_vs_exports_by_cat():
	global catImports, catExports
	print("exports, import/export ratio, category name")
	importsT, exportsT = 0, 0
	for key in catImports.keys():
		print(catExports[key], "\t", catImports[key] / catExports[key], "\t", key)
		importsT += catImports[key]
		exportsT += catExports[key]

	print("\n", exportsT, "\t", importsT / exportsT, "\t", "Overall totals")


# Splits a line on commas, but keeps everything inside of double quotes in the same field
# This is the formatting for csv files when some fields may include commas
# length is the expected length. This returns None if the parsed line doesn't match this length
def non_regex_kaggle_split(line, length=10):
	line = line.strip()
	groups = []
	nextGroup = ""
	quoteStatus = 0
	for c in line:
		if quoteStatus == 0 and c == ",":
			groups.append(nextGroup)
			nextGroup = ""
		# Toggle if we are inside of quotes or not
		elif c == '"':
			quoteStatus = 1 - quoteStatus
		else:
			nextGroup += c
	groups.append(nextGroup)
	if len(groups) != length:
		print(line)
		print(groups, "\n")
		sleep(1)
		return None
	return groups


if __name__ == '__main__':
	main()
