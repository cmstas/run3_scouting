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

# Systematics to combine
systematics = []
systematics.append(['CMS_eff_sel','CMS_eff_sel_2022','CMS_eff_sel_2023'])
systematics.append(['CMS_eff_trg','CMS_eff_trg_2022','CMS_eff_trg_2023'])
systematics.append(['mcstat_ch','stat22_ch','stat23_ch'])

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
            tomerge_card1 = 'tomerge_' + card1
            tomerge_card2 = 'tomerge_' + card2
            os.system('cp %s/%s %s/%s'%(inDir1, card1, inDir1, tomerge_card1))
            os.system('cp %s/%s %s/%s'%(inDir2, card2, inDir2, tomerge_card2))
            # Correlate systematics
            os.system("sed -i 's/CMS_eff_sel_2022/CMS_eff_sel     /g' %s/%s"%(inDir1, card1))
            os.system("sed -i 's/CMS_eff_sel_2023/CMS_eff_sel     /g' %s/%s"%(inDir2, card2))
            os.system("sed -i 's/CMS_eff_trg_2022/CMS_eff_trg     /g' %s/%s"%(inDir1, card1))
            os.system("sed -i 's/CMS_eff_trg_2023/CMS_eff_trg     /g' %s/%s"%(inDir2, card2))
            # Uncorrelate systematics
            os.system("sed -i 's/mcstat_ch/stat22_ch/g' %s/%s"%(inDir1, card1))
            os.system("sed -i 's/mcstat_ch/stat23_ch/g' %s/%s"%(inDir2, card2))
            print("COMBINING ", card_name1)
            print("combineCards.py -S %s/%s %s/%s > %s/%sallEras.txt "%(inDir1, card1, inDir2, card2, outDir, card_name1))
            os.system("combineCards.py -S %s/%s %s/%s > %s/%sallEras.txt "%(inDir1, tomerge_card1, inDir2, tomerge_card2, outDir, card_name1))
            os.system("text2workspace.py %s/%sallEras.txt"%(outDir, card_name1))
            break
