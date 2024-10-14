import os,sys
import ROOT
from datetime import date

user = os.environ.get("USER")
today= date.today().strftime("%b-%d-%Y")
thisDir = os.environ.get("PWD")

if len(sys.argv)>2:
    inDir1 = sys.argv[1]
    inDir2 = sys.argv[2]
else:
    exit

outDir = ("%s/datacards_all_"%(thisDir))+today+"_allEras"
if not os.path.exists(outDir):
    os.makedirs(outDir)

# Loop in cards of dir 1, look for the equivalent in dir 2 and merge:
for card1 in os.listdir(inDir1):
    if '.txt' not in card1 or 'combine' not in card1:
        continue
    card_name1 = ''
    for portion in card1.split('_')[:-1]:
        card_name1 += (portion + '_')
    for card2 in os.listdir(inDir2):
        if '.txt' not in card2:
            continue
        card_name2 = ''
        for portion in card2.split('_')[:-1]:
            card_name2 += (portion + '_')
        if card_name1==card_name2:
            print("COMBINING ", card_name1)
            print("combineCards.py -S %s/%s %s/%s > %s/%sallEras.txt "%(inDir1, card1, inDir2, card2, outDir, card_name1))
            os.system("combineCards.py -S %s/%s %s/%s > %s/%sallEras.txt "%(inDir1, card1, inDir2, card2, outDir, card_name1))
            os.system("text2workspace.py %s/%sallEras.txt"%(outDir, card_name1))
            break
