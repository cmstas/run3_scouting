import os,sys
import ROOT
from datetime import date
import csv

ROOT.gROOT.ProcessLine(".L cpp/helper.C+")

user = os.environ.get("USER")
today= date.today().strftime("%b-%d-%Y")
validation = False

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
useSignalMC = True

# Constant to control the yields of the signal in the datacard (to be used consistently when limits are made)
useNorm = True
NORMCONST = 0.01

doHybridFit = True
doBinnedFit = False # If doHybridFit is set to True this is basically not used
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
usePredefinedGrid = True # only applied if not using MC
dirExt = "standard"
doIndividualRootCard = False
doSmartScaling = False
useOnlyZeroBackground = False

## doc: Smart scaling allows to have the limit around 0.5, or alternatively with the 2.5% quantile above 0.25

# In line arguments
sigModel = ""
if len(sys.argv)>1:
    fit = sys.argv[1]
    _inDir = sys.argv[2]
    year = sys.argv[3]
    if len(sys.argv)>4:
        sigModel = sys.argv[4]
    else:
        sigModel = "HTo2ZdTo2mu2x" # HTo2ZdTo2mu2x : ScenarioB1 : ScenarioA : BToPhi
    if len(sys.argv)>5:
        NORMCONST = float(sys.argv[5])
    else:
        NORMCONST = 0.01
    
if doSmartScaling and not len(sys.argv)>5:
    if sigModel=="HTo2ZdTo2mu2x":
        if not useSignalMC:
            scalingFile = '/ceph/cms/store/user/fernance/Run3ScoutingOutput/limits_Apr-15-2025_HTo2ZdTo2mu2x_Norm0p01_asymptotic_vsMass_allEras/limits_HTo2ZdTo2mu2x_allEras.txt'
        else:
            scalingFile = '/ceph/cms/store/user/fernance/Run3ScoutingOutput/limits_HTo2ZdTo2mu2x_NormSmart_Apr-28-2025_vsCTau_asymptotic_allEras/limits_HTo2ZdTo2mu2x_allEras.txt'
    if sigModel=="BToPhi":
        if not useSignalMC:
            #scalingFile = '/ceph/cms/store/user/fernance/Run3ScoutingOutput/limits_Apr-15-2025_HTo2ZdTo2mu2x_Norm0p01_asymptotic_vsMass_allEras/limits_HTo2ZdTo2mu2x_allEras.txt'
            #scalingFile = 'combineScripts/SmartLimitNorm/limits_BToPhi_asymptotic_allEras_1mm.txt'
            #scalingFile = 'combineScripts/SmartLimitNorm/limits_BToPhi_asymptotic_allEras_10-100mm.txt'
            scalingFile = 'combineScripts/SmartLimitNorm/limits_BToPhi_asymptotic_allEras_vsCTau.txt'
        else:
            scalingFile = 'results_BToPhi_asymptotic/limits_BToPhi_asymptotic_allEras.txt'
    if sigModel=="ScenarioA":
        scalingFile = 'combineScripts/SmartLimitNorm/limits_ScenarioA_asymptotic_allEras_vsCTau.txt'
        #scalingFile = '/ceph/cms/store/user/fernance/Run3ScoutingOutput/limits_ScenarioA_Norm1p0-0p6_Jun-10-2025_vsCTau_asymptotic_allEras/limits_ScenarioA_asymptotic_allEras.txt'
    if sigModel=="ScenarioB1":
        #scalingFile = '/ceph/cms/store/user/fernance/Run3ScoutingOutput/limits_ScenarioB1_Norm1p0-0p6_Jun-10-2025_vsCTau_asymptotic_allEras/limits_ScenarioB1_asymptotic_allEras.txt'
        #scalingFile = 'results_ScenarioB1_asymptotic/limits_ScenarioB1_asymptotic_allEras.txt'
        scalingFile = 'combineScripts/SmartLimitNorm/limits_ScenarioB1_asymptotic_allEras_vsCTau.txt'
else:
    scalingFile = ''

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
if 'BToPhi' not in sigModel:
    if 'ScenarioB1' not in sigModel:
        dNames.append("d_FourMu_sep")
    if 'ScenarioA' not in sigModel and 'HTo2ZdTo2mu2x' not in sigModel:
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

# Output directory
if not doSmartScaling:
    outDir = ("%s/datacards_%s_Norm%s_%s_"%(thisDir, sigModel, float(NORMCONST), dirExt))+today+"_"+year
else:
    outDir =  ("%s/datacards_%s_NormSmart_%s_"%(thisDir, sigModel, dirExt))+today+"_"+year
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
inDir  = "%s/%s"%(thisDir, _inDir)

sigTags = []
if sigModel=="HTo2ZdTo2mu2x":
    if useSignalMC:
        if not validation:
            sigMasses = [1.5, 2.0, 2.5, 5.0, 7.0, 8.0, 14.0, 16.0, 20.0, 22.0, 24.0, 30.0, 34.0, 40.0, 50.0]
            sigMasses = [1.5, 2.0, 2.5, 5.0, 7.0, 8.0, 14.0, 16.0, 20.0, 22.0, 24.0, 30.0, 40.0, 50.0]
            sigMasses = [20.0, 30.0, 40.0, 50.0]
            sigMasses = [5.0]
            #sigMasses = [20.0]
            for  m in sigMasses:
                sigCTaus = [0.10, 0.16, 0.25, 0.40, 0.63, 1.00, 1.60, 2.50, 4.00, 6.30, 10.00, 16.00, 25.00, 40.00, 63.00, 100.00, 160.00, 250.00, 400.00, 630.00, 1000.00]
                #sigCTaus = [160.00, 250.00, 400.00, 630.00, 1000.00]
                #sigCTaus = [100.00]
                sigCTaus = [10.00]
                for t in sigCTaus:
                    if ((m < 1.0 and t > 10) or (m < 2.0 and t > 100)):
                        continue
                    sigTags.append("Signal_HTo2ZdTo2mu2x_MZd-%s_ctau-%.2fmm"%(str(m).replace('.','p'), t))
        else:
            # Only for lifetime-reweighting validation, if not validating don't run!
            print("-> Taking samples for lifetime-reweighting validation")
            sigTags = []
            sigTags.append("Signal_HTo2ZdTo2mu2x_MZd-1p5_ctau-1.00mm")
            sigTags.append("Signal_HTo2ZdTo2mu2x_MZd-1p5_rectau-1.00mm")
            sigTags.append("Signal_HTo2ZdTo2mu2x_MZd-5p0_ctau-1.00mm")
            sigTags.append("Signal_HTo2ZdTo2mu2x_MZd-5p0_rectau-1.00mm")
            sigTags.append("Signal_HTo2ZdTo2mu2x_MZd-8p0_ctau-1.00mm")
            sigTags.append("Signal_HTo2ZdTo2mu2x_MZd-8p0_rectau-1.00mm")
            sigTags.append("Signal_HTo2ZdTo2mu2x_MZd-14p0_ctau-1.00mm")
            sigTags.append("Signal_HTo2ZdTo2mu2x_MZd-14p0_rectau-1.00mm")
            sigTags.append("Signal_HTo2ZdTo2mu2x_MZd-22p0_ctau-1.00mm")
            sigTags.append("Signal_HTo2ZdTo2mu2x_MZd-22p0_rectau-1.00mm")
            sigTags.append("Signal_HTo2ZdTo2mu2x_MZd-40p0_ctau-1.00mm")
            sigTags.append("Signal_HTo2ZdTo2mu2x_MZd-40p0_rectau-1.00mm")
    elif usePredefinedGrid:
        with open('data/sigmasses_HTo2ZdTo2mu2x_fine.txt', 'r') as f:
            masses = f.readlines()
            sigCTaus = [1, 10, 100, 1000]
            for mass in masses:
                m = float(mass)
                for t in sigCTaus:
                    if ((m < 1.0 and t > 10) or (m < 2.0 and t > 100)):
                        continue
                    sigTags.append("Signal_HTo2ZdTo2mu2x_MZd-%.3f_ctau-%.2fmm"%(m, t))
    else:
        sigTags.append("Signal_HTo2ZdTo2mu2x_MZd-2.400_ctau-1.00mm")

elif sigModel=="BToPhi":
    if useSignalMC:
        #sigMasses = [0.25, 0.30, 0.40, 0.50, 0.60, 0.70, 0.90, 1.25, 1.50, 2.0, 2.85, 3.35, 4.00, 5.00]
        sigMasses = [1.25] #Other masses are either too small or too close to SM resonance
        for m in sigMasses:
            sigCTaus = [0.0, 0.1, 1, 10, 100]
            sigCTaus = [0.1]
            for t in sigCTaus:
                sigTags.append("Signal_BToPhi_MPhi-%s_ctau-%.2fmm"%(('%.2f'%m).replace('.','p'), t))
    elif usePredefinedGrid:
        with open('data/BToPhi_limitgrid.txt', 'r') as f:
            masses = f.readlines()
            sigCTaus = [1, 10, 100]
            for mass in masses:
                m = float(mass)
                for t in sigCTaus:
                    sigTags.append("Signal_BToPhi_MPhi-%.3f_ctau-%.2fmm"%(m, t))
elif sigModel=="ScenarioB1":
    sigMasses = []
    sigMasses.append([4,1.33])
    #sigMasses.append([5,2.40])
    #sigCTaus = [0.1, 1, 10, 100]
    sigCTaus = [0.25]
    for m in sigMasses:
        for t in sigCTaus:
            sigTags.append("Signal_ScenarioB1_Mpi-%i_MA-%s_ctau-%.2fmm" % (m[0], ('%.2f'%m[1]).replace('.','p'), float(t)))
elif sigModel=="ScenarioA":
    sigMasses = []
    #sigMasses.append([1,0.33])
    #sigMasses.append([1,0.25])
    #sigMasses.append([2,0.67])
    #sigMasses.append([5,2.40])
    #sigMasses.append([4,1.33])
    sigMasses.append([5,1.67])
    #sigMasses.append([10,2.00])
    #sigMasses.append([10,3.33])
    #sigMasses.append([10,4.90])
    #sigCTaus = [0.1, 1, 10, 100]
    sigCTaus = [0.1]
    for m in sigMasses:
        for t in sigCTaus:
            sigTags.append("Signal_ScenarioA_Mpi-%i_MA-%s_ctau-%.2fmm" % (m[0], ('%.2f'%m[1]).replace('.','p'), float(t)))

f2l = [0.0]
nSigTot = 1.0
if noModel:
    f2l = [0.0, 0.01, 0.05, 0.1, 0.25, 0.5, 0.75, 0.9, 0.95, 0.99, 1.0]

mean = 0.0
sigma = 0.0
for y in years:
    for m in sigTags:
        #isValidPoint = True # Control bool to check if the point can be actually be computed
        M = float(m.split('-')[1].split('_')[0].replace('p','.'))
        if "Scenario" in sigModel:
            M2 = float(m.split('-')[1].split('_')[0].replace('p','.'))
            M = float(m.split('MA-')[1].split('_')[0].replace('p','.'))
        #if validation and "." in m.split('ctau-')[1].split('mm')[0]:
        if validation and "rectau" in m:
            T = float("9"+m.split('ctau-')[1].split('mm')[0])
        else:
            T = float(m.split('ctau-')[1].split('mm')[0].replace('p','.'))
        listOfBins = []
        #
        nSigs = {}
        nBGs = {}
        SOverSqrtB = {}
        #
        if doSmartScaling:
            with open(scalingFile) as fin:
                for l_,l in enumerate(fin.readlines()):
                    if l.startswith("#"):
                        continue
                    ls = l.split(",")
                    if sigModel=="HTo2ZdTo2mu2x":
                        if (float(ls[1])== float(M)) and (float(ls[2])== float(T)):
                            obs = float(ls[3])
                            exp = float(ls[4])
                            e2m = float(ls[5])
                            e1m = float(ls[6])
                            e1p = float(ls[7])
                            e2p = float(ls[8])
                            NORMCONST = 0.01 * ( e2m / 0.6 )
                            print(" -> Using smart scaling of %.5f for em2 limit of %.3f  to be 0.6" % (NORMCONST, e2m))
                            break
                        if (float(ls[1]) > float(M)) and (float(ls[2])== float(T)):
                            obs = float(lsprev[3])
                            exp = float(lsprev[4])
                            e2m = float(lsprev[5])
                            e1m = float(lsprev[6])
                            e1p = float(lsprev[7])
                            e2p = float(lsprev[8])
                            NORMCONST = 0.01 * ( e2m / 0.6 )
                            print(" -> Using smart scaling of %.5f for em2 limit of %.3f  to be 0.6" % (NORMCONST, e2m))
                            break
                        lsprev = ls
                    if "Scenario" in sigModel:
                        print("Openes normalizations for Scenario's")
                        print(ls)
                        #print(float(ls[1]), float(ls[2]), float(ls[3]))
                        #print(float(M), float(M2), float(T))
                        if (float(ls[1])== float(M2)) and (float(ls[2])== float(M)) and (float(ls[3])== float(T)):
                            obs = float(ls[4])
                            exp = float(ls[5])
                            e2m = float(ls[6])
                            e1m = float(ls[7])
                            e1p = float(ls[8])
                            e2p = float(ls[9])
                            NORMCONST = 10.0 * ( e2m / 0.6 ) # This one was used with 1.0 before but in this last test 10.
                            print(" -> Using smart scaling of %.5f for em2 limit of %.3f  to be 0.6" % (NORMCONST, e2m))
                            break

        #
        for d_,d in enumerate(dNames):
            print("Analyzing %s, in region %s"%(m, d))
            print("%s/%s_%s_%s_workspace.root"%(inDir,d,m,y))
            finame = "%s/%s_%s_%s_workspace.root"%(inDir,d,m,y)
            _finame = "%s/%s_%s_%s_workspace.root"%(_inDir,d,m,y)
            #
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
                print("Using a normalization constant of %.5f"%(NORMCONST))
                nSig = NORMCONST*nSig
            if (binidx > 22 and binidx < 35) or (binidx > 39):
                nSig = nSig * 0.82
            nSigs[binidx] = nSig
            print(f"Measured signal: {nSig}")
            # Retrieve signal mean and std. deviation
            mean = w.var("mean%s"%catExtS).getValV()
            sigma = w.var("sigma%s"%catExtS).getValV()
            # Retrieve MC stat. uncertainty from RooDataSet
            if useSignalMC:
                if w.var("signalRawNorm%s"%catExtS).getValV()>0.0:
                    mcstatunc = 1.0/ROOT.TMath.Sqrt(w.var("signalRawNorm%s"%catExtS).getValV())
                else:
                    mcstatunc = 1.0
            else:
                luminosity = 35 if year=="2022" else 27
                ngenfilter = 300000 if year=="2022" else 340000 # averaged between files
                efilter = -99
                if sigModel=="HTo2ZdTo2mu2x":
                    mass = float(m.split('MZd-')[1].split('_')[0])
                    smass = ("MZd-%.1f"%(mass)).replace('.', 'p')
                    with open('data/hahm-request.csv') as mcinfo:
                        reader = csv.reader(mcinfo, delimiter=',')
                        for row in reader:
                            if smass in row[0]:
                                efilter = float(row[-1])
                                break
                    if efilter < 0:
                        with open('data/hahm-request.csv') as mcinfo:
                            smass = ("MZd-%.0f"%(mass)) + 'p0'
                            reader = csv.reader(mcinfo, delimiter=',')
                            for row in reader:
                                if smass in row[0]:
                                    efilter = float(row[-1])
                                    break
                    if efilter < 0:
                        efilter = 0.3
                if efilter < 0:
                    raise Exception("The mcstat uncertainty can't be computed for %s"%(m))
                mcstatunc = 1.0/ROOT.TMath.Sqrt(nSig/NORMCONST*ngenfilter/efilter/(1000*luminosity))
                if mcstatunc > 0.5: mcstatunc = 0.5 # To control < 1 raw events
            # Retrive BG normalization:
            try:
                nBG = w.data("data_obs%s"%catExtB).sumEntries()
            except TypeError: # if it doesn't exist... (assuming there is signal)
                print("Background not found for this mass, skipping to next")
                #isValidPoint = False
                continue
            print(f"Measured background: {nBG}")
            nBGs[binidx] = nBG
            listOfBins.append(binidx)
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
                #spline_trg = filesyst.Get("spline_trgsys_HTo2ZdTo2mu2x_%s_%.1f_%s"%(d, T, y))
                spline_trg = filesyst.Get("spline_trgsys_HTo2ZdTo2mu2x_%s_%.1f_%s"%(d, T, 2022)) # Use always 2022 as systematics are the same (RE-CHECK for better implementation)
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
                #spline_trg = filesyst.Get("spline_selsys_HTo2ZdTo2mu2x_%s_%.1f_%s"%(d, T, y))
                spline_trg = filesyst.Get("spline_selsys_HTo2ZdTo2mu2x_%s_%.1f_%s"%(d, T, 2022)) # Use always 2022 as systematics are the same (RE-CHECK for better implementation)
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

            if "Scenario" not in sigModel:
                cardn = "%s/card%s_ch%d_%s_M%.3f_ctau%.2f_%s.txt"%(outDir,cname,binidx,sigModel,M,T,y)
            else:
                cardn = "%s/card%s_ch%d_%s_M%.3f_M%.3f_ctau%.2f_%s.txt"%(outDir,cname,binidx,sigModel,M2,M,T,y)
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
                if doHybridFit:
                    if nBG > 100:
                        card.write("shapes data_obs * %s %s:hist_obs%s\n"%(_finame,wsname,catExtB))
                    else:
                        card.write("shapes data_obs * %s %s:data_obs%s\n"%(_finame,wsname,catExtB))
                elif doBinnedFit:
                    card.write("shapes data_obs * %s %s:hist_obs%s\n"%(_finame,wsname,catExtB))
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
            #
            # Systematics on signal shape:
            if meanFloat:
                card.write("mean%s param %.3f -%.3f/+%.3f\n"%(catExtS,mean,0.5*sigma,0.5*sigma)) # Shape systematic on dimuon mass mean value
            elif fullMeanFloat:
                card.write("mean param %.3f %.3f\n"%(mean,sigma)) # Shape systematic on dimuon mass mean value
            elif meanvar/float(m)>1e-6:
                card.write("mean param %.3f %.3f\n"%(mean,meanvar))
            if doMuonResolution:
                card.write("sigma%s param %.5f %.5f\n"%(catExtS,sigma,sigmavar))                        
            #
            ## Cut and count or discrete profiling method:
            if doCounting:
                card.write("bg_norm_ch%d gmN %d - 1.0\n"%(binidx,int(nBG)))
            else:
                if not useSinglePDF:
                    card.write("pdf_index_ch%d_%s discrete\n"%(binidx, year)) # For discrete profiling
                    #card.write("pdf_index discrete\n") # For discrete profiling
            card.close()
            print("> %s ready and closed!"%(cardn))
            
            if len(nSigs)==len(nBGs) and nBGs[binidx]!=0:
                SOverSqrtB[binidx] = nSigs[binidx] / (nBGs[binidx]**(0.5))
                print(f"Significance for this model is {SOverSqrtB[binidx]}")
            elif nBGs[binidx]<1e-6:
                SOverSqrtB[binidx] = -999
                print(f"Significance set to {SOverSqrtB[binidx]}")
            else:
                SOverSqrtB[binidx] = 0
                raise Exception("Signal and background points are not the same, probably you shouldn't be doing datacards from these workspaces")
                          
        
            ## text2workspace for individual cards:
            if doIndividualRootCard:
                os.chdir(outDir)
                if noModel:
                    os.system("text2workspace.py %s/card%s_ch%d_nomodel_M%s_%s.txt -m %s"%(_inDir,cname,binidx,m,y,m))
                elif "Scenario" not in sigModel:
                    os.system("text2workspace.py %s/card%s_ch%d_%s_M%.3f_ctau%.2f_%s.txt"%(outDir,cname,binidx,sigModel,M,T,y))                        
                else:
                    os.system("text2workspace.py %s/card%s_ch%d_%s_M%.3f_M%.3f_ctau%.2f_%s.txt"%(outDir,cname,binidx,sigModel,M2,M,T,y))
                os.chdir(thisDir)
        #if not isValidPoint:
        #    continue
        #
        ## Combine cards:
        if len(dNames)>1:
            print("Changing dir to %s"%(outDir))
            print("listOfBins to combine: ", listOfBins)
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
                if "Scenario" not in sigModel:
                    icard = "card%s_ch%d_%s_M%.3f_ctau%.2f_%s.txt "%(cname,binidx,sigModel,M,T,y)
                else:
                    icard = "card%s_ch%d_%s_M%.3f_M%.3f_ctau%.2f_%s.txt "%(cname,binidx,sigModel,M2,M,T,y)
                if useOnlyZeroBackground:
                    if (nSigs[binidx]/NORMCONST > 1e-6) and (nBGs[binidx] < 0.99):
                        combinedCards += icard
                        print('!!!! Adding SR %s with background: %.3f'%(d, nBGs[binidx]))
                    else:
                        print('Skipping card: ', icard)
                else:
                    #if (nSigs[binidx]/NORMCONST > 1e-6) and (SOverSqrtB[binidx] > 1e-4*max(SOverSqrtB.values()) or SOverSqrtB[binidx] < 0):
                    if (nSigs[binidx]/NORMCONST > 1e-6):
                        combinedCards += icard
                    else:
                        print('Skipping card: ', icard)

            print(combinedCards)
            if combinedCards!="":
                print(f"Combining cards: {len(combinedCards.split(' '))}")
                if "Scenario" not in sigModel:
                    os.system("combineCards.py -S %s > card%s_combined_%s_M%.3f_ctau%.2f_%s.txt"%(combinedCards,cname,sigModel,M,T,y))
                    os.system("text2workspace.py %s/card%s_combined_%s_M%.3f_ctau%.2f_%s.txt --channel-masks"%(outDir,cname,sigModel,M,T,y))
                else:    
                    os.system("combineCards.py -S %s > card%s_combined_%s_M%.3f_M%.3f_ctau%.2f_%s.txt"%(combinedCards,cname,sigModel,M2,M,T,y))
                    os.system("text2workspace.py %s/card%s_combined_%s_M%.3f_M%.3f_ctau%.2f_%s.txt --channel-masks"%(outDir,cname,sigModel,M2,M,T,y))
            if not useSignalMC:
                for binidx in listOfBins:
                    if "Scenario" not in sigModel:
                        os.system("rm %s/card%s_ch%d_%s_M%.3f_ctau%.2f_%s.txt"%(outDir,cname,binidx,sigModel,M,T,y))
                    else:
                        os.system("rm %s/card%s_ch%d_%s_M%.3f_M%.3f_ctau%.2f_%s.txt"%(outDir,cname,binidx,sigModel,M2,M,T,y))
            os.chdir(thisDir)

# f it dir within the datacard directory is not needed anymore (avoid using rm -rf)
os.chdir(outDir)
#os.system('rm %s/*'%(_inDir))
#os.system('rmdir %s'%(_inDir))
os.chdir(thisDir)
