import ROOT
import numpy as np
import pickle

###
### HAHM model
###

HAHM_INPUT_LOOPER = '/ceph/cms/store/user/fernance/Run3ScoutingOutput/looperCutFlow_Mar-04-2026_2022_HAHM/'
HAHM_MASSES = [0.5, 0.7, 1.5, 2.0, 2.5, 5.0, 7.0, 8.0, 12.0, 14.0, 16.0, 20.0, 24.0, 30.0, 40.0, 50.0]


HAHM_TOTAL          = {}
HAHM_PASSTRIGGER    = {}
HAHM_PRESELECTION   = {}
HAHM_CANDIDATE      = {}
HAHM_MATERIAL_VETO  = {}
HAHM_ANGULAR        = {}
HAHM_DISPLACED      = {}
HAHM_HIT_VETO       = {}

for ctau in [1, 10, 100, 1000]:
    HAHM_TOTAL[ctau]          = np.zeros(len(HAHM_MASSES))
    HAHM_PASSTRIGGER[ctau]    = np.zeros(len(HAHM_MASSES))
    HAHM_PRESELECTION[ctau]   = np.zeros(len(HAHM_MASSES))
    HAHM_CANDIDATE[ctau]      = np.zeros(len(HAHM_MASSES))
    HAHM_MATERIAL_VETO[ctau]  = np.zeros(len(HAHM_MASSES))
    HAHM_ANGULAR[ctau]        = np.zeros(len(HAHM_MASSES))
    HAHM_DISPLACED[ctau]      = np.zeros(len(HAHM_MASSES))
    HAHM_HIT_VETO[ctau]       = np.zeros(len(HAHM_MASSES))

# ctau = 1mm
for ctau in [1, 10, 100, 1000]:
    for _,m in enumerate(HAHM_MASSES):
        if m < 1.5 and ctau > 10: continue
        if m < 2.0 and ctau > 100: continue
        file_ = ROOT.TFile(HAHM_INPUT_LOOPER + 'output_Signal_HTo2ZdTo2mu2x_MZd-%s_ctau-%imm_2022_2022_0To99.root'%(str(m).replace('.','p'), ctau))
        cutflow = file_.Get('cutflow')
        counts = file_.Get('counts')
        HAHM_TOTAL[ctau][_] = counts.GetBinContent(1)
        HAHM_PASSTRIGGER[ctau][_] = cutflow.GetBinContent(7)
        HAHM_PRESELECTION[ctau][_] = cutflow.GetBinContent(2)
        file_candidate = ROOT.TFile('/ceph/cms/store/user/fernance/Run3ScoutingOutput/fillerCutFlow_Mar-10-2026_2022_HAHM_noCuts/' + 'histograms_Signal_HTo2ZdTo2mu2x_MZd-%s_ctau-%.2fmm_2022_2022_0.root'%(str(m).replace('.','p'), ctau))
        counts_candidate = file_candidate.Get('d_Dimuon_full_inclusive')
        HAHM_CANDIDATE[ctau][_] = counts_candidate.numEntries()
        file_MatVeto = ROOT.TFile('/ceph/cms/store/user/fernance/Run3ScoutingOutput/fillerCutFlow_Mar-10-2026_2022_HAHM_MatVeto/' + 'histograms_Signal_HTo2ZdTo2mu2x_MZd-%s_ctau-%.2fmm_2022_2022_0.root'%(str(m).replace('.','p'), ctau))
        counts_MatVeto = file_MatVeto.Get('d_Dimuon_full_inclusive')
        HAHM_MATERIAL_VETO[ctau][_] = counts_MatVeto.numEntries()
        file_angular = ROOT.TFile('/ceph/cms/store/user/fernance/Run3ScoutingOutput/fillerCutFlow_Mar-10-2026_2022_HAHM_MatVeto_Angular/' + 'histograms_Signal_HTo2ZdTo2mu2x_MZd-%s_ctau-%.2fmm_2022_2022_0.root'%(str(m).replace('.','p'), ctau))
        counts_angular = file_angular.Get('d_Dimuon_full_inclusive')
        HAHM_ANGULAR[ctau][_] = counts_angular.numEntries()
        file_IP = ROOT.TFile('/ceph/cms/store/user/fernance/Run3ScoutingOutput/fillerCutFlow_Mar-10-2026_2022_HAHM_MatVeto_Angular_IP/' + 'histograms_Signal_HTo2ZdTo2mu2x_MZd-%s_ctau-%.2fmm_2022_2022_0.root'%(str(m).replace('.','p'),ctau))
        counts_IP = file_IP.Get('d_Dimuon_full_inclusive')
        HAHM_DISPLACED[ctau][_] = counts_IP.numEntries()
        file_hitVeto = ROOT.TFile('/ceph/cms/store/user/fernance/Run3ScoutingOutput/fillerCutFlow_Mar-10-2026_2022_HAHM_MatVeto_Angular_IP_Hit/' + 'histograms_Signal_HTo2ZdTo2mu2x_MZd-%s_ctau-%.2fmm_2022_2022_0.root'%(str(m).replace('.','p'), ctau))
        counts_hitVeto = file_hitVeto.Get('d_Dimuon_full_inclusive')
        HAHM_HIT_VETO[ctau][_] = counts_hitVeto.numEntries()

print(HAHM_PASSTRIGGER[10]/HAHM_TOTAL[10])
print(HAHM_PRESELECTION[10]/HAHM_TOTAL[10])
print(HAHM_CANDIDATE[10]/HAHM_TOTAL[10])
print(HAHM_MATERIAL_VETO[10]/HAHM_TOTAL[10])
print(HAHM_ANGULAR[10]/HAHM_TOTAL[10])
print(HAHM_DISPLACED[10]/HAHM_TOTAL[10])
print(HAHM_HIT_VETO[10]/HAHM_TOTAL[10])

print(HAHM_PASSTRIGGER[10])
print(HAHM_PRESELECTION[10])
print(HAHM_CANDIDATE[10])
print(HAHM_MATERIAL_VETO[10])
print(HAHM_ANGULAR[10])
print(HAHM_DISPLACED[10])
print(HAHM_HIT_VETO[10])


with open('paperPlots/hepdata_Table_HAHM-eff.pkl', 'wb') as f:
    pickle.dump(HAHM_TOTAL, f)
    pickle.dump(HAHM_PASSTRIGGER, f)
    pickle.dump(HAHM_PRESELECTION, f)
    pickle.dump(HAHM_CANDIDATE, f)
    pickle.dump(HAHM_MATERIAL_VETO, f)
    pickle.dump(HAHM_ANGULAR, f)
    pickle.dump(HAHM_DISPLACED, f)
    pickle.dump(HAHM_HIT_VETO, f)

###
### BToPhi model
###

BTOPHI_INPUT_LOOPER = '/ceph/cms/store/user/fernance/Run3ScoutingOutput/looperCutFlow_Mar-11-2026_2022_BToPhi/'
BTOPHI_MASSES = [1.25, 2.00, 2.85, 4.6]


BTOPHI_TOTAL          = {}
BTOPHI_PASSTRIGGER    = {}
BTOPHI_PRESELECTION   = {}
BTOPHI_CANDIDATE      = {}
BTOPHI_MATERIAL_VETO  = {}
BTOPHI_ANGULAR        = {}
BTOPHI_DISPLACED      = {}
BTOPHI_HIT_VETO       = {}

for ctau in [1, 10, 100]:
    BTOPHI_TOTAL[ctau]          = np.zeros(len(BTOPHI_MASSES))
    BTOPHI_PASSTRIGGER[ctau]    = np.zeros(len(BTOPHI_MASSES))
    BTOPHI_PRESELECTION[ctau]   = np.zeros(len(BTOPHI_MASSES))
    BTOPHI_CANDIDATE[ctau]      = np.zeros(len(BTOPHI_MASSES))
    BTOPHI_MATERIAL_VETO[ctau]  = np.zeros(len(BTOPHI_MASSES))
    BTOPHI_ANGULAR[ctau]        = np.zeros(len(BTOPHI_MASSES))
    BTOPHI_DISPLACED[ctau]      = np.zeros(len(BTOPHI_MASSES))
    BTOPHI_HIT_VETO[ctau]       = np.zeros(len(BTOPHI_MASSES))

# ctau = 1mm
for ctau in [1, 10, 100]:
    for _,m in enumerate(BTOPHI_MASSES):
        file_ = ROOT.TFile(BTOPHI_INPUT_LOOPER + 'output_Signal_BToPhi_MPhi-%s_ctau-%imm_2022_2022_0To99.root'%(str(m).replace('.','p'), ctau))
        cutflow = file_.Get('cutflow')
        counts = file_.Get('counts')
        BTOPHI_TOTAL[ctau][_] = counts.GetBinContent(1)
        BTOPHI_PASSTRIGGER[ctau][_] = cutflow.GetBinContent(7)
        BTOPHI_PRESELECTION[ctau][_] = cutflow.GetBinContent(2)
        file_candidate = ROOT.TFile('/ceph/cms/store/user/fernance/Run3ScoutingOutput/fillerCutFlow_Mar-10-2026_2022_BToPhi_noCuts/' + 'histograms_Signal_BToPhi_MPhi-%s_ctau-%.2fmm_2022_2022_0.root'%(("%.2f"%(m)).replace('.','p'), ctau))
        counts_candidate = file_candidate.Get('d_Dimuon_full_inclusive')
        BTOPHI_CANDIDATE[ctau][_] = counts_candidate.numEntries()
        file_MatVeto = ROOT.TFile('/ceph/cms/store/user/fernance/Run3ScoutingOutput/fillerCutFlow_Mar-10-2026_2022_BToPhi_MatVeto/' + 'histograms_Signal_BToPhi_MPhi-%s_ctau-%.2fmm_2022_2022_0.root'%(("%.2f"%(m)).replace('.','p'), ctau))
        counts_MatVeto = file_MatVeto.Get('d_Dimuon_full_inclusive')
        BTOPHI_MATERIAL_VETO[ctau][_] = counts_MatVeto.numEntries()
        file_angular = ROOT.TFile('/ceph/cms/store/user/fernance/Run3ScoutingOutput/fillerCutFlow_Mar-10-2026_2022_BToPhi_MatVeto_Angular/' + 'histograms_Signal_BToPhi_MPhi-%s_ctau-%.2fmm_2022_2022_0.root'%(("%.2f"%(m)).replace('.','p'), ctau))
        counts_angular = file_angular.Get('d_Dimuon_full_inclusive')
        BTOPHI_ANGULAR[ctau][_] = counts_angular.numEntries()
        file_IP = ROOT.TFile('/ceph/cms/store/user/fernance/Run3ScoutingOutput/fillerCutFlow_Mar-10-2026_2022_BToPhi_MatVeto_Angular_IP/' + 'histograms_Signal_BToPhi_MPhi-%s_ctau-%.2fmm_2022_2022_0.root'%(("%.2f"%(m)).replace('.','p'),ctau))
        counts_IP = file_IP.Get('d_Dimuon_full_inclusive')
        BTOPHI_DISPLACED[ctau][_] = counts_IP.numEntries()
        file_hitVeto = ROOT.TFile('/ceph/cms/store/user/fernance/Run3ScoutingOutput/fillerCutFlow_Mar-10-2026_2022_BToPhi_MatVeto_Angular_IP_Hit/' + 'histograms_Signal_BToPhi_MPhi-%s_ctau-%.2fmm_2022_2022_0.root'%(("%.2f"%(m)).replace('.','p'), ctau))
        counts_hitVeto = file_hitVeto.Get('d_Dimuon_full_inclusive')
        BTOPHI_HIT_VETO[ctau][_] = counts_hitVeto.numEntries()

print(BTOPHI_PASSTRIGGER[10]/BTOPHI_TOTAL[10])
print(BTOPHI_PRESELECTION[10]/BTOPHI_TOTAL[10])
print(BTOPHI_CANDIDATE[10]/BTOPHI_TOTAL[10])
print(BTOPHI_MATERIAL_VETO[10]/BTOPHI_TOTAL[10])
print(BTOPHI_ANGULAR[10]/BTOPHI_TOTAL[10])
print(BTOPHI_DISPLACED[10]/BTOPHI_TOTAL[10])
print(BTOPHI_HIT_VETO[10]/BTOPHI_TOTAL[10])

print(BTOPHI_PASSTRIGGER[10])
print(BTOPHI_PRESELECTION[10])
print(BTOPHI_CANDIDATE[10])
print(BTOPHI_MATERIAL_VETO[10])
print(BTOPHI_ANGULAR[10])
print(BTOPHI_DISPLACED[10])
print(BTOPHI_HIT_VETO[10])


with open('paperPlots/hepdata_Table_BToPhi-eff.pkl', 'wb') as f:
    pickle.dump(BTOPHI_TOTAL, f)
    pickle.dump(BTOPHI_PASSTRIGGER, f)
    pickle.dump(BTOPHI_PRESELECTION, f)
    pickle.dump(BTOPHI_CANDIDATE, f)
    pickle.dump(BTOPHI_MATERIAL_VETO, f)
    pickle.dump(BTOPHI_ANGULAR, f)
    pickle.dump(BTOPHI_DISPLACED, f)
    pickle.dump(BTOPHI_HIT_VETO, f)




#print(PASSTRIGGER/TOTAL)
#print(PRESELECTION/TOTAL)
#print(CANDIDATE/TOTAL)
#print(MATERIAL_VETO/TOTAL)
#print(ANGULAR/TOTAL)
#print(DISPLACED/TOTAL)
#print(HIT_VETO/TOTAL)
