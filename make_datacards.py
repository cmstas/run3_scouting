import os,sys
import ROOT
from datetime import date

ROOT.gROOT.ProcessLine(".L cpp/helper.C+")

user = os.environ.get("USER")
today= date.today().strftime("%b-%d-%Y")

wsname = "wfit"
thisDir = os.environ.get("PWD")

#fnfitParamsForShapeUnc = "%s/utils/signalFitParameters_muonResolutionUnc.root"%thisDir
#ffitParamsForShapeUnc = ROOT.TFile.Open(fnfitParamsForShapeUnc,"READ")
#fnfitParamsForAccUnc = "%s/data/acceff_interpolation_Run2.root"%thisDir
#ffitParamsForAccUnc = ROOT.TFile.Open(fnfitParamsForAccUnc,"READ")
#minMforSpline =  200.0
#maxMforSpline = 2500.0

useCategorizedSignal = True
useCategorizedBackground = True

useData = True
useSignalMC = False

# Constant to control the yields of the signal in the datacard (to be used consistently when limits are made)
useNorm = True
NORMCONST = 0.01 

doPartiaUnblinding = False
ext = "data"
if not useData:
    ext = "BGMC"

doCounting = False
useOnlyExponential = False
useOnlyPowerLaw = False
useOnlyBernstein = False
fullMeanFloat = False
meanFloat = True
doMuonResolution = True
noModel = False
dirExt = ""

# In line arguments
if len(sys.argv)>1:
    fit = sys.argv[1]
    _inDir = sys.argv[2]
    year = sys.argv[3]

# Channel selection flags
doAll = True
doIso0HighPt = False
doIso1HighPt = False
doIso0LowPt = False
doIso1LowPt = False
doNonPointing = False
doFourMuon = False
if len(sys.argv) > 4:
    try:
        exec("%s = True"%(sys.argv[4]))
    except:
        sys.exit("Search region selection not recognized, aborting...")

if (doIso0HighPt or doIso1HighPt or doIso0LowPt or doIso1LowPt or doNonPointing or doFourMuon):
    doAll = False


if len(sys.argv)>1:
    if sys.argv[1]=="expo":
        useOnlyExponential = True
        dirExt = "_expoOnly"
    elif sys.argv[1]=="plaw":
        useOnlyPowerLaw = True
        dirExt = "_plawOnly"
    elif sys.argv[1]=="bern":
        useOnlyBernstein = True
        dirExt = "_bernOnly"
    elif sys.argv[1]=="count":
        doCounting = True
        dirExt = "_count"
    elif sys.argv[1]=="fullmeanfloat":
        fullMeanFloat = True
        dirExt = "_fullMeanFloat"
    elif sys.argv[1]=="meanfloat":
        meanFloat = True
        dirExt = "_meanFloat"
    elif sys.argv[1]=="nomodel":
        noModel=True
        dirExt = "_nomodel"
    if len(sys.argv)>2 and sys.argv[2]=="nomodel":
        noModel=True
        dirExt = dirExt+"_nomodel"


useSinglePDF = False
if useOnlyExponential or useOnlyPowerLaw or useOnlyBernstein:
    useSinglePDF = True


#### Caution, here the names AND order should be consistent to the ones set in cpp/doAll_fitDimuonMass.C 
# Example of workspace: d_Dimuon_lxy0p0to2p7_iso0_pthigh_Signal_HTo2ZdTo2mu2x_MZd-7p0_ctau-1mm_2022_workspace.root
dNames = []
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
dNames.append("d_Dimuon_lxy0p0to0p2_non-pointing")
dNames.append("d_Dimuon_lxy0p2to1p0_non-pointing")
dNames.append("d_Dimuon_lxy1p0to2p4_non-pointing")
dNames.append("d_Dimuon_lxy2p4to3p1_non-pointing")
dNames.append("d_Dimuon_lxy3p1to7p0_non-pointing")
dNames.append("d_Dimuon_lxy7p0to11p0_non-pointing")
dNames.append("d_Dimuon_lxy11p0to16p0_non-pointing")
dNames.append("d_Dimuon_lxy16p0to70p0_non-pointing")
if doIso0HighPt:
    dNames = [s for s in dNames if "iso0_pthigh" in s]
elif doIso1HighPt:
    dNames = [s for s in dNames if "iso1_pthigh" in s]
elif doIso0LowPt:
    dNames = [s for s in dNames if "iso0_ptlow" in s]
elif doIso1LowPt:
    dNames = [s for s in dNames if "iso1_ptlow" in s]
elif doNonPointing:
    dNames = [s for s in dNames if "non-pointing" in s]
elif doFourMuon:
    dNames = [s for s in dNames if "FourMu" in s]


years = []
years.append(year)
###
#years.append("allEras")

#years.append("2023")

# Output directory
outDir = ("%s/datacards_all%s_"%(thisDir,dirExt))+today+"_"+year
if doIso0HighPt:
    outDir = outDir + "_Iso0HighPt"
if doIso1HighPt:
    outDir = outDir + "_Iso1HighPt"
if doIso0LowPt:
    outDir = outDir + "_Iso0LowPt"
if doIso1LowPt:
    outDir = outDir + "_Iso1LowPt"
if doNonPointing:
    outDir = outDir + "_NonPointing"
if doFourMuon:
    outDir = outDir + "_FourMuon"
if not os.path.exists(outDir):
    os.makedirs(outDir)
os.system('cp -r %s %s/'%(_inDir, outDir))
inDir  = "%s/%s/"%(thisDir, _inDir)

# Signals
sigModel = "ScenarioB1"
sigModel = "HTo2ZdTo2mu2x"


sigTags = []
if sigModel=="HTo2ZdTo2mu2x":
    if useSignalMC:
        sigMasses = [0.5, 0.7, 1.5, 2.0, 2.5, 5.0, 6.0, 7.0, 8.0, 14.0, 16.0, 20.0, 22.0, 24.0, 30.0, 34.0, 40.0, 44.0, 50.0]
        for  m in sigMasses:
            sigCTaus = [1, 10, 100]
            for t in sigCTaus:
                if ((m < 1.0 and t > 10) or (m < 30.0 and t > 100)):
                    continue
                sigTags.append("Signal_HTo2ZdTo2mu2x_MZd-%s_ctau-%imm"%(str(m).replace('.','p'), t))
    else:
        sigCTaus = [1, 10, 100, 1000]
        lastmass = 0.5
        while (lastmass < 50.0):
            lastmass = 1.04*lastmass
            if not ROOT.passMassVeto(lastmass):
                continue
            m = lastmass
            for t in sigCTaus:
                if ((m < 1.0 and t > 10) or (m < 30.0 and t > 100)):
                    continue
                sigTags.append("Signal_HTo2ZdTo2mu2x_MZd-%.3f_ctau-%.1fmm"%(m, t))
elif sigModel=="ScenarioB1":
    sigMasses = [1.33]
    sigCTaus = [0.1, 1, 10, 100]
    for m in sigMasses:
        for t in sigCTaus:
            sigTags.append("Signal_ScenarioB1_mpi-4_mA-%s_ctau-%smm"%(str(m).replace(".", "p"),str(t).replace('.','p')))

f2l = [0.0]
nSigTot = 1.0
if noModel:
    f2l = [0.0, 0.01, 0.05, 0.1, 0.25, 0.5, 0.75, 0.9, 0.95, 0.99, 1.0]

mean = 0.0
sigma = 0.0
for y in years:
    for m in sigTags:
        isValidPoint = True # Control bool to check if the point can be actually be computed
        M = float(m.split('-')[1].split('_')[0].replace('p','.'))
        T = float(m.split('ctau-')[1].split('mm')[0].replace('p','.'))
        listOfBins = []
        for d_,d in enumerate(dNames):
            print("Analyzing %s, in region %s"%(m, d))
            print("%s/%s_%s_%s_workspace.root"%(inDir,d,m,y))
            finame = "%s/%s_%s_%s_workspace.root"%(inDir,d,m,y)
            _finame = "%s/%s_%s_%s_workspace.root"%(_inDir,d,m,y)
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
            catExtS = ""
            catExtB = ""
            if useCategorizedSignal:
                catExtS = "_ch%d_%s"%(binidx, year)
            if useCategorizedBackground:
                catExtB = "_ch%d_%s"%(binidx, year)
            listOfBins.append(binidx)
            # Open input file with workspace
            f = ROOT.TFile(finame)
            # Retrieve workspace from file
            w = f.Get(wsname)
            # Retrieve signal normalization
            nSig = w.var("signalNorm%s"%catExtS).getValV()
            if doPartiaUnblinding:
                nSig = 0.1*nSig
            if nSig < 1e-6:
                nSig = 1e-6
            if useNorm:
                nSig = NORMCONST*nSig
            # Retrieve signal mean and std. deviation
            mean = w.var("mean%s"%catExtS).getValV()
            sigma = w.var("sigma%s"%catExtS).getValV()
            # Retrieve MC stat. uncertainty from RooDataSet
            if w.var("signalRawNorm%s"%catExtS).getValV()>0.0:
                mcstatunc = 1.0/ROOT.TMath.Sqrt(w.var("signalRawNorm%s"%catExtS).getValV())
            else:
                mcstatunc = 1.0
            # Retrive BG normalization:
            try:
                nBG = w.data("data_obs%s"%catExtB).sumEntries()
            except TypeError: # if it doesn't exist... (assuming there ir signal)
                print("Background not found for this mass, skipping to next")
                isValidPoint = False
                break
            #if not doCounting:
            #    os.system("cp %s %s/"%(finame,outDir))
            #    finame = "%s/%s_%s_%s_workspace.root"%(inDir,d,m,y)
                #finame = "%s_%s_M%s_%s_workspace.root"%(d,s,m,y)

            ## Define systematics from up and down variations
            # Trigger systematic:
            try:
                w_trg_up = f.Get(wsname + '_trg_up')
                w_trg_down = f.Get(wsname + '_trg_down')
                nSig_trgUp = w_trg_up.var("signalNorm%s"%catExtS).getValV()
                nSig_trgDown = w_trg_down.var("signalNorm%s"%catExtS).getValV()
                if useNorm:
                    nSig_trgUp = NORMCONST*nSig_trgUp
                    nSig_trgDown = NORMCONST*nSig_trgDown
                trgsyst = max([(nSig_trgUp/nSig - 1.0), (1.0 - nSig_trgDown/nSig)])
            except AttributeError: # No up and down variations in this tree, probably interpolated point
                filesyst = ROOT.TFile.Open("data/systematicSplines_2022.root", "READ")
                spline_trg = filesyst.Get("spline_trgsys_%s_%s_%.1f_%s"%(sigModel, d, T, y))
                trgsyst = spline_trg.Eval(M)
                filesyst.Close()
            #
            # Selection systematic:
            try:
                w_sel_up = f.Get(wsname + '_sel_up')
                w_sel_down = f.Get(wsname + '_sel_down')
                nSig_selUp = w_sel_up.var("signalNorm%s"%catExtS).getValV()
                nSig_selDown = w_sel_down.var("signalNorm%s"%catExtS).getValV()
                if useNorm:
                    nSig_selUp = NORMCONST*nSig_selUp
                    nSig_selDown = NORMCONST*nSig_selDown
                selsyst = max([(nSig_selUp/nSig - 1.0), (1.0 - nSig_selDown/nSig)])
            except AttributeError: # No up and down variations in this tree, probably interpolated point
                filesyst = ROOT.TFile.Open("data/systematicSplines_2022.root", "READ")
                spline_trg = filesyst.Get("spline_selsys_%s_%s_%.1f_%s"%(sigModel, d, T, y))
                selsyst = spline_trg.Eval(M)
                filesyst.Close()
            #
            ## Close input file with workspace
            f.Close()
            #muonselsyst = 0.05
            #
            ## Derive mass-dependent systematic uncertainties
            #minm = 200.0
            #maxm = 2000.0
            ##
            #minsyst = 0.015
            #maxsyst = 0.03
            #muonsfsyst = max(0.0,(maxsyst-minsyst)/(maxm-minm)*float(m) + minsyst - minm/(maxm-minm)*(maxsyst-minsyst))
            ##
            #minsyst = 0.01
            #maxsyst = 0.05
            #triggersyst = max(0.0,(maxsyst-minsyst)/(maxm-minm)*float(m) + minsyst - minm/(maxm-minm)*(maxsyst-minsyst))
            ##
            #if binidx<2:
            #    minsyst = 0.015
            #    maxsyst = 0.01
            #else:
            #    minsyst = 0.05
            #    maxsyst = 0.02
            #jecsyst = max(0.0,(maxsyst-minsyst)/(maxm-minm)*float(m) + minsyst - minm/(maxm-minm)*(maxsyst-minsyst))

            ## Shape systematic on signal mean, linearly increasing with mass
            #minsyst = 0.000
            #maxsyst = 0.002
            #meanvar = max(0.0,(maxsyst-minsyst)/(maxm-minm)*float(m) + minsyst - minm/(maxm-minm)*(maxsyst-minsyst))*float(m)
            #
            #sigmavar = 0.0
            #if float(m) > minMforSpline-0.001 and float(m) < maxMforSpline+0.001:
            #    fsigmavar = ffitParamsForShapeUnc.Get("splines")
            #    sigmavar = abs(fsigmavar.Eval(float(m))-sigma)
            #else:
            #    fsigmavar =ffitParamsForShapeUnc.Get("fsigma")
            #    sigmavar = abs(fsigmavar.Eval(float(m))-sigma)
            sigmavar = 0.06*sigma # 0.5*sigma
            #
            #if float(m) > minMforSpline-0.001 and float(m) < maxMforSpline+0.001:
            #    accbb_nb1 = ffitParamsForAccUnc.Get("spline_avg_acceff_bb_Nb_eq_1_Run2")
            #    accbb_nb2 = ffitParamsForAccUnc.Get("spline_avg_acceff_bb_Nb_geq_2_Run2")
            #    accsb_nb1 = ffitParamsForAccUnc.Get("spline_avg_acceff_sb_Nb_eq_1_Run2")
            #    accsb_nb2 = ffitParamsForAccUnc.Get("spline_avg_acceff_sb_Nb_geq_2_Run2")
            #    errupbb_nb1 = ffitParamsForAccUnc.Get("spline_avg_errsq_up_acceff_bb_Nb_eq_1_Run2")
            #    errupbb_nb2 = ffitParamsForAccUnc.Get("spline_avg_errsq_up_acceff_bb_Nb_geq_2_Run2")
            #    errupsb_nb1 = ffitParamsForAccUnc.Get("spline_avg_errsq_up_acceff_sb_Nb_eq_1_Run2")
            #    errupsb_nb2 = ffitParamsForAccUnc.Get("spline_avg_errsq_up_acceff_sb_Nb_geq_2_Run2")
            #    errdnbb_nb1 = ffitParamsForAccUnc.Get("spline_avg_errsq_dn_acceff_bb_Nb_eq_1_Run2")
            #    errdnbb_nb2 = ffitParamsForAccUnc.Get("spline_avg_errsq_dn_acceff_bb_Nb_geq_2_Run2")
            #    errdnsb_nb1 = ffitParamsForAccUnc.Get("spline_avg_errsq_dn_acceff_sb_Nb_eq_1_Run2")
            #    errdnsb_nb2 = ffitParamsForAccUnc.Get("spline_avg_errsq_dn_acceff_sb_Nb_geq_2_Run2")
            #    tacctot = 0.0
            #    taccbb  = 0.0
            #    taccsb  = 0.0
            #    terrtot = 0.0
            #    terrbb  = 0.0
            #    terrsb  = 0.0
            #    if binidx == 0:
            #        taccbb  = accbb_nb1.Eval(float(m))+accbb_nb2.Eval(float(m))
            #        taccsb  = accsb_nb1.Eval(float(m))+accsb_nb2.Eval(float(m))
            #        tacctot = taccbb+taccsb
            #        terrbb  = max(errupbb_nb1.Eval(float(m)),errdnbb_nb1.Eval(float(m)))+max(errupbb_nb2.Eval(float(m)),errdnbb_nb2.Eval(float(m)))
            #        terrsb  = max(errupsb_nb1.Eval(float(m)),errdnsb_nb1.Eval(float(m)))+max(errupsb_nb2.Eval(float(m)),errdnsb_nb2.Eval(float(m)))
            #        terrtot = ROOT.TMath.Sqrt(terrbb+terrsb)/tacctot if tacctot > 0.0 else 1.0
            #    elif binidx == 1:
            #        taccbb  = accbb_nb1.Eval(float(m))
            #        taccsb  = accsb_nb1.Eval(float(m))
            #        tacctot = taccbb+taccsb
            #        terrbb  = max(errupbb_nb1.Eval(float(m)),errdnbb_nb1.Eval(float(m)))
            #        terrsb  = max(errupsb_nb1.Eval(float(m)),errdnsb_nb1.Eval(float(m)))
            #        terrtot = ROOT.TMath.Sqrt(terrbb+terrsb)/tacctot if tacctot > 0.0 else 1.0
            #    elif binidx == 2:
            #        taccbb  = accbb_nb2.Eval(float(m))
            #        taccsb  = accsb_nb2.Eval(float(m))
            #        tacctot = taccbb+taccsb
            #        terrbb  = max(errupbb_nb2.Eval(float(m)),errdnbb_nb2.Eval(float(m)))
            #        terrsb  = max(errupsb_nb2.Eval(float(m)),errdnsb_nb2.Eval(float(m)))
            #        terrtot = ROOT.TMath.Sqrt(terrbb+terrsb)/tacctot if tacctot > 0.0 else 1.0
            
            # Check if it has uniform (meaning no other functions are there)
            useOnlyUniform = False
            for obj in list(w.allPdfs()):
                if "background_uniform" in obj.GetName():
                    useOnlyUniform = True
                    break
            #
            # Card creation
            cname = ""
            if noModel:
                nSig = nSigTot
                if binidx == 1:
                    nSig = nSigTot*(1-f)
                elif binidx == 2:
                    nSig = nSigTot*f
                if binidx > 0:
                    cname = "_f2b%d"%(f*100)
            cardn = "%s/card%s_ch%d_%s_M%.1f_ctau%i_%s.txt"%(outDir,cname,binidx,sigModel,M,T,y)
            if noModel:
                cardn = "%s/card%s_ch%d_nomodel_M%s_%s.txt"%(outDir,cname,binidx,m,y)
            card = open("%s"%cardn,"w")
            card.write("imax *\n")
            card.write("jmax *\n")
            card.write("kmax *\n")
            card.write("------------\n")
            if doCounting:
                card.write("shapes * * FAKE\n")
            else:
                card.write("shapes data_obs * %s %s:data_obs%s\n"%(_finame,wsname,catExtB))
                card.write("shapes signal * %s %s:signal%s\n"%(_finame,wsname,catExtS))
                if not useSinglePDF:
                    card.write("shapes background * %s %s:roomultipdf%s\n"%(_finame,wsname,catExtB))
                elif useOnlyUniform:
                    card.write("shapes background * %s %s:background_uniform%s\n"%(_finame,wsname,catExtB))
                elif useOnlyExponential:
                    card.write("shapes background * %s %s:background_exponential%s\n"%(_finame,wsname,catExtB))
                elif useOnlyPowerLaw:
                    card.write("shapes background * %s %s:background_powerlaw%s\n"%(_finame,wsname,catExtB))
                elif useOnlyBernstein:
                    card.write("shapes background * %s %s:background_bernstein%s\n"%(_finame,wsname,catExtB))
            card.write("------------\n")
            # Observation (taken directly from RooDataSet data_obs)
            card.write("bin ch%d\n"%(binidx))
            if doCounting:
                card.write("observation %.3f\n"%nBG)
            else:
                card.write("observation -1\n")
            card.write("------------\n")  
            # Rates (background is left freely floating)
            card.write("bin ch%d ch%d\n"%(binidx,binidx))
            card.write("process signal background\n")
            card.write("process 0 1\n")
            if doCounting:
                card.write("rate %.3f %.3f\n"%(nSig,nBG))
            else:
                card.write("rate %e 1\n"%(nSig)) # CELIANOTE: Is this really correct? 
            card.write("------------\n")  
            # Systematics
            card.write("lumi_13p6TeV lnN 1.014 -\n") # Integrated luminosity uncertainty on signal (fully correlated)
            card.write("CMS_eff_trg_%s lnN %.3f -\n"%(year, 1.0+trgsyst)) # Systematic uncertainty on signal from b-tagging (fully correlated)
            card.write("CMS_eff_sel_%s lnN %.3f -\n"%(year, 1.0+selsyst)) # Systematic uncertainty on signal from b-tagging (fully correlated)
            card.write("mcstat_ch%d lnN %.3f -\n"%(binidx,1.0+mcstatunc)) # MC stat. uncertainty (uncorrelated)
            #card.write("accstat_ch%d lnN %.3f -\n"%(binidx,1.0+terrtot)) # Stat. uncertainty on average acceptance (uncorrelated)
            if meanFloat:
                card.write("mean%s param %.3f -%.3f/+%.3f\n"%(catExtS,mean,0.5*sigma,0.5*sigma)) # Shape systematic on dimuon mass mean value
            elif fullMeanFloat:
                card.write("mean param %.3f %.3f\n"%(mean,sigma)) # Shape systematic on dimuon mass mean value
            elif meanvar/float(m)>1e-6:
                card.write("mean param %.3f %.3f\n"%(mean,meanvar))
            if doMuonResolution:
                card.write("sigma%s param %.5f %.5f\n"%(catExtS,sigma,sigmavar))                        
            if doCounting:
                card.write("bg_norm_ch%d gmN %d - 1.0\n"%(binidx,int(nBG)))
            else:
                if not useSinglePDF:
                    card.write("pdf_index_ch%d_%s discrete\n"%(binidx, year)) # For discrete profiling
                    #card.write("pdf_index discrete\n") # For discrete profiling
            card.close()
        
            ## text2workspace for individual cards:
            #os.chdir(outDir)
            if noModel:
                os.system("text2workspace.py %s/card%s_ch%d_nomodel_M%s_%s.txt -m %s"%(_inDir,cname,binidx,m,y,m))
            else:
                os.system("text2workspace.py %s/card%s_ch%d_%s_M%.1f_ctau%i_%s.txt"%(outDir,cname,binidx,sigModel,M,T,y))                        
            #os.chdir(thisDir)
        if not isValidPoint:
            continue
        #
        ## Combine cards:
        if len(dNames)>1:
            os.chdir(outDir)
            combinedCards = ""
            for binidx in listOfBins:
                cname = ""
                #if noModel and binidx > 0:
                #    cname = "_f2b%d"%(f*100)
                #if noModel:
                #    os.system("combineCards.py -S card%s_ch1_nomodel_M%s_%s.txt card%s_ch2_nomodel_M%s_%s.txt > card%s_combined_nomodel_M%s_%s.txt"%(cname,m,y,cname,m,y,cname,m,y))
                #    os.system("text2workspace.py card%s_combined_nomodel_M%s_%s.txt -m %s"%(cname,m,y,m))
                #else:
                #    os.system("combineCards.py -S card%s_ch1_%s_M%s_%s.txt card%s_ch2_%s_M%s_%s.txt > card%s_combined_%s_M%s_%s.txt"%(cname,s,m,y,cname,s,m,y,cname,s,m,y))
                #    os.system("text2workspace.py card%s_combined_%s_M%s_%s.txt -m %s"%(cname,s,m,y,m))
                combinedCards += "%s/card%s_ch%d_%s_M%.1f_ctau%i_%s.txt "%(outDir,cname,binidx,sigModel,M,T,y)
            os.system("combineCards.py -S %s > card%s_combined_%s_M%.1f_ctau%i_%s.txt"%(combinedCards,cname,sigModel,M,T,y))
            os.system("text2workspace.py %s/card%s_combined_%s_M%.1f_ctau%i_%s.txt --channel-masks"%(outDir,cname,sigModel,M,T,y))
            os.chdir(thisDir)

# f it dir within the datacard directory is not needed anymore (avoid using rm -rf)
os.chdir(outDir)
os.system('rm %s/*'%(_inDir))
os.system('rmdir %s'%(_inDir))
os.chdir(thisDir)
