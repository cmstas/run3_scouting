import os

def parse_table(table_name):
    lines = []
    with open(table_name, 'r') as f:
        for line in f.readlines():
            content = line.split('\t')
            while '' in content:
                content.remove('')
            content[-1] = content[-1].strip('\n')
            lines.append(content)
    return lines



### test parse_table()
info = parse_table('model-tables/HiggsedDarkPhoton_BrTableData.txt')
