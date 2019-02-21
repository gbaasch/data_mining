inpath = "data/merchandise_values_annual_dataset.csv"
outpath = "data/output.tsv"


def main():
	connections = []
	with open(inpath, 'r') as infile:
		lines = infile.readlines()[1:]

		for line in lines:
			line = line.split(',')
			if line[7].startswith("\"Exports"):
				newConn = [line[1], line[3]]
				if newConn not in connections:
					connections.append(newConn)
			if line[7].startswith("\"Imports"):
				newConn = [line[3], line[1]]
				if newConn not in connections:
					connections.append(newConn)

	with open(outpath, 'w+') as outfile:
		for i in range(4):
			outfile.write("#this is an empty line\n")
		for conn in connections:
			for item in conn:
				outfile.write(str(item) + "\t")
			outfile.write("\n")


if __name__ == '__main__':
	main()
