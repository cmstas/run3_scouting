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
mass = -99
ctau = -99
model = ""
outDir = "output"
rinj = 5
limFile = "/ceph/cms/store/user/fernance/Run3ScoutingOutput/limits_Aug-01-2024_2022/limits_HTo2ZdTo2mu2x_2022.txt"
if len(sys.argv)>1:
    inDir=sys.argv[1]
    if len(sys.argv)>2:
        outDir=sys.argv[2]
        if len(sys.argv)>3:
            limFile=sys.argv[3]
            if len(sys.argv)>4:
                model=sys.argv[4]
                if len(sys.argv)>5:
                    rinj=int(sys.argv[5])
                if len(sys.argv)>6:
                    mass=float(sys.argv[6])
                    if len(sys.argv)>7:
                        ctau=int(sys.argv[7])

wsname = "w"
thisDir = os.environ.get("PWD")
inDir  = "%s/%s"%(thisDir,inDir)

biasCombination = True
biasPerChannel = False
biasPerPDF = False
nToysPerChannel = 300
nToysPerCombination = 300
biasSummary = False
checkIndividualPDFs = False
plotEnvelope = False
redoCombinedCard = True

useCategorizedSignal = True
useCategorizedBackground = True

rs = [0,1,2]
rs = [rinj]
#rs.append(3)

if outDir=="":
    outDir = "%s/limits_all_%s_bias/"%(thisDir,outDate)
if not os.path.exists(outDir):
    os.makedirs(outDir)

dNames = []
"""
dNames.append("d_FourMu_sep")
dNames.append("d_Dimuon_lxy0p0to0p2_iso1_pthigh")
dNames.append("d_Dimuon_lxy0p2to1p0_iso1_pthigh")
dNames.append("d_Dimuon_lxy1p0to2p4_iso1_pthigh")
dNames.append("d_Dimuon_lxy2p4to3p1_iso1_pthigh")
dNames.append("d_Dimuon_lxy3p1to7p0_iso1_pthigh")
dNames.append("d_Dimuon_lxy7p0to11p0_iso1_pthigh")
dNames.append("d_Dimuon_lxy11p0to16p0_iso1_pthigh")
dNames.append("d_Dimuon_lxy16p0to70p0_iso1_pthigh")
dNames.append("d_Dimuon_lxy0p0to0p2_iso1_ptlow")
dNames.append("d_Dimuon_lxy0p2to1p0_iso1_ptlow")
dNames.append("d_Dimuon_lxy1p0to2p4_iso1_ptlow")
dNames.append("d_Dimuon_lxy2p4to3p1_iso1_ptlow")
dNames.append("d_Dimuon_lxy3p1to7p0_iso1_ptlow")
dNames.append("d_Dimuon_lxy7p0to11p0_iso1_ptlow")
dNames.append("d_Dimuon_lxy11p0to16p0_iso1_ptlow")
dNames.append("d_Dimuon_lxy16p0to70p0_iso1_ptlow")
dNames.append("d_Dimuon_lxy0p0to0p2_iso0_pthigh")
dNames.append("d_Dimuon_lxy0p2to1p0_iso0_pthigh")
dNames.append("d_Dimuon_lxy1p0to2p4_iso0_pthigh")
dNames.append("d_Dimuon_lxy2p4to3p1_iso0_pthigh")
dNames.append("d_Dimuon_lxy3p1to7p0_iso0_pthigh")
dNames.append("d_Dimuon_lxy7p0to11p0_iso0_pthigh")
dNames.append("d_Dimuon_lxy11p0to16p0_iso0_pthigh")
dNames.append("d_Dimuon_lxy16p0to70p0_iso0_pthigh")
"""

dNames.append("d_FourMu_sep")
dNames.append("d_FourMu_osv")
dNames.append("d_Dimuon_lxy0p0to0p2_iso0_ptlow")
dNames.append("d_Dimuon_lxy0p0to0p2_iso0_pthigh")
dNames.append("d_Dimuon_lxy0p0to0p2_iso1_ptlow")
dNames.append("d_Dimuon_lxy0p0to0p2_iso1_pthigh")
dNames.append("d_Dimuon_lxy0p2to1p0_iso0_ptlow")
dNames.append("d_Dimuon_lxy0p2to1p0_iso0_pthigh")
dNames.append("d_Dimuon_lxy0p2to1p0_iso1_ptlow")
dNames.append("d_Dimuon_lxy0p2to1p0_iso1_pthigh")
dNames.append("d_Dimuon_lxy1p0to2p4_iso0_ptlow")
dNames.append("d_Dimuon_lxy1p0to2p4_iso0_pthigh")
dNames.append("d_Dimuon_lxy1p0to2p4_iso1_ptlow")
dNames.append("d_Dimuon_lxy1p0to2p4_iso1_pthigh")
dNames.append("d_Dimuon_lxy2p4to3p1_iso0_ptlow")
dNames.append("d_Dimuon_lxy2p4to3p1_iso0_pthigh")
dNames.append("d_Dimuon_lxy2p4to3p1_iso1_ptlow")
dNames.append("d_Dimuon_lxy2p4to3p1_iso1_pthigh")
dNames.append("d_Dimuon_lxy3p1to7p0_iso0_ptlow")
dNames.append("d_Dimuon_lxy3p1to7p0_iso0_pthigh")
dNames.append("d_Dimuon_lxy3p1to7p0_iso1_ptlow")
dNames.append("d_Dimuon_lxy3p1to7p0_iso1_pthigh")
dNames.append("d_Dimuon_lxy7p0to11p0_iso0_ptlow")
dNames.append("d_Dimuon_lxy7p0to11p0_iso0_pthigh")
dNames.append("d_Dimuon_lxy7p0to11p0_iso1_ptlow")
dNames.append("d_Dimuon_lxy7p0to11p0_iso1_pthigh")
dNames.append("d_Dimuon_lxy11p0to16p0_iso0_ptlow")
dNames.append("d_Dimuon_lxy11p0to16p0_iso0_pthigh")
dNames.append("d_Dimuon_lxy11p0to16p0_iso1_ptlow")
dNames.append("d_Dimuon_lxy11p0to16p0_iso1_pthigh")
dNames.append("d_Dimuon_lxy16p0to70p0_iso0_ptlow")
dNames.append("d_Dimuon_lxy16p0to70p0_iso0_pthigh")
dNames.append("d_Dimuon_lxy16p0to70p0_iso1_ptlow")
dNames.append("d_Dimuon_lxy16p0to70p0_iso1_pthigh")
#dNames.append("d_Dimuon_lxy0p0to0p2_non-pointing")
#dNames.append("d_Dimuon_lxy0p2to1p0_non-pointing")
#dNames.append("d_Dimuon_lxy1p0to2p4_non-pointing")
#dNames.append("d_Dimuon_lxy2p4to3p1_non-pointing")
#dNames.append("d_Dimuon_lxy3p1to7p0_non-pointing")
#dNames.append("d_Dimuon_lxy7p0to11p0_non-pointing")
#dNames.append("d_Dimuon_lxy11p0to16p0_non-pointing")
#dNames.append("d_Dimuon_lxy16p0to70p0_non-pointing")


years = []
###
years.append("2023")

# Signals
sigModels = []
sigModels.append("HTo2ZdTo2mu2x")

sigMasses = []
#sigMasses = [0.5, 0.7, 1.5, 2.0, 2.5, 5.0, 6.0, 7.0, 8.0, 14.0, 16.0, 20.0, 22.0, 24.0, 30.0, 34.0, 40.0, 44.0, 50.0]
sigMasses = [5.0, 6.0, 7.0, 8.0, 14.0, 16.0, 20.0, 22.0, 24.0, 30.0, 34.0, 40.0, 44.0, 50.0]
sigMasses = [5.0]
#sigMasses = [5.0, 7.0]
#sigMasses = [5.0]
#sigCTaus = [1, 10, 100]
sigCTaus = [10]
if mass > 0:
    sigMasses = [mass]
if ctau > 0:
    sigCTaus = [ctau]


mean = 0.0
sigma = 0.0
for y in years:
    for s in sigModels:
        meanfit  = dict()
        sigmafit = dict()
        namefit  = dict()
        ### Excluded channels for combination
        if s=='HTo2ZdTo2mu2x':
            excl_chs = [2, 35, 36, 37, 38, 39, 40, 41, 42]
        # Loop over masses
        for m in sigMasses:
            meanfit[m]  = dict()
            sigmafit[m] = dict()
            namefit[m]  = dict()
            # Loop over lifetimes
            for t in sigCTaus:
                if (t == 1):
                    nToysPerChannel = 100
                    nToysPerCombination = 100
                if (t == 10):
                    nToysPerChannel = 200
                    nToysPerCombination = 200
                if (t == 100):
                    nToysPerChannel = 300
                    nToysPerCombination = 300
                # Find limit for given (mass,ctau) point
                expLim = 1.0
                if os.path.exists(limFile):
                    print('> Limit file opened successfully')
                    flim = open(limFile,"r")
                    for ll in flim.readlines():
                        if ll.split(",")[1]!=str(m) or ll.split(",")[2]!=str(t):
                            continue
                        expLim=float(ll.split(",")[8]) # Expected limit
                        break
                    flim.close()
                    print('> Found expected limit %f'%(expLim))
                else:
                    print('> Expected limit not found')
                # Define model identifier
                modelTag = ""
                if s=="HTo2ZdTo2mu2x":
                    modelTag = "Signal_HTo2ZdTo2mu2x_MZd-%.3f_ctau-%.2fmm"%(m, t)
                ### Add more models when ready
                combinedCards = ""
                # Loop over card channels:
                for d in dNames:
                    meanfit[m][d]  = dict()
                    sigmafit[m][d] = dict()
                    namefit[m][d]  = dict()
                    #finame = "%s/%s_%s_%s_workspace.root"%(fitDir,d,modelTag,y)
                    binidx=-1
                    if d=="d_FourMu_sep":
                        binidx=1
                    elif d=="d_FourMu_osv":
                        binidx=2
                    elif d=="d_Dimuon_lxy0p0to0p2_iso0_ptlow":
                        binidx=3
                    elif d=="d_Dimuon_lxy0p0to0p2_iso0_pthigh":
                        binidx=4
                    elif d=="d_Dimuon_lxy0p0to0p2_iso1_ptlow":
                        binidx=5
                    elif d=="d_Dimuon_lxy0p0to0p2_iso1_pthigh":
                        binidx=6
                    elif d=="d_Dimuon_lxy0p2to1p0_iso0_ptlow":
                        binidx=7
                    elif d=="d_Dimuon_lxy0p2to1p0_iso0_pthigh":
                        binidx=8
                    elif d=="d_Dimuon_lxy0p2to1p0_iso1_ptlow":
                        binidx=9
                    elif d=="d_Dimuon_lxy0p2to1p0_iso1_pthigh":
                        binidx=10
                    elif d=="d_Dimuon_lxy1p0to2p4_iso0_ptlow":
                        binidx=11
                    elif d=="d_Dimuon_lxy1p0to2p4_iso0_pthigh":
                        binidx=12
                    elif d=="d_Dimuon_lxy1p0to2p4_iso1_ptlow":
                        binidx=13
                    elif d=="d_Dimuon_lxy1p0to2p4_iso1_pthigh":
                        binidx=14
                    elif d=="d_Dimuon_lxy2p4to3p1_iso0_ptlow":
                        binidx=15
                    elif d=="d_Dimuon_lxy2p4to3p1_iso0_pthigh":
                        binidx=16
                    elif d=="d_Dimuon_lxy2p4to3p1_iso1_ptlow":
                        binidx=17
                    elif d=="d_Dimuon_lxy2p4to3p1_iso1_pthigh":
                        binidx=18
                    elif d=="d_Dimuon_lxy3p1to7p0_iso0_ptlow":
                        binidx=19
                    elif d=="d_Dimuon_lxy3p1to7p0_iso0_pthigh":
                        binidx=20
                    elif d=="d_Dimuon_lxy3p1to7p0_iso1_ptlow":
                        binidx=21
                    elif d=="d_Dimuon_lxy3p1to7p0_iso1_pthigh":
                        binidx=22
                    elif d=="d_Dimuon_lxy7p0to11p0_iso0_ptlow":
                        binidx=23
                    elif d=="d_Dimuon_lxy7p0to11p0_iso0_pthigh":
                        binidx=24
                    elif d=="d_Dimuon_lxy7p0to11p0_iso1_ptlow":
                        binidx=25
                    elif d=="d_Dimuon_lxy7p0to11p0_iso1_pthigh":
                        binidx=26
                    elif d=="d_Dimuon_lxy11p0to16p0_iso0_ptlow":
                        binidx=27
                    elif d=="d_Dimuon_lxy11p0to16p0_iso0_pthigh":
                        binidx=28
                    elif d=="d_Dimuon_lxy11p0to16p0_iso1_ptlow":
                        binidx=29
                    elif d=="d_Dimuon_lxy11p0to16p0_iso1_pthigh":
                        binidx=30
                    elif d=="d_Dimuon_lxy16p0to70p0_iso0_ptlow":
                        binidx=31
                    elif d=="d_Dimuon_lxy16p0to70p0_iso0_pthigh":
                        binidx=32
                    elif d=="d_Dimuon_lxy16p0to70p0_iso1_ptlow":
                        binidx=33
                    elif d=="d_Dimuon_lxy16p0to70p0_iso1_pthigh":
                        binidx=34
                    elif d=="d_Dimuon_lxy0p0to0p2_non-pointing":
                        binidx=35
                    elif d=="d_Dimuon_lxy0p2to1p0_non-pointing":
                        binidx=36
                    elif d=="d_Dimuon_lxy1p0to2p4_non-pointing":
                        binidx=37
                    elif d=="d_Dimuon_lxy2p4to3p1_non-pointing":
                        binidx=38
                    elif d=="d_Dimuon_lxy3p1to7p0_non-pointing":
                        binidx=39
                    elif d=="d_Dimuon_lxy7p0to11p0_non-pointing":
                        binidx=40
                    elif d=="d_Dimuon_lxy11p0to16p0_non-pointing":
                        binidx=41
                    elif d=="d_Dimuon_lxy16p0to70p0_non-pointing":
                        binidx=42    
                    # Exclude if channels is not considered in the model:
                    if binidx in excl_chs:
                        continue
                    # Define categories
                    catExtS = ""
                    catExtB = ""
                    if useCategorizedSignal:
                        catExtS = "_ch%d_%s"%(binidx,y)
                    if useCategorizedBackground:
                        catExtB = "_ch%d_%s"%(binidx,y)
                    # Open input file with workspace
                    card = "%s/card_ch%d_%s_M%.3f_ctau%.2f_%s.root"%(inDir,binidx,s,m,t,y)
                    print("> Reading card: %s"%(card))
                    f = ROOT.TFile(card)
                    print("> Opened file: %s"%(card))
                    # Retrieve workspace from file
                    w = f.Get(wsname)
                    #print("> Workspace contents:")
                    #w.Print()
                    # Retrieve signal normalization
                    #nSig = w.var("signalNorm%s"%catExtS).getValV() # Signal should be already normalized in the RooDataSet
                    nSig = w.function("n_exp_binch%i_proc_signal"%(binidx)).getVal()
                    # Retrieve background normalization
                    #nBG = w.var("roomultipdf%s_norm"%catExtB).getValV()
                    nBG = w.function("n_exp_final_binch%i_proc_background"%(binidx)).getVal()
                    # Retrieve (number of) PDFs in envelope
                    nPDF = w.cat("pdf_index%s"%catExtB).numTypes()
                    pdfnames = []
                    numpars = []
                    pdfs = w.pdf("shapeBkg_background_ch%i"%(binidx))
                    for p in range(nPDF):
                        numpars.append(w.pdf(pdfs.getPdf(p).GetName()).getVariables().getSize()-1)
                        if "exponential" in pdfs.getPdf(p).GetName():
                            pdfnames.append("Exponential")
                        elif "powerlaw" in pdfs.getPdf(p).GetName():
                            pdfnames.append("Power-law")
                        elif "bernstein" in pdfs.getPdf(p).GetName():
                            pdfnames.append("Bernstein<%d>"%(numpars[p]))
                        else:
                            pdfnames.append("Uniform")
                    pdfnames.append("Envelope")
                    # Retrieve range
                    if 'Dimuon' in d:
                        maxm = w.var("mfit").getMax()
                        minm = w.var("mfit").getMin()
                    else:
                        maxm = w.var("m4fit").getMax()
                        minm = w.var("m4fit").getMin()
                    mrange = abs(maxm-minm)
                    # Close input file with workspace
                    f.Close()
                    # Get limit on r:
                    options="--cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_freezeDisassociatedParams --toysFrequentist --bypassFrequentist --robustFit 1"
                    #options=options+" --X-rtd TMCSO_PseudoAsimov=5000"
                    #options=options+"--X-rtd TMCSO_AdaptivePseudoAsimov=1"
                    # Get r expected for one bin: 
                    rLimOneBin = -1.0
                    rLimExpOneBin = -1.0
                    os.system("combine -M AsymptoticLimits -d %s --cminDefaultMinimizerStrategy 0 -v 0 -n _temp_ch%i > log_asym_ch%i.txt"%(card,binidx,binidx))
                    flob = open("log_asym_ch%i.txt"%(binidx),"r")
                    for ll in flob.readlines():
                        if "Expected 97" in ll:
                            rLimOneBin = float(ll.split()[len(ll.split())-1])
                        if "Expected 50" in ll:
                            rLimExpOneBin = float(ll.split()[len(ll.split())-1])
                    flob.close()
                    os.system("rm log_asym_ch%i.txt"%(binidx))
                    os.system("rm higgsCombine_temp_ch%i.AsymptoticLimits.mH120.root"%(binidx))
                    print("Using an expected +2sigma limit per bin of %f"%(rLimOneBin))
                    print("The expected limit for this bin is %f"%(rLimExpOneBin))
                    print("The expected signal in this bin is %e"%(nSig))
                    print("The measured background in this bin is %i"%(nBG))
                    if (nSig < 1e-6) or (rLimOneBin < 0) or ((nBG**0.5)/nSig > 10): # Selects significant regions: 10 for 0p1 (100 fb) and 100 for 0p01 (10 fb)
                        print("Excluding channel: %i"%(binidx))
                        continue
                    else:
                        print("Accepting channel: %i"%(binidx))
                    ### Evaluate -2dLL for envelope
                    extra = ""
                    #extra = extra+" --X-rtd TMCSO_PseudoAsimov=10000"
                    if plotEnvelope:
                        #print("combine -M MultiDimFit -d %s -P r --algo grid --saveNLL --forceRecreateNLL -n _%s_envelope%s -m %s --rMin -1 --rMax 3 --setParameterRanges r=-0.3,3 --X-rtd REMOVE_CONSTANT_ZERO_POINT=1 --setParameters myIndex=-1 --expectSignal 0 -t -1 --points 90 --cminDefaultMinimizerStrategy 0 --toysFrequentist --bypassFrequentist --robustFit 1 --X-rtd MINIMIZER_freezeDisassociatedParams %s"%(card,s,catExtB,m,extra))
                        #os.system("combine -M MultiDimFit -d %s -P r --algo grid --saveNLL --forceRecreateNLL -n _%s_envelope%s -m %s --rMin -1 --rMax 3 --setParameterRanges r=-0.3,3 --X-rtd REMOVE_CONSTANT_ZERO_POINT=1 --setParameters myIndex=-1 --expectSignal 0 -t -1 --points 90 --cminDefaultMinimizerStrategy 0 --toysFrequentist --bypassFrequentist --robustFit 1 --X-rtd MINIMIZER_freezeDisassociatedParams %s"%(card,s,catExtB,m,extra))
                        print("combine -M MultiDimFit -d %s -P r --algo grid --saveNLL --forceRecreateNLL -n _%s_envelope%s -m %s --rMin -1 --rMax 3 --setParameterRanges r=-0.3,3 --X-rtd REMOVE_CONSTANT_ZERO_POINT=1 --expectSignal 0 -t -1 --points 90 --cminDefaultMinimizerStrategy 0 --toysFrequentist --bypassFrequentist --robustFit 1 --X-rtd MINIMIZER_freezeDisassociatedParams %s"%(card,s,catExtB,m,extra))
                        os.system("combine -M MultiDimFit -d %s -P r --algo grid --saveNLL --forceRecreateNLL -n _%s_envelope%s -m %s --rMin -1 --rMax 3 --setParameterRanges r=-0.3,3 --X-rtd REMOVE_CONSTANT_ZERO_POINT=1 --expectSignal 0 -t -1 --points 90 --cminDefaultMinimizerStrategy 0 --toysFrequentist --bypassFrequentist --robustFit 1 --X-rtd MINIMIZER_freezeDisassociatedParams %s"%(card,s,catExtB,m,extra))
                    fnmultidim = []
                    combinedCards += (card.replace('.root','.txt') + " ")
                    for rn,r in enumerate(rs):
                        meanfit[m][d][r]  = []
                        sigmafit[m][d][r] = []
                        namefit[m][d][r]  = []
                        fnfitdiag = []
                        for p in range(nPDF):
                    
                            ### Evaluate -2dLL per PDF
                            if rn==0 and plotEnvelope:
                                print("combine -M MultiDimFit -d %s -P r --algo grid --saveNLL --forceRecreateNLL --freezeParameters pdf_index%s --setParameters pdf_index%s=%d -n _%s_index%d%s -m %s --rMin -1 --rMax 3 --setParameterRanges r=-0.3,3 --X-rtd REMOVE_CONSTANT_ZERO_POINT=1 --expectSignal 0 -t -1 --points 90 --cminDefaultMinimizerStrategy 0 --toysFrequentist --bypassFrequentist --robustFit 1 --X-rtd MINIMIZER_freezeDisassociatedParams %s"%(card,catExtB,catExtB,p,s,p,catExtB,m,extra))
                                os.system("combine -M MultiDimFit -d %s -P r --algo grid --saveNLL --forceRecreateNLL --freezeParameters pdf_index%s --setParameters pdf_index%s=%d -n _%s_index%d%s -m %s --rMin -1 --rMax 3 --setParameterRanges r=-0.3,3 --X-rtd REMOVE_CONSTANT_ZERO_POINT=1 --expectSignal 0 -t -1 --points 90 --cminDefaultMinimizerStrategy 0 --toysFrequentist --bypassFrequentist --robustFit 1 --X-rtd MINIMIZER_freezeDisassociatedParams %s"%(card,catExtB,catExtB,p,s,p,catExtB,m,extra))
                                fnmultidim.append("_%s_index%d%s.MultiDimFit.mH%i"%(s,p,catExtB,int(m)))

                            if not biasPerChannel or not biasPerPDF:
                                continue
                            ### If injected signal is >3x the existing background, do not perform test
                            #if float(r)*expLim*nSig/nBG>3.0:
                            #    continue
                            ### If total yield is <=10.0 and yield/GeV<0.1, do not perform test
                            if float(r)*expLim*nSig+nBG<=10.0 and (float(r)*expLim*nSig+nBG)/mrange<0.1:
                                continue
                            ### Bias, per channel, per PDF
                            print("PDF index = ", p)
                            print("combine %s -M GenerateOnly --setParameters pdf_index%s=%d --toysFrequentist -t 100 --expectSignal %f --saveToys -m %s --freezeParameters pdf_index%s -n _%s_M%s_ctau%i_r%d_index%d%s"%(card,catExtB,p,float(r)*expLim,m,catExtB,s,m,t,r,p,catExtB))
                            os.system("combine %s -M GenerateOnly --setParameters pdf_index%s=%d --toysFrequentist -t 100 --expectSignal %f --saveToys -m %s --freezeParameters pdf_index%s -n _%s_M%s_ctau%i_r%d_index%d%s"%(card,catExtB,p,float(r)*expLim,m,catExtB,s,m,t,r,p,catExtB))
                            print("combine %s -M FitDiagnostics --toysFile higgsCombine_%s_M%s_ctau%i_r%d_index%d%s.GenerateOnly.mH%s.123456.root -t 100 --rMin %f --rMax %f -n _%s_M%s_ctau%i_r%d_envelope_genindex%d%s -m %s %s"%(card,s,m,t,r,p,catExtB,int(m),max(0,float(r)*expLim-5),max(5,float(r)*expLim+5),s,m,t,r,p,catExtB,m,options))
                            os.system("combine %s -M FitDiagnostics --toysFile higgsCombine_%s_M%s_ctau%i_r%d_index%d%s.GenerateOnly.mH%s.123456.root -t 100 --rMin %f --rMax %f -n _%s_M%s_ctau%i_r%d_envelope_genindex%d%s -m %s %s"%(card,s,m,t,r,p,catExtB,int(m),max(0,float(r)*expLim-5),max(5,float(r)*expLim+5),s,m,t,r,p,catExtB,m,options))
                            exit
                            fnfitdiag.append("_%s_M%s_ctau%i_r%d_envelope_genindex%d%s"%(s,m,t,r,p,catExtB))
                            for pp in range(nPDF):
                                if not checkIndividualPDFs:
                                    break
                                elif pp!=p:
                                    #os.system("combine %s -M FitDiagnostics --setParameters pdf_index%s=%d --toysFile higgsCombine_%s_M%s_r%d_index%d%s.GenerateOnly.mH%s.123456.root -t 100 --rMin %f --rMax %f --freezeParameters pdf_index%s -n _%s_M%s_r%d_index%d_genindex%d%s -m %s %s"%(card,catExtB,pp,s,m,r,p,catExtB,m,max(-5,float(r)*expLim-5),max(5,float(r)*expLim+5),catExtB,s,m,r,pp,p,catExtB,m,options))
                                    print("combine %s -M FitDiagnostics --setParameters pdf_index%s=%d --toysFile higgsCombine_%s_M%s_r%d_index%d%s.GenerateOnly.mH%s.123456.root -t 100 --rMin %f --rMax %f --freezeParameters pdf_index%s -n _%s_M%s_r%d_index%d_genindex%d%s -m %s %s"%(card,catExtB,pp,s,m,r,p,catExtB,m,max(-5,float(r)*expLim-5),max(5,float(r)*expLim+5),catExtB,s,m,r,pp,p,catExtB,m,options))
                                    fnfitdiag.append("_%s_M%s_r%d_index%d_genindex%d%s"%(s,m,r,pp,p,catExtB))

                        if not biasPerChannel:
                            break
                        ### If injected signal is >3x the existing background, do not perform test
                        if float(r)*expLim*nSig/nBG>3.0:
                            break
                        #### If total yield is <=10.0 and yield/GeV<0.1, do not perform test
                        if (float(r)*expLim*nSig+nBG<=10.0 and (float(r)*expLim*nSig+nBG)/mrange<0.1) or (nBG < 10):
                            break
                        ### Bias, per channel
                        print("combine %s -M GenerateOnly --toysFrequentist -t %i --expectSignal %f --saveToys -m %s -n _%s_M%s_r%d%s"%(card,nToysPerChannel,float(r)*expLim,m,s,m,r,catExtB))
                        os.system("combine %s -M GenerateOnly --toysFrequentist -t %i --expectSignal %f --saveToys -m %s -n _%s_M%s_ctau%i_r%d%s"%(card,nToysPerChannel,float(r)*expLim,m,s,m,t,r,catExtB))
                        print("combine %s -M FitDiagnostics --toysFile higgsCombine_%s_M%s_r%d%s.GenerateOnly.mH%s.123456.root -t %i --rMin %f --rMax %f -n _%s_M%s_ctau%i_r%d_envelope%s -m %s  %s"%(card,s,m,r,catExtB,int(m),nToysPerChannel,max(1e-3,float(r)*expLim-10),max(5,float(r)*expLim+10),s,m,t,r,catExtB,m,options))
                        os.system("combine %s -M FitDiagnostics --toysFile higgsCombine_%s_M%s_ctau%i_r%d%s.GenerateOnly.mH%s.123456.root -t %i --rMin %f --rMax %f -n _%s_M%s_ctau%i_r%d_envelope%s -m %s  %s"%(card,s,m,t,r,catExtB,int(m),nToysPerChannel,max(1e-3,float(r)*expLim-10),max(5,float(r)*expLim+10),s,m,t,r,catExtB,m,options))
                        fnfitdiag.append("_%s_M%s_ctau%i_r%d_envelope%s"%(s,m,t,r,catExtB))
                        for pp in range(nPDF):
                            if not checkIndividualPDFs:
                                break
                            elif pp!=p:
                                #os.system("combine %s -M FitDiagnostics --setParameters pdf_index%s=%d --toysFile higgsCombine_%s_M%s_r%d_index%d%s.GenerateOnly.mH%s.123456.root -t 100 --rMin %f --rMax %f --freezeParameters pdf_index%s -n _%s_M%s_r%d_index%d_genindex%d%s -m %s  %s"%(card,catExtB,pp,s,m,r,p,catExtB,m,max(-5,float(r)*expLim-5),max(5,float(r)*expLim+5),catExtB,s,m,r,pp,p,catExtB,m,options))
                                print("combine %s -M FitDiagnostics --setParameters pdf_index%s=%d --toysFile higgsCombine_%s_M%s_r%d_index%d%s.GenerateOnly.mH%s.123456.root -t 100 --rMin %f --rMax %f --freezeParameters pdf_index%s -n _%s_M%s_r%d_index%d_genindex%d%s -m %s  %s"%(card,catExtB,pp,s,m,r,p,catExtB,m,max(-5,float(r)*expLim-5),max(5,float(r)*expLim+5),catExtB,s,m,r,pp,p,catExtB,m,options))
                                fnfitdiag.append("_%s_M%s_ctau%i_r%d_index%d_genindex%d%s"%(s,m,t,r,pp,p,catExtB))

                        ### Plot bias from fit diagnostics, per channel
                        for fdn in fnfitdiag:
                            fd = ROOT.TFile.Open("fitDiagnostics%s.root"%fdn)
                            td = fd.Get("tree_fit_sb")
                            h = ROOT.TH1D("h","",41,-6.1,6.1)
                            h.GetXaxis().SetTitle("(r_{out} - r_{in})/#sigma_{r}")
                            h.GetYaxis().SetTitle("Number of toys")
                            todraw = "(r-%f)/((rLoErr/rHiErr>3.0 || rHiErr/rLoErr>3.0) ? rErr : (r>%f ? rLoErr : rHiErr))>>h"%(float(r)*rLimOneBin,float(r)*rLimOneBin)
                            #todraw = "(r-%f)/((rLoErr/rHiErr>2.0 || rHiErr/rLoErr>2.0) ? rErr : 0.5*(rLoErr+rHiErr))>>h"%(float(r)*rLimOneBin)
                            td.Draw(todraw,"fit_status==0 && abs(r-%f)<4.95 && (r-rLoErr)>0.0011"%(float(r)*rLimOneBin),"goff")
                            print("Histogram for ch%i has %i entries"%(binidx, h.GetEntries()))
                            fg = ROOT.TF1("fg","gaus",-5.0,5.0)
                            fg.SetLineColor(2)
                            h.Fit(fg,"0L","",-5.0,5.0)
                            meanfit[m][d][r].append(fg.GetParameter(1))
                            sigmafit[m][d][r].append(fg.GetParameter(2))
                            #
                            plt.style.use(hep.style.CMS)
                            fig, ax = plt.subplots(figsize=(10, 10))
                            bins = h.GetNbinsX()
                            vx = [h.GetBinLowEdge(i) for i in range(1, bins + 1)]
                            vx.append(h.GetBinLowEdge(bins) + h.GetBinWidth(bins))
                            vy = [h.GetBinContent(i) for i in range(1, bins + 1)]
                            vyerr = [h.GetBinError(i) for i in range(1, bins + 1)]
                            x_fit = np.linspace(-5.0, 5.0, 1000)
                            y_fit = [fg.Eval(xi) for xi in x_fit]
                            quantiles = np.zeros(1)
                            prob = np.array([0.5])
                            h.GetQuantiles(1, quantiles, prob)
                            hep.histplot(vy, bins=vx, ax=ax,histtype='step')
                            ax.plot(x_fit, y_fit, label='Gaussian fit', color='tab:red')
                            ax.set_xlabel(r'$(r_{out} - r_{in})/\sigma_{r}$')
                            ax.set_ylabel('Number of toys')
                            ax.legend(loc='best', frameon = True)
                            ax.text(0.65, 0.8, 'Fit parameters:', fontsize=18, color='tab:red', horizontalalignment='left', verticalalignment='top', transform=ax.transAxes)
                            ax.text(0.65, 0.76, r' - Mean = %.2f $\pm$ %.2f'%(fg.GetParameter(1),fg.GetParError(1)), fontsize=18, color='tab:red', horizontalalignment='left', verticalalignment='top', transform=ax.transAxes)
                            ax.text(0.65, 0.72, r' - Width = %.2f $\pm$ %.2f'%(fg.GetParameter(2),fg.GetParError(2)), fontsize=18, color='tab:red', horizontalalignment='left', verticalalignment='top', transform=ax.transAxes)
                            ax.text(0.03, 0.90, 'Mean = %.2f'%(h.GetMean()), fontsize=18, color='tab:blue', horizontalalignment='left', verticalalignment='top', transform=ax.transAxes)
                            ax.text(0.03, 0.85, 'Median = %.2f'%(quantiles[0]), fontsize=18, color='tab:blue', horizontalalignment='left', verticalalignment='top', transform=ax.transAxes)
                            ax.text(0.03, 0.81, 'std. dev = %.2f'%(h.GetStdDev()), fontsize=18, color='tab:blue', horizontalalignment='left', verticalalignment='top', transform=ax.transAxes)
                            ax.text(0.03, 0.97, r'nBG = %i, $r_{in} = %.0f x r_{+2\sigma} (r_{+2\sigma} = %.2f)$'%(nBG,float(r),rLimOneBin), fontsize=18, color='k', horizontalalignment='left', verticalalignment='top', transform=ax.transAxes)
                            hep.cms.label("Internal", data=True, year=y, com='13.6')
                            fig.savefig("%s/bias%s.png"%(outDir,fdn), dpi=140)
                            #
                            #can = ROOT.TCanvas("can","",600,600)
                            #h.Draw()
                            #can.Update()
                            #can.Clear()
                            #h.Draw()
                            #fg.Draw("same")
                            #text = ROOT.TLatex()
                            #text.SetTextSize(0.03);
                            #text.SetTextFont(42);
                            #text.DrawLatexNDC(0.15,0.85,"%s, M=%s GeV"%(s,m))
                            #bintext = ""
                            #if binidx==1:
                            #    bintext="=1"
                            #elif binidx==2:
                            #    bintext="#geq2"
                            #text.DrawLatexNDC(0.15,0.8,"N_{b-tag}%s (%.0f events)"%(bintext,nBG))
                            #text.DrawLatexNDC(0.15,0.75,"r_{in}=%d (%.1f)"%(r,r*nSig*expLim))
                            #if len(fdn.split("_"))>6:
                            #    genPdfIdx = int(fdn.split("_")[5].replace("genindex",""))
                            #    text.DrawLatexNDC(0.15,0.7,"Gen. PDF: %s"%(pdfnames[genPdfIdx].lower()))
                            #    namefit[m][d][r].append(pdfnames[genPdfIdx].lower())
                            #else:
                            #    text.DrawLatexNDC(0.15,0.7,"Gen. PDF: envelope")
                            #    namefit[m][d][r].append("envelope")
                            #can.Update()
                            #can.SaveAs("%s/bias%s.png"%(outDir,fdn))

                    if plotEnvelope:
                        fnmultidim.append("_%s_envelope%s.MultiDimFit.mH%i"%(s,catExtB,int(m)))

                        ### Plot -2dLL, per channel
                        gs = []
                        miny = +1e9
                        maxy = -1e9
                        legend = ROOT.TLegend(0.65,0.7,0.85,0.87)
                        legend.SetLineColor(0)
                        legend.SetFillColor(0)
                        pdfcolors = dict()
                        pdfcolors["Envelope"]=1
                        pdfcolors["Exponential"]=2
                        pdfcolors["Power-law"]=4
                        pdfcolors["Bernstein"]=6
                        pdfcolors["Uniform"]=8
                        for nf,fdn in enumerate(fnmultidim):
                            fd = ROOT.TFile.Open("higgsCombine%s.root"%fdn)
                            td = fd.Get("limit")
                            xl = []
                            yl = []
                            ### Penalty assigned to PDFs with >1 DOF:
                            #penalty=0.0
                            #if nf<len(fnmultidim)-1:
                            #    penalty=0.5*(numpars[nf]-1)
                            for e in range(td.GetEntries()):
                                td.GetEntry(e)
                                if (td.deltaNLL>1e-9 or td.deltaNLL<-1e-9) and td.deltaNLL>-1e9 and td.deltaNLL<1e9:
                                    xl.append(td.r)
                                    yl.append(2*(td.deltaNLL+td.nll+td.nll0))
                            xv = np.array(xl,"d")
                            yv = np.array(yl,"d")
                            gs.append(ROOT.TGraph(len(xl),xv,yv))
                            gs[nf].SetLineColor(pdfcolors[pdfnames[nf].split("<")[0]])
                            gs[nf].SetMarkerColor(pdfcolors[pdfnames[nf].split("<")[0]])
                            gs[nf].SetMarkerStyle(4)
                            gs[nf].SetMarkerSize(0.5)
                            if np.amin(yv)<miny:
                                miny = np.amin(yv)
                            if np.amax(yv)>maxy:
                                maxy = np.amax(yv)
                            if nf<len(fnmultidim)-1:
                                legend.AddEntry(gs[nf],pdfnames[nf],"L")
                            else:
                                legend.AddEntry(gs[nf],pdfnames[nf],"P")
                        h = ROOT.TH2D("h","",1,-0.3,3.0,1,miny,miny+1.25*(maxy-miny))
                        h.GetXaxis().SetTitle("r")
                        h.GetYaxis().SetTitle("-2Log(L)+c")
                        h.GetYaxis().SetLabelSize(0.02)
                        ROOT.gStyle.SetOptStat(0)
                        ROOT.gStyle.SetOptFit(0)
                        can = ROOT.TCanvas("can","",600,600)
                        h.Draw()
                        for nf,fdn in enumerate(fnmultidim):
                            if nf<len(fnmultidim)-1:
                                gs[nf].Draw("L")
                            else:
                                gs[nf].Draw("P")
                        legend.Draw("same")
                        text = ROOT.TLatex()
                        text.SetTextSize(0.03);
                        text.SetTextFont(42);
                        text.DrawLatexNDC(0.15,0.85,"M=%s GeV"%(m))
                        bintext = ""
                        if binidx==1:
                            bintext="=1"
                        elif binidx==2:
                            bintext="#geq2"
                        text.DrawLatexNDC(0.15,0.8,"N_{b-tag}%s"%(bintext))
                        can.Update()
                        can.SaveAs("%s/PDFEnvelope_expected_M%s%s.png"%(outDir,m,catExtB))

                if not biasCombination:
                    continue
                ### Bias, combination
                print("Proceed to channel combination")
                if redoCombinedCard:
                    card = "%s/card_combined_%s_M%s_ctau%i_%s_selectedChannels.root"%(inDir,s,m,t,y)
                    os.system("combineCards.py -S %s > %s"%(combinedCards, card.replace('.root','.txt')))
                    os.system("text2workspace.py %s"%(card.replace('.root','.txt')))
                else:
                    card = "%s/card_combined_%s_M%.3f_ctau%i_%s.root"%(inDir,s,m,t,y)
                #options="--cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_freezeDisassociatedParams --toysFrequentist --bypassFrequentist --robustFit 1"
                options="--cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_freezeDisassociatedParams --toysFrequentist --robustFit 1"
                #options="--cminDefaultMinimizerStrategy 0 --ignoreCovWarning --cminDefaultMinimizerTolerance 0.01 --X-rtd MINIMIZER_freezeDisassociatedParams --X-rtd MINIMIZER_multiMin_hideConstants --X-rtd MINIMIZER_multiMin_maskConstraints --X-rtd MINIMIZER_multiMin_maskChannels=1 --toysFrequentist"
                os.system("combine -M AsymptoticLimits -d %s --cminDefaultMinimizerStrategy 0 -v 0 -n _temp_combined > log_asym_combined_%s_M%s_ctau%i_%s.txt"%(card,s,m,t,y))
                flobc = open("log_asym_combined_%s_M%s_ctau%i_%s.txt"%(s,m,t,y),"r")
                for ll in flobc.readlines():
                    if "Expected 97" in ll:
                        rLimOneBin = float(ll.split()[len(ll.split())-1])
                    if "Expected 50" in ll:
                        rLimExpOneBin = float(ll.split()[len(ll.split())-1])
                flobc.close()
                print('Now we inject %f'%rLimOneBin)
                expLim = rLimOneBin
                #options=options+" --X-rtd TMCSO_PseudoAsimov=5000"
                #options=options+"--X-rtd TMCSO_AdaptivePseudoAsimov=1"
                #
                exclusion = '' # Not used here anymore
                #
                meanfit[m]["combined"] = dict()
                sigmafit[m]["combined"] = dict()
                namefit[m]["combined"] = dict()
                for rn,r in enumerate(rs):
                    meanfit[m]["combined"][r] = []
                    sigmafit[m]["combined"][r] = []
                    namefit[m]["combined"][r] = []
                    ### If injected signal is >3x the existing background, do not perform test
                    #if float(r)*expLim*(nS1b+nS2b)/nBGAll>3.0:
                    #    break
                    ### If total yield is <=10.0 and yield/GeV<0.1, do not perform test
                    #if (float(r)*expLim*(nS1b+nS2b)+nBGAll)/mrange<0.1 and float(r)*expLim*(nS1b+nS2b)+nBGAll<=10.0:
                    #    break
                    print("combine %s -M GenerateOnly --toysFrequentist -t %i --expectSignal %f --saveToys -m %s -n _%s_M%s_ctau%i_r%d_envelope_combined %s"%(card,nToysPerCombination,float(r)*expLim,m,s,m,t,r,exclusion))
                    os.system("combine %s -M GenerateOnly --toysFrequentist -t %i --expectSignal %f --saveToys -m %s -n _%s_M%s_ctau%i_r%d_envelope_combined %s"%(card,nToysPerCombination,float(r)*expLim,m,s,m,t,r,exclusion))
                    print("combine %s -M FitDiagnostics --toysFile higgsCombine_%s_M%s_ctau%i_r%d_envelope_combined.GenerateOnly.mH%s.123456.root -t %i --rMin %f --rMax %f -n _%s_M%s_ctau%i_r%d_envelope_combined -m %s %s %s"%(card,s,m,t,r,int(m),nToysPerCombination,max(0.01,float(r)*expLim-5),max(5,float(r)*expLim+5),s,m,t,r,m,options,exclusion))
                    if m < 1.0 or m==1.5 or m==2.5:
                        os.system("combine %s -M FitDiagnostics --toysFile higgsCombine_%s_M%s_ctau%i_r%d_envelope_combined.GenerateOnly.mH%s.123456.root -t %i --rMin %f --rMax %f -n _%s_M%s_ctau%i_r%d_envelope_combined -m %s %s %s"%(card,s,m,t,r,m,nToysPerCombination,max(0.01,float(r)*expLim-5),max(5,float(r)*expLim+5),s,m,t,r,m,options,exclusion))
                    else:
                        os.system("combine %s -M FitDiagnostics --toysFile higgsCombine_%s_M%s_ctau%i_r%d_envelope_combined.GenerateOnly.mH%s.123456.root -t %i --rMin %f --rMax %f -n _%s_M%s_ctau%i_r%d_envelope_combined -m %s %s %s"%(card,s,m,t,r,int(m),nToysPerCombination,max(0.01,float(r)*expLim-5),max(5,float(r)*expLim+5),s,m,t,r,m,options,exclusion))
                    fnfitdiag = ["_%s_M%s_ctau%i_r%d_envelope_combined"%(s,m,t,r)]

                    ### Plot bias from fit diagnostics for combination
                    for fdn in fnfitdiag:
                        ROOT.gStyle.SetOptStat(0)
                        ROOT.gStyle.SetOptFit(111)
                        fd = ROOT.TFile.Open("fitDiagnostics%s.root"%fdn)
                        td = fd.Get("tree_fit_sb")
                        h = ROOT.TH1D("h","",41,-6.1,6.1)
                        #h = ROOT.TH1D("h","",31,-1.0,1.0)
                        h.GetXaxis().SetTitle("(r_{out} - r_{in})/#sigma_{r}")
                        h.GetYaxis().SetTitle("Number of toys")
                        todraw = "(r-%f)/((rLoErr/rHiErr>3.0 || rHiErr/rLoErr>3.0) ? rErr : (r>%f ? rLoErr : rHiErr))>>h"%(float(r)*expLim,float(r)*expLim)
                        #todraw = "(r-%f)/(r>%f ? rLoErr : rHiErr)>>h"%(float(r)*expLim,float(r)*expLim)
                        #todraw = "(r-%f)/((rLoErr/rHiErr>2.0 || rHiErr/rLoErr>2.0) ? rErr : 0.5*(rLoErr+rHiErr))>>h"%(float(r)*expLim)
                        #todraw = "(r-%f)>>h"%(float(r)*expLim)
                        td.Draw(todraw,"fit_status>1 && abs(r-%f)<4.95"%(float(r)*expLim),"goff")
                        fg = ROOT.TF1("fg","gaus",-5.0,5.0)
                        #fg = ROOT.TF1("fg","gaus",-1.0,1.0)
                        fg.SetLineColor(2)
                        h.Fit(fg,"0L","",-5.0,5.0)
                        meanfit[m]["combined"][r].append(fg.GetParameter(1))
                        sigmafit[m]["combined"][r].append(fg.GetParameter(2))
                        namefit[m]["combined"][r].append("envelope")
                        #
                        plt.style.use(hep.style.CMS)
                        fig, ax = plt.subplots(figsize=(10, 10))
                        bins = h.GetNbinsX()
                        vx = [h.GetBinLowEdge(i) for i in range(1, bins + 1)]
                        vx.append(h.GetBinLowEdge(bins) + h.GetBinWidth(bins))
                        vy = [h.GetBinContent(i) for i in range(1, bins + 1)]
                        vyerr = [h.GetBinError(i) for i in range(1, bins + 1)]
                        x_fit = np.linspace(-5.0, 5.0, 1000)
                        y_fit = [fg.Eval(xi) for xi in x_fit]
                        quantiles = np.zeros(1)
                        prob = np.array([0.5])
                        h.GetQuantiles(1, quantiles, prob)
                        hep.histplot(vy, bins=vx, ax=ax,histtype='step')
                        ax.plot(x_fit, y_fit, label='Gaussian fit', color='red')
                        ax.set_xlabel(r'$(r_{out} - r_{in})/\sigma_{r}$')
                        ax.set_ylabel('Number of toys')
                        ax.legend(loc='best', frameon = True)
                        ax.text(0.65, 0.8, 'Fit parameters:', fontsize=18, color='tab:red', horizontalalignment='left', verticalalignment='top', transform=ax.transAxes)
                        ax.text(0.65, 0.76, r' - Mean = %.2f $\pm$ %.2f'%(fg.GetParameter(1),fg.GetParError(1)), fontsize=18, color='tab:red', horizontalalignment='left', verticalalignment='top', transform=ax.transAxes)
                        ax.text(0.65, 0.72, r' - Width = %.2f $\pm$ %.2f'%(fg.GetParameter(2),fg.GetParError(2)), fontsize=18, color='tab:red', horizontalalignment='left', verticalalignment='top', transform=ax.transAxes)
                        ax.text(0.03, 0.90, 'Mean = %.2f'%(h.GetMean()), fontsize=18, color='tab:blue', horizontalalignment='left', verticalalignment='top', transform=ax.transAxes)
                        ax.text(0.03, 0.85, 'Median = %.2f'%(quantiles[0]), fontsize=18, color='tab:blue', horizontalalignment='left', verticalalignment='top', transform=ax.transAxes)
                        ax.text(0.03, 0.81, 'std. dev = %.2f'%(h.GetStdDev()), fontsize=18, color='tab:blue', horizontalalignment='left', verticalalignment='top', transform=ax.transAxes)
                        ax.text(0.03, 0.97, r'$r_{in} = %.0f x r_{+2\sigma}$  $(r_{+2\sigma} = %.2f)$'%(float(r),expLim), fontsize=18, color='k', horizontalalignment='left', verticalalignment='top', transform=ax.transAxes)
                        hep.cms.label("Internal", data=True, year=y, com='13.6')
                        fig.savefig("%s/bias%s.png"%(outDir,fdn), dpi=140)
        # Move everything to output
        os.system('mv fitDiagnostics*.root %s'%(outDir))
        os.system('mv log_asym_combined_%s_M%s_ctau%i_%s.txt %s'%(s,m,t,y, outDir))
        #os.system('mv higgsCombine*.root %s'%(outDir))
