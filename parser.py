encoding = "ISO-8859-1"
inpath = "data/merchandise_values_annual_dataset.csv"


def main(encoding='utf-8', include_imports=True, include_exports=True):
    if include_imports and include_exports:
        outpath = 'output-data/imports_exports.tsv'
    if include_imports and not include_exports:
        outpath = 'output-data/imports.tsv'
    if not include_imports and include_exports:
        outpath = 'output-data/exports.tsv'

    connections = []
    with open(inpath, 'r', encoding=encoding) as infile:
        lines = infile.readlines()[1:]

        for line in lines:
            line = line.split(',')
            if include_exports:
                if line[7].startswith("\"Exports"):
                    newConn = [line[1], line[3]]
                    if newConn not in connections:
                        connections.append(newConn)

            if include_imports:
                if line[7].startswith("\"Imports"):
                    newConn = [line[3], line[1]]
                    if newConn not in connections:
                        connections.append(newConn)

    with open(outpath, 'w+', encoding=encoding) as outfile:
        for i in range(4):
            outfile.write("#this is an empty line\n")
        for conn in connections:
            for item in conn:
                outfile.write(str(item) + "\t")
            outfile.write("\n")


if __name__ == '__main__':
    main(encoding, include_exports=False)
