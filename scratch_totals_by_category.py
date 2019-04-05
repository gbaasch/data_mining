inpath = "data/merchandise_values_annual_dataset.csv"

categories = ['Total merchandise', 'Agricultural products', 'Manufactures',
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
				'Miscellaneous manufactures', 'Other transport equipment', 'Fish']

encoding = "ISO-8859-1"


def print_to_file(cat_dict_import, cat_dict_export):
	with open("category_totals.tsv", "w+", encoding="ISO-8859-1") as outfile:
		for key in cat_dict_export.keys():
			outfile.write(key + "\t" + str(cat_dict_export[key]) + "\t")
			if key in cat_dict_import:
				outfile.write(str(cat_dict_import[key]) + "\n")
			else:
				outfile.write("0\n")


def main(encoding):
	category_dict_import = {}
	category_dict_export = {}
	importTotal = 0
	exportTotal = 0
	with open(inpath, 'r', encoding=encoding) as infile:
		lines = infile.readlines()[1:]

		for line in lines:
			line = line.split('","')
			import_type_val = category_dict_import.get(line[5])

			if line[7].startswith("Exports"):
				#if line[0].startswith("\"AF"):
				exportTotal += float(line[-4])
				export_type_val = category_dict_export.get(line[5])
				export_type_val = 0 if export_type_val is None else export_type_val + float(line[-4])
				category_dict_export[line[5]] = export_type_val
			if line[7].startswith("Imports"):
				#if line[2].startswith("\"AF"):
				importTotal += float(line[-4])
				import_type_val = category_dict_import.get(line[5])
				import_type_val = 0 if import_type_val is None else import_type_val + float(line[-4])
				category_dict_import[line[5]] = import_type_val

	# for inCon in imports:
	# 	if inCon not in exports:
	# 		print(inCon)
	#
	# print(importTotal)
	# print(exportTotal)
	for key in categories:
		export = 0 if category_dict_export.get(key) is None else category_dict_export.get(key)
		importt = 0 if category_dict_import.get(key) is None else category_dict_import.get(key)
		print(key + ' ====================')
		if export:
			print("ratio of missing vals in import: ", (export - importt) / export)
			print("ratio of exports to total: ", export / exportTotal)
		else:
			print("does not exist")
		print("\n")

	print(category_dict_export)
	print(category_dict_import)
	print_to_file(category_dict_import, category_dict_export)


if __name__ == '__main__':
	main(encoding)
