import os,sys
import ROOT
from datetime import date

user = os.environ.get("USER")
today= date.today().strftime("%b-%d-%Y")

wsname = "wfit"
thisDir = os.environ.get("PWD")
#inDir  = "%s/cpp/fitResults_fullRange_forCards/"%thisDir
inDir  = "%s/fitResults/"%thisDir

#fnfitParamsForShapeUnc = "%s/utils/signalFitParameters_muonResolutionUnc.root"%thisDir
#ffitParamsForShapeUnc = ROOT.TFile.Open(fnfitParamsForShapeUnc,"READ")
#fnfitParamsForAccUnc = "%s/data/acceff_interpolation_Run2.root"%thisDir
#ffitParamsForAccUnc = ROOT.TFile.Open(fnfitParamsForAccUnc,"READ")
#minMforSpline =  200.0
#maxMforSpline = 2500.0

useCategorizedSignal = True
useCategorizedBackground = True

useData = True
intLumi = 3.51
useSignalMC = True
doPartiaUnblinding = False
ext = "data"
if not useData:
    ext = "BGMC"

doCounting = False
useOnlyExponential = False
useOnlyPowerLaw = False
useOnlyBernstein = False
fullMeanFloat = False
meanFloat = False
doMuonResolution = True
noModel = False
dirExt = ""
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

outDir = ("%s/datacards_all%s_"%(thisDir,dirExt))+today
if not os.path.exists(outDir):
    os.makedirs(outDir)

useSinglePDF = False
if useOnlyExponential or useOnlyPowerLaw or useOnlyBernstein:
    useSinglePDF = True

dNames = []

#d_Dimuon_lxy0p0to2p7_iso0_pthigh_Signal_HTo2ZdTo2mu2x_MZd-7p0_ctau-1mm_2022_workspace.root
dNames.append("d_Dimuon_lxy0p0to0p5_iso0_ptlow")
dNames.append("d_Dimuon_lxy0p0to0p5_iso0_pthigh")
dNames.append("d_Dimuon_lxy0p0to0p5_iso1_ptlow")
dNames.append("d_Dimuon_lxy0p0to0p5_iso1_pthigh")
dNames.append("d_Dimuon_lxy0p5to2p7_iso0_ptlow")
dNames.append("d_Dimuon_lxy0p5to2p7_iso0_pthigh")
dNames.append("d_Dimuon_lxy0p5to2p7_iso1_ptlow")
dNames.append("d_Dimuon_lxy0p5to2p7_iso1_pthigh")
dNames.append("d_Dimuon_lxy2p7to6p5_iso0_ptlow")
dNames.append("d_Dimuon_lxy2p7to6p5_iso0_pthigh")
dNames.append("d_Dimuon_lxy2p7to6p5_iso1_ptlow")
dNames.append("d_Dimuon_lxy2p7to6p5_iso1_pthigh")
dNames.append("d_Dimuon_lxy6p5to11p0_iso0_ptlow")
dNames.append("d_Dimuon_lxy6p5to11p0_iso0_pthigh")
dNames.append("d_Dimuon_lxy6p5to11p0_iso1_ptlow")
dNames.append("d_Dimuon_lxy6p5to11p0_iso1_pthigh")
dNames.append("d_Dimuon_lxy11p0to16p0_iso0_ptlow")
dNames.append("d_Dimuon_lxy11p0to16p0_iso0_pthigh")
dNames.append("d_Dimuon_lxy11p0to16p0_iso1_ptlow")
dNames.append("d_Dimuon_lxy11p0to16p0_iso1_pthigh")
dNames.append("d_Dimuon_lxy16p0to70p0_iso0_ptlow")
dNames.append("d_Dimuon_lxy16p0to70p0_iso0_pthigh")
dNames.append("d_Dimuon_lxy16p0to70p0_iso1_ptlow")
dNames.append("d_Dimuon_lxy16p0to70p0_iso1_pthigh")
dNames.append("d_FourMu_sep")
#dNames.append("d_FourMu_osv") # Exclude for now, getting so many problems

years = []
#years.append("2022")
###
years.append("allEras")

# Signals
sigModels = []
sigModels.append("HTo2ZdTo2mu2x")
sigModel = "HTo2ZdTo2mu2x"


sigTags = []
if useSignalMC:
    if sigModel=="HTo2ZdTo2mu2x":
        sigMasses = [0.5, 0.7, 1.5, 2.0, 2.5, 5.0, 6.0, 7.0, 8.0, 10.0, 12.0, 14.0, 16.0, 20.0, 22.0, 24.0, 30.0, 34.0, 40.0, 44.0, 50.0]
        for  m in sigMasses:
            sigCTaus = [1, 10, 100, 100]
            for t in sigCTaus:
                if ((m < 1.0 and t > 10) or (m < 30.0 and t > 100)):
                    continue
                sigTags.append("Signal_HTo2ZdTo2mu2x_MZd-%s_ctau-%imm"%(str(m).replace('.','p'), t))

f2l = [0.0]
nSigTot = 1.0
if noModel:
    f2l = [0.0, 0.01, 0.05, 0.1, 0.25, 0.5, 0.75, 0.9, 0.95, 0.99, 1.0]

mean = 0.0
sigma = 0.0
for y in years:
   for m in sigTags:
       M = float(m.split('-')[1].split('_')[0].replace('p','.'))
       T = int(m.split('-')[2].split('mm')[0])
       listOfBins = []
       for d in dNames:
           print("Analyzing %s, in region %s"%(m, d))
           print("%s/%s_%s_%s_workspace.root"%(inDir,d,m,y))
           finame = "%s/%s_%s_%s_workspace.root"%(inDir,d,m,y)
           binidx=-1
           if d=="d_Dimuon_lxy0p0to0p5_iso0_ptlow":
               binidx=0
           elif d=="d_Dimuon_lxy0p0to0p5_iso0_pthigh":
               binidx=1
           elif d=="d_Dimuon_lxy0p0to0p5_iso1_ptlow":
               binidx=2
           elif d=="d_Dimuon_lxy0p0to0p5_iso1_pthigh":
               binidx=3
           elif d=="d_Dimuon_lxy0p5to2p7_iso0_ptlow":
               binidx=4
           elif d=="d_Dimuon_lxy0p5to2p7_iso0_pthigh":
               binidx=5
           elif d=="d_Dimuon_lxy0p5to2p7_iso1_ptlow":
               binidx=6
           elif d=="d_Dimuon_lxy0p5to2p7_iso1_pthigh":
               binidx=7
           elif d=="d_Dimuon_lxy2p7to6p5_iso0_ptlow":
               binidx=8
           elif d=="d_Dimuon_lxy2p7to6p5_iso0_pthigh":
               binidx=9
           elif d=="d_Dimuon_lxy2p7to6p5_iso1_ptlow":
               binidx=10
           elif d=="d_Dimuon_lxy2p7to6p5_iso1_pthigh":
               binidx=11
           elif d=="d_Dimuon_lxy6p5to11p0_iso0_ptlow":
               binidx=12
           elif d=="d_Dimuon_lxy6p5to11p0_iso0_pthigh":
               binidx=13
           elif d=="d_Dimuon_lxy6p5to11p0_iso1_ptlow":
               binidx=14
           elif d=="d_Dimuon_lxy6p5to11p0_iso1_pthigh":
               binidx=15
           elif d=="d_Dimuon_lxy11p0to16p0_iso0_ptlow":
               binidx=16
           elif d=="d_Dimuon_lxy11p0to16p0_iso0_pthigh":
               binidx=17
           elif d=="d_Dimuon_lxy11p0to16p0_iso1_ptlow":
               binidx=18
           elif d=="d_Dimuon_lxy11p0to16p0_iso1_pthigh":
               binidx=19
           elif d=="d_Dimuon_lxy16p0to70p0_iso0_ptlow":
               binidx=20
           elif d=="d_Dimuon_lxy16p0to70p0_iso0_pthigh":
               binidx=21
           elif d=="d_Dimuon_lxy16p0to70p0_iso1_ptlow":
               binidx=22
           elif d=="d_Dimuon_lxy16p0to70p0_iso1_pthigh":
               binidx=23                
           elif d=="d_FourMu_sep":
               binidx=24
           elif d=="d_FourMu_osv":
               binidx=25                
           catExtS = ""
           catExtB = ""
           if useCategorizedSignal:
               catExtS = "_ch%d"%binidx
           if useCategorizedBackground:
               catExtB = "_ch%d"%binidx
           listOfBins.append(binidx)
           # Open input file with workspace
           f = ROOT.TFile(finame)
           # Retrieve workspace from file
           w = f.Get(wsname)
           # Retrieve signal normalization
           nSig = w.var("signalNorm%s"%catExtS).getValV()
           #nSig = nSig*intLumi*1000.0/200000.0
           if doPartiaUnblinding:
               nSig = 0.1*nSig
           # Retrieve signal mean and std. deviation
           mean = w.var("mean%s"%catExtS).getValV()
           sigma = w.var("sigma%s"%catExtS).getValV()
           # Retrieve MC stat. uncertainty from RooDataSet
           if w.var("signalRawNorm%s"%catExtS).getValV()>0.0:
               mcstatunc = 1.0/ROOT.TMath.Sqrt(w.var("signalRawNorm%s"%catExtS).getValV())
           else:
               mcstatunc = 1.0
           # Retrive BG normalization:
           nBG = w.data("data_obs%s"%catExtB).sumEntries()
           # Close input file with workspace
           f.Close()
           #if not doCounting:
           #    os.system("cp %s %s/"%(finame,outDir))
           #    finame = "%s/%s_%s_%s_workspace.root"%(inDir,d,m,y)
               #finame = "%s_%s_M%s_%s_workspace.root"%(d,s,m,y)

           # Define systematics that are independent of signal mass
           btagsyst = 0.10
           #if binidx>=2:
           #    btagsyst = 0.05
           #
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

           f2l = [1.0]
           for f in f2l:
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
                   card.write("shapes data_obs * %s %s:data_obs%s\n"%(finame,wsname,catExtB))
                   card.write("shapes signal * %s %s:signal%s\n"%(finame,wsname,catExtS))
                   if not useSinglePDF:
                       card.write("shapes background * %s %s:roomultipdf%s\n"%(finame,wsname,catExtB))
                   elif useOnlyExponential:
                       card.write("shapes background * %s %s:background_exponential%s\n"%(finame,wsname,catExtB))
                   elif useOnlyPowerLaw:
                       card.write("shapes background * %s %s:background_powerlaw%s\n"%(finame,wsname,catExtB))
                   elif useOnlyBernstein:
                       card.write("shapes background * %s %s:background_bernstein%s\n"%(finame,wsname,catExtB))
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
                   card.write("rate %.3f 1\n"%(nSig)) # CELIANOTE: Is this really correct? 
               card.write("------------\n")  
               # Systematics
               card.write("lumi_13TeV lnN 1.016 -\n") # Integrated luminosity uncertainty on signal (fully correlated)
               #card.write("CMS_eff_trigger lnN %.3f -\n"%(1.0+triggersyst)) # Systematic uncertainty on signal from trigger (fully correlated)
               #card.write("CMS_eff_muonid lnN %.3f -\n"%(1.0+muonsfsyst)) # Systematic uncertainty on signal from muon RECO, ID, isolation (fully correlated)
               #card.write("CMS_eff_muonsel lnN %.3f -\n"%(1.0+muonselsyst)) # Systematic uncertainty on signal from muon additional selection (fully correlated)
               card.write("CMS_eff_btag lnN %.3f -\n"%(1.0+btagsyst)) # Systematic uncertainty on signal from b-tagging (fully correlated)
               #card.write("CMS_scale_jet_ch%d lnN %.3f -\n"%(binidx,1.0+jecsyst)) # Systematic uncertainty on signal from JES (uncorrelated)
               #card.write("mcstat_ch%d lnN %.3f -\n"%(binidx,1.0+mcstatunc)) # MC stat. uncertainty (uncorrelated)
               #card.write("accstat_ch%d lnN %.3f -\n"%(binidx,1.0+terrtot)) # Stat. uncertainty on average acceptance (uncorrelated)
               #if meanFloat:
               #    card.write("mean param %.3f -%.3f/+%.3f\n"%(mean,0.5*sigma,0.5*sigma)) # Shape systematic on dimuon mass mean value
               #elif fullMeanFloat:
               #    card.write("mean param %.3f %.3f\n"%(mean,sigma)) # Shape systematic on dimuon mass mean value
               #elif meanvar/float(m)>1e-6:
               #    card.write("mean param %.3f %.3f\n"%(mean,meanvar))
               #if doMuonResolution:
               #    card.write("sigma param %.3f %.3f\n"%(sigma,sigmavar))                        
               if doCounting:
                   card.write("bg_norm_ch%d gmN %d - 1.0\n"%(binidx,int(nBG)))
               else:
                   if not useSinglePDF:
                       card.write("pdf_index_ch%d discrete\n"%(binidx)) # For discrete profiling
                       #card.write("pdf_index discrete\n") # For discrete profiling
               card.close()
           
               ## text2workspace for individual cards:
               #os.chdir(outDir)
               #if noModel:
               #    os.system("text2workspace.py card%s_ch%d_nomodel_M%s_%s.txt -m %s"%(cname,binidx,m,y,m))
               #else:
               #    os.system("text2workspace.py card%s_ch%d_%s_M%.1f_ctau%i_%s.txt"%(cname,binidx,sigModel,M,T,y))                        
               #os.chdir(thisDir)

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
           os.system("text2workspace.py card%s_combined_%s_M%.1f_ctau%i_%s.txt"%(cname,sigModel,M,T,y))
           os.chdir(thisDir)
       

      
