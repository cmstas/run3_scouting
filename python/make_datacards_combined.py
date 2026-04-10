import os,sys
import ROOT
from datetime import date
import csv
import numpy as np

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
doRootCard = True
doSmartScaling = True
useOnlyZeroBackground = False
mergeEmptyBins = True
combineMeans = False
combineSigmas = False

## doc: Smart scaling allows to have the limit around 0.5, or alternatively with the 2.5% quantile above 0.25

# In line arguments
sigModel = ""
if len(sys.argv)>1:
    fit = sys.argv[1]
    inDirs = sys.argv[2].split(',')
    years = sys.argv[3].split(',')
    if len(sys.argv)>4:
        sigModel = sys.argv[4]
    else:
        sigModel = "HTo2ZdTo2mu2x" # HTo2ZdTo2mu2x : ScenarioB1 : ScenarioA : BToPhi
    if len(sys.argv)>5:
        NORMCONST = float(sys.argv[5])
    else:
        NORMCONST = 0.001
    
if doSmartScaling and not len(sys.argv)>5:
    print("---------------------------Accessing file")
    if sigModel=="HTo2ZdTo2mu2x":
        if not useSignalMC:
            scalingFile = '/ceph/cms/store/user/fernance/Run3ScoutingOutput/limits_Apr-15-2025_HTo2ZdTo2mu2x_Norm0p01_asymptotic_vsMass_allEras/limits_HTo2ZdTo2mu2x_allEras.txt'
        else:
            scalingFile = '/ceph/cms/store/user/fernance/Run3ScoutingOutput/limits_HTo2ZdTo2mu2x_NormSmart_Apr-28-2025_vsCTau_asymptotic_allEras/limits_HTo2ZdTo2mu2x_asymptotic_allEras.txt'
    if sigModel=="BToPhi":
        if not useSignalMC:
            #scalingFile = '/ceph/cms/store/user/fernance/Run3ScoutingOutput/limits_Apr-15-2025_HTo2ZdTo2mu2x_Norm0p01_asymptotic_vsMass_allEras/limits_HTo2ZdTo2mu2x_allEras.txt'
            #scalingFile = 'combineScripts/SmartLimitNorm/limits_BToPhi_asymptotic_allEras_1mm.txt'
            #scalingFile = 'combineScripts/SmartLimitNorm/limits_BToPhi_asymptotic_allEras_10-100mm.txt'
            scalingFile = 'combineScripts/SmartLimitNorm/limits_BToPhi_asymptotic_allEras_vsCTau.txt'
        else:
            scalingFile = 'results_BToPhi_asymptotic/limits_BToPhi_asymptotic_allEras.txt'
            scalingFile = 'results_BToPhi_MC/limits_BToPhi_asymptotic_allEras.txt'
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
    if 'ScenarioA' not in sigModel:
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
if 'ScenarioA' not in sigModel:
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


# Output directory
if not doSmartScaling:
    outDir = ("%s/datacards_%s_Norm%s_%s_"%(thisDir, sigModel, float(NORMCONST), dirExt))+today+"_allEras"
else:
    outDir =  ("%s/datacards_%s_NormSmart_%s_"%(thisDir, sigModel, dirExt))+today+"_allEras"
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

for y_,y in enumerate(years):
    #
    inDir = "%s/%s"%(thisDir, inDirs[y_])
    os.system('cp -r %s %s/'%(inDir, outDir))
    os.system('chmod u+w %s/%s/*.root'%(outDir, inDirs[y_]))


sigTags = []
if sigModel=="HTo2ZdTo2mu2x":
    if useSignalMC:
        if not validation:
            sigMasses = [1.5, 2.0, 2.5, 5.0, 7.0, 8.0, 14.0, 16.0, 20.0, 22.0, 24.0, 30.0, 34.0, 40.0, 50.0]
            sigMasses = [1.5, 2.0, 2.5, 5.0, 7.0, 8.0, 14.0, 16.0, 20.0, 22.0, 24.0, 30.0, 40.0, 50.0]
            sigMasses = [30.0, 40.0, 50.0]
            #sigMasses = [20.0]
            sigMasses = [2.0]
            for  m in sigMasses:
                sigCTaus = [0.10, 0.16, 0.25, 0.40, 0.63, 1.00, 1.60, 2.50, 4.00, 6.30, 10.00, 16.00, 25.00, 40.00, 63.00, 100.00, 160.00, 250.00, 400.00, 630.00, 1000.00]
                #sigCTaus = [160.00, 250.00, 400.00, 630.00, 1000.00]
                sigCTaus = [ 0.63, 1.00, 1.60, 2.50]
                #sigCTaus = [0.10, 0.16, 0.25, 0.40, 0.63, 1.00, 1.60, 2.50, 4.00, 6.30, 10.00]
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
        #sigMasses = [0.30, 1.25, 1.50, 2.00] #Other masses are either too small or too close to SM resonance
        sigMasses = [1.25, 1.50, 2.00] #Other masses are either too small or too close to SM resonance
        for m in sigMasses:
            #sigCTaus = [0.1, 1, 10, 100]
            sigCTaus = [0.10, 0.16, 0.25, 0.40, 0.63, 1.00, 1.60, 2.50, 4.00, 6.30, 10.00, 16.00, 25.00, 40.00, 63.00, 100.00]
            for t in sigCTaus:
                sigTags.append("Signal_BToPhi_MPhi-%s_ctau-%.2fmm"%(('%.2f'%m).replace('.','p'), t))
    elif usePredefinedGrid:
        with open('data/BToPhi_limitgrid.txt', 'r') as f:
            masses = f.readlines()
            sigCTaus = [100]
            for mass in masses:
                m = float(mass)
                for t in sigCTaus:
                    sigTags.append("Signal_BToPhi_MPhi-%.3f_ctau-%.2fmm"%(m, t))
elif sigModel=="ScenarioB1":
    sigMasses = []
    #sigMasses.append([1,0.33])
    #sigMasses.append([2,0.67])
    #sigMasses.append([4,1.33])
    sigMasses.append([5,1.67])
    #sigMasses.append([3.33,0.33])
    #sigMasses.append([6.,2.])
    #sigMasses.append([7.5,2.5])
    #sigMasses.append([12.,1.20])
    #sigCTaus = [0.10, 0.25, 0.60, 1.00, 2.50, 6.00, 10.00, 25.00, 60.00, 100.00]
    #sigCTaus = [0.10, 1.00, 10.00]
    #sigCTaus = [1000.00]
    sigCTaus = [0.10, 0.25]
    for m in sigMasses:
        for t in sigCTaus:
            if m==[6.,2.]:
                sigTags.append("Signal_ScenarioB1_Mpi-6_MA-2_ctau-%.2fmm" % (float(t)))
            elif m==[7.5,2.5]:
                sigTags.append("Signal_ScenarioB1_Mpi-7p50_MA-2p50_ctau-%.2fmm" % (float(t)))
            else:
                sigTags.append("Signal_ScenarioB1_Mpi-%i_MA-%s_ctau-%.2fmm" % (m[0], ('%.2f'%m[1]).replace('.','p'), float(t)))

elif sigModel=="ScenarioA":
    sigMasses = []
    #sigMasses.append([1,0.33])
    #sigMasses.append([2,0.67])
    #sigMasses.append([4,1.33])
    sigMasses.append([5,1.67])
    #sigMasses.append([3.33,0.33])
    #sigMasses.append([6.,2.])
    #sigMasses.append([7.5,2.5])
    #sigMasses.append([12.,1.20])
    #sigCTaus = [0.1, 1, 10, 100]
    #sigCTaus = [0.10, 0.25, 0.60, 1.00, 2.50, 6.00, 10.00, 25.00, 60.00, 100.00, 1000.0]
    #sigCTaus = [1000.00]
    sigCTaus = [0.10]
    for m in sigMasses:
        for t in sigCTaus:
            if m==[6.,2.]:
                sigTags.append("Signal_ScenarioA_Mpi-6_MA-2_ctau-%.2fmm" % (float(t)))
            elif m==[7.5,2.5]:
                sigTags.append("Signal_ScenarioA_Mpi-7p50_MA-2p50_ctau-%.2fmm" % (float(t)))
            else:
                sigTags.append("Signal_ScenarioA_Mpi-%i_MA-%s_ctau-%.2fmm" % (m[0], ('%.2f'%m[1]).replace('.','p'), float(t)))

f2l = [0.0]
nSigTot = 1.0
if noModel:
    f2l = [0.0, 0.01, 0.05, 0.1, 0.25, 0.5, 0.75, 0.9, 0.95, 0.99, 1.0]

mean = 0.0
sigma = 0.0
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
                if sigModel=="BToPhi":
                    if (float(ls[1])== float(M)) and (float(ls[2])== float(T)):
                        obs = float(ls[3])
                        exp = float(ls[4])
                        e2m = float(ls[5])
                        e1m = float(ls[6])
                        e1p = float(ls[7])
                        e2p = float(ls[8])
                        NORMCONST = 1.00 * ( e2m / 0.6 )
                        print(" -> Using smart scaling of %.5f for em2 limit of %.3f  to be 0.6" % (NORMCONST, e2m))
                        break
                    if (float(ls[1]) > float(M)) and (float(ls[2])== float(T)):
                        obs = float(lsprev[3])
                        exp = float(lsprev[4])
                        e2m = float(lsprev[5])
                        e1m = float(lsprev[6])
                        e1p = float(lsprev[7])
                        e2p = float(lsprev[8])
                        NORMCONST = 1.00 * ( e2m / 0.6 )
                        print(" -> Using smart scaling of %.5f for em2 limit of %.3f  to be 0.6" % (NORMCONST, e2m))
                        break
                    lsprev = ls
                if "Scenario" in sigModel:
                    print("Openes normalizations for Scenario's")
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
    #
    #
    #
    channel_name        = []
    shapes_background   = []
    shapes_data         = []
    shapes_signal       = []
    bins_names          = []
    process_nSig        = []
    nuis_CMS_eff_sel    = []
    nuis_CMS_eff_trg    = []
    nuis_lumi_13p6TeV   = []
    nuis_mcstat         = []
    nuis_mean           = []
    nuis_width          = []
    nuis_width          = []
    nuis_sigmas_2mu     = []
    nuis_sigmas_s4mu    = []
    nuis_sigmas_o4mu    = []
    nuis_pdf_index      = []
    #
    #
    for d_,d in enumerate(dNames):
        print("Analyzing %s, in region %s"%(m, d))
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

        #
        ## Loop over years
        #
        factor_dataEvents = 1
        sum_dataEvents    = 0
        y_shapes_background   = []
        y_shapes_data         = []
        y_shapes_signal       = []
        y_bins_names          = []
        y_process_nSig        = []
        y_process_nBG         = []
        y_nuis_CMS_eff_sel    = []
        y_nuis_CMS_eff_trg    = []
        y_nuis_lumi_13p6TeV   = []
        y_nuis_mcstat         = []
        y_nuis_mean           = []
        y_nuis_width          = []
        y_nuis_pdf_index      = []
        #
        for y_,y in enumerate(years):
            #
            inDir = "%s/%s"%(outDir, inDirs[y_])
            print("%s/%s_%s_%s_workspace.root"%(inDir,d,m,y))
            finame = "%s/%s_%s_%s_workspace.root"%(inDir,d,m,y)
            _finame = "%s/%s_%s_%s_workspace.root"%(inDirs[y_],d,m,y)
            #
            if y=='2022':
                chname = 'ch22_%i'%(binidx)
            else:
                chname = 'ch23_%i'%(binidx)
            #
            catExtS = ""
            catExtB = ""
            if useCategorizedSignal:
                catExtS = "_ch%d_%s"%(binidx, y)
            if useCategorizedBackground:
                catExtB = "_ch%d_%s"%(binidx, y)
            # Open input file with workspace
            print('Modifying finame!!!!')
            f = ROOT.TFile(finame, "UPDATE")
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
            if ((binidx > 22 and binidx < 35) or (binidx > 39)):
                print("Manually applying the scale factor on the most displaced regions")
                nSig = nSig * 0.82 # Manually applying the scale factor on the most displaced regions
            print(f"Measured signal: {nSig}")
            # Retrieve signal mean and std. deviation
            mean = w.var("mean%s"%catExtS).getValV()
            sigma = w.var("sigma%s"%catExtS).getValV()
            #sigmavar = 0.06*sigma # 0.5*sigma
            sigmavar = 0.5*sigma # 0.5*sigma
            #
            if combineMeans:
                mean_variable = w.var("mean%s"%catExtS)
                if 'Dimuon' in d:
                    mean_variable.SetName('mean_signal_2mu')
                    mean_variable.SetTitle('mean_signal_2mu')
                elif 'FourMu_sep' in d:
                    mean_variable.SetName('mean_signal_s4mu')
                    mean_variable.SetTitle('mean_signal_s4mu')
                else:
                    mean_variable.SetName('mean_signal_o4mu')
                    mean_variable.SetTitle('mean_signal_o4mu')
                w.Write("", ROOT.TFile.kOverwrite)
            if combineSigmas:
                sigma_variable = w.var("sigma%s"%catExtS)
                if 'Dimuon' in d:
                    sigma_variable.SetName('sigma_signal_2mu')
                    sigma_variable.SetTitle('sigma_signal_2mu')
                elif 'FourMu_sep' in d:
                    sigma_variable.SetName('sigma_signal_s4mu')
                    sigma_variable.SetTitle('sigma_signal_s4mu')
                else:
                    sigma_variable.SetName('sigma_signal_o4mu')
                    sigma_variable.SetTitle('sigma_signal_o4mu')
                w.Write("", ROOT.TFile.kOverwrite)
            # Retrieve MC stat. uncertainty from RooDataSet
            if useSignalMC:
                if w.var("signalRawNorm%s"%catExtS).getValV()>0.0:
                    mcstatunc = 1.0/ROOT.TMath.Sqrt(w.var("signalRawNorm%s"%catExtS).getValV())
                    print(f'>> Numero raw de eventos:  {w.var("signalRawNorm%s"%catExtS).getValV()}')
                else:
                    mcstatunc = 1.0
            else:
                luminosity = 35 if y=="2022" else 27
                ngenfilter = 300000 if y=="2022" else 340000 # averaged between files
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
                if sigModel=="BToPhi":
                    efilter=1.0
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
            #
            # 
            ## Define systematics from up and down variations
            #
            #
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
            #
            # Selection systematic:
            # This is how it was before:
            #try:
            #    w_sel_up = f.Get(wsname + '_sel_up')
            #    w_sel_down = f.Get(wsname + '_sel_down')
            #    nSig_selUp = w_sel_up.var("signalNorm%s"%catExtS).getValV()
            #    nSig_selDown = w_sel_down.var("signalNorm%s"%catExtS).getValV()
            #    if useNorm:
            #        nSig_selUp = NORMCONST*nSig_selUp
            #        nSig_selDown = NORMCONST*nSig_selDown
            #    selsyst = max([(nSig_selUp/nSig - 1.0), (1.0 - nSig_selDown/nSig)])
            #except AttributeError: # No up and down variations in this tree, probably interpolated point
            #    filesyst = ROOT.TFile.Open("data/systematicSplines_2022.root", "READ")
            #    #spline_trg = filesyst.Get("spline_selsys_HTo2ZdTo2mu2x_%s_%.1f_%s"%(d, T, y))
            #    spline_trg = filesyst.Get("spline_selsys_HTo2ZdTo2mu2x_%s_%.1f_%s"%(d, T, 2022)) # Use always 2022 as systematics are the same (RE-CHECK for better implementation)
            #    selsyst = spline_trg.Eval(M)
            #    filesyst.Close()
            #
            # This is the correct way to do it:
            if 'FourMu' in d:
                selsyst = 0.1
            if 'lxy0p0to0p2' in d:
                selsyst = 0.01
            elif 'lxy0p2to1p0' in d:
                selsyst = 0.02
            elif 'lxy1p0to2p4' in d:
                selsyst = 0.03
            elif 'lxy2p4to3p1' in d:
                selsyst = 0.06
            elif 'lxy3p1to7p0' in d:
                selsyst = 0.1
            elif 'lxy7p0to11p0' in d:
                selsyst = 0.3
            elif 'lxy11p0to16p0' in d:
                selsyst = 0.3
            elif 'lxy16p0to70p0' in d:
                selsyst = 0.3
            ## Close input file with workspace
            f.Close()

            ##
            if nBG!=0:
                SOverSqrtB = nSig / (nBG**(0.5))
                print(f"Significance for this model is {SOverSqrtB}")
            elif nBG<1e-6:
                SOverSqrtB = -999
                print(f"Significance set to {SOverSqrtB}")
            else:
                SOverSqrtB = 0
                raise Exception("Signal and background points are not the same, probably you shouldn't be doing datacards from these workspaces")

            if nSig/NORMCONST <= 1e-6 or w.var("signalRawNorm%s"%catExtS).getValV() < 10:
                print('REJECTED')
                continue

            #
            #
            y_bins_names.append(chname)
            #
            if doHybridFit:
                if nBG > 100:
                    y_shapes_data.append("%s %s:hist_obs%s\n"%(_finame,wsname,catExtB))
                else:
                    y_shapes_data.append("%s %s:data_obs%s\n"%(_finame,wsname,catExtB))
            elif doBinnedFit:
                y_shapes_data.append("%s %s:hist_obs%s\n"%(_finame,wsname,catExtB))
            else:
                y_shapes_data.append("%s %s:data_obs%s\n"%(_finame,wsname,catExtB))
            y_shapes_background.append("%s %s:roomultipdf%s\n"%(_finame,wsname,catExtB))
            y_shapes_signal.append("%s %s:signal%s\n"%(_finame,wsname,catExtS))
            #
            factor_dataEvents = factor_dataEvents * nBG
            sum_dataEvents = sum_dataEvents + nBG            
            y_process_nBG.append(nBG)
            y_process_nSig.append(nSig)
            ## Other systematics
            #
            y_nuis_CMS_eff_trg.append(trgsyst)
            y_nuis_CMS_eff_sel.append(selsyst)
            y_nuis_lumi_13p6TeV.append(0.014)
            y_nuis_mean.append("mean%s param %.3f -%.3f/+%.3f"%(catExtS,mean,0.5*sigma,0.5*sigma))
            y_nuis_width.append("sigma%s param %.5f %.5f"%(catExtS,sigma,sigmavar))
            y_nuis_pdf_index.append("pdf_index_ch%d_%s discrete"%(binidx, y))
            y_nuis_mcstat.append(mcstatunc)
            if 'Dimuon' in d:
                nuis_sigmas_2mu.append(sigma)
            elif 'FourMu_sep' in d:
                nuis_sigmas_s4mu.append(sigma)
            else:
                nuis_sigmas_o4mu.append(sigma)
            #
            #
        #if factor_dataEvents < 0.99 and mergeEmptyBins:
        if sum_dataEvents < 1.00 and mergeEmptyBins and len(y_bins_names) > 0:
            print("Years merged")
            print(y_nuis_mcstat)
            bins_names.append('chFF_%i'%(binidx))
            data_max = y_process_nBG.index(max(y_process_nBG))
            shapes_data.append(y_shapes_data[data_max])
            shapes_background.append(y_shapes_background[data_max])
            shapes_signal.append(y_shapes_signal[0])
            process_nSig.append(sum(y_process_nSig))
            nuis_CMS_eff_sel.append(sum(y_nuis_CMS_eff_sel)/len(y_nuis_CMS_eff_sel))
            nuis_CMS_eff_trg.append(sum(y_nuis_CMS_eff_trg)/len(y_nuis_CMS_eff_trg))
            nuis_lumi_13p6TeV.append(sum(y_nuis_lumi_13p6TeV)/len(y_nuis_lumi_13p6TeV))
            if len(y_nuis_mcstat) == 2:
                nuis_mcstat.append(1.0 / (1.0/y_nuis_mcstat[0] + 1.0/y_nuis_mcstat[1])) # hardcoded to two years
            else:
                nuis_mcstat.append(y_nuis_mcstat[0])
            nuis_mean.append(y_nuis_mean[0])
            nuis_width.append(y_nuis_width[0])
            nuis_pdf_index.append(y_nuis_pdf_index[data_max])
        else:
            print("Years not merged")
            #
            bins_names = bins_names + y_bins_names
            shapes_data = shapes_data + y_shapes_data
            shapes_background = shapes_background + y_shapes_background
            shapes_signal = shapes_signal + y_shapes_signal
            process_nSig = process_nSig + y_process_nSig
            nuis_CMS_eff_sel = nuis_CMS_eff_sel + y_nuis_CMS_eff_sel
            nuis_CMS_eff_trg = nuis_CMS_eff_trg + y_nuis_CMS_eff_trg
            nuis_lumi_13p6TeV = nuis_lumi_13p6TeV + y_nuis_lumi_13p6TeV
            nuis_mcstat = nuis_mcstat + y_nuis_mcstat
            nuis_mean = nuis_mean + y_nuis_mean
            nuis_width = nuis_width + y_nuis_width
            nuis_pdf_index = nuis_pdf_index + y_nuis_pdf_index

    #
    #
    ## Card creation
    #
    nRegions = len(bins_names)
    line_bin            = "bin          "
    line_obs            = "observation  "
    line_bintitle       = "bin                                 "
    line_processtitle   = "process                             "
    line_processtype    = "process                             "
    line_rate           = "rate                                "
    line_CMS_eff_sel    = "CMS_eff_sel             lnN         "
    line_CMS_eff_trg    = "CMS_eff_trg             lnN         "
    line_lumi_13p6TeV   = "lumi_13p6TeV            lnN         "
    #
    cname = ""
    if "Scenario" not in sigModel:
        cardn = "%s/card%s_combined_%s_M%.3f_ctau%.2f_allEras.txt"%(outDir,cname,sigModel,M,T)
    else:
        cardn = "%s/card%s_combined_%s_M%.3f_M%.3f_ctau%.2f_allEras.txt"%(outDir,cname,sigModel,M2,M,T)
    if noModel:
        cardn = "%s/card%s_combined_nomodel_M%s_%s.txt"%(outDir,cname,m,y)
    #
    card = open("%s"%cardn,"w")
    card.write("imax %i number of bins\n"%(nRegions))
    card.write("jmax 1 number of processes minus 1\n")
    if not combineMeans and not combineSigmas:
        card.write("kmax %i number of nuisance parameters\n"%(3 + 3*nRegions))
    elif (combineMeans and not combineSigmas) or (combineSigmas and not combineMeans):
        if 'Scenario' in sigModel:
            if len(nuis_sigmas_s4mu) > 0:
                card.write("kmax %i number of nuisance parameters\n"%(3 + 2*nRegions + 2))
            else:
                card.write("kmax %i number of nuisance parameters\n"%(3 + 2*nRegions + 1))
        else:
            card.write("kmax %i number of nuisance parameters\n"%(3 + 2*nRegions + 3))
    else:
        if 'Scenario' in sigModel:
            card.write("kmax %i number of nuisance parameters\n"%(3 + nRegions + 4))
        else:
            card.write("kmax %i number of nuisance parameters\n"%(3 + nRegions + 6))
    card.write("----------------------------------------------------------------------------------------------------------------------------------\n")
    #
    #
    #
    for r in range(nRegions):
        card.write("shapes background %s %s"%(bins_names[r], shapes_background[r]))
        card.write("shapes data_obs %s %s"%(bins_names[r], shapes_data[r]))
        card.write("shapes signal %s %s"%(bins_names[r], shapes_signal[r]))
    card.write("----------------------------------------------------------------------------------------------------------------------------------\n")                       
    #
    for r in range(nRegions):
        line_bin += "%s  "%(bins_names[r])
        line_obs += "-1" + len(bins_names[r])*" "
    card.write(line_bin + '\n')
    card.write(line_obs + '\n')
    card.write("----------------------------------------------------------------------------------------------------------------------------------\n")
    #
    for r in range(nRegions):
        line_bintitle += bins_names[r] + (13 - len(bins_names[r]))*" "
        line_bintitle += bins_names[r] + (13 - len(bins_names[r]))*" " # x2
        line_processtitle += "signal       background   "
        line_processtype += "0            1            "
        line_rate += "%.7f    1            "%(process_nSig[r])
    card.write(line_bintitle + '\n')
    card.write(line_processtitle + '\n')
    card.write(line_processtype + '\n')
    card.write(line_rate + '\n')
    card.write("----------------------------------------------------------------------------------------------------------------------------------\n")
    # Systematics
    for r in range(nRegions):
        line_CMS_eff_sel += "%.3f        -            "%(1.0+nuis_CMS_eff_sel[r])
        line_CMS_eff_trg += "%.3f        -            "%(1.0+nuis_CMS_eff_trg[r])
        line_lumi_13p6TeV += "%.3f        -            "%(1.0+nuis_lumi_13p6TeV[r])
    card.write(line_CMS_eff_sel + '\n')
    card.write(line_CMS_eff_trg + '\n')
    card.write(line_lumi_13p6TeV + '\n')
    #
    for r in range(nRegions):
        line_mcstat_r = "mcstat_%s"%(bins_names[r]) + (17 - len(bins_names[r]))*" " + "lnN         "
        for rr in range(nRegions):
            if r==rr:
                line_mcstat_r += "%.3f        -            "%(1.0+nuis_mcstat[r])
            else:
                line_mcstat_r += "-            -            "
        card.write(line_mcstat_r + '\n') # MC stat. uncertainty (uncorrelated)
    #
    print('>> All sigmas')
    print(nuis_sigmas_2mu)
    print(nuis_sigmas_s4mu)
    print(nuis_sigmas_o4mu)
    if not combineMeans:
        for r in range(nRegions):
            card.write(nuis_mean[r] + '\n') # Shape systematic on dimuon mass mean value
    else:
        card.write("mean_signal_2mu param %.3f -%.3f/+%.3f\n"%(M,0.5*np.mean(nuis_sigmas_2mu),0.5*np.mean(nuis_sigmas_2mu)))
        if 'ScenarioB1' not in sigModel and 'BToPhi' not in sigModel and len(nuis_sigmas_s4mu) > 0:
            card.write("mean_signal_s4mu param %.3f -%.3f/+%.3f\n"%(M2,0.5*np.mean(nuis_sigmas_s4mu),0.5*np.mean(nuis_sigmas_s4mu)))
        if 'ScenarioA' not in sigModel and 'BToPhi' not in sigModel:
            card.write("mean_signal_o4mu param %.3f -%.3f/+%.3f\n"%(M2,0.5*np.mean(nuis_sigmas_o4mu),0.5*np.mean(nuis_sigmas_o4mu)))
    if not combineSigmas:
        for r in range(nRegions):
            card.write(nuis_width[r] + '\n') # Shape systematic on dimuon sigma value
    else:
        card.write("sigma_signal_2mu param %.3f -%.3f/+%.3f\n"%(np.mean(nuis_sigmas_2mu),0.06*np.mean(nuis_sigmas_2mu),0.06*np.mean(nuis_sigmas_2mu)))
        if 'ScenarioB1' not in sigModel and 'BToPhi' not in sigModel and len(nuis_sigmas_s4mu) > 0:
            card.write("sigma_signal_s4mu param %.3f -%.3f/+%.3f\n"%(np.mean(nuis_sigmas_s4mu),0.06*np.mean(nuis_sigmas_s4mu),0.06*np.mean(nuis_sigmas_s4mu)))
        if 'ScenarioA' not in sigModel and 'BToPhi' not in sigModel and len(nuis_sigmas_o4mu) > 0:
            card.write("sigma_signal_o4mu param %.3f -%.3f/+%.3f\n"%(np.mean(nuis_sigmas_o4mu),0.06*np.mean(nuis_sigmas_o4mu),0.06*np.mean(nuis_sigmas_o4mu)))
    for r in range(nRegions):
        card.write(nuis_pdf_index[r] + '\n') # For discrete profiling
    card.close()
    print("> %s ready and closed!"%(cardn))

    if combineMeans:
        print('> Correlating the means...')


    ## text2workspace for individual cards:
    if doRootCard:
        os.chdir(outDir)
        if noModel:
            os.system("text2workspace.py %s/card%s_combined_nomodel_M%s_%s.txt -m %s"%(_inDir,cname,m,y,m))
        elif "Scenario" not in sigModel:
            os.system("text2workspace.py %s/card%s_combined_%s_M%.3f_ctau%.2f_allEras.txt"%(outDir,cname,sigModel,M,T))                        
        else:
            os.system("text2workspace.py %s/card%s_combined_%s_M%.3f_M%.3f_ctau%.2f_allEras.txt"%(outDir,cname,sigModel,M2,M,T))
        os.chdir(thisDir)


# f it dir within the datacard directory is not needed anymore (avoid using rm -rf)
os.chdir(outDir)
#os.system('rm %s/*'%(_inDir))
#os.system('rmdir %s'%(_inDir))
os.chdir(thisDir)
