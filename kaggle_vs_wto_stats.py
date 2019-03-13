from time import time, sleep

from kaggle_stats import non_regex_kaggle_split


kagglePath = "data/commodity_trade_statistics_data.csv"
wtoPath = "data/merchandise_values_annual_dataset.csv"

# for annual_export functions
annualExportKaggle = {}
annualExportWto = {}

# for countries functions
countriesKaggle = {}
countriesWto = {}


# Traverses and parses all of the provided Kaggle input into lists of the data.
# Calls each function in "functions" on each input line (passing the parsed lists as a parameter)
# order (all strings): country, year, comCode, comName, flow, usd, kg, quantity name, quantity, category
def traverse_kaggle(functions):
	tic = time()
	with open(kagglePath, "r") as kFile:
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
			m = non_regex_kaggle_split(line)
			if m:
				for f in functions:
					f(m)

			# get next line if there is one
			line = nextLine
			# if time() - tic > 20:
			# 	print("Early kaggle abort")
			# 	return


# Traverses and parses all of the provided wto input into lists of the data.
# Calls each function in "functions" on each input line (passing the parsed lists as a parameter)
def traverse_wto(functions):
	with open(wtoPath, "r") as wFile:
		# parse each line, skipping the first
		wFile.readline()
		line = wFile.readline()
		while line:
			split = non_regex_kaggle_split(line, 14)
			for f in functions:
				f(split)

			line = wFile.readline()


# Calculates the sum of exports, divided by year
def calc_annual_exports_kaggle(parsed):
	global annualExportKaggle
	isExport = parsed[4].startswith("E")
	if isExport:
		year = int(parsed[1])
		val = int(parsed[5])
		try:
			annualExportKaggle[year] = annualExportKaggle[year] + val
		except KeyError:
			annualExportKaggle[year] = val


# Calculates the sum of exports, divided by year
def calc_annual_exports_wto(parsed):
	global annualExportWto
	isExport = parsed[7].startswith("E")
	if isExport:
		year = int(parsed[8])
		val = float(parsed[10])
		try:
			annualExportWto[year] = annualExportWto[year] + val
		except KeyError:
			annualExportWto[year] = val


def print_annual_exports_compared():
	global annualExportWto, annualExportKaggle

	# Just do common years. WTO is bigger than the kaggle set
	keys = list(annualExportKaggle.keys())
	keys.sort()
	print("year, wto exports, kaggle/wto ratio")
	for key in keys:
		print(str(key) + ": " + str(annualExportWto[key]),
			  str(annualExportKaggle[key] / 1000000 / annualExportWto[key]))


def parse_countries_kaggle(parsed):
	global countriesKaggle
	country = parsed[0]
	countriesKaggle[country] = True


def parse_countries_wto(parsed):
	global countriesWto
	country = parsed[1]
	countriesWto[country] = True


# WIP not done for listing common and distinct countries in both sets
# def print_common_countries():
# 	global countriesWto, countriesKaggle
# 	wto = list(countriesWto.keys())
# 	kaggle = list(countriesKaggle.keys())
# 	for c in wto:



if __name__ == '__main__':
	tic = time()
	traverse_kaggle([calc_annual_exports_kaggle])
	traverse_wto([calc_annual_exports_wto])
	print_annual_exports_compared()

	toc = time()
	print("total processing time:", str(toc - tic), "seconds")
