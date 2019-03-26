infile = '../output-data/exports.tsv'

reporter_code = 0
reporter_description = 1
partner_code = 2
partner_description = 3
indicator_code = 4
indicator_description = 5
flow_Code = 6
flow_Description = 7
year = 8
unit = 9
value = 10
flag = 11
source_Description = 12
note = 13

if __name__ == '__main__':
    with open(infile, encoding="ISO-8859-1") as f:
        lines = f.readlines()
        for line in lines[4:]:
