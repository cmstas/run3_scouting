import os
# This is a very ugly script to read the datasets

input_ = open('dqcd_2022.txt', 'r')

list2022 = []
list2022_postEE = []

for line in input_.readlines():
    if 'NOT DONE' in line:
        continue
    # This is for 2022
    if 'jleonhol' in line:
        info = line.split(':')[1]
        info2 = info.split(',')[0]
        info3 = info2.replace(' ', '')
        info4 = info3.replace('"', '')
        list2022.append(info4)
    if 'tafoyava' in line:
        info = line.split(':')[1]
        info2 = info.split(',')[0]
        info3 = info2.replace(' ', '')
        info4 = info3.replace('"', '')
        list2022_postEE.append(info4)
        
with open('datasets_dqcd_2022.txt', 'w') as f:
    for x in list2022:
        f.write(x)
        f.write('\n')
    f.close()
with open('datasets_dqcd_2022postEE.txt', 'w') as f:
    for x in list2022_postEE:
        f.write(x)
        f.write('\n')
    f.close()
        