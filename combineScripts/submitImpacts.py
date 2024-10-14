import os,sys
import ROOT
import numpy as np
from datetime import date
import mplhep as hep
import matplotlib.pyplot as plt

user = os.environ.get("USER")
today= date.today().strftime("%b-%d-%Y")

### if date ("MMM-DD-YYYY") is not specified, use today's date
inDate = today
outDate = today
thisDir = os.environ.get("PWD")
if len(sys.argv)>3:
    inDir=sys.argv[1]
    tag=sys.argv[2]
    model=sys.argv[3]
elif len(sys.argv)>2:
    inDir=sys.argv[1]
    tag=sys.argv[2]
else:
    inDir  = "%s/datacards_all_Sep-16-2024_2022_Iso1HighPt"%(thisDir)
    #inDir  = "%s/datacards_all_Sep-12-2024_2022"%(thisDir)
    tag = "Iso1HighPt"
    #tag = "_all"

# Options
unblind = False

# Output
outDir = "%s/impacts_%s"%(thisDir,outDate)
if unblind:
    outDir = outDir + "_unblind"
outDir = outDir + "/"
if not os.path.exists(outDir):
    os.makedirs(outDir)

# Select years
years = []
years.append("2022")

# Signals
sigModels = []
sigModels.append("HTo2ZdTo2mu2x")
#sigModels.append("ScenarioB1")

sigMasses = []
# All masses are: [0.5, 0.7, 1.5, 2.0, 2.5, 5.0, 6.0, 7.0, 8.0, 14.0, 16.0, 20.0, 22.0, 24.0, 30.0, 34.0, 40.0, 44.0, 50.0]
sigMasses = [2.0]
sigCTaus = [1, 10, 100]

# Injected for impacts
inj = [1, 5]
rmin = -20 # Always in between -3 and -15
rminmax = -3

# Command log:
cfile = open(outDir+'commands.txt', 'w')

# Loop over years, models, masses and ctaus to compute impacts:
for y in years:
    for s in sigModels:
        for m in sigMasses:
            for t in sigCTaus:
                for r in inj:
                    if r==0:
                        rmin = 0
                    elif r==1 and tag!="NonPointing":
                        rmin = -0.3
                    elif r==2 and tag!="NonPointing":
                        rmin = -1.5
                    card = "%s/card_combined_%s_M%.1f_ctau%i_%s.root"%(inDir,s,m,t,y)
                    masked = []
                    cfile.write('-------> IMPACTS for: Year=%s, Model=%s, Mass=%f, ctau=%i, r=%i \n'%(y,s,m,t,r))
                    cfile.write('\n>>\n')
                    for ch in range(1, 8+1): # Hardcoded (merged lxy's)
                        if r>0:
                            continue
                        # Open datacard
                        f = ROOT.TFile(card)
                        print("> Opened file: %s"%(card))
                        # Retrieve workspace from file
                        w = f.Get('w')
                        print("> Workspace contents:")
                        #w.Print()
                        # Retrieve signal normalization
                        nSig = w.obj("n_exp_binch%i_proc_signal"%ch).getVal()
                        # Retrieve background normalization
                        nBG = w.obj("n_exp_final_binch%i_proc_background"%ch).getVal()
                        # Close input file with workspace
                        f.Close()
                        print('Found numbers for channel ch%i:'%ch)
                        print('> nSig = %f'%nSig)
                        print('> nBG = %i'%nBG)
                        if (((abs(rminmax)+0.1)*nSig > (nBG+r*nSig))):
                            masked.append(ch)
                            continue
                        if r==0 and nBG < 1:
                            masked.append(ch)
                            continue
                        rmin = min([rminmax, max([rmin, -(nBG+r*nSig)/(nSig) + 0.2])])
                    print('Mask:')
                    print(masked)
                    # Define the mask:
                    if len(masked) > 0:
                        mask = '--setParameters '
                        for ch in masked:
                            mask = mask + 'mask_ch%i=1,'%ch
                    else:
                        mask = ''
                    mask = mask[:-1] # remove last coma
                    # Define workdir
                    subDir = '%s/%s_M%.1f_ctau%i_%s'%(outDir,s,m,t,y)
                    if not os.path.exists(subDir):
                        os.mkdir(subDir)
                    # Options
                    if unblind:
                        options = "--cminDefaultMinimizerStrategy 0"
                    else:
                        options = "--cminDefaultMinimizerStrategy 0 -t -1"
                    name = "_%s_M%.1f_ctau%i_%s_t%i"%(s,m,t,tag,r)
                    # Initial fit:
                    print("combine -M FitDiagnostics %s %s --expectSignal %i -n %s -m %.0f --forceRecreateNLL --rMin %.2f %s"%(card,options,r,name,m,rmin,mask))
                    os.system("combine -M FitDiagnostics %s %s --expectSignal %i -n %s -m %.0f --forceRecreateNLL --rMin %.2f %s"%(card,options,r,name,m,rmin,mask))
                    cfile.write("combine -M FitDiagnostics %s %s --expectSignal %i -n %s -m %.0f --forceRecreateNLL --rMin %.2f %s"%(card,options,r,name,m,rmin,mask))
                    cfile.write("\n>>\n")
                    print("python3 $CMSSW_BASE/src/HiggsAnalysis/CombinedLimit/test/diffNuisances.py -a fitDiagnostics%s.root -g plots%s.root >& fitResults%s.txt"%(name,name,name))
                    os.system("python3 $CMSSW_BASE/src/HiggsAnalysis/CombinedLimit/test/diffNuisances.py -a fitDiagnostics%s.root -g plots%s.root >& fitResults%s.txt"%(name,name,name))
                    cfile.write("python3 $CMSSW_BASE/src/HiggsAnalysis/CombinedLimit/test/diffNuisances.py -a fitDiagnostics%s.root -g plots%s.root >& fitResults%s.txt"%(name,name,name))
                    cfile.write("\n>>\n")
                    #
                    print("combineTool.py -M Impacts -d %s %s --expectSignal %i -n %s -m %.0f --doInitialFit --rMin %.2f %s"%(card,options,r,name,m,rmin,mask))
                    os.system("combineTool.py -M Impacts -d %s %s --expectSignal %i -n %s -m %.0f --doInitialFit --rMin %.2f %s"%(card,options,r,name,m,rmin,mask))
                    cfile.write("combineTool.py -M Impacts -d %s %s --expectSignal %i -n %s -m %.0f --doInitialFit --rMin %.2f %s"%(card,options,r,name,m,rmin,mask))
                    cfile.write("\n>>\n")
                    #
                    print("combineTool.py -M Impacts -d %s -o impacts%s.json %s --expectSignal %i -n %s -m %.0f --doFits --parallel 20 --task-name %s %s  >& /dev/null"%(card,name,options,r,name,m,name,mask))
                    os.system("combineTool.py -M Impacts -d %s -o impacts%s.json %s --expectSignal %i -n %s -m %.0f --rMin %.2f --doFits --parallel 20 --task-name %s %s >& /dev/null"%(card,name,options,r,name,m,rmin,name,mask))
                    cfile.write("combineTool.py -M Impacts -d %s -o impacts%s.json %s --expectSignal %i -n %s -m %.0f --rMin %.2f --doFits --parallel 20 --task-name %s %s >& /dev/null"%(card,name,options,r,name,m,rmin,name,mask))
                    cfile.write("\n>>\n")
                    #
                    print("combineTool.py -M Impacts -d %s -m %.0f -n %s -o impacts%s.json"%(card,m,name,name))
                    os.system("combineTool.py -M Impacts -d %s -m %.0f -n %s -o impacts%s.json"%(card,m,name,name))
                    cfile.write("combineTool.py -M Impacts -d %s -m %.0f -n %s -o impacts%s.json"%(card,m,name,name))
                    cfile.write("\n>>\n")
                    #
                    print("plotImpacts.py -i impacts%s.json -o impacts%s"%(name,name))
                    os.system("plotImpacts.py -i impacts%s.json -o impacts%s"%(name,name))
                    cfile.write("plotImpacts.py -i impacts%s.json -o impacts%s"%(name,name))
                    cfile.write("\n>>\n")
                    cfile.write("\n###\n")
                    #
                    # Save roots:
                    os.system('mv fitDiagnostics%s.root %s'%(name,subDir))
                    os.system('mv higgsCombine%s.FitDiagnostics.mH%.0f.root %s'%(name,m,subDir))
                    os.system('mv fitResults%s.txt %s'%(name,subDir))
                    os.system('mv higgsCombine_initialFit_%s.MultiDimFit.mH%.0f.root %s'%(name,m,subDir))
                    os.system('mv higgsCombine_paramFit_%s_*.MultiDimFit.mH%.0f.root %s'%(name,m,subDir))
                    os.system('mv plots%s.root %s'%(name,subDir))
                    os.system('mv impacts%s.json %s'%(name,subDir))
                    os.system('mv impacts%s.pdf %s'%(name,subDir))
                    os.system('cp utils/index.php %s'%(subDir))

cfile.close()
