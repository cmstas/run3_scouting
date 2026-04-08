import os

file_ = open('cpp/input/centralDatasets.txt','r')

for l in file_.readlines():
    if 'Signal_BToPhi-' in l and 'central' in l and l[0]!='#':
        os.system("""echo "(SCOUTINGOUTPUTDIR) 2022 %s 0 100 1 1" >> input.txt"""%(l.split(',')[0]))

file_.close()
