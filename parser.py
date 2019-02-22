encoding = "ISO-8859-1"
inpath = "data/merchandise_values_annual_dataset.csv"


def main(encoding='utf-8',
         include_imports=True,
         include_exports=True,
         start_year=1950,
         end_year=2017):
    outpath = 'output-data/{}-{}-{}.tsv'
    if include_imports and include_exports:
        filename = 'imports_exports'
    if include_imports and not include_exports:
        filename = 'imports'
    if not include_imports and include_exports:
        filename = 'exports'

    outpath = outpath.format(filename, start_year, end_year)

    connections = []
    connectionValues = {}
    with open(inpath, 'r', encoding=encoding) as infile:
        lines = infile.readlines()[1:]

        for line in lines:
            line = line.split('","')
            if not start_year <= int(line[8]) <= end_year:
                continue
            conVal = float(line[10])

            # skip conns with value 0
            if conVal == 0:
                continue
            if include_exports:
                if line[7].startswith("Exports"):
                    newConn = (line[1], line[3])
                    if newConn not in connections:
                        connections.append(newConn)
                        connectionValues[newConn] = conVal
                    else:
                        connectionValues[newConn] = connectionValues[newConn] + conVal

            if include_imports:
                if line[7].startswith("Imports"):
                    newConn = [line[3], line[1]]
                    if newConn not in connections:
                        connections.append(newConn)
                        connectionValues[newConn] = conVal
                    else:
                        connectionValues[newConn] = connectionValues[newConn] + conVal

    with open(outpath, 'w+', encoding=encoding) as outfile:
        for i in range(4):
            outfile.write("#this is an empty line\n")
        for conn in connections:
            for item in conn:
                outfile.write(str(item) + "\t")
            outfile.write(str(connectionValues[conn]))
            outfile.write("\n")


if __name__ == '__main__':
    main(encoding, include_imports=False) #, start_year=2000, end_year=2000)
