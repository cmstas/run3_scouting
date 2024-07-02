import ROOT

# Histogram definition
def H1(name,nbins,low,high,xtitle,ytitle,labels=[]):
    hname = ROOT.TH1D(name,"",nbins,low,high) 
    hname.GetXaxis().SetTitle(xtitle)
    hname.GetYaxis().SetTitle(ytitle)
    if len(labels)>0:
        for b in range(1,len(labels)+1):
            hname.GetXaxis().SetBinLabel(b,labels[b-1])
    return hname

def H2(name,nbinsX,lowX,highX,xtitle,nbinsY,lowY,highY,ytitle,ztitle):
    hname = ROOT.TH2D(name,"",nbinsX,lowX,highX,nbinsY,lowY,highY)
    hname.GetXaxis().SetTitle(xtitle)
    hname.GetYaxis().SetTitle(ytitle)
    hname.GetZaxis().SetTitle(ztitle)
    return hname

def hist2dDefinition(nbinsX, lowX, highX, xtitle2d, nbinsY, lowY, highY, ytitle2d, ztitle2d, variablesXY):
    # 2D histograms
    nbinsX     ["yvsx"] = 2200
    lowX       ["yvsx"] = -110
    highX      ["yvsx"] = 110
    nbinsY     ["yvsx"] = 2200
    lowY       ["yvsx"] = -110
    highY      ["yvsx"] = 110
    xtitle2d   ["yvsx"] = "x [cm]"
    ytitle2d   ["yvsx"] = "y [cm]"
    ztitle2d   ["yvsx"] = "Number of SVs"
    variablesXY["yvsx"] = ["t.SV_x[v]","t.SV_y[v]"]

    nbinsX     ["xerrvslxy"] = 100
    lowX       ["xerrvslxy"] = 0.0
    highX      ["xerrvslxy"] = 70.0
    nbinsY     ["xerrvslxy"] = 100
    lowY       ["xerrvslxy"] = 0.0
    highY      ["xerrvslxy"] = 0.05
    xtitle2d   ["xerrvslxy"] = "SV l_{xy} (from PV) [cm]"
    ytitle2d   ["xerrvslxy"] = "SV x error [cm]"
    ztitle2d   ["xerrvslxy"] = "Number of SVs"
    variablesXY["xerrvslxy"] = ["t.SV_lxy[v]","t.SV_xe[v]"]

    nbinsX     ["yerrvslxy"] = 100
    lowX       ["yerrvslxy"] = 0.0
    highX      ["yerrvslxy"] = 70.0
    nbinsY     ["yerrvslxy"] = 100
    lowY       ["yerrvslxy"] = 0.0
    highY      ["yerrvslxy"] = 0.05
    xtitle2d   ["yerrvslxy"] = "SV l_{xy} (from PV) [cm]"
    ytitle2d   ["yerrvslxy"] = "SV y error [cm]"
    ztitle2d   ["yerrvslxy"] = "Number of SVs"
    variablesXY["yerrvslxy"] = ["t.SV_lxy[v]","t.SV_ye[v]"]

    nbinsX     ["zerrvslxy"] = 100
    lowX       ["zerrvslxy"] = 0.0
    highX      ["zerrvslxy"] = 70.0
    nbinsY     ["zerrvslxy"] = 100
    lowY       ["zerrvslxy"] = 0.0
    highY      ["zerrvslxy"] = 0.1
    xtitle2d   ["zerrvslxy"] = "SV l_{xy} (from PV) [cm]"
    ytitle2d   ["zerrvslxy"] = "SV z error [cm]"
    ztitle2d   ["zerrvslxy"] = "Number of SVs"
    variablesXY["zerrvslxy"] = ["t.SV_lxy[v]","t.SV_ze[v]"]

    nbinsX     ["xerrvsz"] = 100
    lowX       ["xerrvsz"] = 0.0
    highX      ["xerrvsz"] = 110.0
    nbinsY     ["xerrvsz"] = 100
    lowY       ["xerrvsz"] = 0.0
    highY      ["xerrvsz"] = 0.05
    xtitle2d   ["xerrvsz"] = "SV z [cm]"
    ytitle2d   ["xerrvsz"] = "SV x error [cm]"
    ztitle2d   ["xerrvsz"] = "Number of SVs"
    variablesXY["xerrvsz"] = ["t.SV_z[v]","t.SV_xe[v]"]

    nbinsX     ["yerrvsz"] = 100
    lowX       ["yerrvsz"] = 0.0
    highX      ["yerrvsz"] = 110.0
    nbinsY     ["yerrvsz"] = 100
    lowY       ["yerrvsz"] = 0.0
    highY      ["yerrvsz"] = 0.05
    xtitle2d   ["yerrvsz"] = "SV z [cm]"
    ytitle2d   ["yerrvsz"] = "SV y error [cm]"
    ztitle2d   ["yerrvsz"] = "Number of SVs"
    variablesXY["yerrvsz"] = ["t.SV_z[v]","t.SV_ye[v]"]

    nbinsX     ["zerrvsz"] = 100
    lowX       ["zerrvsz"] = 0.0
    highX      ["zerrvsz"] = 110.0
    nbinsY     ["zerrvsz"] = 100
    lowY       ["zerrvsz"] = 0.0
    highY      ["zerrvsz"] = 0.1
    xtitle2d   ["zerrvsz"] = "SV z [cm]"
    ytitle2d   ["zerrvsz"] = "SV z error [cm]"
    ztitle2d   ["zerrvsz"] = "Number of SVs"
    variablesXY["zerrvsz"] = ["t.SV_z[v]","t.SV_ze[v]"]

    nbinsX     ["mindvslxy"] = 1000
    lowX       ["mindvslxy"] = 0.0
    highX      ["mindvslxy"] = 40.0
    nbinsY     ["mindvslxy"] = 200
    lowY       ["mindvslxy"] = 0.0
    highY      ["mindvslxy"] = 5.0
    xtitle2d   ["mindvslxy"] = "SV l_{xy} (from PV) [cm]"
    ytitle2d   ["mindvslxy"] = "Min. distance to module"
    ztitle2d   ["mindvslxy"] = "Number of SVs"
    variablesXY["mindvslxy"] = ["t.SV_lxy[v]", "t.SV_minDistanceFromDet[v]"]

    nbinsX     ["mindxyvslxy"] = 1000
    lowX       ["mindxyvslxy"] = 0.0
    highX      ["mindxyvslxy"] = 40.0
    nbinsY     ["mindxyvslxy"] = 200
    lowY       ["mindxyvslxy"] = 0.0
    highY      ["mindxyvslxy"] = 5.0
    xtitle2d   ["mindxyvslxy"] = "SV l_{xy} (from PV) [cm]"
    ytitle2d   ["mindxyvslxy"] = "Min. xy distance to module"
    ztitle2d   ["mindxyvslxy"] = "Number of SVs"
    variablesXY["mindxyvslxy"] = ["t.SV_lxy[v]", "((t.SV_minDistanceFromDet_x[v])**2.0 + (t.SV_minDistanceFromDet_y[v])**2.0)**0.5"]

    nbinsX     ["lxyvslxygen"] = 110
    lowX       ["lxyvslxygen"] = 0
    highX      ["lxyvslxygen"] = 110
    nbinsY     ["lxyvslxygen"] = 110
    lowY       ["lxyvslxygen"] = 0
    highY      ["lxyvslxygen"] = 110
    xtitle2d   ["lxyvslxygen"] = "Generated l_{xy} [cm]"
    ytitle2d   ["lxyvslxygen"] = "Reconstructed l_{xy} [cm]"
    ztitle2d   ["lxyvslxygen"] = "Gen-matched dimuons"
    variablesXY["lxyvslxygen"] = ["lxygen","lxy"]

    nbinsX     ["pfisovspt"] = 100
    lowX       ["pfisovspt"] = 0
    highX      ["pfisovspt"] = 100
    nbinsY     ["pfisovspt"] = 30
    lowY       ["pfisovspt"] = 0
    highY      ["pfisovspt"] = 30
    xtitle2d   ["pfisovspt"] = "Muon p_{T} [GeV]"
    ytitle2d   ["pfisovspt"] = "Muon PF-all isolation (#DeltaR<0.4) [GeV]"
    ztitle2d   ["pfisovspt"] = "Number of muons"
    variablesXY["pfisovspt"] = ["t.Muon_pt[m]","t.Muon_PFIsoAll0p4[m]"]


def hist1dDefinition(nbins, low, high, xtitle, ytitle, labels, variable):
    # 1D histograms

    #Event

    nbins   ["npv"] = 80
    low     ["npv"] = 0
    high    ["npv"] = 80
    xtitle  ["npv"] = "Number of PVs"
    ytitle  ["npv"] = "Events"
    variable["npv"] = "t.nPV"

    #Gen

    nbins   ["jpsilxy"] = 400
    low     ["jpsilxy"] = 0
    high    ["jpsilxy"] = 40
    xtitle  ["jpsilxy"] = "Decay length l_{xy} (cm)"
    ytitle  ["jpsilxy"] = "Simulated JPsis"
    variable["jpsilxy"] = "lxygen"

    nbins   ["llplxy"] = 1100
    low     ["llplxy"] = 0
    high    ["llplxy"] = 110
    xtitle  ["llplxy"] = "Decay length l_{xy} (cm)"
    ytitle  ["llplxy"] = "Simulated LLPs"
    variable["llplxy"] = "lxygen"

    nbins   ["deltalxy"] = 100
    low     ["deltalxy"] = -0.5
    high    ["deltalxy"] = 0.5
    xtitle  ["deltalxy"] = "#Delta(reco l_{xy}, gen l_{xy})/gen l_{xy}"
    ytitle  ["deltalxy"] = "Dimuons"
    variable["deltalxy"] = "deltalxy"

    nbins   ["genmupt"] = 50
    low     ["genmupt"] = 0
    high    ["genmupt"] = 150
    xtitle  ["genmupt"] = "Generated muon p_{T} [GeV]"
    ytitle  ["genmupt"] = "Simulated muons"
    variable["genmupt"] = "t.GenPart_pt[i]"

    nbins   ["isgen"] = 2
    low     ["isgen"] = 0
    high    ["isgen"] = 2
    xtitle  ["isgen"] = "Is matched with generation"
    ytitle  ["isgen"] = "Events"
    variable["isgen"] = "isgen"

    #Displaced vertices

    nbins   ["nsv"] = 10
    low     ["nsv"] = 0
    high    ["nsv"] = 10
    xtitle  ["nsv"] = "Number of SVs"
    ytitle  ["nsv"] = "Events"
    variable["nsv"] = "nSVs"

    nbins   ["svchi2"] = 100
    low     ["svchi2"] = 0
    high    ["svchi2"] = 10
    xtitle  ["svchi2"] = "SV #chi^{2}"
    ytitle  ["svchi2"] = "Events / 0.1"
    variable["svchi2"] = "t.SV_chi2Ndof[v]"

    nbins   ["svchi2prob"] = 100
    low     ["svchi2prob"] = 0
    high    ["svchi2prob"] = 1
    xtitle  ["svchi2prob"] = "SV #chi^{2} probability"
    ytitle  ["svchi2prob"] = "Events / 0.01"
    variable["svchi2prob"] = "t.SV_prob[v]"

    nbins   ["svxerr"] = 500
    low     ["svxerr"] = 0
    high    ["svxerr"] = 0.5
    xtitle  ["svxerr"] = "SV x error [cm]"
    ytitle  ["svxerr"] = "Events / 0.001 cm"
    variable["svxerr"] = "t.SV_xe[v]"

    nbins   ["svyerr"] = 500
    low     ["svyerr"] = 0
    high    ["svyerr"] = 0.5
    xtitle  ["svyerr"] = "SV y error [cm]"
    ytitle  ["svyerr"] = "Events / 0.001 cm"
    variable["svyerr"] = "t.SV_ye[v]"

    nbins   ["svzerr"] = 500
    low     ["svzerr"] = 0
    high    ["svzerr"] = 0.5
    xtitle  ["svzerr"] = "SV z error [cm]"
    ytitle  ["svzerr"] = "Events / 0.001 cm"
    variable["svzerr"] = "t.SV_ze[v]"

    nbins   ["svxyerr"] = 500
    low     ["svxyerr"] = 0
    high    ["svxyerr"] = 0.5
    xtitle  ["svxyerr"] = "SV l_{xy} error [cm]"
    ytitle  ["svxyerr"] = "Events / 0.001 cm"
    variable["svxyerr"] = "ROOT.TMath.Sqrt(t.SV_xe[v]*t.SV_xe[v]+t.SV_ye[v]*t.SV_ye[v])"

    nbins   ["sv3derr"] = 500
    low     ["sv3derr"] = 0
    high    ["sv3derr"] = 0.5
    xtitle  ["sv3derr"] = "SV l_{3D} error [cm]"
    ytitle  ["sv3derr"] = "Events / 0.001 cm"
    variable["sv3derr"] = "ROOT.TMath.Sqrt(t.SV_xe[v]*t.SV_xe[v]+t.SV_ye[v]*t.SV_ye[v]+t.SV_ze[v]*t.SV_ze[v])"

    nbins   ["svxsig"] = 500
    low     ["svxsig"] = 0
    high    ["svxsig"] = 50.0
    xtitle  ["svxsig"] = "SV x / (x error)"
    ytitle  ["svxsig"] = "Events / 0.1"
    variable["svxsig"] = "abs(t.SV_x[v]/t.SV_xe[v])"

    nbins   ["svysig"] = 500
    low     ["svysig"] = 0
    high    ["svysig"] = 50.0
    xtitle  ["svysig"] = "SV y / (y error)"
    ytitle  ["svysig"] = "Events / 0.1"
    variable["svysig"] = "abs(t.SV_y[v]/t.SV_ye[v])"

    nbins   ["svzsig"] = 500
    low     ["svzsig"] = 0
    high    ["svzsig"] = 50.0
    xtitle  ["svzsig"] = "SV z / (z error)"
    ytitle  ["svzsig"] = "Events / 0.1"
    variable["svzsig"] = "abs(t.SV_z[v]/t.SV_ze[v])"

    nbins   ["svxpvsig"] = 500
    low     ["svxpvsig"] = 0
    high    ["svxpvsig"] = 50.0
    xtitle  ["svxpvsig"] = "SV x (from PV) / (x error)"
    ytitle  ["svxpvsig"] = "Events / 0.1"
    variable["svxpvsig"] = "abs((t.SV_x[v]-t.PV_x)/t.SV_xe[v])"

    nbins   ["svypvsig"] = 500
    low     ["svypvsig"] = 0
    high    ["svypvsig"] = 50.0
    xtitle  ["svypvsig"] = "SV y (from PV) / (y error)"
    ytitle  ["svypvsig"] = "Events / 0.1"
    variable["svypvsig"] = "abs((t.SV_y[v]-t.PV_y)/t.SV_ye[v])"

    nbins   ["svzpvsig"] = 500
    low     ["svzpvsig"] = 0
    high    ["svzpvsig"] = 50.0
    xtitle  ["svzpvsig"] = "SV z (from PV) / (z error)"
    ytitle  ["svzpvsig"] = "Events / 0.1"
    variable["svzpvsig"] = "abs((t.SV_z[v]-t.PV_z)/t.SV_ze[v])"

    nbins   ["svxysig"] = 500
    low     ["svxysig"] = 0
    high    ["svxysig"] = 50.0
    xtitle  ["svxysig"] = "SV d_{xy} / (l_{xy} error)"
    ytitle  ["svxysig"] = "Events / 0.1"
    variable["svxysig"] = "ROOT.TMath.Sqrt(t.SV_x[v]*t.SV_x[v]+t.SV_y[v]*t.SV_y[v])/ROOT.TMath.Sqrt(t.SV_xe[v]*t.SV_xe[v]+t.SV_ye[v]*t.SV_ye[v])"

    nbins   ["sv3dsig"] = 500
    low     ["sv3dsig"] = 0
    high    ["sv3dsig"] = 50.0
    xtitle  ["sv3dsig"] = "SV d_{3D} / (l_{3D} error)"
    ytitle  ["sv3dsig"] = "Events / 0.1"
    variable["sv3dsig"] = "ROOT.TMath.Sqrt(t.SV_xe[v]*t.SV_xe[v]+t.SV_ye[v]*t.SV_ye[v]+t.SV_ze[v]*t.SV_ze[v])"
    variable["sv3dsig"] = "ROOT.TMath.Sqrt(t.SV_x[v]*t.SV_x[v]+t.SV_y[v]*t.SV_y[v]+t.SV_z[v]*t.SV_z[v])/ROOT.TMath.Sqrt(t.SV_xe[v]*t.SV_xe[v]+t.SV_ye[v]*t.SV_ye[v]+t.SV_ze[v]*t.SV_ze[v])"

    nbins   ["svdxy"] = 1100
    low     ["svdxy"] = 0
    high    ["svdxy"] = 110.0
    xtitle  ["svdxy"] = "SV d_{xy} [cm]"
    ytitle  ["svdxy"] = "Events / 0.1 cm"
    variable["svdxy"] = "ROOT.TMath.Sqrt(t.SV_x[v]*t.SV_x[v]+t.SV_y[v]*t.SV_y[v])"

    nbins   ["svd3d"] = 1500
    low     ["svd3d"] = 0
    high    ["svd3d"] = 150.0
    xtitle  ["svd3d"] = "SV d_{3d} [cm]"
    ytitle  ["svd3d"] = "Events / 0.1 cm"
    variable["svd3d"] = "ROOT.TMath.Sqrt(t.SV_x[v]*t.SV_x[v]+t.SV_y[v]*t.SV_y[v]+t.SV_z[v]*t.SV_z[v])"

    nbins   ["lxy"] = 1100
    low     ["lxy"] = 0
    high    ["lxy"] = 110.0
    xtitle  ["lxy"] = "l_{xy} (from PV) [cm]"
    ytitle  ["lxy"] = "Events / 0.1 cm"
    variable["lxy"] = "lxy"

    nbins   ["lxysig"] = 1000
    low     ["lxysig"] = 0
    high    ["lxysig"] = 100.0
    xtitle  ["lxysig"] = "l_{xy} (from PV) / (l_{xy} error)"
    ytitle  ["lxysig"] = "Events / 0.1"
    variable["lxysig"] = "lxy/ROOT.TMath.Sqrt(t.SV_xe[v]*t.SV_xe[v]+t.SV_ye[v]*t.SV_ye[v])"

    nbins   ["minlxy"] = 1100
    low     ["minlxy"] = 0
    high    ["minlxy"] = 110.0
    xtitle  ["minlxy"] = "min l_{xy} (from PV) [cm]"
    ytitle  ["minlxy"] = "Events / 0.1 cm"
    variable["minlxy"] = "minlxy"
    
    nbins   ["maxlxy"] = 1100
    low     ["maxlxy"] = 0
    high    ["maxlxy"] = 110.0
    xtitle  ["maxlxy"] = "max l_{xy} (from PV) [cm]"
    ytitle  ["maxlxy"] = "Events / 0.1 cm"
    variable["maxlxy"] = "maxlxy"
    
    nbins   ["l3d"] = 1500
    low     ["l3d"] = 0
    high    ["l3d"] = 150.0
    xtitle  ["l3d"] = "l_{3D} (from PV) [cm]"
    ytitle  ["l3d"] = "Events / 0.1 cm"
    variable["l3d"] = "t.SV_l3d[v]"

    nbins   ["l3dsig"] = 1000
    low     ["l3dsig"] = 0
    high    ["l3dsig"] = 100.0
    xtitle  ["l3dsig"] = "l_{3D} (from PV) / (l_{3D} error)"
    ytitle  ["l3dsig"] = "Events / 0.1"
    variable["l3dsig"] = "t.SV_l3d[v]/ROOT.TMath.Sqrt(t.SV_xe[v]*t.SV_xe[v]+t.SV_ye[v]*t.SV_ye[v]+t.SV_ze[v]*t.SV_ze[v])"

    nbins   ["mindx"] = 100
    low     ["mindx"] = 0
    high    ["mindx"] = 1
    xtitle  ["mindx"] = "min D_{x} (SV_{i}, SV_{j}) [cm]"
    ytitle  ["mindx"] = "Events / 0.01 cm"    
    variable["mindx"] = "t.SV_mindx[v]"

    nbins   ["mindy"] = 100
    low     ["mindy"] = 0
    high    ["mindy"] = 1
    xtitle  ["mindy"] = "min D_{y} (SV_{i}, SV_{j}) [cm]"
    ytitle  ["mindy"] = "Events / 0.01 cm"    
    variable["mindy"] = "t.SV_mindy[v]"

    nbins   ["mindz"] = 100
    low     ["mindz"] = 0
    high    ["mindz"] = 1
    xtitle  ["mindz"] = "min D_{z} (SV_{i}, SV_{j}) [cm]"
    ytitle  ["mindz"] = "Events / 0.01 cm"    
    variable["mindz"] = "t.SV_mindz[v]"

    nbins   ["maxdx"] = 100
    low     ["maxdx"] = 0
    high    ["maxdx"] = 1
    xtitle  ["maxdx"] = "max D_{x} (SV_{i}, SV_{j}) [cm]"
    ytitle  ["maxdx"] = "Events / 0.01 cm"    
    variable["maxdx"] = "t.SV_maxdx[v]"

    nbins   ["maxdy"] = 100
    low     ["maxdy"] = 0
    high    ["maxdy"] = 1
    xtitle  ["maxdy"] = "max D_{y} (SV_{i}, SV_{j}) [cm]"
    ytitle  ["maxdy"] = "Events / 0.01 cm"    
    variable["maxdy"] = "t.SV_maxdy[v]"

    nbins   ["maxdz"] = 100
    low     ["maxdz"] = 0
    high    ["maxdz"] = 1
    xtitle  ["maxdz"] = "max D_{z} (SV_{i}, SV_{j}) [cm]"
    ytitle  ["maxdz"] = "Events / 0.01 cm"    
    variable["maxdz"] = "t.SV_maxdz[v]"

    #Muons

    nbins   ["nmusel"] = 10
    low     ["nmusel"] = 0
    high    ["nmusel"] = 10
    xtitle  ["nmusel"] = "Number of muons (p_{T}>3 GeV, |#eta|<2.4)"
    ytitle  ["nmusel"] = "Events"
    variable["nmusel"] = "nMuSel"

    nbins   ["nmusv"] = 10
    low     ["nmusv"] = 0
    high    ["nmusv"] = 10
    xtitle  ["nmusv"] = "Number of muons (p_{T}>3 GeV, |#eta|<2.4, from SV)"
    ytitle  ["nmusv"] = "Events"
    variable["nmusv"] = "nMuAss"

    nbins   ["nmuosv"] = 10
    low     ["nmuosv"] = 0
    high    ["nmuosv"] = 10
    xtitle  ["nmuosv"] = "Number of muons (p_{T}>3 GeV, |#eta|<2.4, from overlapping SV)"
    ytitle  ["nmuosv"] = "Events"
    variable["nmuosv"] = "nMuAssOverlap"

    nbins   ["mupt"] = 50
    low     ["mupt"] = 0
    high    ["mupt"] = 150
    xtitle  ["mupt"] = "Muon p_{T} [GeV]"
    ytitle  ["mupt"] = "Events / 3 GeV"
    variable["mupt"] = "t.Muon_pt[m]"

    nbins   ["mueta"] = 50
    low     ["mueta"] = -2.5
    high    ["mueta"] = 2.5
    xtitle  ["mueta"] = "Muon #eta"
    ytitle  ["mueta"] = "Events / 0.1"
    variable["mueta"] = "t.Muon_eta[m]"

    nbins   ["muphi"] = 64
    low     ["muphi"] = -3.2
    high    ["muphi"] = 3.2
    xtitle  ["muphi"] = "Muon #phi"
    ytitle  ["muphi"] = "Events / 0.1"
    variable["muphi"] = "t.Muon_phiCorr[m]"

    nbins   ["muuphi"] = 64
    low     ["muuphi"] = -3.2
    high    ["muuphi"] = 3.2
    xtitle  ["muuphi"] = "Muon #phi (uncorrected)"
    ytitle  ["muuphi"] = "Events / 0.1"
    variable["muuphi"] = "t.Muon_phi[m]"

    nbins   ["much"] = 3
    low     ["much"] = -1.5
    high    ["much"] = 1.5
    xtitle  ["much"] = "Muon charge"
    ytitle  ["much"] = "Events"
    variable["much"] = "t.Muon_ch[m]"

    nbins   ["mumindr"] = 100
    low     ["mumindr"] = 0
    high    ["mumindr"] = 5
    xtitle  ["mumindr"] = "min #DeltaR(#mu_{i}, #mu_{j})"
    ytitle  ["mumindr"] = "Events / 0.05"
    variable["mumindr"] = "t.Muon_mindr[m]"

    nbins   ["mumaxdr"] = 100
    low     ["mumaxdr"] = 0
    high    ["mumaxdr"] = 5
    xtitle  ["mumaxdr"] = "max #DeltaR(#mu_{i}, #mu_{j})"
    ytitle  ["mumaxdr"] = "Events / 0.05"
    variable["mumaxdr"] = "t.Muon_maxdr[m]"

    nbins   ["muchi2ndof"] = 100
    low     ["muchi2ndof"] = 0
    high    ["muchi2ndof"] = 10
    xtitle  ["muchi2ndof"] = "Muon #chi^{2}/ndof"
    ytitle  ["muchi2ndof"] = "Events / 0.1"
    variable["muchi2ndof"] = "t.Muon_chi2Ndof[m]"

    labels  ["mutype"] = ["G & T","G & !T","!G & T","SA & !G & !T","!SA & !G & !T"]
    nbins   ["mutype"] = len(labels["mutype"])
    low     ["mutype"] = 0
    high    ["mutype"] = len(labels["mutype"])
    xtitle  ["mutype"] = "Muon type"
    ytitle  ["mutype"] = "Events"
    variable["mutype"] = "muonType(t.Muon_isGlobal[m], t.Muon_isTracker[m], t.Muon_isStandAlone[m])"

    nbins   ["muecaliso"] = 40
    low     ["muecaliso"] = 0
    high    ["muecaliso"] = 10
    xtitle  ["muecaliso"] = "Muon ECAL isolation [GeV]"
    ytitle  ["muecaliso"] = "Events / 0.5 GeV"
    variable["muecaliso"] = "t.Muon_ecalIso[m]"

    nbins   ["muhcaliso"] = 40
    low     ["muhcaliso"] = 0
    high    ["muhcaliso"] = 10
    xtitle  ["muhcaliso"] = "Muon HCAL isolation [GeV]"
    ytitle  ["muhcaliso"] = "Events / 0.5 GeV"
    variable["muhcaliso"] = "t.Muon_hcalIso[m]"

    nbins   ["mutrkiso"] = 40
    low     ["mutrkiso"] = 0
    high    ["mutrkiso"] = 10
    xtitle  ["mutrkiso"] = "Muon track isolation [GeV]"
    ytitle  ["mutrkiso"] = "Events / 0.5 GeV"
    variable["mutrkiso"] = "t.Muon_trackIso[m]"

    nbins   ["mupfalliso0p3"] = 40
    low     ["mupfalliso0p3"] = 0
    high    ["mupfalliso0p3"] = 10
    xtitle  ["mupfalliso0p3"] = "Muon PF-all isolation (#DeltaR<0.3, #delta#beta-corrected) [GeV]"
    ytitle  ["mupfalliso0p3"] = "Events / 0.5 GeV"
    variable["mupfalliso0p3"] = "t.Muon_PFIsoAll0p3[m]"

    nbins   ["mupfchgiso0p3"] = 40
    low     ["mupfchgiso0p3"] = 0
    high    ["mupfchgiso0p3"] = 10
    xtitle  ["mupfchgiso0p3"] = "Muon PF-charged isolation (#DeltaR<0.3) [GeV]"
    ytitle  ["mupfchgiso0p3"] = "Events / 0.5 GeV"
    variable["mupfchgiso0p3"] = "t.Muon_PFIsoChg0p3[m]"

    nbins   ["mupfalliso0p4"] = 40
    low     ["mupfalliso0p4"] = 0
    high    ["mupfalliso0p4"] = 10
    xtitle  ["mupfalliso0p4"] = "Muon PF-all isolation (#DeltaR<0.4, #delta#beta-corrected) [GeV]"
    ytitle  ["mupfalliso0p4"] = "Events / 0.5 GeV"
    variable["mupfalliso0p4"] = "t.Muon_PFIsoAll0p4[m]"

    nbins   ["mupfchgiso0p4"] = 40
    low     ["mupfchgiso0p4"] = 0
    high    ["mupfchgiso0p4"] = 10
    xtitle  ["mupfchgiso0p4"] = "Muon PF-charged isolation (#DeltaR<0.4, #delta#beta-corrected) [GeV]"
    ytitle  ["mupfchgiso0p4"] = "Events / 0.5 GeV"
    variable["mupfchgiso0p4"] = "t.Muon_PFIsoChg0p4[m]"

    nbins   ["muecalreliso"] = 40
    low     ["muecalreliso"] = 0
    high    ["muecalreliso"] = 2
    xtitle  ["muecalreliso"] = "Muon ECAL isolation / p_{T}"
    ytitle  ["muecalreliso"] = "Events / 0.05"
    variable["muecalreliso"] = "t.Muon_ecalRelIso[m]"

    nbins   ["muhcalreliso"] = 40
    low     ["muhcalreliso"] = 0
    high    ["muhcalreliso"] = 2
    xtitle  ["muhcalreliso"] = "Muon HCAL isolation / p_{T}"
    ytitle  ["muhcalreliso"] = "Events / 0.05"
    variable["muhcalreliso"] = "t.Muon_hcalRelIso[m]"

    nbins   ["mutrkreliso"] = 40
    low     ["mutrkreliso"] = 0
    high    ["mutrkreliso"] = 2
    xtitle  ["mutrkreliso"] = "Muon track isolation / p_{T}"
    ytitle  ["mutrkreliso"] = "Events / 0.05"
    variable["mutrkreliso"] = "t.Muon_trackRelIso[m]"

    nbins   ["mupfallreliso0p3"] = 40
    low     ["mupfallreliso0p3"] = 0
    high    ["mupfallreliso0p3"] = 2
    xtitle  ["mupfallreliso0p3"] = "Muon PF-all relisolation (#DeltaR<0.3, #delta#beta-corrected) / p_{T}"
    ytitle  ["mupfallreliso0p3"] = "Events / 0.05"
    variable["mupfallreliso0p3"] = "t.Muon_PFRelIsoAll0p3[m]"

    nbins   ["mupfchgreliso0p3"] = 40
    low     ["mupfchgreliso0p3"] = 0
    high    ["mupfchgreliso0p3"] = 2
    xtitle  ["mupfchgreliso0p3"] = "Muon PF-charged isolation (#DeltaR<0.3) / p_{T}"
    ytitle  ["mupfchgreliso0p3"] = "Events / 0.05"
    variable["mupfchgreliso0p3"] = "t.Muon_PFRelIsoChg0p3[m]"

    nbins   ["mupfallreliso0p4"] = 40
    low     ["mupfallreliso0p4"] = 0
    high    ["mupfallreliso0p4"] = 2
    xtitle  ["mupfallreliso0p4"] = "Muon PF-all relisolation (#DeltaR<0.4, #delta#beta-corrected) / p_{T}"
    ytitle  ["mupfallreliso0p4"] = "Events / 0.05"
    variable["mupfallreliso0p4"] = "t.Muon_PFRelIsoAll0p4[m]"

    nbins   ["mupfchgreliso0p4"] = 40
    low     ["mupfchgreliso0p4"] = 0
    high    ["mupfchgreliso0p4"] = 2
    xtitle  ["mupfchgreliso0p4"] = "Muon PF-charged isolation (#DeltaR<0.4) / p_{T}"
    ytitle  ["mupfchgreliso0p4"] = "Events / 0.05"
    variable["mupfchgreliso0p4"] = "t.Muon_PFRelIsoChg0p4[m]"

    nbins   ["mumindrjet"] = 100
    low     ["mumindrjet"] = 0
    high    ["mumindrjet"] = 5
    xtitle  ["mumindrjet"] = "min #DeltaR(#mu, PF jet)"
    ytitle  ["mumindrjet"] = "Events / 0.05"
    variable["mumindrjet"] = "t.Muon_mindrJet[m]"

    nbins   ["mumindpjet"] = 320
    low     ["mumindpjet"] = 0
    high    ["mumindpjet"] = 3.2
    xtitle  ["mumindpjet"] = "#Delta#phi(#mu, nearest PF jet in #DeltaR)"
    ytitle  ["mumindpjet"] = "Events / 0.01"
    variable["mumindpjet"] = "t.Muon_mindphiJet[m]"

    nbins   ["mumindejet"] = 500
    low     ["mumindejet"] = 0
    high    ["mumindejet"] = 5
    xtitle  ["mumindejet"] = "#Delta#eta(#mu, nearest PF jet in #DeltaR)"
    ytitle  ["mumindejet"] = "Events / 0.01"
    variable["mumindejet"] = "t.Muon_mindetaJet[m]"

    nbins   ["mumindrpfc"] = 100
    low     ["mumindrpfc"] = 0
    high    ["mumindrpfc"] = 0.1
    xtitle  ["mumindrpfc"] = "min #DeltaR(#mu, PF candidate)"
    ytitle  ["mumindrpfc"] = "Events / 0.001"
    variable["mumindrpfc"] = "t.Muon_mindrPF0p4[m]"

    nbins   ["mudxy"] = 100
    low     ["mudxy"] = 0
    high    ["mudxy"] = 5.0
    xtitle  ["mudxy"] = "Muon |d_{xy}| [cm]"
    ytitle  ["mudxy"] = "Events / 0.05 cm"
    variable["mudxy"] = "abs(t.Muon_dxyCorr[m])"

    nbins   ["mudxysigned"] = 100
    low     ["mudxysigned"] = -5.0
    high    ["mudxysigned"] = 5.0
    xtitle  ["mudxysigned"] = "Muon signed #vec{d_{xy}} [cm]"
    ytitle  ["mudxysigned"] = "Events / 0.05 cm"
    variable["mudxysigned"] = "abs(t.Muon_dxyCorr[m])*dxysign"

    nbins   ["mudxysig"] = 100
    low     ["mudxysig"] = 0
    high    ["mudxysig"] = 50
    xtitle  ["mudxysig"] = "Muon |d_{xy}|/#sigma_{xy}"
    ytitle  ["mudxysig"] = "Events / 0.5"
    variable["mudxysig"] = "abs(t.Muon_dxyCorr[m]/t.Muon_dxye[m])"

    nbins   ["mudxyscaled"] = 500
    low     ["mudxyscaled"] = 0
    high    ["mudxyscaled"] = 5
    xtitle  ["mudxyscaled"] = "Muon |d_{xy}|/(l_{xy}m_{#mu#mu}/p_{T}^{#mu#mu})"
    ytitle  ["mudxyscaled"] = "Events / 0.01"
    variable["mudxyscaled"] = "abs(t.Muon_dxyCorr[m])/(lxy*mass/pt)"

    nbins   ["mudz"] = 300
    low     ["mudz"] = 0
    high    ["mudz"] = 30.0
    xtitle  ["mudz"] = "Muon |d_{z}| [cm]"
    ytitle  ["mudz"] = "Events / 0.1 cm"
    variable["mudz"] = "abs(t.Muon_dz[m])"

    nbins   ["mudzsig"] = 100
    low     ["mudzsig"] = 0
    high    ["mudzsig"] = 50
    xtitle  ["mudzsig"] = "Muon |d_{z}|/#sigma_{z}"
    ytitle  ["mudzsig"] = "Events / 0.5"
    variable["mudzsig"] = "abs(t.Muon_dzsig[m])"

    nbins   ["musahits"] = 50
    low     ["musahits"] = 0
    high    ["musahits"] = 50
    xtitle  ["musahits"] = "Number of valid SA muon hits"
    ytitle  ["musahits"] = "Events"
    variable["musahits"] = "t.Muon_saHits[m]"

    nbins   ["musamatchedstats"] = 10
    low     ["musamatchedstats"] = 0
    high    ["musamatchedstats"] = 10
    xtitle  ["musamatchedstats"] = "Number of SA muon matched stations"
    ytitle  ["musamatchedstats"] = "Events"
    variable["musamatchedstats"] = "t.Muon_saMatchedStats[m]"

    nbins   ["muhits"] = 50
    low     ["muhits"] = 0
    high    ["muhits"] = 50
    xtitle  ["muhits"] = "Number of valid muon hits"
    ytitle  ["muhits"] = "Events"
    variable["muhits"] = "t.Muon_muHits[m]"

    nbins   ["muchambs"] = 25
    low     ["muchambs"] = 0
    high    ["muchambs"] = 25
    xtitle  ["muchambs"] = "Number of muon chambers"
    ytitle  ["muchambs"] = "Events"
    variable["muchambs"] = "t.Muon_muChambs[m]"

    nbins   ["mucscdt"] = 20
    low     ["mucscdt"] = 0
    high    ["mucscdt"] = 20
    xtitle  ["mucscdt"] = "Number of muon chambers (CSC or DT)"
    ytitle  ["mucscdt"] = "Events"
    variable["mucscdt"] = "t.Muon_muCSCDT[m]"

    nbins   ["mumatches"] = 10
    low     ["mumatches"] = 0
    high    ["mumatches"] = 10
    xtitle  ["mumatches"] = "Number of muon matches"
    ytitle  ["mumatches"] = "Events"
    variable["mumatches"] = "t.Muon_muMatch[m]"

    nbins   ["mumatchedstats"] = 10
    low     ["mumatchedstats"] = 0
    high    ["mumatchedstats"] = 10
    xtitle  ["mumatchedstats"] = "Number of muon matched stations"
    ytitle  ["mumatchedstats"] = "Events"
    variable["mumatchedstats"] = "t.Muon_muMatchedStats[m]"

    nbins   ["muexpmatchedstats"] = 10
    low     ["muexpmatchedstats"] = 0
    high    ["muexpmatchedstats"] = 10
    xtitle  ["muexpmatchedstats"] = "Number of muon expected matched stations"
    ytitle  ["muexpmatchedstats"] = "Events"
    variable["muexpmatchedstats"] = "t.Muon_muExpMatchedStats[m]"

    nbins   ["mumatchedstatsmexp"] = 20
    low     ["mumatchedstatsmexp"] = -10
    high    ["mumatchedstatsmexp"] = 10
    xtitle  ["mumatchedstatsmexp"] = "Number of muon matched stations - expected"
    ytitle  ["mumatchedstatsmexp"] = "Events"
    variable["mumatchedstatsmexp"] = "(t.Muon_muMatchedStats[m]-t.Muon_muExpMatchedStats[m])"

    nbins   ["mumatchedrpc"] = 5
    low     ["mumatchedrpc"] = 0
    high    ["mumatchedrpc"] = 5
    xtitle  ["mumatchedrpc"] = "Number of muon matched RPC layers"
    ytitle  ["mumatchedrpc"] = "Events"
    variable["mumatchedrpc"] = "t.Muon_muMatchedRPC[m]"

    nbins   ["mupixelhits"] = 10
    low     ["mupixelhits"] = 0
    high    ["mupixelhits"] = 10
    xtitle  ["mupixelhits"] = "Number of pixel hits"
    ytitle  ["mupixelhits"] = "Events"
    variable["mupixelhits"] = "t.Muon_pixHits[m]"

    nbins   ["mupixellayers"] = 10
    low     ["mupixellayers"] = 0
    high    ["mupixellayers"] = 10
    xtitle  ["mupixellayers"] = "Number of pixel layers"
    ytitle  ["mupixellayers"] = "Events"
    variable["mupixellayers"] = "t.Muon_pixLayers[m]"

    nbins   ["mustriphits"] = 30
    low     ["mustriphits"] = 0
    high    ["mustriphits"] = 30
    xtitle  ["mustriphits"] = "Number of strip"
    ytitle  ["mustriphits"] = "Events"
    variable["mustriphits"] = "t.Muon_stripHits[m]"

    nbins   ["mutrackerlayers"] = 25
    low     ["mutrackerlayers"] = 0
    high    ["mutrackerlayers"] = 25
    xtitle  ["mutrackerlayers"] = "Number of tracker layers"
    ytitle  ["mutrackerlayers"] = "Events"
    variable["mutrackerlayers"] = "t.Muon_trkLayers[m]"

    nbins   ["muhitsbeforesv"] = 10
    low     ["muhitsbeforesv"] = 0
    high    ["muhitsbeforesv"] = 10
    xtitle  ["muhitsbeforesv"] = "Number of hits before SV"
    ytitle  ["muhitsbeforesv"] = "Events"
    variable["muhitsbeforesv"] = "t.Muon_nhitsbeforesv[m]"

    nbins   ["muobsmexplayers"] = 20
    low     ["muobsmexplayers"] = -10
    high    ["muobsmexplayers"] = 10
    xtitle  ["muobsmexplayers"] = "Number of observed - expected tracker layers"
    ytitle  ["muobsmexplayers"] = "Events"
    variable["muobsmexplayers"] = "t.Muon_trkLayers[m]-t.Muon_nexpectedhitstotal[m]"

    nbins   ["muobsmexppixlayers"] = 20
    low     ["muobsmexppixlayers"] = -10
    high    ["muobsmexppixlayers"] = 10
    xtitle  ["muobsmexppixlayers"] = "Number of observed - expected pixel layers"
    ytitle  ["muobsmexppixlayers"] = "Events"
    variable["muobsmexppixlayers"] = "t.Muon_pixLayers[m]-t.Muon_nexpectedhits[m]"

    nbins   ["muobsmexphits"] = 20
    low     ["muobsmexphits"] = -10
    high    ["muobsmexphits"] = 10
    xtitle  ["muobsmexphits"] = "Number of observed - expected hits"
    ytitle  ["muobsmexphits"] = "Events"
    variable["muobsmexphits"] = "t.Muon_pixHits[m]+t.Muon_stripHits[m]-t.Muon_nexpectedhitsmultipletotal[m]"

    nbins   ["muobsmexppixhits"] = 20
    low     ["muobsmexppixhits"] = -10
    high    ["muobsmexppixhits"] = 10
    xtitle  ["muobsmexppixhits"] = "Number of observed - expected hits"
    ytitle  ["muobsmexppixhits"] = "Events"
    variable["muobsmexppixhits"] = "t.Muon_pixHits[m]-t.Muon_nexpectedhitsmultiple[m]"

    nbins   ["mudphisv"] = 320
    low     ["mudphisv"] = 0
    high    ["mudphisv"] = 3.2
    xtitle  ["mudphisv"] = "|#Delta#phi(#mu, #vec{SV})| [rad]"
    ytitle  ["mudphisv"] = "Events / 0.01 rad"
    variable["mudphisv"] = "svphi"

    nbins   ["mudphisvu"] = 320
    low     ["mudphisvu"] = 0
    high    ["mudphisvu"] = 3.2
    xtitle  ["mudphisvu"] = "|#Delta#phi(#mu, #vec{SV})| [rad]"
    ytitle  ["mudphisvu"] = "Events / 0.01 rad"
    variable["mudphisvu"] = "svphiu"

    nbins   ["mudphimm"] = 320
    low     ["mudphimm"] = -3.2/2.0
    high    ["mudphimm"] = 3.2/2.0
    xtitle  ["mudphimm"] = "|#Delta#phi(#mu, #vec{#mu#mu})| [rad]"
    ytitle  ["mudphimm"] = "Events / 0.01 rad"
    variable["mudphimm"] = "mmuphi"

    nbins   ["mudphimmu"] = 320
    low     ["mudphimmu"] = -3.2/2.0
    high    ["mudphimmu"] = 3.2/2.0
    xtitle  ["mudphimmu"] = "|#Delta#phi(#mu, #vec{#mu#mu})| [rad]"
    ytitle  ["mudphimmu"] = "Events / 0.01 rad"
    variable["mudphimmu"] = "mmuphiu"

    nbins   ["mutheta"] = 320
    low     ["mutheta"] = 0.0
    high    ["mutheta"] = 3.2
    xtitle  ["mutheta"] = "|#Delta#phi(IP, #vec{#mu#mu})| [rad]"
    ytitle  ["mutheta"] = "Events / 0.01 rad"
    variable["mutheta"] = "mmtheta"

    nbins   ["muthetau"] = 320
    low     ["muthetau"] = 0.0
    high    ["muthetau"] = 3.2
    xtitle  ["muthetau"] = "|#Delta#phi(IP, #vec{#mu#mu})| [rad]"
    ytitle  ["muthetau"] = "Events / 0.01 rad"
    variable["muthetau"] = "mmthetau"

    nbins   ["muthetamm"] = 320
    low     ["muthetamm"] = 0.0
    high    ["muthetamm"] = 3.2
    xtitle  ["muthetamm"] = "|#Delta#phi(IP, #vec{#mu#mu})| [rad]"
    ytitle  ["muthetamm"] = "Events / 0.01 rad"
    variable["muthetamm"] = "mmtheta_mmsign"

    nbins   ["muthetammu"] = 320
    low     ["muthetammu"] = 0.0
    high    ["muthetammu"] = 3.2
    xtitle  ["muthetammu"] = "|#Delta#phi(IP, #vec{#mu#mu})| [rad]"
    ytitle  ["muthetammu"] = "Events / 0.01 rad"
    variable["muthetammu"] = "mmthetau_mmsign"

    #Di-muon

    nbins   ["dimumass"] = 15000
    low     ["dimumass"] = 0
    high    ["dimumass"] = 150
    xtitle  ["dimumass"] = "m_{#mu#mu} [GeV]"
    ytitle  ["dimumass"] = "Events / 0.01 GeV"
    variable["dimumass"] = "mass"

    nbins   ["dimupt"] = 200
    low     ["dimupt"] = 0
    high    ["dimupt"] = 500
    xtitle  ["dimupt"] = "p_{T}^{#mu#mu} [GeV]"
    ytitle  ["dimupt"] = "Events / 2.5 GeV"
    variable["dimupt"] = "pt"

    nbins   ["dimudr"] = 100
    low     ["dimudr"] = 0
    high    ["dimudr"] = 5
    xtitle  ["dimudr"] = "#DeltaR(#mu, #mu)"
    ytitle  ["dimudr"] = "Events / 0.05"
    variable["dimudr"] = "drmm"

    nbins   ["dimudphi"] = 32
    low     ["dimudphi"] = 0
    high    ["dimudphi"] = 3.2
    xtitle  ["dimudphi"] = "|#Delta#phi(#mu, #mu)| [rad]"
    ytitle  ["dimudphi"] = "Events / 0.1 rad"
    variable["dimudphi"] = "dpmm"

    nbins   ["dimudeta"] = 50
    low     ["dimudeta"] = 0
    high    ["dimudeta"] = 5
    xtitle  ["dimudeta"] = "|#Delta#eta(#mu, #mu)|"
    ytitle  ["dimudeta"] = "Events / 0.1"
    variable["dimudeta"] = "demm"

    nbins   ["dimudetadphiratio"] = 100
    low     ["dimudetadphiratio"] = -5
    high    ["dimudetadphiratio"] = 5
    xtitle  ["dimudetadphiratio"] = "log_{10}|#Delta#eta(#mu, #mu) / #Delta#phi(#mu, #mu)|"
    ytitle  ["dimudetadphiratio"] = "Events / 0.1"
    variable["dimudetadphiratio"] = "ROOT.TMath.Log10(dedpmm)"

    nbins   ["dimu3dangle"] = 32
    low     ["dimu3dangle"] = 0
    high    ["dimu3dangle"] = 3.2
    xtitle  ["dimu3dangle"] = "|3D angle(#mu, #mu)|"
    ytitle  ["dimu3dangle"] = "Events / 0.1"
    variable["dimu3dangle"] = "a3dmm"

    nbins   ["dimudphisv"] = 320
    low     ["dimudphisv"] = 0
    high    ["dimudphisv"] = 3.2
    xtitle  ["dimudphisv"] = "|#Delta#phi(#vec{(#mu, #mu)}, #vec{SV})| [rad]"
    ytitle  ["dimudphisv"] = "Events / 0.01 rad"
    variable["dimudphisv"] = "dphisv"

    nbins   ["dimudetasv"] = 50
    low     ["dimudetasv"] = 0
    high    ["dimudetasv"] = 5
    xtitle  ["dimudetasv"] = "|#Delta#eta(#vec{(#mu, #mu)}, #vec{SV})|"
    ytitle  ["dimudetasv"] = "Events / 0.1"
    variable["dimudetasv"] = "detasv"

    nbins   ["dimudetadphisvratio"] = 100
    low     ["dimudetadphisvratio"] = -5
    high    ["dimudetadphisvratio"] = 5
    xtitle  ["dimudetadphisvratio"] = "log_{10}(|#Delta#eta(#vec{(#mu, #mu)}, #vec{SV})|/|#Delta#phi(#vec{(#mu, #mu)}, #vec{SV})|)"
    ytitle  ["dimudetadphisvratio"] = "Events / 0.1"
    variable["dimudetadphisvratio"] = "ROOT.TMath.Log10(detadphisv)"

    nbins   ["dimu3danglesv"] = 320
    low     ["dimu3danglesv"] = 0
    high    ["dimu3danglesv"] = 3.2
    xtitle  ["dimu3danglesv"] = "|3D angle(#vec{(#mu, #mu)}, #vec{SV})|"
    ytitle  ["dimu3danglesv"] = "Events / 0.01"
    variable["dimu3danglesv"] = "a3dsv"

    #
    nbins   ["dimuumass"] = 15000
    low     ["dimuumass"] = 0
    high    ["dimuumass"] = 150
    xtitle  ["dimuumass"] = "Uncorrected m_{#mu#mu} [GeV]"
    ytitle  ["dimuumass"] = "Events / 0.01"
    variable["dimuumass"] = "umass"

    nbins   ["seagullumass"] = 15000
    low     ["seagullumass"] = 0
    high    ["seagullumass"] = 150
    xtitle  ["seagullumass"] = "Uncorrected m_{#mu#mu} [GeV]"
    ytitle  ["seagullumass"] = "Events / 0.01"
    variable["seagullumass"] = "seagullumass"

    nbins   ["cowboyumass"] = 15000
    low     ["cowboyumass"] = 0
    high    ["cowboyumass"] = 150
    xtitle  ["cowboyumass"] = "Uncorrected m_{#mu#mu} [GeV]"
    ytitle  ["cowboyumass"] = "Events / 0.01"
    variable["cowboyumass"] = "cowboyumass"

    nbins   ["dimuupdr"] = 100
    low     ["dimuupdr"] = 0
    high    ["dimuupdr"] = 5
    xtitle  ["dimuupdr"] = "#DeltaR(#mu, #mu)"
    ytitle  ["dimuupdr"] = "Events / 0.05"
    variable["dimuupdr"] = "drmmu"

    nbins   ["dimuupdphi"] = 32
    low     ["dimuupdphi"] = 0
    high    ["dimuupdphi"] = 3.2
    xtitle  ["dimuupdphi"] = "|#Delta#phi(#mu, #mu)| [rad]"
    ytitle  ["dimuupdphi"] = "Events / 0.1 rad"
    variable["dimuupdphi"] = "dpmmu"

    nbins   ["dimuupdeta"] = 50
    low     ["dimuupdeta"] = 0
    high    ["dimuupdeta"] = 5
    xtitle  ["dimuupdeta"] = "|#Delta#eta(#mu, #mu)|"
    ytitle  ["dimuupdeta"] = "Events / 0.1"
    variable["dimuupdeta"] = "demmu"

    nbins   ["dimuupdetadphiratio"] = 100
    low     ["dimuupdetadphiratio"] = -5
    high    ["dimuupdetadphiratio"] = 5
    xtitle  ["dimuupdetadphiratio"] = "log_{10}|#Delta#eta(#mu, #mu) / #Delta#phi(#mu, #mu)|"
    ytitle  ["dimuupdetadphiratio"] = "Events / 0.1"
    variable["dimuupdetadphiratio"] = "ROOT.TMath.Log10(dedpmmu)"

    nbins   ["dimuup3dangle"] = 32
    low     ["dimuup3dangle"] = 0
    high    ["dimuup3dangle"] = 3.2
    xtitle  ["dimuup3dangle"] = "|3D angle(#mu, #mu)|"
    ytitle  ["dimuup3dangle"] = "Events / 0.1"
    variable["dimuup3dangle"] = "a3dmmu"

    nbins   ["dimuupdphisv"] = 320
    low     ["dimuupdphisv"] = 0
    high    ["dimuupdphisv"] = 3.2
    xtitle  ["dimuupdphisv"] = "|#Delta#phi(#vec{(#mu, #mu)}, #vec{SV})| [rad]"
    ytitle  ["dimuupdphisv"] = "Events / 0.01 rad"
    variable["dimuupdphisv"] = "dphisvu"

    nbins   ["dimuupdetasv"] = 50
    low     ["dimuupdetasv"] = 0
    high    ["dimuupdetasv"] = 5
    xtitle  ["dimuupdetasv"] = "|#Delta#eta(#vec{(#mu, #mu)}, #vec{SV})|"
    ytitle  ["dimuupdetasv"] = "Events / 0.1"
    variable["dimuupdetasv"] = "detasvu"

    nbins   ["dimuupdetadphisvratio"] = 100
    low     ["dimuupdetadphisvratio"] = -5
    high    ["dimuupdetadphisvratio"] = 5
    xtitle  ["dimuupdetadphisvratio"] = "log_{10}(|#Delta#eta(#vec{(#mu, #mu)}, #vec{SV})|/|#Delta#phi(#vec{(#mu, #mu)}, #vec{SV})|)"
    ytitle  ["dimuupdetadphisvratio"] = "Events / 0.1"
    variable["dimuupdetadphisvratio"] = "ROOT.TMath.Log10(detadphisvu)"

    nbins   ["dimuup3danglesv"] = 320
    low     ["dimuup3danglesv"] = 0
    high    ["dimuup3danglesv"] = 3.2
    xtitle  ["dimuup3danglesv"] = "|3D angle(#vec{(#mu, #mu)}, #vec{SV})|"
    ytitle  ["dimuup3danglesv"] = "Events / 0.01"
    variable["dimuup3danglesv"] = "a3dsvu"

    nbins   ["dimudetamindphimusvratio"] = 100
    low     ["dimudetamindphimusvratio"] = -5
    high    ["dimudetamindphimusvratio"] = 5
    xtitle  ["dimudetamindphimusvratio"] = "log_{10}(|#Delta#eta(#mu, #mu), #vec{SV})|/min |#Delta#phi(#mu, #vec{SV})|)"
    ytitle  ["dimudetamindphimusvratio"] = "Events / 0.1"
    variable["dimudetamindphimusvratio"] = "ROOT.TMath.Log10(demmdpsvmin)"

    nbins   ["dimudetasvmindphimusvratio"] = 100
    low     ["dimudetasvmindphimusvratio"] = -5
    high    ["dimudetasvmindphimusvratio"] = 5
    xtitle  ["dimudetasvmindphimusvratio"] = "log_{10}(|#Delta#eta(#vec{(#mu, #mu)}, #vec{SV})|/min |#Delta#phi(#mu, #vec{SV})|)"
    ytitle  ["dimudetasvmindphimusvratio"] = "Events / 0.1"
    variable["dimudetasvmindphimusvratio"] = "ROOT.TMath.Log10(desvdpsvmin)"

    nbins   ["dimusdphisvlxy"] = 1100
    low     ["dimusdphisvlxy"] = 0
    high    ["dimusdphisvlxy"] = 110.0
    xtitle  ["dimusdphisvlxy"] = "|sin (#Delta#phi(#vec{(#mu, #mu)}, #vec{SV}))| l_{xy} [cm]"
    ytitle  ["dimusdphisvlxy"] = "Events / 0.1 cm"
    variable["dimusdphisvlxy"] = "sindpsvlxy"

    nbins   ["dimus3danglesvl3d"] = 1500
    low     ["dimus3danglesvl3d"] = 0
    high    ["dimus3danglesvl3d"] = 150.0
    xtitle  ["dimus3danglesvl3d"] = "|sin (3D angle(#vec{(#mu, #mu)}, #vec{SV}))| l_{3D} [cm]"
    ytitle  ["dimus3danglesvl3d"] = "Events / 0.1 cm"
    variable["dimus3danglesvl3d"] = "sina3dsvl3d"

    nbins   ["dimuupdetamindphimusvratio"] = 100
    low     ["dimuupdetamindphimusvratio"] = -5
    high    ["dimuupdetamindphimusvratio"] = 5
    xtitle  ["dimuupdetamindphimusvratio"] = "log_{10}(|#Delta#eta(#mu, #mu), #vec{SV})|/min |#Delta#phi(#mu, #vec{SV})|)"
    ytitle  ["dimuupdetamindphimusvratio"] = "Events / 0.1"
    variable["dimuupdetamindphimusvratio"] = "ROOT.TMath.Log10(demmdpsvminu)"

    nbins   ["dimuupdetasvmindphimusvratio"] = 100
    low     ["dimuupdetasvmindphimusvratio"] = -5
    high    ["dimuupdetasvmindphimusvratio"] = 5
    xtitle  ["dimuupdetasvmindphimusvratio"] = "log_{10}(|#Delta#eta(#vec{(#mu, #mu)}, #vec{SV})|/min |#Delta#phi(#mu, #vec{SV})|)"
    ytitle  ["dimuupdetasvmindphimusvratio"] = "Events / 0.1"
    variable["dimuupdetasvmindphimusvratio"] = "ROOT.TMath.Log10(desvdpsvminu)"

    nbins   ["dimuupsdphisvlxy"] = 1100
    low     ["dimuupsdphisvlxy"] = 0
    high    ["dimuupsdphisvlxy"] = 110.0
    xtitle  ["dimuupsdphisvlxy"] = "|sin (#Delta#phi(#vec{(#mu, #mu)}, #vec{SV}))| l_{xy} [cm]"
    ytitle  ["dimuupsdphisvlxy"] = "Events / 0.1 cm"
    variable["dimuupsdphisvlxy"] = "sindpsvlxyu"

    nbins   ["dimuups3danglesvl3d"] = 1500
    low     ["dimuups3danglesvl3d"] = 0
    high    ["dimuups3danglesvl3d"] = 150.0
    xtitle  ["dimuups3danglesvl3d"] = "|sin (3D angle(#vec{(#mu, #mu)}, #vec{SV}))| l_{3D} [cm]"
    ytitle  ["dimuups3danglesvl3d"] = "Events / 0.1 cm"
    variable["dimuups3danglesvl3d"] = "sina3dsvl3du"

    nbins   ["totalmuhitsbeforesv"] = 10
    low     ["totalmuhitsbeforesv"] = 0
    high    ["totalmuhitsbeforesv"] = 10
    xtitle  ["totalmuhitsbeforesv"] = "Number of hits before SV"
    ytitle  ["totalmuhitsbeforesv"] = "Events"
    variable["totalmuhitsbeforesv"] = "nhitsbeforesvtotal"

    nbins   ["dimugenmatchingdr"] = 100
    low     ["dimugenmatchingdr"] = 0
    high    ["dimugenmatchingdr"] = 3.0 
    xtitle  ["dimugenmatchingdr"] = "Min. #DeltaR(#vec{(#mu, #mu)}, gen))"
    ytitle  ["dimugenmatchingdr"] = "Events / 0.1 cm"
    variable["dimugenmatchingdr"] = "drgen"

    nbins   ["dimuisocat"] = 3
    low     ["dimuisocat"] = 0
    high    ["dimuisocat"] = 3.0 
    xtitle  ["dimuisocat"] = "Dimuon isolation category"
    ytitle  ["dimuisocat"] = "Events / Category"
    variable["dimuisocat"] = "isocat"

    # Four-muon

    nbins   ["fourmumass"] = 15000
    low     ["fourmumass"] = 0
    high    ["fourmumass"] = 150
    xtitle  ["fourmumass"] = "m_{4#mu} [GeV]"
    ytitle  ["fourmumass"] = "Events / 0.01 GeV"
    variable["fourmumass"] = "mass"

    nbins   ["fourmuminmass"] = 15000
    low     ["fourmuminmass"] = 0
    high    ["fourmuminmass"] = 150
    xtitle  ["fourmuminmass"] = "m_{#mu#mu}^{max} [GeV]"
    ytitle  ["fourmuminmass"] = "Events / 0.01 GeV"
    variable["fourmuminmass"] = "minmass"

    nbins   ["fourmumaxmass"] = 15000
    low     ["fourmumaxmass"] = 0
    high    ["fourmumaxmass"] = 150
    xtitle  ["fourmumaxmass"] = "m_{#mu#mu}^{min} [GeV]"
    ytitle  ["fourmumaxmass"] = "Events / 0.01 GeV"
    variable["fourmumaxmass"] = "maxmass"

    nbins   ["fourmuavgmass"] = 15000
    low     ["fourmuavgmass"] = 0
    high    ["fourmuavgmass"] = 150
    xtitle  ["fourmuavgmass"] = "<m_{#mu#mu}> [GeV]"
    ytitle  ["fourmuavgmass"] = "Events / 0.01 GeV"
    variable["fourmuavgmass"] = "avgmass"

    nbins   ["fourmureldmass"] = 500
    low     ["fourmureldmass"] = 0
    high    ["fourmureldmass"] = 5
    xtitle  ["fourmureldmass"] = "(m_{#mu#mu}^{max} - m_{#mu#mu}^{min})/<m_{#mu#mu}>"
    ytitle  ["fourmureldmass"] = "Events / 0.01"
    variable["fourmureldmass"] = "reldmass"

    nbins   ["fourmupt"] = 200
    low     ["fourmupt"] = 0
    high    ["fourmupt"] = 500
    xtitle  ["fourmupt"] = "p_{T}^{4#mu} [GeV]"
    ytitle  ["fourmupt"] = "Events / 2.5 GeV"
    variable["fourmupt"] = "pt"

    nbins   ["fourmuminpt"] = 200
    low     ["fourmuminpt"] = 0
    high    ["fourmuminpt"] = 500
    xtitle  ["fourmuminpt"] = "min p_{T}^{#mu#mu} [GeV]"
    ytitle  ["fourmuminpt"] = "Events / 2.5 GeV"
    variable["fourmuminpt"] = "minpt"

    nbins   ["fourmumaxpt"] = 200
    low     ["fourmumaxpt"] = 0
    high    ["fourmumaxpt"] = 500
    xtitle  ["fourmumaxpt"] = "max p_{T}^{#mu#mu} [GeV]"
    ytitle  ["fourmumaxpt"] = "Events / 2.5 GeV"
    variable["fourmumaxpt"] = "maxpt"

    nbins   ["fourmumindr"] = 100
    low     ["fourmumindr"] = 0
    high    ["fourmumindr"] = 5
    xtitle  ["fourmumindr"] = "min #DeltaR(#mu, #mu)"
    ytitle  ["fourmumindr"] = "Events / 0.05"
    variable["fourmumindr"] = "mindrmm"

    nbins   ["fourmumaxdr"] = 100
    low     ["fourmumaxdr"] = 0
    high    ["fourmumaxdr"] = 5
    xtitle  ["fourmumaxdr"] = "max #DeltaR(#mu, #mu)"
    ytitle  ["fourmumaxdr"] = "Events / 0.05"
    variable["fourmumaxdr"] = "maxdrmm"

    nbins   ["fourmumindphi"] = 32
    low     ["fourmumindphi"] = 0
    high    ["fourmumindphi"] = 3.2
    xtitle  ["fourmumindphi"] = "min |#Delta#phi(#mu, #mu)| [rad]"
    ytitle  ["fourmumindphi"] = "Events / 0.1 rad"
    variable["fourmumindphi"] = "mindpmm"

    nbins   ["fourmumaxdphi"] = 32
    low     ["fourmumaxdphi"] = 0
    high    ["fourmumaxdphi"] = 3.2
    xtitle  ["fourmumaxdphi"] = "max |#Delta#phi(#mu, #mu)| [rad]"
    ytitle  ["fourmumaxdphi"] = "Events / 0.1 rad"
    variable["fourmumaxdphi"] = "maxdpmm"

    nbins   ["fourmumindeta"] = 50
    low     ["fourmumindeta"] = 0
    high    ["fourmumindeta"] = 5
    xtitle  ["fourmumindeta"] = "min |#Delta#eta(#mu, #mu)|"
    ytitle  ["fourmumindeta"] = "Events / 0.1"
    variable["fourmumindeta"] = "mindemm"

    nbins   ["fourmumaxdeta"] = 50
    low     ["fourmumaxdeta"] = 0
    high    ["fourmumaxdeta"] = 5
    xtitle  ["fourmumaxdeta"] = "max |#Delta#eta(#mu, #mu)|"
    ytitle  ["fourmumaxdeta"] = "Events / 0.1"
    variable["fourmumaxdeta"] = "maxdemm"

    nbins   ["fourmumindetadphiratio"] = 100
    low     ["fourmumindetadphiratio"] = -5
    high    ["fourmumindetadphiratio"] = 5
    xtitle  ["fourmumindetadphiratio"] = "log_{10}(min(|#Delta#eta(#mu, #mu) / #Delta#phi(#mu, #mu)|))"
    ytitle  ["fourmumindetadphiratio"] = "Events / 0.1"
    variable["fourmumindetadphiratio"] = "ROOT.TMath.Log10(mindedpmm)"

    nbins   ["fourmumaxdetadphiratio"] = 100
    low     ["fourmumaxdetadphiratio"] = -5
    high    ["fourmumaxdetadphiratio"] = 5
    xtitle  ["fourmumaxdetadphiratio"] = "log_{10}(max(|#Delta#eta(#mu, #mu) / #Delta#phi(#mu, #mu)|))"
    ytitle  ["fourmumaxdetadphiratio"] = "Events / 0.1"
    variable["fourmumaxdetadphiratio"] = "ROOT.TMath.Log10(maxdedpmm)"

    nbins   ["fourmumin3dangle"] = 32
    low     ["fourmumin3dangle"] = 0
    high    ["fourmumin3dangle"] = 3.2
    xtitle  ["fourmumin3dangle"] = "min |3D angle(#mu, #mu)|"
    ytitle  ["fourmumin3dangle"] = "Events / 0.1"
    variable["fourmumin3dangle"] = "mina3dmm"

    nbins   ["fourmumax3dangle"] = 32
    low     ["fourmumax3dangle"] = 0
    high    ["fourmumax3dangle"] = 3.2
    xtitle  ["fourmumax3dangle"] = "max |3D angle(#mu, #mu)|"
    ytitle  ["fourmumax3dangle"] = "Events / 0.1"
    variable["fourmumax3dangle"] = "maxa3dmm"

    nbins   ["fourmudphisv"] = 320
    low     ["fourmudphisv"] = 0
    high    ["fourmudphisv"] = 3.2
    xtitle  ["fourmudphisv"] = "|#Delta#phi(#vec{4#mu}, #vec{SV})| [rad]"
    ytitle  ["fourmudphisv"] = "Events / 0.01 rad"
    variable["fourmudphisv"] = "dphisv"

    nbins   ["fourmumindphisv"] = 320
    low     ["fourmumindphisv"] = 0
    high    ["fourmumindphisv"] = 3.2
    xtitle  ["fourmumindphisv"] = "min |#Delta#phi(#vec{(#mu, #mu)}, #vec{SV})| [rad]"
    ytitle  ["fourmumindphisv"] = "Events / 0.01 rad"
    variable["fourmumindphisv"] = "mindphisv"

    nbins   ["fourmumaxdphisv"] = 320
    low     ["fourmumaxdphisv"] = 0
    high    ["fourmumaxdphisv"] = 3.2
    xtitle  ["fourmumaxdphisv"] = "max |#Delta#phi(#vec{(#mu, #mu)}, #vec{SV})| [rad]"
    ytitle  ["fourmumaxdphisv"] = "Events / 0.01 rad"
    variable["fourmumaxdphisv"] = "maxdphisv"

    nbins   ["fourmudetasv"] = 50
    low     ["fourmudetasv"] = 0
    high    ["fourmudetasv"] = 5
    xtitle  ["fourmudetasv"] = "|#Delta#eta(#vec{4#mu}, #vec{SV})|"
    ytitle  ["fourmudetasv"] = "Events / 0.1"
    variable["fourmudetasv"] = "detasv"

    nbins   ["fourmumindetasv"] = 50
    low     ["fourmumindetasv"] = 0
    high    ["fourmumindetasv"] = 5
    xtitle  ["fourmumindetasv"] = "min |#Delta#eta(#vec{(#mu, #mu)}, #vec{SV})|"
    ytitle  ["fourmumindetasv"] = "Events / 0.1"
    variable["fourmumindetasv"] = "mindetasv"

    nbins   ["fourmumaxdetasv"] = 50
    low     ["fourmumaxdetasv"] = 0
    high    ["fourmumaxdetasv"] = 5
    xtitle  ["fourmumaxdetasv"] = "max |#Delta#eta(#vec{(#mu, #mu)}, #vec{SV})|"
    ytitle  ["fourmumaxdetasv"] = "Events / 0.1"
    variable["fourmumaxdetasv"] = "maxdetasv"

    nbins   ["fourmudetadphisvratio"] = 100
    low     ["fourmudetadphisvratio"] = -5
    high    ["fourmudetadphisvratio"] = 5
    xtitle  ["fourmudetadphisvratio"] = "log_{10}(|#Delta#eta(#vec{4#mu}, #vec{SV})|/|#Delta#phi(#vec{4#mu}, #vec{SV})|)"
    ytitle  ["fourmudetadphisvratio"] = "Events / 0.1"
    variable["fourmudetadphisvratio"] = "ROOT.TMath.Log10(detadphisv)"

    nbins   ["fourmumindetadphisvratio"] = 100
    low     ["fourmumindetadphisvratio"] = -5
    high    ["fourmumindetadphisvratio"] = 5
    xtitle  ["fourmumindetadphisvratio"] = "log_{10}(min(|#Delta#eta(#vec{(#mu, #mu)}, #vec{SV})|/|#Delta#phi(#vec{(#mu, #mu)}, #vec{SV})|))"
    ytitle  ["fourmumindetadphisvratio"] = "Events / 0.1"
    variable["fourmumindetadphisvratio"] = "ROOT.TMath.Log10(mindetadphisv)"

    nbins   ["fourmumaxdetadphisvratio"] = 100
    low     ["fourmumaxdetadphisvratio"] = -5
    high    ["fourmumaxdetadphisvratio"] = 5
    xtitle  ["fourmumaxdetadphisvratio"] = "log_{10}(max(|#Delta#eta(#vec{(#mu, #mu)}, #vec{SV})|/|#Delta#phi(#vec{(#mu, #mu)}, #vec{SV})|))"
    ytitle  ["fourmumaxdetadphisvratio"] = "Events / 0.1"
    variable["fourmumaxdetadphisvratio"] = "ROOT.TMath.Log10(maxdetadphisv)"

    nbins   ["fourmu3danglesv"] = 320
    low     ["fourmu3danglesv"] = 0
    high    ["fourmu3danglesv"] = 3.2
    xtitle  ["fourmu3danglesv"] = "|3D angle(#vec{4#mu}, #vec{SV})|"
    ytitle  ["fourmu3danglesv"] = "Events / 0.01"
    variable["fourmu3danglesv"] = "a3dsv"

    nbins   ["fourmumin3danglesv"] = 320
    low     ["fourmumin3danglesv"] = 0
    high    ["fourmumin3danglesv"] = 3.2
    xtitle  ["fourmumin3danglesv"] = "min |3D angle(#vec{(#mu, #mu)}, #vec{SV})|"
    ytitle  ["fourmumin3danglesv"] = "Events / 0.01"
    variable["fourmumin3danglesv"] = "mina3dsv"

    nbins   ["fourmumax3danglesv"] = 320
    low     ["fourmumax3danglesv"] = 0
    high    ["fourmumax3danglesv"] = 3.2
    xtitle  ["fourmumax3danglesv"] = "max |3D angle(#vec{(#mu, #mu)}, #vec{SV})|"
    ytitle  ["fourmumax3danglesv"] = "Events / 0.01"
    variable["fourmumax3danglesv"] = "mina3dsv"

    #

    nbins   ["fourmuupmindr"] = 100
    low     ["fourmuupmindr"] = 0
    high    ["fourmuupmindr"] = 5
    xtitle  ["fourmuupmindr"] = "min #DeltaR(#mu, #mu)"
    ytitle  ["fourmuupmindr"] = "Events / 0.05"
    variable["fourmuupmindr"] = "mindrmmu"

    nbins   ["fourmuupmaxdr"] = 100
    low     ["fourmuupmaxdr"] = 0
    high    ["fourmuupmaxdr"] = 5
    xtitle  ["fourmuupmaxdr"] = "max #DeltaR(#mu, #mu)"
    ytitle  ["fourmuupmaxdr"] = "Events / 0.05"
    variable["fourmuupmaxdr"] = "maxdrmmu"

    nbins   ["fourmuupmindphi"] = 32
    low     ["fourmuupmindphi"] = 0
    high    ["fourmuupmindphi"] = 3.2
    xtitle  ["fourmuupmindphi"] = "min |#Delta#phi(#mu, #mu)| [rad]"
    ytitle  ["fourmuupmindphi"] = "Events / 0.1 rad"
    variable["fourmuupmindphi"] = "mindpmmu"

    nbins   ["fourmuupmaxdphi"] = 32
    low     ["fourmuupmaxdphi"] = 0
    high    ["fourmuupmaxdphi"] = 3.2
    xtitle  ["fourmuupmaxdphi"] = "max |#Delta#phi(#mu, #mu)| [rad]"
    ytitle  ["fourmuupmaxdphi"] = "Events / 0.1 rad"
    variable["fourmuupmaxdphi"] = "maxdpmmu"

    nbins   ["fourmuupmindeta"] = 50
    low     ["fourmuupmindeta"] = 0
    high    ["fourmuupmindeta"] = 5
    xtitle  ["fourmuupmindeta"] = "min |#Delta#eta(#mu, #mu)|"
    ytitle  ["fourmuupmindeta"] = "Events / 0.1"
    variable["fourmuupmindeta"] = "mindemmu"

    nbins   ["fourmuupmaxdeta"] = 50
    low     ["fourmuupmaxdeta"] = 0
    high    ["fourmuupmaxdeta"] = 5
    xtitle  ["fourmuupmaxdeta"] = "max |#Delta#eta(#mu, #mu)|"
    ytitle  ["fourmuupmaxdeta"] = "Events / 0.1"
    variable["fourmuupmaxdeta"] = "maxdemmu"

    nbins   ["fourmuupmindetadphiratio"] = 100
    low     ["fourmuupmindetadphiratio"] = -5
    high    ["fourmuupmindetadphiratio"] = 5
    xtitle  ["fourmuupmindetadphiratio"] = "log_{10}(min(|#Delta#eta(#mu, #mu) / #Delta#phi(#mu, #mu)|))"
    ytitle  ["fourmuupmindetadphiratio"] = "Events / 0.1"
    variable["fourmuupmindetadphiratio"] = "ROOT.TMath.Log10(mindedpmmu)"

    nbins   ["fourmuupmaxdetadphiratio"] = 100
    low     ["fourmuupmaxdetadphiratio"] = -5
    high    ["fourmuupmaxdetadphiratio"] = 5
    xtitle  ["fourmuupmaxdetadphiratio"] = "log_{10}(max(|#Delta#eta(#mu, #mu) / #Delta#phi(#mu, #mu)|))"
    ytitle  ["fourmuupmaxdetadphiratio"] = "Events / 0.1"
    variable["fourmuupmaxdetadphiratio"] = "ROOT.TMath.Log10(maxdedpmmu)"

    nbins   ["fourmuupmin3dangle"] = 32
    low     ["fourmuupmin3dangle"] = 0
    high    ["fourmuupmin3dangle"] = 3.2
    xtitle  ["fourmuupmin3dangle"] = "min |3D angle(#mu, #mu)|"
    ytitle  ["fourmuupmin3dangle"] = "Events / 0.1"
    variable["fourmuupmin3dangle"] = "mina3dmmu"

    nbins   ["fourmuupmax3dangle"] = 32
    low     ["fourmuupmax3dangle"] = 0
    high    ["fourmuupmax3dangle"] = 3.2
    xtitle  ["fourmuupmax3dangle"] = "max |3D angle(#mu, #mu)|"
    ytitle  ["fourmuupmax3dangle"] = "Events / 0.1"
    variable["fourmuupmax3dangle"] = "maxa3dmmu"

    nbins   ["fourmuupdphisv"] = 320
    low     ["fourmuupdphisv"] = 0
    high    ["fourmuupdphisv"] = 3.2
    xtitle  ["fourmuupdphisv"] = "|#Delta#phi(#vec{4#mu}, #vec{SV})| [rad]"
    ytitle  ["fourmuupdphisv"] = "Events / 0.01 rad"
    variable["fourmuupdphisv"] = "dphisvu"

    nbins   ["fourmuupmindphisv"] = 320
    low     ["fourmuupmindphisv"] = 0
    high    ["fourmuupmindphisv"] = 3.2
    xtitle  ["fourmuupmindphisv"] = "min |#Delta#phi(#vec{(#mu, #mu)}, #vec{SV})| [rad]"
    ytitle  ["fourmuupmindphisv"] = "Events / 0.01 rad"
    variable["fourmuupmindphisv"] = "mindphisvu"

    nbins   ["fourmuupmaxdphisv"] = 320
    low     ["fourmuupmaxdphisv"] = 0
    high    ["fourmuupmaxdphisv"] = 3.2
    xtitle  ["fourmuupmaxdphisv"] = "max |#Delta#phi(#vec{(#mu, #mu)}, #vec{SV})| [rad]"
    ytitle  ["fourmuupmaxdphisv"] = "Events / 0.01 rad"
    variable["fourmuupmaxdphisv"] = "maxdphisvu"

    nbins   ["fourmuupdetasv"] = 50
    low     ["fourmuupdetasv"] = 0
    high    ["fourmuupdetasv"] = 5
    xtitle  ["fourmuupdetasv"] = "|#Delta#eta(#vec{4#mu}, #vec{SV})|"
    ytitle  ["fourmuupdetasv"] = "Events / 0.1"
    variable["fourmuupdetasv"] = "detasvu"

    nbins   ["fourmuupmindetasv"] = 50
    low     ["fourmuupmindetasv"] = 0
    high    ["fourmuupmindetasv"] = 5
    xtitle  ["fourmuupmindetasv"] = "min |#Delta#eta(#vec{(#mu, #mu)}, #vec{SV})|"
    ytitle  ["fourmuupmindetasv"] = "Events / 0.1"
    variable["fourmuupmindetasv"] = "mindetasvu"

    nbins   ["fourmuupmaxdetasv"] = 50
    low     ["fourmuupmaxdetasv"] = 0
    high    ["fourmuupmaxdetasv"] = 5
    xtitle  ["fourmuupmaxdetasv"] = "max |#Delta#eta(#vec{(#mu, #mu)}, #vec{SV})|"
    ytitle  ["fourmuupmaxdetasv"] = "Events / 0.1"
    variable["fourmuupmaxdetasv"] = "maxdetasvu"

    nbins   ["fourmuupdetadphisvratio"] = 100
    low     ["fourmuupdetadphisvratio"] = -5
    high    ["fourmuupdetadphisvratio"] = 5
    xtitle  ["fourmuupdetadphisvratio"] = "log_{10}(|#Delta#eta(#vec{4#mu}, #vec{SV})|/|#Delta#phi(#vec{4#mu}, #vec{SV})|)"
    ytitle  ["fourmuupdetadphisvratio"] = "Events / 0.1"
    variable["fourmuupdetadphisvratio"] = "ROOT.TMath.Log10(detadphisvu)"

    nbins   ["fourmuupmindetadphisvratio"] = 100
    low     ["fourmuupmindetadphisvratio"] = -5
    high    ["fourmuupmindetadphisvratio"] = 5
    xtitle  ["fourmuupmindetadphisvratio"] = "log_{10}(min(|#Delta#eta(#vec{(#mu, #mu)}, #vec{SV})|/|#Delta#phi(#vec{(#mu, #mu)}, #vec{SV})|))"
    ytitle  ["fourmuupmindetadphisvratio"] = "Events / 0.1"
    variable["fourmuupmindetadphisvratio"] = "ROOT.TMath.Log10(mindetadphisvu)"

    nbins   ["fourmuupmaxdetadphisvratio"] = 100
    low     ["fourmuupmaxdetadphisvratio"] = -5
    high    ["fourmuupmaxdetadphisvratio"] = 5
    xtitle  ["fourmuupmaxdetadphisvratio"] = "log_{10}(max(|#Delta#eta(#vec{(#mu, #mu)}, #vec{SV})|/|#Delta#phi(#vec{(#mu, #mu)}, #vec{SV})|))"
    ytitle  ["fourmuupmaxdetadphisvratio"] = "Events / 0.1"
    variable["fourmuupmaxdetadphisvratio"] = "ROOT.TMath.Log10(maxdetadphisvu)"

    nbins   ["fourmuup3danglesv"] = 320
    low     ["fourmuup3danglesv"] = 0
    high    ["fourmuup3danglesv"] = 3.2
    xtitle  ["fourmuup3danglesv"] = "|3D angle(#vec{4#mu}, #vec{SV})|"
    ytitle  ["fourmuup3danglesv"] = "Events / 0.01"
    variable["fourmuup3danglesv"] = "a3dsvu"

    nbins   ["fourmuupmin3danglesv"] = 320
    low     ["fourmuupmin3danglesv"] = 0
    high    ["fourmuupmin3danglesv"] = 3.2
    xtitle  ["fourmuupmin3danglesv"] = "min |3D angle(#vec{(#mu, #mu)}, #vec{SV})|"
    ytitle  ["fourmuupmin3danglesv"] = "Events / 0.01"
    variable["fourmuupmin3danglesv"] = "mina3dsvu"

    nbins   ["fourmuupmax3danglesv"] = 320
    low     ["fourmuupmax3danglesv"] = 0
    high    ["fourmuupmax3danglesv"] = 3.2
    xtitle  ["fourmuupmax3danglesv"] = "max |3D angle(#vec{(#mu, #mu)}, #vec{SV})|"
    ytitle  ["fourmuupmax3danglesv"] = "Events / 0.01"
    variable["fourmuupmax3danglesv"] = "mina3dsvu"

    #

    nbins   ["fourmudetamindphimusvratio"] = 100
    low     ["fourmudetamindphimusvratio"] = -5
    high    ["fourmudetamindphimusvratio"] = 5
    xtitle  ["fourmudetamindphimusvratio"] = "log_{10}(|#Delta#eta(#mu, #mu), #vec{SV})|/min |#Delta#phi(#mu, #vec{SV})|)"
    ytitle  ["fourmudetamindphimusvratio"] = "Events / 0.1"
    variable["fourmudetamindphimusvratio"] = "ROOT.TMath.Log10(demmdpsvmin)"

    nbins   ["fourmumindetamindphimusvratio"] = 100
    low     ["fourmumindetamindphimusvratio"] = -5
    high    ["fourmumindetamindphimusvratio"] = 5
    xtitle  ["fourmumindetamindphimusvratio"] = "min log_{10}(|#Delta#eta(#mu, #mu), #vec{SV})|/min |#Delta#phi(#mu, #vec{SV})|)"
    ytitle  ["fourmumindetamindphimusvratio"] = "Events / 0.1"
    variable["fourmumindetamindphimusvratio"] = "ROOT.TMath.Log10(mindemmdpsvmin)"

    nbins   ["fourmumaxdetamindphimusvratio"] = 100
    low     ["fourmumaxdetamindphimusvratio"] = -5
    high    ["fourmumaxdetamindphimusvratio"] = 5
    xtitle  ["fourmumaxdetamindphimusvratio"] = "max log_{10}(|#Delta#eta(#mu, #mu), #vec{SV})|/min |#Delta#phi(#mu, #vec{SV})|)"
    ytitle  ["fourmumaxdetamindphimusvratio"] = "Events / 0.1"
    variable["fourmumaxdetamindphimusvratio"] = "ROOT.TMath.Log10(maxdemmdpsvmin)"

    nbins   ["fourmudetasvmindphimusvratio"] = 100
    low     ["fourmudetasvmindphimusvratio"] = -5
    high    ["fourmudetasvmindphimusvratio"] = 5
    xtitle  ["fourmudetasvmindphimusvratio"] = "log_{10}(|#Delta#eta(#vec{4#mu}, #vec{SV})|/min |#Delta#phi(#mu, #vec{SV})|)"
    ytitle  ["fourmudetasvmindphimusvratio"] = "Events / 0.1"
    variable["fourmudetasvmindphimusvratio"] = "ROOT.TMath.Log10(desvdpsvmin)"

    nbins   ["fourmumindetasvmindphimusvratio"] = 100
    low     ["fourmumindetasvmindphimusvratio"] = -5
    high    ["fourmumindetasvmindphimusvratio"] = 5
    xtitle  ["fourmumindetasvmindphimusvratio"] = "min log_{10}(|#Delta#eta(#vec{(#mu, #mu)}, #vec{SV})|/min |#Delta#phi(#mu, #vec{SV})|)"
    ytitle  ["fourmumindetasvmindphimusvratio"] = "Events / 0.1"
    variable["fourmumindetasvmindphimusvratio"] = "ROOT.TMath.Log10(mindesvdpsvmin)"

    nbins   ["fourmumaxdetasvmindphimusvratio"] = 100
    low     ["fourmumaxdetasvmindphimusvratio"] = -5
    high    ["fourmumaxdetasvmindphimusvratio"] = 5
    xtitle  ["fourmumaxdetasvmindphimusvratio"] = "max log_{10}(|#Delta#eta(#vec{(#mu, #mu)}, #vec{SV})|/min |#Delta#phi(#mu, #vec{SV})|)"
    ytitle  ["fourmumaxdetasvmindphimusvratio"] = "Events / 0.1"
    variable["fourmumaxdetasvmindphimusvratio"] = "ROOT.TMath.Log10(maxdesvdpsvmin)"

    nbins   ["fourmusdphisvlxy"] = 1100
    low     ["fourmusdphisvlxy"] = 0
    high    ["fourmusdphisvlxy"] = 110.0
    xtitle  ["fourmusdphisvlxy"] = "|sin (#Delta#phi(#vec{4#mu}, #vec{SV}))| l_{xy} [cm]"
    ytitle  ["fourmusdphisvlxy"] = "Events / 0.1 cm"
    variable["fourmusdphisvlxy"] = "sindpsvlxy"

    nbins   ["fourmuminsdphisvlxy"] = 1100
    low     ["fourmuminsdphisvlxy"] = 0
    high    ["fourmuminsdphisvlxy"] = 110.0
    xtitle  ["fourmuminsdphisvlxy"] = "min |sin (#Delta#phi(#vec{(#mu, #mu)}, #vec{SV}))| l_{xy} [cm]"
    ytitle  ["fourmuminsdphisvlxy"] = "Events / 0.1 cm"
    variable["fourmuminsdphisvlxy"] = "minsindpsvlxy"

    nbins   ["fourmumaxsdphisvlxy"] = 1100
    low     ["fourmumaxsdphisvlxy"] = 0
    high    ["fourmumaxsdphisvlxy"] = 110.0
    xtitle  ["fourmumaxsdphisvlxy"] = "max |sin (#Delta#phi(#vec{(#mu, #mu)}, #vec{SV}))| l_{xy} [cm]"
    ytitle  ["fourmumaxsdphisvlxy"] = "Events / 0.1 cm"
    variable["fourmumaxsdphisvlxy"] = "maxsindpsvlxy"

    nbins   ["fourmus3danglesvl3d"] = 1500
    low     ["fourmus3danglesvl3d"] = 0
    high    ["fourmus3danglesvl3d"] = 150.0
    xtitle  ["fourmus3danglesvl3d"] = "|sin (3D angle(#vec{4#mu}, #vec{SV}))| l_{3D} [cm]"
    ytitle  ["fourmus3danglesvl3d"] = "Events / 0.1 cm"
    variable["fourmus3danglesvl3d"] = "sina3dsvl3d"

    nbins   ["fourmumins3danglesvl3d"] = 1500
    low     ["fourmumins3danglesvl3d"] = 0
    high    ["fourmumins3danglesvl3d"] = 150.0
    xtitle  ["fourmumins3danglesvl3d"] = "min |sin (3D angle(#vec{(#mu, #mu)}, #vec{SV}))| l_{3D} [cm]"
    ytitle  ["fourmumins3danglesvl3d"] = "Events / 0.1 cm"
    variable["fourmumins3danglesvl3d"] = "minsina3dsvl3d"

    nbins   ["fourmumaxs3danglesvl3d"] = 1500
    low     ["fourmumaxs3danglesvl3d"] = 0
    high    ["fourmumaxs3danglesvl3d"] = 150.0
    xtitle  ["fourmumaxs3danglesvl3d"] = "max |sin (3D angle(#vec{(#mu, #mu)}, #vec{SV}))| l_{3D} [cm]"
    ytitle  ["fourmumaxs3danglesvl3d"] = "Events / 0.1 cm"
    variable["fourmumaxs3danglesvl3d"] = "maxsina3dsvl3d"

    #

    nbins   ["fourmuupdetamindphimusvratio"] = 100
    low     ["fourmuupdetamindphimusvratio"] = -5
    high    ["fourmuupdetamindphimusvratio"] = 5
    xtitle  ["fourmuupdetamindphimusvratio"] = "log_{10}(|#Delta#eta(#mu, #mu), #vec{SV})|/min |#Delta#phi(#mu, #vec{SV})|)"
    ytitle  ["fourmuupdetamindphimusvratio"] = "Events / 0.1"
    variable["fourmuupdetamindphimusvratio"] = "ROOT.TMath.Log10(demmdpsvminu)"

    nbins   ["fourmuupmindetamindphimusvratio"] = 100
    low     ["fourmuupmindetamindphimusvratio"] = -5
    high    ["fourmuupmindetamindphimusvratio"] = 5
    xtitle  ["fourmuupmindetamindphimusvratio"] = "min log_{10}(|#Delta#eta(#mu, #mu), #vec{SV})|/min |#Delta#phi(#mu, #vec{SV})|)"
    ytitle  ["fourmuupmindetamindphimusvratio"] = "Events / 0.1"
    variable["fourmuupmindetamindphimusvratio"] = "ROOT.TMath.Log10(mindemmdpsvminu)"

    nbins   ["fourmuupmaxdetamindphimusvratio"] = 100
    low     ["fourmuupmaxdetamindphimusvratio"] = -5
    high    ["fourmuupmaxdetamindphimusvratio"] = 5
    xtitle  ["fourmuupmaxdetamindphimusvratio"] = "max log_{10}(|#Delta#eta(#mu, #mu), #vec{SV})|/min |#Delta#phi(#mu, #vec{SV})|)"
    ytitle  ["fourmuupmaxdetamindphimusvratio"] = "Events / 0.1"
    variable["fourmuupmaxdetamindphimusvratio"] = "ROOT.TMath.Log10(maxdemmdpsvminu)"

    nbins   ["fourmuupdetasvmindphimusvratio"] = 100
    low     ["fourmuupdetasvmindphimusvratio"] = -5
    high    ["fourmuupdetasvmindphimusvratio"] = 5
    xtitle  ["fourmuupdetasvmindphimusvratio"] = "log_{10}(|#Delta#eta(#vec{4#mu}, #vec{SV})|/min |#Delta#phi(#mu, #vec{SV})|)"
    ytitle  ["fourmuupdetasvmindphimusvratio"] = "Events / 0.1"
    variable["fourmuupdetasvmindphimusvratio"] = "ROOT.TMath.Log10(desvdpsvminu)"

    nbins   ["fourmuupmindetasvmindphimusvratio"] = 100
    low     ["fourmuupmindetasvmindphimusvratio"] = -5
    high    ["fourmuupmindetasvmindphimusvratio"] = 5
    xtitle  ["fourmuupmindetasvmindphimusvratio"] = "min log_{10}(|#Delta#eta(#vec{(#mu, #mu)}, #vec{SV})|/min |#Delta#phi(#mu, #vec{SV})|)"
    ytitle  ["fourmuupmindetasvmindphimusvratio"] = "Events / 0.1"
    variable["fourmuupmindetasvmindphimusvratio"] = "ROOT.TMath.Log10(mindesvdpsvminu)"

    nbins   ["fourmuupmaxdetasvmindphimusvratio"] = 100
    low     ["fourmuupmaxdetasvmindphimusvratio"] = -5
    high    ["fourmuupmaxdetasvmindphimusvratio"] = 5
    xtitle  ["fourmuupmaxdetasvmindphimusvratio"] = "max log_{10}(|#Delta#eta(#vec{(#mu, #mu)}, #vec{SV})|/min |#Delta#phi(#mu, #vec{SV})|)"
    ytitle  ["fourmuupmaxdetasvmindphimusvratio"] = "Events / 0.1"
    variable["fourmuupmaxdetasvmindphimusvratio"] = "ROOT.TMath.Log10(maxdesvdpsvminu)"

    nbins   ["fourmuupsdphisvlxy"] = 1100
    low     ["fourmuupsdphisvlxy"] = 0
    high    ["fourmuupsdphisvlxy"] = 110.0
    xtitle  ["fourmuupsdphisvlxy"] = "|sin (#Delta#phi(#vec{4#mu}, #vec{SV}))| l_{xy} [cm]"
    ytitle  ["fourmuupsdphisvlxy"] = "Events / 0.1 cm"
    variable["fourmuupsdphisvlxy"] = "sindpsvlxyu"

    nbins   ["fourmuupminsdphisvlxy"] = 1100
    low     ["fourmuupminsdphisvlxy"] = 0
    high    ["fourmuupminsdphisvlxy"] = 110.0
    xtitle  ["fourmuupminsdphisvlxy"] = "min |sin (#Delta#phi(#vec{(#mu, #mu)}, #vec{SV}))| l_{xy} [cm]"
    ytitle  ["fourmuupminsdphisvlxy"] = "Events / 0.1 cm"
    variable["fourmuupminsdphisvlxy"] = "minsindpsvlxyu"

    nbins   ["fourmuupmaxsdphisvlxy"] = 1100
    low     ["fourmuupmaxsdphisvlxy"] = 0
    high    ["fourmuupmaxsdphisvlxy"] = 110.0
    xtitle  ["fourmuupmaxsdphisvlxy"] = "max |sin (#Delta#phi(#vec{(#mu, #mu)}, #vec{SV}))| l_{xy} [cm]"
    ytitle  ["fourmuupmaxsdphisvlxy"] = "Events / 0.1 cm"
    variable["fourmuupmaxsdphisvlxy"] = "maxsindpsvlxyu"

    nbins   ["fourmuups3danglesvl3d"] = 1500
    low     ["fourmuups3danglesvl3d"] = 0
    high    ["fourmuups3danglesvl3d"] = 150.0
    xtitle  ["fourmuups3danglesvl3d"] = "|sin (3D angle(#vec{4#mu}, #vec{SV}))| l_{3D} [cm]"
    ytitle  ["fourmuups3danglesvl3d"] = "Events / 0.1 cm"
    variable["fourmuups3danglesvl3d"] = "sina3dsvl3du"

    nbins   ["fourmuupmins3danglesvl3d"] = 1500
    low     ["fourmuupmins3danglesvl3d"] = 0
    high    ["fourmuupmins3danglesvl3d"] = 150.0
    xtitle  ["fourmuupmins3danglesvl3d"] = "min |sin (3D angle(#vec{(#mu, #mu)}, #vec{SV}))| l_{3D} [cm]"
    ytitle  ["fourmuupmins3danglesvl3d"] = "Events / 0.1 cm"
    variable["fourmuupmins3danglesvl3d"] = "minsina3dsvl3du"

    nbins   ["fourmuupmaxs3danglesvl3d"] = 1500
    low     ["fourmuupmaxs3danglesvl3d"] = 0
    high    ["fourmuupmaxs3danglesvl3d"] = 150.0
    xtitle  ["fourmuupmaxs3danglesvl3d"] = "max |sin (3D angle(#vec{(#mu, #mu)}, #vec{SV}))| l_{3D} [cm]"
    ytitle  ["fourmuupmaxs3danglesvl3d"] = "Events / 0.1 cm"
    variable["fourmuupmaxs3danglesvl3d"] = "maxsina3dsvl3du"


# Histogram booking
### Add your histograms here

def histBooking(presel=True, dimuon=True, fourmuon=True, fourmuonosv=True):
    #
    histname = dict()
    histtype = dict()
    #
    histname2d = dict()
    histtype2d = dict()
    #
    ##
    # Event
    histname["event"] = []
    #
    histname["event"].append("hevent_npv")
    histtype[histname["event"][-1]]="npv"
    ##
    # Gen
    histname["jpsi"] = []
    #
    histname["jpsi"].append("hjpsi_lxy")
    histtype[histname["jpsi"][-1]]="jpsilxy"
    #
    histname["llp"] = []
    #
    histname["llp"].append("hllp_lxy")
    histtype[histname["llp"][-1]]="llplxy"
    #
    histname["genmu"] = []
    #
    histname["genmu"].append("hgenmu_pt")
    histtype[histname["genmu"][-1]]="genmupt"
    #
    ##
    # Displaced vertices
    histname["nsvsel"] = []
    histname["svsel"] = []
    histname2d["svsel"] = []
    if presel:
        #
        histname["nsvsel"].append("h_nsvsel")
        histtype[histname["nsvsel"][-1]]="nsv"
        #
        histname["svsel"].append("hsvsel_chi2ndof")
        histtype[histname["svsel"][-1]]="svchi2"
        #
        histname["svsel"].append("hsvsel_chi2prob")
        histtype[histname["svsel"][-1]]="svchi2prob"
        #
        histname["svsel"].append("hsvsel_xerr")
        histtype[histname["svsel"][-1]]="svxerr"
        #
        histname["svsel"].append("hsvsel_yerr")
        histtype[histname["svsel"][-1]]="svyerr"
        #
        histname["svsel"].append("hsvsel_zerr")
        histtype[histname["svsel"][-1]]="svzerr"
        #
        histname["svsel"].append("hsvsel_xsig")
        histtype[histname["svsel"][-1]]="svxsig"
        #
        histname["svsel"].append("hsvsel_ysig")
        histtype[histname["svsel"][-1]]="svysig"
        #
        histname["svsel"].append("hsvsel_zsig")
        histtype[histname["svsel"][-1]]="svzsig"
        #
        histname["svsel"].append("hsvsel_xpvsig")
        histtype[histname["svsel"][-1]]="svxpvsig"
        #
        histname["svsel"].append("hsvsel_ypvsig")
        histtype[histname["svsel"][-1]]="svypvsig"
        #
        histname["svsel"].append("hsvsel_zpvsig")
        histtype[histname["svsel"][-1]]="svzpvsig"
        #
        histname["svsel"].append("hsvsel_dxy")
        histtype[histname["svsel"][-1]]="svdxy"
        #
        histname["svsel"].append("hsvsel_d3d")
        histtype[histname["svsel"][-1]]="svd3d"
        #
        histname["svsel"].append("hsvsel_dxyerr")
        histtype[histname["svsel"][-1]]="svxyerr"
        #
        histname["svsel"].append("hsvsel_d3derr")
        histtype[histname["svsel"][-1]]="sv3derr"
        #
        histname["svsel"].append("hsvsel_dxysig")
        histtype[histname["svsel"][-1]]="svxysig"
        #
        histname["svsel"].append("hsvsel_d3dsig")
        histtype[histname["svsel"][-1]]="sv3dsig"
        #
        histname["svsel"].append("hsvsel_lxy")
        histtype[histname["svsel"][-1]]="lxy"
        #
        histname["svsel"].append("hsvsel_l3d")
        histtype[histname["svsel"][-1]]="l3d"
        #
        histname["svsel"].append("hsvsel_lxysig")
        histtype[histname["svsel"][-1]]="lxysig"
        #
        histname["svsel"].append("hsvsel_l3dsig")
        histtype[histname["svsel"][-1]]="l3dsig"
        #
        histname["svsel"].append("hsvsel_mindx")
        histtype[histname["svsel"][-1]]="mindx"
        #
        histname["svsel"].append("hsvsel_mindy")
        histtype[histname["svsel"][-1]]="mindy"
        #
        histname["svsel"].append("hsvsel_mindz")
        histtype[histname["svsel"][-1]]="mindz"
        #
        histname["svsel"].append("hsvsel_maxdx")
        histtype[histname["svsel"][-1]]="maxdx"
        #
        histname["svsel"].append("hsvsel_maxdy")
        histtype[histname["svsel"][-1]]="maxdy"
        #
        histname["svsel"].append("hsvsel_maxdz")
        histtype[histname["svsel"][-1]]="maxdz"
        #
        histname2d["svsel"].append("hsvsel_yvsx")
        histtype2d[histname2d["svsel"][-1]]="yvsx"
        #
        histname2d["svsel"].append("hsvsel_xerrvslxy")
        histtype2d[histname2d["svsel"][-1]]="xerrvslxy"
        #
        histname2d["svsel"].append("hsvsel_yerrvslxy")
        histtype2d[histname2d["svsel"][-1]]="yerrvslxy"
        #
        histname2d["svsel"].append("hsvsel_zerrvslxy")
        histtype2d[histname2d["svsel"][-1]]="zerrvslxy"
        #
        histname2d["svsel"].append("hsvsel_xerrvsz")
        histtype2d[histname2d["svsel"][-1]]="xerrvsz"
        #
        histname2d["svsel"].append("hsvsel_yerrvsz")
        histtype2d[histname2d["svsel"][-1]]="yerrvsz"
        #
        histname2d["svsel"].append("hsvsel_zerrvsz")
        histtype2d[histname2d["svsel"][-1]]="zerrvsz"
        #
        histname2d["svsel"].append("hsvsel_mindvslxy")
        histtype2d[histname2d["svsel"][-1]]="mindvslxy"
        #
        histname2d["svsel"].append("hsvsel_mindxyvslxy")
        histtype2d[histname2d["svsel"][-1]]="mindxyvslxy"
        #
    ##
    histname["nsvselass"] = []
    histname["svselass"] = []
    histname2d["svselass"] = []
    #
    histname["nsvselass_osv"] = []
    histname["svselass_osv"] = []
    histname2d["svselass_osv"] = []
    if dimuon:
        #
        #
        histname["nsvselass"].append("h_nsvselass")
        histtype[histname["nsvselass"][-1]]="nsv"
        #
        histname["svselass"].append("hsvselass_chi2ndof")
        histtype[histname["svselass"][-1]]="svchi2"
        #
        histname["svselass"].append("hsvselass_chi2prob")
        histtype[histname["svselass"][-1]]="svchi2prob"
        #
        histname["svselass"].append("hsvselass_xerr")
        histtype[histname["svselass"][-1]]="svxerr"
        #
        histname["svselass"].append("hsvselass_yerr")
        histtype[histname["svselass"][-1]]="svyerr"
        #
        histname["svselass"].append("hsvselass_zerr")
        histtype[histname["svselass"][-1]]="svzerr"
        #
        histname["svselass"].append("hsvselass_xsig")
        histtype[histname["svselass"][-1]]="svxsig"
        #
        histname["svselass"].append("hsvselass_ysig")
        histtype[histname["svselass"][-1]]="svysig"
        #
        histname["svselass"].append("hsvselass_zsig")
        histtype[histname["svselass"][-1]]="svzsig"
        #
        histname["svselass"].append("hsvselass_xpvsig")
        histtype[histname["svselass"][-1]]="svxpvsig"
        #
        histname["svselass"].append("hsvselass_ypvsig")
        histtype[histname["svselass"][-1]]="svypvsig"
        #
        histname["svselass"].append("hsvselass_zpvsig")
        histtype[histname["svselass"][-1]]="svzpvsig"
        #
        histname["svselass"].append("hsvselass_dxy")
        histtype[histname["svselass"][-1]]="svdxy"
        #
        histname["svselass"].append("hsvselass_d3d")
        histtype[histname["svselass"][-1]]="svd3d"
        #
        histname["svselass"].append("hsvselass_dxyerr")
        histtype[histname["svselass"][-1]]="svxyerr"
        #
        histname["svselass"].append("hsvselass_d3derr")
        histtype[histname["svselass"][-1]]="sv3derr"
        #
        histname["svselass"].append("hsvselass_dxysig")
        histtype[histname["svselass"][-1]]="svxysig"
        #
        histname["svselass"].append("hsvselass_d3dsig")
        histtype[histname["svselass"][-1]]="sv3dsig"
        #
        histname["svselass"].append("hsvselass_lxy")
        histtype[histname["svselass"][-1]]="lxy"
        #
        histname["svselass"].append("hsvselass_l3d")
        histtype[histname["svselass"][-1]]="l3d"
        #
        histname["svselass"].append("hsvselass_lxysig")
        histtype[histname["svselass"][-1]]="lxysig"
        #
        histname["svselass"].append("hsvselass_l3dsig")
        histtype[histname["svselass"][-1]]="l3dsig"
        #
        histname["svselass"].append("hsvselass_mindx")
        histtype[histname["svselass"][-1]]="mindx"
        #
        histname["svselass"].append("hsvselass_mindy")
        histtype[histname["svselass"][-1]]="mindy"
        #
        histname["svselass"].append("hsvselass_mindz")
        histtype[histname["svselass"][-1]]="mindz"
        #
        histname["svselass"].append("hsvselass_maxdx")
        histtype[histname["svselass"][-1]]="maxdx"
        #
        histname["svselass"].append("hsvselass_maxdy")
        histtype[histname["svselass"][-1]]="maxdy"
        #
        histname["svselass"].append("hsvselass_maxdz")
        histtype[histname["svselass"][-1]]="maxdz"
        #
        histname2d["svselass"].append("hsvselass_yvsx")
        histtype2d[histname2d["svselass"][-1]]="yvsx"
        #
        histname2d["svselass"].append("hsvselass_mindvslxy")
        histtype2d[histname2d["svselass"][-1]]="mindvslxy"
        #
        histname2d["svselass"].append("hsvselass_mindxyvslxy")
        histtype2d[histname2d["svselass"][-1]]="mindxyvslxy"
        #
        histname2d["svselass"].append("hsvselass_xerrvslxy")
        histtype2d[histname2d["svselass"][-1]]="xerrvslxy"
        #
        histname2d["svselass"].append("hsvselass_yerrvslxy")
        histtype2d[histname2d["svselass"][-1]]="yerrvslxy"
        #
        histname2d["svselass"].append("hsvselass_zerrvslxy")
        histtype2d[histname2d["svselass"][-1]]="zerrvslxy"
        #
        histname2d["svselass"].append("hsvselass_xerrvsz")
        histtype2d[histname2d["svselass"][-1]]="xerrvsz"
        #
        histname2d["svselass"].append("hsvselass_yerrvsz")
        histtype2d[histname2d["svselass"][-1]]="yerrvsz"
        #
        histname2d["svselass"].append("hsvselass_zerrvsz")
        histtype2d[histname2d["svselass"][-1]]="zerrvsz"
        #
        ##
        #
        histname["nsvselass_osv"].append("h_nsvselass_osv")
        histtype[histname["nsvselass_osv"][-1]]="nsv"
        #
        histname["svselass_osv"].append("hsvselass_osv_chi2ndof")
        histtype[histname["svselass_osv"][-1]]="svchi2"
        #
        histname["svselass_osv"].append("hsvselass_osv_chi2prob")
        histtype[histname["svselass_osv"][-1]]="svchi2prob"
        #
        histname["svselass_osv"].append("hsvselass_osv_xerr")
        histtype[histname["svselass_osv"][-1]]="svxerr"
        #
        histname["svselass_osv"].append("hsvselass_osv_yerr")
        histtype[histname["svselass_osv"][-1]]="svyerr"
        #
        histname["svselass_osv"].append("hsvselass_osv_zerr")
        histtype[histname["svselass_osv"][-1]]="svzerr"
        #
        histname["svselass_osv"].append("hsvselass_osv_xsig")
        histtype[histname["svselass_osv"][-1]]="svxsig"
        #
        histname["svselass_osv"].append("hsvselass_osv_ysig")
        histtype[histname["svselass_osv"][-1]]="svysig"
        #
        histname["svselass_osv"].append("hsvselass_osv_zsig")
        histtype[histname["svselass_osv"][-1]]="svzsig"
        #
        histname["svselass_osv"].append("hsvselass_osv_xpvsig")
        histtype[histname["svselass_osv"][-1]]="svxpvsig"
        #
        histname["svselass_osv"].append("hsvselass_osv_ypvsig")
        histtype[histname["svselass_osv"][-1]]="svypvsig"
        #
        histname["svselass_osv"].append("hsvselass_osv_zpvsig")
        histtype[histname["svselass_osv"][-1]]="svzpvsig"
        #
        histname["svselass_osv"].append("hsvselass_osv_dxy")
        histtype[histname["svselass_osv"][-1]]="svdxy"
        #
        histname["svselass_osv"].append("hsvselass_osv_d3d")
        histtype[histname["svselass_osv"][-1]]="svd3d"
        #
        histname["svselass_osv"].append("hsvselass_osv_dxyerr")
        histtype[histname["svselass_osv"][-1]]="svxyerr"
        #
        histname["svselass_osv"].append("hsvselass_osv_d3derr")
        histtype[histname["svselass_osv"][-1]]="sv3derr"
        #
        histname["svselass_osv"].append("hsvselass_osv_dxysig")
        histtype[histname["svselass_osv"][-1]]="svxysig"
        #
        histname["svselass_osv"].append("hsvselass_osv_d3dsig")
        histtype[histname["svselass_osv"][-1]]="sv3dsig"
        #
        histname["svselass_osv"].append("hsvselass_osv_lxy")
        histtype[histname["svselass_osv"][-1]]="lxy"
        #
        histname["svselass_osv"].append("hsvselass_osv_l3d")
        histtype[histname["svselass_osv"][-1]]="l3d"
        #
        histname["svselass_osv"].append("hsvselass_osv_lxysig")
        histtype[histname["svselass_osv"][-1]]="lxysig"
        #
        histname["svselass_osv"].append("hsvselass_osv_l3dsig")
        histtype[histname["svselass_osv"][-1]]="l3dsig"
        #
        histname["svselass_osv"].append("hsvselass_osv_mindx")
        histtype[histname["svselass_osv"][-1]]="mindx"
        #
        histname["svselass_osv"].append("hsvselass_osv_mindy")
        histtype[histname["svselass_osv"][-1]]="mindy"
        #
        histname["svselass_osv"].append("hsvselass_osv_mindz")
        histtype[histname["svselass_osv"][-1]]="mindz"
        #
        histname["svselass_osv"].append("hsvselass_osv_maxdx")
        histtype[histname["svselass_osv"][-1]]="maxdx"
        #
        histname["svselass_osv"].append("hsvselass_osv_maxdy")
        histtype[histname["svselass_osv"][-1]]="maxdy"
        #
        histname["svselass_osv"].append("hsvselass_osv_maxdz")
        histtype[histname["svselass_osv"][-1]]="maxdz"
        #
        histname2d["svselass_osv"].append("hsvselass_osv_yvsx")
        histtype2d[histname2d["svselass_osv"][-1]]="yvsx"
        #
        histname2d["svselass_osv"].append("hsvselass_osv_mindvslxy")
        histtype2d[histname2d["svselass_osv"][-1]]="mindvslxy"
        #
        histname2d["svselass_osv"].append("hsvselass_osv_mindxyvslxy")
        histtype2d[histname2d["svselass_osv"][-1]]="mindxyvslxy"
        #
    ##
    histname["nsvselass_fourmu"] = []
    histname["svselass_fourmu"] = []
    histname2d["svselass_fourmu"] = []
    if fourmuon:
        #
        histname["nsvselass_fourmu"].append("h_nsvselass_fourmu")
        histtype[histname["nsvselass_fourmu"][-1]]="nsv"
        #
        histname["svselass_fourmu"].append("hsvselass_fourmu_chi2ndof")
        histtype[histname["svselass_fourmu"][-1]]="svchi2"
        #
        histname["svselass_fourmu"].append("hsvselass_fourmu_chi2prob")
        histtype[histname["svselass_fourmu"][-1]]="svchi2prob"
        #
        histname["svselass_fourmu"].append("hsvselass_fourmu_xerr")
        histtype[histname["svselass_fourmu"][-1]]="svxerr"
        #
        histname["svselass_fourmu"].append("hsvselass_fourmu_yerr")
        histtype[histname["svselass_fourmu"][-1]]="svyerr"
        #
        histname["svselass_fourmu"].append("hsvselass_fourmu_zerr")
        histtype[histname["svselass_fourmu"][-1]]="svzerr"
        #
        histname["svselass_fourmu"].append("hsvselass_fourmu_xsig")
        histtype[histname["svselass_fourmu"][-1]]="svxsig"
        #
        histname["svselass_fourmu"].append("hsvselass_fourmu_ysig")
        histtype[histname["svselass_fourmu"][-1]]="svysig"
        #
        histname["svselass_fourmu"].append("hsvselass_fourmu_zsig")
        histtype[histname["svselass_fourmu"][-1]]="svzsig"
        #
        histname["svselass_fourmu"].append("hsvselass_fourmu_xpvsig")
        histtype[histname["svselass_fourmu"][-1]]="svxpvsig"
        #
        histname["svselass_fourmu"].append("hsvselass_fourmu_ypvsig")
        histtype[histname["svselass_fourmu"][-1]]="svypvsig"
        #
        histname["svselass_fourmu"].append("hsvselass_fourmu_zpvsig")
        histtype[histname["svselass_fourmu"][-1]]="svzpvsig"
        #
        histname["svselass_fourmu"].append("hsvselass_fourmu_dxy")
        histtype[histname["svselass_fourmu"][-1]]="svdxy"
        #
        histname["svselass_fourmu"].append("hsvselass_fourmu_d3d")
        histtype[histname["svselass_fourmu"][-1]]="svd3d"
        #
        histname["svselass_fourmu"].append("hsvselass_fourmu_dxyerr")
        histtype[histname["svselass_fourmu"][-1]]="svxyerr"
        #
        histname["svselass_fourmu"].append("hsvselass_fourmu_d3derr")
        histtype[histname["svselass_fourmu"][-1]]="sv3derr"
        #
        histname["svselass_fourmu"].append("hsvselass_fourmu_dxysig")
        histtype[histname["svselass_fourmu"][-1]]="svxysig"
        #
        histname["svselass_fourmu"].append("hsvselass_fourmu_d3dsig")
        histtype[histname["svselass_fourmu"][-1]]="sv3dsig"
        #
        histname["svselass_fourmu"].append("hsvselass_fourmu_lxy")
        histtype[histname["svselass_fourmu"][-1]]="lxy"
        #
        histname["svselass_fourmu"].append("hsvselass_fourmu_l3d")
        histtype[histname["svselass_fourmu"][-1]]="l3d"
        #
        histname["svselass_fourmu"].append("hsvselass_fourmu_lxysig")
        histtype[histname["svselass_fourmu"][-1]]="lxysig"
        #
        histname["svselass_fourmu"].append("hsvselass_fourmu_l3dsig")
        histtype[histname["svselass_fourmu"][-1]]="l3dsig"
        #
        histname["svselass_fourmu"].append("hsvselass_fourmu_mindx")
        histtype[histname["svselass_fourmu"][-1]]="mindx"
        #
        histname["svselass_fourmu"].append("hsvselass_fourmu_mindy")
        histtype[histname["svselass_fourmu"][-1]]="mindy"
        #
        histname["svselass_fourmu"].append("hsvselass_fourmu_mindz")
        histtype[histname["svselass_fourmu"][-1]]="mindz"
        #
        histname["svselass_fourmu"].append("hsvselass_fourmu_maxdx")
        histtype[histname["svselass_fourmu"][-1]]="maxdx"
        #
        histname["svselass_fourmu"].append("hsvselass_fourmu_maxdy")
        histtype[histname["svselass_fourmu"][-1]]="maxdy"
        #
        histname["svselass_fourmu"].append("hsvselass_fourmu_maxdz")
        histtype[histname["svselass_fourmu"][-1]]="maxdz"
        #
        histname2d["svselass_fourmu"].append("hsvselass_fourmu_yvsx")
        histtype2d[histname2d["svselass_fourmu"][-1]]="yvsx"
        #
    ##
    histname["nsvselass_fourmu_osv"] = []
    histname["svselass_fourmu_osv"] = []
    histname2d["svselass_fourmu_osv"] = []
    if fourmuonosv:
        #
        histname["nsvselass_fourmu_osv"].append("h_nsvselass_fourmu_osv")
        histtype[histname["nsvselass_fourmu_osv"][-1]]="nsv"
        #
        histname["svselass_fourmu_osv"].append("hsvselass_fourmu_osv_chi2ndof")
        histtype[histname["svselass_fourmu_osv"][-1]]="svchi2"
        #
        histname["svselass_fourmu_osv"].append("hsvselass_fourmu_osv_chi2prob")
        histtype[histname["svselass_fourmu_osv"][-1]]="svchi2prob"
        #
        histname["svselass_fourmu_osv"].append("hsvselass_fourmu_osv_xerr")
        histtype[histname["svselass_fourmu_osv"][-1]]="svxerr"
        #
        histname["svselass_fourmu_osv"].append("hsvselass_fourmu_osv_yerr")
        histtype[histname["svselass_fourmu_osv"][-1]]="svyerr"
        #
        histname["svselass_fourmu_osv"].append("hsvselass_fourmu_osv_zerr")
        histtype[histname["svselass_fourmu_osv"][-1]]="svzerr"
        #
        histname["svselass_fourmu_osv"].append("hsvselass_fourmu_osv_xsig")
        histtype[histname["svselass_fourmu_osv"][-1]]="svxsig"
        #
        histname["svselass_fourmu_osv"].append("hsvselass_fourmu_osv_ysig")
        histtype[histname["svselass_fourmu_osv"][-1]]="svysig"
        #
        histname["svselass_fourmu_osv"].append("hsvselass_fourmu_osv_zsig")
        histtype[histname["svselass_fourmu_osv"][-1]]="svzsig"
        #
        histname["svselass_fourmu_osv"].append("hsvselass_fourmu_osv_xpvsig")
        histtype[histname["svselass_fourmu_osv"][-1]]="svxpvsig"
        #
        histname["svselass_fourmu_osv"].append("hsvselass_fourmu_osv_ypvsig")
        histtype[histname["svselass_fourmu_osv"][-1]]="svypvsig"
        #
        histname["svselass_fourmu_osv"].append("hsvselass_fourmu_osv_zpvsig")
        histtype[histname["svselass_fourmu_osv"][-1]]="svzpvsig"
        #
        histname["svselass_fourmu_osv"].append("hsvselass_fourmu_osv_dxy")
        histtype[histname["svselass_fourmu_osv"][-1]]="svdxy"
        #
        histname["svselass_fourmu_osv"].append("hsvselass_fourmu_osv_d3d")
        histtype[histname["svselass_fourmu_osv"][-1]]="svd3d"
        #
        histname["svselass_fourmu_osv"].append("hsvselass_fourmu_osv_dxyerr")
        histtype[histname["svselass_fourmu_osv"][-1]]="svxyerr"
        #
        histname["svselass_fourmu_osv"].append("hsvselass_fourmu_osv_d3derr")
        histtype[histname["svselass_fourmu_osv"][-1]]="sv3derr"
        #
        histname["svselass_fourmu_osv"].append("hsvselass_fourmu_osv_dxysig")
        histtype[histname["svselass_fourmu_osv"][-1]]="svxysig"
        #
        histname["svselass_fourmu_osv"].append("hsvselass_fourmu_osv_d3dsig")
        histtype[histname["svselass_fourmu_osv"][-1]]="sv3dsig"
        #
        histname["svselass_fourmu_osv"].append("hsvselass_fourmu_osv_lxy")
        histtype[histname["svselass_fourmu_osv"][-1]]="lxy"
        #
        histname["svselass_fourmu_osv"].append("hsvselass_fourmu_osv_l3d")
        histtype[histname["svselass_fourmu_osv"][-1]]="l3d"
        #
        histname["svselass_fourmu_osv"].append("hsvselass_fourmu_osv_lxysig")
        histtype[histname["svselass_fourmu_osv"][-1]]="lxysig"
        #
        histname["svselass_fourmu_osv"].append("hsvselass_fourmu_osv_l3dsig")
        histtype[histname["svselass_fourmu_osv"][-1]]="l3dsig"
        #
        histname["svselass_fourmu_osv"].append("hsvselass_fourmu_osv_mindx")
        histtype[histname["svselass_fourmu_osv"][-1]]="mindx"
        #
        histname["svselass_fourmu_osv"].append("hsvselass_fourmu_osv_mindy")
        histtype[histname["svselass_fourmu_osv"][-1]]="mindy"
        #
        histname["svselass_fourmu_osv"].append("hsvselass_fourmu_osv_mindz")
        histtype[histname["svselass_fourmu_osv"][-1]]="mindz"
        #
        histname["svselass_fourmu_osv"].append("hsvselass_fourmu_osv_maxdx")
        histtype[histname["svselass_fourmu_osv"][-1]]="maxdx"
        #
        histname["svselass_fourmu_osv"].append("hsvselass_fourmu_osv_maxdy")
        histtype[histname["svselass_fourmu_osv"][-1]]="maxdy"
        #
        histname["svselass_fourmu_osv"].append("hsvselass_fourmu_osv_maxdz")
        histtype[histname["svselass_fourmu_osv"][-1]]="maxdz"
        #
        histname2d["svselass_fourmu_osv"].append("hsvselass_fourmu_osv_yvsx")
        histtype2d[histname2d["svselass_fourmu_osv"][-1]]="yvsx"
        #
    ##
    # Muons
    histname["nmuon"] = []
    histname["muon"] = []
    histname2d["muon"] = []
    if presel:
        #
        histname["nmuon"].append("h_nmuonssel")
        histtype[histname["nmuon"][-1]]="nmusel"
        #
        histname["nmuon"].append("h_nmuonsass")
        histtype[histname["nmuon"][-1]]="nmusv"
        #
        histname["nmuon"].append("h_nmuonsassoverlap")
        histtype[histname["nmuon"][-1]]="nmuosv"
        #
        histname["muon"].append("hmuon_pt")
        histtype[histname["muon"][-1]]="mupt"
        #
        histname["muon"].append("hmuon_eta")
        histtype[histname["muon"][-1]]="mueta"
        #
        histname["muon"].append("hmuon_phi")
        histtype[histname["muon"][-1]]="muphi"
        #
        histname["muon"].append("hmuon_uphi")
        histtype[histname["muon"][-1]]="muuphi"
        #
        histname["muon"].append("hmuon_ch")
        histtype[histname["muon"][-1]]="much"
        #
        histname["muon"].append("hmuon_mindr")
        histtype[histname["muon"][-1]]="mumindr"
        #
        histname["muon"].append("hmuon_maxdr")
        histtype[histname["muon"][-1]]="mumaxdr"
        #
        histname["muon"].append("hmuon_chi2ndof")
        histtype[histname["muon"][-1]]="muchi2ndof"
        #
        histname["muon"].append("hmuon_type")
        histtype[histname["muon"][-1]]="mutype"
        #
        histname["muon"].append("hmuon_ecaliso")
        histtype[histname["muon"][-1]]="muecaliso"
        #
        histname["muon"].append("hmuon_ecalreliso")
        histtype[histname["muon"][-1]]="muecalreliso"
        #
        histname["muon"].append("hmuon_hcaliso")
        histtype[histname["muon"][-1]]="muhcaliso"
        #
        histname["muon"].append("hmuon_hcalreliso")
        histtype[histname["muon"][-1]]="muhcalreliso"
        #
        histname["muon"].append("hmuon_trackiso")
        histtype[histname["muon"][-1]]="mutrkiso"
        #
        histname["muon"].append("hmuon_trackreliso")
        histtype[histname["muon"][-1]]="mutrkreliso"
        #
        histname["muon"].append("hmuon_pfiso0p3all")
        histtype[histname["muon"][-1]]="mupfalliso0p3"
        #
        histname["muon"].append("hmuon_pfreliso0p3all")
        histtype[histname["muon"][-1]]="mupfallreliso0p3"
        #
        histname["muon"].append("hmuon_pfiso0p3chg")
        histtype[histname["muon"][-1]]="mupfchgiso0p3"
        #
        histname["muon"].append("hmuon_pfreliso0p3chg")
        histtype[histname["muon"][-1]]="mupfchgreliso0p3"
        #
        histname["muon"].append("hmuon_pfiso0p4all")
        histtype[histname["muon"][-1]]="mupfalliso0p4"
        #
        histname["muon"].append("hmuon_pfreliso0p4all")
        histtype[histname["muon"][-1]]="mupfallreliso0p4"
        #
        histname["muon"].append("hmuon_pfiso0p4chg")
        histtype[histname["muon"][-1]]="mupfchgiso0p4"
        #
        histname["muon"].append("hmuon_pfreliso0p4chg")
        histtype[histname["muon"][-1]]="mupfchgreliso0p4"
        #
        histname2d["muon"].append("hmuon_pfiso0p4allvspt")
        histtype2d[histname2d["muon"][-1]]="pfisovspt"
        #
        histname["muon"].append("hmuon_mindrjet")
        histtype[histname["muon"][-1]]="mumindrjet"
        #
        histname["muon"].append("hmuon_dphimindrjet")
        histtype[histname["muon"][-1]]="mumindpjet"
        #
        histname["muon"].append("hmuon_detamindrjet")
        histtype[histname["muon"][-1]]="mumindejet"
        #
        histname["muon"].append("hmuon_mindrpfc")
        histtype[histname["muon"][-1]]="mumindrpfc"
        #
        histname["muon"].append("hmuon_dxy")
        histtype[histname["muon"][-1]]="mudxy"
        #
        histname["muon"].append("hmuon_dxysig")
        histtype[histname["muon"][-1]]="mudxysig"
        #
        histname["muon"].append("hmuon_dz")
        histtype[histname["muon"][-1]]="mudz"
        #
        histname["muon"].append("hmuon_dzsig")
        histtype[histname["muon"][-1]]="mudzsig"
        #
        histname["muon"].append("hmuon_nsahits")
        histtype[histname["muon"][-1]]="musahits"
        #
        histname["muon"].append("hmuon_nsamatchedstats")
        histtype[histname["muon"][-1]]="musamatchedstats"
        #
        histname["muon"].append("hmuon_nmuhits")
        histtype[histname["muon"][-1]]="muhits"
        #
        histname["muon"].append("hmuon_nmuchambs")
        histtype[histname["muon"][-1]]="muchambs"
        #
        histname["muon"].append("hmuon_nmuCSCorDT")
        histtype[histname["muon"][-1]]="mucscdt"
        #
        histname["muon"].append("hmuon_nmumatches")
        histtype[histname["muon"][-1]]="mumatches"
        #
        histname["muon"].append("hmuon_nmumatchedstats")
        histtype[histname["muon"][-1]]="mumatchedstats"
        #
        histname["muon"].append("hmuon_nmuexpmatchedstats")
        histtype[histname["muon"][-1]]="muexpmatchedstats"
        #
        histname["muon"].append("hmuon_nmumatchedstatsmexp")
        histtype[histname["muon"][-1]]="mumatchedstatsmexp"
        #
        histname["muon"].append("hmuon_nmumatchedRPC")
        histtype[histname["muon"][-1]]="mumatchedrpc"
        #
        histname["muon"].append("hmuon_npixelhits")
        histtype[histname["muon"][-1]]="mupixelhits"
        #
        histname["muon"].append("hmuon_npixellayers")
        histtype[histname["muon"][-1]]="mupixellayers"
        #
        histname["muon"].append("hmuon_nstriphits")
        histtype[histname["muon"][-1]]="mustriphits"
        #
        histname["muon"].append("hmuon_ntrackerlayers")
        histtype[histname["muon"][-1]]="mutrackerlayers"
        #
        histname["muon"].append("hmuon_nhitsbeforesv")
        histtype[histname["muon"][-1]]="muhitsbeforesv"
        #
        histname["muon"].append("hmuon_nobsmexplayers")
        histtype[histname["muon"][-1]]="muobsmexplayers"
        #
        histname["muon"].append("hmuon_nobsmexppixellayers")
        histtype[histname["muon"][-1]]="muobsmexppixlayers"
        #
        histname["muon"].append("hmuon_nobsmexphits")
        histtype[histname["muon"][-1]]="muobsmexphits"
        #
        histname["muon"].append("hmuon_nobsmexppixelhits")
        histtype[histname["muon"][-1]]="muobsmexppixhits"
        #
    ##
    histname["selmuon"] = []
    histname2d["selmuon"] = []
    histname["selmuon_osv"] = []
    histname2d["selmuon_osv"] = []
    if dimuon:
        #
        histname["selmuon"].append("hselmuon_pt")
        histtype[histname["selmuon"][-1]]="mupt"
        #
        histname["selmuon"].append("hselmuon_eta")
        histtype[histname["selmuon"][-1]]="mueta"
        #
        histname["selmuon"].append("hselmuon_phi")
        histtype[histname["selmuon"][-1]]="muphi"
        #
        histname["selmuon"].append("hselmuon_uphi")
        histtype[histname["selmuon"][-1]]="muuphi"
        #
        histname["selmuon"].append("hselmuon_ch")
        histtype[histname["selmuon"][-1]]="much"
        #
        histname["selmuon"].append("hselmuon_mindr")
        histtype[histname["selmuon"][-1]]="mumindr"
        #
        histname["selmuon"].append("hselmuon_maxdr")
        histtype[histname["selmuon"][-1]]="mumaxdr"
        #
        histname["selmuon"].append("hselmuon_chi2ndof")
        histtype[histname["selmuon"][-1]]="muchi2ndof"
        #
        histname["selmuon"].append("hselmuon_type")
        histtype[histname["selmuon"][-1]]="mutype"
        #
        histname["selmuon"].append("hselmuon_ecaliso")
        histtype[histname["selmuon"][-1]]="muecaliso"
        #
        histname["selmuon"].append("hselmuon_ecalreliso")
        histtype[histname["selmuon"][-1]]="muecalreliso"
        #
        histname["selmuon"].append("hselmuon_hcaliso")
        histtype[histname["selmuon"][-1]]="muhcaliso"
        #
        histname["selmuon"].append("hselmuon_hcalreliso")
        histtype[histname["selmuon"][-1]]="muhcalreliso"
        #
        histname["selmuon"].append("hselmuon_trackiso")
        histtype[histname["selmuon"][-1]]="mutrkiso"
        #
        histname["selmuon"].append("hselmuon_trackreliso")
        histtype[histname["selmuon"][-1]]="mutrkreliso"
        #
        histname["selmuon"].append("hselmuon_pfiso0p3all")
        histtype[histname["selmuon"][-1]]="mupfalliso0p3"
        #
        histname["selmuon"].append("hselmuon_pfreliso0p3all")
        histtype[histname["selmuon"][-1]]="mupfallreliso0p3"
        #
        histname["selmuon"].append("hselmuon_pfiso0p3chg")
        histtype[histname["selmuon"][-1]]="mupfchgiso0p3"
        #
        histname["selmuon"].append("hselmuon_pfreliso0p3chg")
        histtype[histname["selmuon"][-1]]="mupfchgreliso0p3"
        #
        histname["selmuon"].append("hselmuon_pfiso0p4all")
        histtype[histname["selmuon"][-1]]="mupfalliso0p4"
        #
        histname["selmuon"].append("hselmuon_pfreliso0p4all")
        histtype[histname["selmuon"][-1]]="mupfallreliso0p4"
        #
        histname["selmuon"].append("hselmuon_pfiso0p4chg")
        histtype[histname["selmuon"][-1]]="mupfchgiso0p4"
        #
        histname["selmuon"].append("hselmuon_pfreliso0p4chg")
        histtype[histname["selmuon"][-1]]="mupfchgreliso0p4"
        #
        histname2d["selmuon"].append("hselmuon_pfiso0p4allvspt")
        histtype2d[histname2d["selmuon"][-1]]="pfisovspt"
        #
        histname["selmuon"].append("hselmuon_mindrjet")
        histtype[histname["selmuon"][-1]]="mumindrjet"
        #
        histname["selmuon"].append("hselmuon_dphimindrjet")
        histtype[histname["selmuon"][-1]]="mumindpjet"
        #
        histname["selmuon"].append("hselmuon_detamindrjet")
        histtype[histname["selmuon"][-1]]="mumindejet"
        #
        histname["selmuon"].append("hselmuon_mindrpfc")
        histtype[histname["selmuon"][-1]]="mumindrpfc"
        #
        histname["selmuon"].append("hselmuon_dxy")
        histtype[histname["selmuon"][-1]]="mudxy"
        #
        histname["selmuon"].append("hselmuon_dxysigned")
        histtype[histname["selmuon"][-1]]="mudxysigned"
        #
        histname["selmuon"].append("hselmuon_dxysig")
        histtype[histname["selmuon"][-1]]="mudxysig"
        #
        histname["selmuon"].append("hselmuon_dxyscaled")
        histtype[histname["selmuon"][-1]]="mudxyscaled"
        #
        histname["selmuon"].append("hselmuon_dz")
        histtype[histname["selmuon"][-1]]="mudz"
        #
        histname["selmuon"].append("hselmuon_dzsig")
        histtype[histname["selmuon"][-1]]="mudzsig"
        #
        histname["selmuon"].append("hselmuon_nsahits")
        histtype[histname["selmuon"][-1]]="musahits"
        #
        histname["selmuon"].append("hselmuon_nsamatchedstats")
        histtype[histname["selmuon"][-1]]="musamatchedstats"
        #
        histname["selmuon"].append("hselmuon_nmuhits")
        histtype[histname["selmuon"][-1]]="muhits"
        #
        histname["selmuon"].append("hselmuon_nmuchambs")
        histtype[histname["selmuon"][-1]]="muchambs"
        #
        histname["selmuon"].append("hselmuon_nmuCSCorDT")
        histtype[histname["selmuon"][-1]]="mucscdt"
        #
        histname["selmuon"].append("hselmuon_nmumatches")
        histtype[histname["selmuon"][-1]]="mumatches"
        #
        histname["selmuon"].append("hselmuon_nmumatchedstats")
        histtype[histname["selmuon"][-1]]="mumatchedstats"
        #
        histname["selmuon"].append("hselmuon_nmuexpmatchedstats")
        histtype[histname["selmuon"][-1]]="muexpmatchedstats"
        #
        histname["selmuon"].append("hselmuon_nmumatchedstatsmexp")
        histtype[histname["selmuon"][-1]]="mumatchedstatsmexp"
        #
        histname["selmuon"].append("hselmuon_nmumatchedRPC")
        histtype[histname["selmuon"][-1]]="mumatchedrpc"
        #
        histname["selmuon"].append("hselmuon_npixelhits")
        histtype[histname["selmuon"][-1]]="mupixelhits"
        #
        histname["selmuon"].append("hselmuon_npixellayers")
        histtype[histname["selmuon"][-1]]="mupixellayers"
        #
        histname["selmuon"].append("hselmuon_nstriphits")
        histtype[histname["selmuon"][-1]]="mustriphits"
        #
        histname["selmuon"].append("hselmuon_ntrackerlayers")
        histtype[histname["selmuon"][-1]]="mutrackerlayers"
        #
        histname["selmuon"].append("hselmuon_nhitsbeforesv")
        histtype[histname["selmuon"][-1]]="muhitsbeforesv"
        #
        histname["selmuon"].append("hselmuon_nobsmexplayers")
        histtype[histname["selmuon"][-1]]="muobsmexplayers"
        #
        histname["selmuon"].append("hselmuon_nobsmexppixellayers")
        histtype[histname["selmuon"][-1]]="muobsmexppixlayers"
        #
        histname["selmuon"].append("hselmuon_nobsmexphits")
        histtype[histname["selmuon"][-1]]="muobsmexphits"
        #
        histname["selmuon"].append("hselmuon_nobsmexppixelhits")
        histtype[histname["selmuon"][-1]]="muobsmexppixhits"
        #
        histname["selmuon"].append("hselmuon_dphisv")
        histtype[histname["selmuon"][-1]]="mudphisv"
        #
        histname["selmuon"].append("hselmuon_uphi_dphisv")
        histtype[histname["selmuon"][-1]]="mudphisvu"
        #
        histname["selmuon"].append("hselmuon_mudphimm")
        histtype[histname["selmuon"][-1]]="mudphimm"
        #
        histname["selmuon"].append("hselmuon_uphi_mudphimm")
        histtype[histname["selmuon"][-1]]="mudphimmu"
        #
        histname["selmuon"].append("hselmuon_mutheta")
        histtype[histname["selmuon"][-1]]="mutheta"
        #
        histname["selmuon"].append("hselmuon_uphi_mutheta")
        histtype[histname["selmuon"][-1]]="muthetau"
        #
        histname["selmuon"].append("hselmuon_muthetamm")
        histtype[histname["selmuon"][-1]]="muthetamm"
        #
        histname["selmuon"].append("hselmuon_uphi_muthetamm")
        histtype[histname["selmuon"][-1]]="muthetammu"
        #
        ##
        #
        histname["selmuon_osv"].append("hselmuon_osv_pt")
        histtype[histname["selmuon_osv"][-1]]="mupt"
        #
        histname["selmuon_osv"].append("hselmuon_osv_eta")
        histtype[histname["selmuon_osv"][-1]]="mueta"
        #
        histname["selmuon_osv"].append("hselmuon_osv_phi")
        histtype[histname["selmuon_osv"][-1]]="muphi"
        #
        histname["selmuon_osv"].append("hselmuon_osv_ch")
        histtype[histname["selmuon_osv"][-1]]="much"
        #
        histname["selmuon_osv"].append("hselmuon_osv_mindr")
        histtype[histname["selmuon_osv"][-1]]="mumindr"
        #
        histname["selmuon_osv"].append("hselmuon_osv_maxdr")
        histtype[histname["selmuon_osv"][-1]]="mumaxdr"
        #
        histname["selmuon_osv"].append("hselmuon_osv_chi2ndof")
        histtype[histname["selmuon_osv"][-1]]="muchi2ndof"
        #
        histname["selmuon_osv"].append("hselmuon_osv_type")
        histtype[histname["selmuon_osv"][-1]]="mutype"
        #
        histname["selmuon_osv"].append("hselmuon_osv_ecaliso")
        histtype[histname["selmuon_osv"][-1]]="muecaliso"
        #
        histname["selmuon_osv"].append("hselmuon_osv_ecalreliso")
        histtype[histname["selmuon_osv"][-1]]="muecalreliso"
        #
        histname["selmuon_osv"].append("hselmuon_osv_hcaliso")
        histtype[histname["selmuon_osv"][-1]]="muhcaliso"
        #
        histname["selmuon_osv"].append("hselmuon_osv_hcalreliso")
        histtype[histname["selmuon_osv"][-1]]="muhcalreliso"
        #
        histname["selmuon_osv"].append("hselmuon_osv_trackiso")
        histtype[histname["selmuon_osv"][-1]]="mutrkiso"
        #
        histname["selmuon_osv"].append("hselmuon_osv_trackreliso")
        histtype[histname["selmuon_osv"][-1]]="mutrkreliso"
        #
        histname["selmuon_osv"].append("hselmuon_osv_pfiso0p3all")
        histtype[histname["selmuon_osv"][-1]]="mupfalliso0p3"
        #
        histname["selmuon_osv"].append("hselmuon_osv_pfreliso0p3all")
        histtype[histname["selmuon_osv"][-1]]="mupfallreliso0p3"
        #
        histname["selmuon_osv"].append("hselmuon_osv_pfiso0p3chg")
        histtype[histname["selmuon_osv"][-1]]="mupfchgiso0p3"
        #
        histname["selmuon_osv"].append("hselmuon_osv_pfreliso0p3chg")
        histtype[histname["selmuon_osv"][-1]]="mupfchgreliso0p3"
        #
        histname["selmuon_osv"].append("hselmuon_osv_pfiso0p4all")
        histtype[histname["selmuon_osv"][-1]]="mupfalliso0p4"
        #
        histname["selmuon_osv"].append("hselmuon_osv_pfreliso0p4all")
        histtype[histname["selmuon_osv"][-1]]="mupfallreliso0p4"
        #
        histname["selmuon_osv"].append("hselmuon_osv_pfiso0p4chg")
        histtype[histname["selmuon_osv"][-1]]="mupfchgiso0p4"
        #
        histname["selmuon_osv"].append("hselmuon_osv_pfreliso0p4chg")
        histtype[histname["selmuon_osv"][-1]]="mupfchgreliso0p4"
        #
        histname2d["selmuon_osv"].append("hselmuon_osv_pfiso0p4allvspt")
        histtype2d[histname2d["selmuon_osv"][-1]]="pfisovspt"
        #
        histname["selmuon_osv"].append("hselmuon_osv_mindrjet")
        histtype[histname["selmuon_osv"][-1]]="mumindrjet"
        #
        histname["selmuon_osv"].append("hselmuon_osv_dphimindrjet")
        histtype[histname["selmuon_osv"][-1]]="mumindpjet"
        #
        histname["selmuon_osv"].append("hselmuon_osv_detamindrjet")
        histtype[histname["selmuon_osv"][-1]]="mumindejet"
        #
        histname["selmuon_osv"].append("hselmuon_osv_mindrpfc")
        histtype[histname["selmuon_osv"][-1]]="mumindrpfc"
        #
        histname["selmuon_osv"].append("hselmuon_osv_dxy")
        histtype[histname["selmuon_osv"][-1]]="mudxy"
        #
        histname["selmuon_osv"].append("hselmuon_osv_dxysigned")
        histtype[histname["selmuon_osv"][-1]]="mudxysigned"
        #
        histname["selmuon_osv"].append("hselmuon_osv_dxysig")
        histtype[histname["selmuon_osv"][-1]]="mudxysig"
        #
        histname["selmuon_osv"].append("hselmuon_osv_dxyscaled")
        histtype[histname["selmuon_osv"][-1]]="mudxyscaled"
        #
        histname["selmuon_osv"].append("hselmuon_osv_dz")
        histtype[histname["selmuon_osv"][-1]]="mudz"
        #
        histname["selmuon_osv"].append("hselmuon_osv_dzsig")
        histtype[histname["selmuon_osv"][-1]]="mudzsig"
        #
        histname["selmuon_osv"].append("hselmuon_osv_nsahits")
        histtype[histname["selmuon_osv"][-1]]="musahits"
        #
        histname["selmuon_osv"].append("hselmuon_osv_nsamatchedstats")
        histtype[histname["selmuon_osv"][-1]]="musamatchedstats"
        #
        histname["selmuon_osv"].append("hselmuon_osv_nmuhits")
        histtype[histname["selmuon_osv"][-1]]="muhits"
        #
        histname["selmuon_osv"].append("hselmuon_osv_nmuchambs")
        histtype[histname["selmuon_osv"][-1]]="muchambs"
        #
        histname["selmuon_osv"].append("hselmuon_osv_nmuCSCorDT")
        histtype[histname["selmuon_osv"][-1]]="mucscdt"
        #
        histname["selmuon_osv"].append("hselmuon_osv_nmumatches")
        histtype[histname["selmuon_osv"][-1]]="mumatches"
        #
        histname["selmuon_osv"].append("hselmuon_osv_nmumatchedstats")
        histtype[histname["selmuon_osv"][-1]]="mumatchedstats"
        #
        histname["selmuon_osv"].append("hselmuon_osv_nmuexpmatchedstats")
        histtype[histname["selmuon_osv"][-1]]="muexpmatchedstats"
        #
        histname["selmuon_osv"].append("hselmuon_osv_nmumatchedstatsmexp")
        histtype[histname["selmuon_osv"][-1]]="mumatchedstatsmexp"
        #
        histname["selmuon_osv"].append("hselmuon_osv_nmumatchedRPC")
        histtype[histname["selmuon_osv"][-1]]="mumatchedrpc"
        #
        histname["selmuon_osv"].append("hselmuon_osv_npixelhits")
        histtype[histname["selmuon_osv"][-1]]="mupixelhits"
        #
        histname["selmuon_osv"].append("hselmuon_osv_npixellayers")
        histtype[histname["selmuon_osv"][-1]]="mupixellayers"
        #
        histname["selmuon_osv"].append("hselmuon_osv_nstriphits")
        histtype[histname["selmuon_osv"][-1]]="mustriphits"
        #
        histname["selmuon_osv"].append("hselmuon_osv_ntrackerlayers")
        histtype[histname["selmuon_osv"][-1]]="mutrackerlayers"
        #
        histname["selmuon_osv"].append("hselmuon_osv_nhitsbeforesv")
        histtype[histname["selmuon_osv"][-1]]="muhitsbeforesv"
        #
        histname["selmuon_osv"].append("hselmuon_osv_nobsmexplayers")
        histtype[histname["selmuon_osv"][-1]]="muobsmexplayers"
        #
        histname["selmuon_osv"].append("hselmuon_osv_nobsmexppixellayers")
        histtype[histname["selmuon_osv"][-1]]="muobsmexppixlayers"
        #
        histname["selmuon_osv"].append("hselmuon_osv_nobsmexphits")
        histtype[histname["selmuon_osv"][-1]]="muobsmexphits"
        #
        histname["selmuon_osv"].append("hselmuon_osv_nobsmexppixelhits")
        histtype[histname["selmuon_osv"][-1]]="muobsmexppixhits"
        #
        histname["selmuon_osv"].append("hselmuon_osv_dphisv")
        histtype[histname["selmuon_osv"][-1]]="mudphisv"
        #
        histname["selmuon_osv"].append("hselmuon_osv_uphi_dphisv")
        histtype[histname["selmuon_osv"][-1]]="mudphisvu"
        #
        histname["selmuon_osv"].append("hselmuon_osv_mudphimm")
        histtype[histname["selmuon_osv"][-1]]="mudphimm"
        #
        histname["selmuon_osv"].append("hselmuon_osv_uphi_mudphimm")
        histtype[histname["selmuon_osv"][-1]]="mudphimmu"
        #
        histname["selmuon_osv"].append("hselmuon_osv_mutheta")
        histtype[histname["selmuon_osv"][-1]]="mutheta"
        #
        histname["selmuon_osv"].append("hselmuon_osv_uphi_mutheta")
        histtype[histname["selmuon_osv"][-1]]="muthetau"
        #
        histname["selmuon_osv"].append("hselmuon_osv_muthetamm")
        histtype[histname["selmuon_osv"][-1]]="muthetamm"
        #
        histname["selmuon_osv"].append("hselmuon_osv_uphi_muthetamm")
        histtype[histname["selmuon_osv"][-1]]="muthetammu"
        #
    ##
    histname["selmuon_fourmu"] = []
    histname2d["selmuon_fourmu"] = []
    if fourmuon:
        #
        histname["selmuon_fourmu"].append("hselmuon_fourmu_pt")
        histtype[histname["selmuon_fourmu"][-1]]="mupt"
        #
        histname["selmuon_fourmu"].append("hselmuon_fourmu_eta")
        histtype[histname["selmuon_fourmu"][-1]]="mueta"
        #
        histname["selmuon_fourmu"].append("hselmuon_fourmu_phi")
        histtype[histname["selmuon_fourmu"][-1]]="muphi"
        #
        histname["selmuon_fourmu"].append("hselmuon_fourmu_uphi")
        histtype[histname["selmuon_fourmu"][-1]]="muuphi"
        #
        histname["selmuon_fourmu"].append("hselmuon_fourmu_ch")
        histtype[histname["selmuon_fourmu"][-1]]="much"
        #
        histname["selmuon_fourmu"].append("hselmuon_fourmu_mindr")
        histtype[histname["selmuon_fourmu"][-1]]="mumindr"
        #
        histname["selmuon_fourmu"].append("hselmuon_fourmu_maxdr")
        histtype[histname["selmuon_fourmu"][-1]]="mumaxdr"
        #
        histname["selmuon_fourmu"].append("hselmuon_fourmu_chi2ndof")
        histtype[histname["selmuon_fourmu"][-1]]="muchi2ndof"
        #
        histname["selmuon_fourmu"].append("hselmuon_fourmu_type")
        histtype[histname["selmuon_fourmu"][-1]]="mutype"
        #
        histname["selmuon_fourmu"].append("hselmuon_fourmu_ecaliso")
        histtype[histname["selmuon_fourmu"][-1]]="muecaliso"
        #
        histname["selmuon_fourmu"].append("hselmuon_fourmu_ecalreliso")
        histtype[histname["selmuon_fourmu"][-1]]="muecalreliso"
        #
        histname["selmuon_fourmu"].append("hselmuon_fourmu_hcaliso")
        histtype[histname["selmuon_fourmu"][-1]]="muhcaliso"
        #
        histname["selmuon_fourmu"].append("hselmuon_fourmu_hcalreliso")
        histtype[histname["selmuon_fourmu"][-1]]="muhcalreliso"
        #
        histname["selmuon_fourmu"].append("hselmuon_fourmu_trackiso")
        histtype[histname["selmuon_fourmu"][-1]]="mutrkiso"
        #
        histname["selmuon_fourmu"].append("hselmuon_fourmu_trackreliso")
        histtype[histname["selmuon_fourmu"][-1]]="mutrkreliso"
        #
        histname["selmuon_fourmu"].append("hselmuon_fourmu_pfiso0p3all")
        histtype[histname["selmuon_fourmu"][-1]]="mupfalliso0p3"
        #
        histname["selmuon_fourmu"].append("hselmuon_fourmu_pfreliso0p3all")
        histtype[histname["selmuon_fourmu"][-1]]="mupfallreliso0p3"
        #
        histname["selmuon_fourmu"].append("hselmuon_fourmu_pfiso0p3chg")
        histtype[histname["selmuon_fourmu"][-1]]="mupfchgiso0p3"
        #
        histname["selmuon_fourmu"].append("hselmuon_fourmu_pfreliso0p3chg")
        histtype[histname["selmuon_fourmu"][-1]]="mupfchgreliso0p3"
        #
        histname["selmuon_fourmu"].append("hselmuon_fourmu_pfiso0p4all")
        histtype[histname["selmuon_fourmu"][-1]]="mupfalliso0p4"
        #
        histname["selmuon_fourmu"].append("hselmuon_fourmu_pfreliso0p4all")
        histtype[histname["selmuon_fourmu"][-1]]="mupfallreliso0p4"
        #
        histname["selmuon_fourmu"].append("hselmuon_fourmu_pfiso0p4chg")
        histtype[histname["selmuon_fourmu"][-1]]="mupfchgiso0p4"
        #
        histname["selmuon_fourmu"].append("hselmuon_fourmu_pfreliso0p4chg")
        histtype[histname["selmuon_fourmu"][-1]]="mupfchgreliso0p4"
        #
        histname["selmuon_fourmu"].append("hselmuon_fourmu_mindrjet")
        histtype[histname["selmuon_fourmu"][-1]]="mumindrjet"
        #
        histname["selmuon_fourmu"].append("hselmuon_fourmu_dphimindrjet")
        histtype[histname["selmuon_fourmu"][-1]]="mumindpjet"
        #
        histname["selmuon_fourmu"].append("hselmuon_fourmu_detamindrjet")
        histtype[histname["selmuon_fourmu"][-1]]="mumindejet"
        #
        histname["selmuon_fourmu"].append("hselmuon_fourmu_mindrpfc")
        histtype[histname["selmuon_fourmu"][-1]]="mumindrpfc"
        #
        histname["selmuon_fourmu"].append("hselmuon_fourmu_dxy")
        histtype[histname["selmuon_fourmu"][-1]]="mudxy"
        #
        histname["selmuon_fourmu"].append("hselmuon_fourmu_dxysig")
        histtype[histname["selmuon_fourmu"][-1]]="mudxysig"
        #
        histname["selmuon_fourmu"].append("hselmuon_fourmu_dxyscaled")
        histtype[histname["selmuon_fourmu"][-1]]="mudxyscaled"
        #
        histname["selmuon_fourmu"].append("hselmuon_fourmu_dz")
        histtype[histname["selmuon_fourmu"][-1]]="mudz"
        #
        histname["selmuon_fourmu"].append("hselmuon_fourmu_dzsig")
        histtype[histname["selmuon_fourmu"][-1]]="mudzsig"
        #
        histname["selmuon_fourmu"].append("hselmuon_fourmu_nsahits")
        histtype[histname["selmuon_fourmu"][-1]]="musahits"
        #
        histname["selmuon_fourmu"].append("hselmuon_fourmu_nsamatchedstats")
        histtype[histname["selmuon_fourmu"][-1]]="musamatchedstats"
        #
        histname["selmuon_fourmu"].append("hselmuon_fourmu_nmuhits")
        histtype[histname["selmuon_fourmu"][-1]]="muhits"
        #
        histname["selmuon_fourmu"].append("hselmuon_fourmu_nmuchambs")
        histtype[histname["selmuon_fourmu"][-1]]="muchambs"
        #
        histname["selmuon_fourmu"].append("hselmuon_fourmu_nmuCSCorDT")
        histtype[histname["selmuon_fourmu"][-1]]="mucscdt"
        #
        histname["selmuon_fourmu"].append("hselmuon_fourmu_nmumatches")
        histtype[histname["selmuon_fourmu"][-1]]="mumatches"
        #
        histname["selmuon_fourmu"].append("hselmuon_fourmu_nmumatchedstats")
        histtype[histname["selmuon_fourmu"][-1]]="mumatchedstats"
        #
        histname["selmuon_fourmu"].append("hselmuon_fourmu_nmuexpmatchedstats")
        histtype[histname["selmuon_fourmu"][-1]]="muexpmatchedstats"
        #
        histname["selmuon_fourmu"].append("hselmuon_fourmu_nmumatchedstatsmexp")
        histtype[histname["selmuon_fourmu"][-1]]="mumatchedstatsmexp"
        #
        histname["selmuon_fourmu"].append("hselmuon_fourmu_nmumatchedRPC")
        histtype[histname["selmuon_fourmu"][-1]]="mumatchedrpc"
        #
        histname["selmuon_fourmu"].append("hselmuon_fourmu_npixelhits")
        histtype[histname["selmuon_fourmu"][-1]]="mupixelhits"
        #
        histname["selmuon_fourmu"].append("hselmuon_fourmu_npixellayers")
        histtype[histname["selmuon_fourmu"][-1]]="mupixellayers"
        #
        histname["selmuon_fourmu"].append("hselmuon_fourmu_nstriphits")
        histtype[histname["selmuon_fourmu"][-1]]="mustriphits"
        #
        histname["selmuon_fourmu"].append("hselmuon_fourmu_ntrackerlayers")
        histtype[histname["selmuon_fourmu"][-1]]="mutrackerlayers"
        #
        histname["selmuon_fourmu"].append("hselmuon_fourmu_nhitsbeforesv")
        histtype[histname["selmuon_fourmu"][-1]]="muhitsbeforesv"
        #
    ##
    histname["selmuon_fourmu_osv"] = []
    histname2d["selmuon_fourmu_osv"] = []
    if fourmuonosv:
        #
        histname["selmuon_fourmu_osv"].append("hselmuon_fourmu_osv_pt")
        histtype[histname["selmuon_fourmu_osv"][-1]]="mupt"
        #
        histname["selmuon_fourmu_osv"].append("hselmuon_fourmu_osv_eta")
        histtype[histname["selmuon_fourmu_osv"][-1]]="mueta"
        #
        histname["selmuon_fourmu_osv"].append("hselmuon_fourmu_osv_phi")
        histtype[histname["selmuon_fourmu_osv"][-1]]="muphi"
        #
        histname["selmuon_fourmu_osv"].append("hselmuon_fourmu_osv_uphi")
        histtype[histname["selmuon_fourmu_osv"][-1]]="muuphi"
        #
        histname["selmuon_fourmu_osv"].append("hselmuon_fourmu_osv_ch")
        histtype[histname["selmuon_fourmu_osv"][-1]]="much"
        #
        histname["selmuon_fourmu_osv"].append("hselmuon_fourmu_osv_mindr")
        histtype[histname["selmuon_fourmu_osv"][-1]]="mumindr"
        #
        histname["selmuon_fourmu_osv"].append("hselmuon_fourmu_osv_maxdr")
        histtype[histname["selmuon_fourmu_osv"][-1]]="mumaxdr"
        #
        histname["selmuon_fourmu_osv"].append("hselmuon_fourmu_osv_chi2ndof")
        histtype[histname["selmuon_fourmu_osv"][-1]]="muchi2ndof"
        #
        histname["selmuon_fourmu_osv"].append("hselmuon_fourmu_osv_type")
        histtype[histname["selmuon_fourmu_osv"][-1]]="mutype"
        #
        histname["selmuon_fourmu_osv"].append("hselmuon_fourmu_osv_ecaliso")
        histtype[histname["selmuon_fourmu_osv"][-1]]="muecaliso"
        #
        histname["selmuon_fourmu_osv"].append("hselmuon_fourmu_osv_ecalreliso")
        histtype[histname["selmuon_fourmu_osv"][-1]]="muecalreliso"
        #
        histname["selmuon_fourmu_osv"].append("hselmuon_fourmu_osv_hcaliso")
        histtype[histname["selmuon_fourmu_osv"][-1]]="muhcaliso"
        #
        histname["selmuon_fourmu_osv"].append("hselmuon_fourmu_osv_hcalreliso")
        histtype[histname["selmuon_fourmu_osv"][-1]]="muhcalreliso"
        #
        histname["selmuon_fourmu_osv"].append("hselmuon_fourmu_osv_trackiso")
        histtype[histname["selmuon_fourmu_osv"][-1]]="mutrkiso"
        #
        histname["selmuon_fourmu_osv"].append("hselmuon_fourmu_osv_trackreliso")
        histtype[histname["selmuon_fourmu_osv"][-1]]="mutrkreliso"
        #
        histname["selmuon_fourmu_osv"].append("hselmuon_fourmu_osv_pfiso0p3all")
        histtype[histname["selmuon_fourmu_osv"][-1]]="mupfalliso0p3"
        #
        histname["selmuon_fourmu_osv"].append("hselmuon_fourmu_osv_pfreliso0p3all")
        histtype[histname["selmuon_fourmu_osv"][-1]]="mupfallreliso0p3"
        #
        histname["selmuon_fourmu_osv"].append("hselmuon_fourmu_osv_pfiso0p3chg")
        histtype[histname["selmuon_fourmu_osv"][-1]]="mupfchgiso0p3"
        #
        histname["selmuon_fourmu_osv"].append("hselmuon_fourmu_osv_pfreliso0p3chg")
        histtype[histname["selmuon_fourmu_osv"][-1]]="mupfchgreliso0p3"
        #
        histname["selmuon_fourmu_osv"].append("hselmuon_fourmu_osv_pfiso0p4all")
        histtype[histname["selmuon_fourmu_osv"][-1]]="mupfalliso0p4"
        #
        histname["selmuon_fourmu_osv"].append("hselmuon_fourmu_osv_pfreliso0p4all")
        histtype[histname["selmuon_fourmu_osv"][-1]]="mupfallreliso0p4"
        #
        histname["selmuon_fourmu_osv"].append("hselmuon_fourmu_osv_pfiso0p4chg")
        histtype[histname["selmuon_fourmu_osv"][-1]]="mupfchgiso0p4"
        #
        histname["selmuon_fourmu_osv"].append("hselmuon_fourmu_osv_pfreliso0p4chg")
        histtype[histname["selmuon_fourmu_osv"][-1]]="mupfchgreliso0p4"
        #
        histname["selmuon_fourmu_osv"].append("hselmuon_fourmu_osv_mindrjet")
        histtype[histname["selmuon_fourmu_osv"][-1]]="mumindrjet"
        #
        histname["selmuon_fourmu_osv"].append("hselmuon_fourmu_osv_dphimindrjet")
        histtype[histname["selmuon_fourmu_osv"][-1]]="mumindpjet"
        #
        histname["selmuon_fourmu_osv"].append("hselmuon_fourmu_osv_detamindrjet")
        histtype[histname["selmuon_fourmu_osv"][-1]]="mumindejet"
        #
        histname["selmuon_fourmu_osv"].append("hselmuon_fourmu_osv_mindrpfc")
        histtype[histname["selmuon_fourmu_osv"][-1]]="mumindrpfc"
        #
        histname["selmuon_fourmu_osv"].append("hselmuon_fourmu_osv_dxy")
        histtype[histname["selmuon_fourmu_osv"][-1]]="mudxy"
        #
        histname["selmuon_fourmu_osv"].append("hselmuon_fourmu_osv_dxysig")
        histtype[histname["selmuon_fourmu_osv"][-1]]="mudxysig"
        #
        histname["selmuon_fourmu_osv"].append("hselmuon_fourmu_osv_dxyscaled")
        histtype[histname["selmuon_fourmu_osv"][-1]]="mudxyscaled"
        #
        histname["selmuon_fourmu_osv"].append("hselmuon_fourmu_osv_dz")
        histtype[histname["selmuon_fourmu_osv"][-1]]="mudz"
        #
        histname["selmuon_fourmu_osv"].append("hselmuon_fourmu_osv_dzsig")
        histtype[histname["selmuon_fourmu_osv"][-1]]="mudzsig"
        #
        histname["selmuon_fourmu_osv"].append("hselmuon_fourmu_osv_nsahits")
        histtype[histname["selmuon_fourmu_osv"][-1]]="musahits"
        #
        histname["selmuon_fourmu_osv"].append("hselmuon_fourmu_osv_nsamatchedstats")
        histtype[histname["selmuon_fourmu_osv"][-1]]="musamatchedstats"
        #
        histname["selmuon_fourmu_osv"].append("hselmuon_fourmu_osv_nmuhits")
        histtype[histname["selmuon_fourmu_osv"][-1]]="muhits"
        #
        histname["selmuon_fourmu_osv"].append("hselmuon_fourmu_osv_nmuchambs")
        histtype[histname["selmuon_fourmu_osv"][-1]]="muchambs"
        #
        histname["selmuon_fourmu_osv"].append("hselmuon_fourmu_osv_nmuCSCorDT")
        histtype[histname["selmuon_fourmu_osv"][-1]]="mucscdt"
        #
        histname["selmuon_fourmu_osv"].append("hselmuon_fourmu_osv_nmumatches")
        histtype[histname["selmuon_fourmu_osv"][-1]]="mumatches"
        #
        histname["selmuon_fourmu_osv"].append("hselmuon_fourmu_osv_nmumatchedstats")
        histtype[histname["selmuon_fourmu_osv"][-1]]="mumatchedstats"
        #
        histname["selmuon_fourmu_osv"].append("hselmuon_fourmu_osv_nmuexpmatchedstats")
        histtype[histname["selmuon_fourmu_osv"][-1]]="muexpmatchedstats"
        #
        histname["selmuon_fourmu_osv"].append("hselmuon_fourmu_osv_nmumatchedstatsmexp")
        histtype[histname["selmuon_fourmu_osv"][-1]]="mumatchedstatsmexp"
        #
        histname["selmuon_fourmu_osv"].append("hselmuon_fourmu_osv_nmumatchedRPC")
        histtype[histname["selmuon_fourmu_osv"][-1]]="mumatchedrpc"
        #
        histname["selmuon_fourmu_osv"].append("hselmuon_fourmu_osv_npixelhits")
        histtype[histname["selmuon_fourmu_osv"][-1]]="mupixelhits"
        #
        histname["selmuon_fourmu_osv"].append("hselmuon_fourmu_osv_npixellayers")
        histtype[histname["selmuon_fourmu_osv"][-1]]="mupixellayers"
        #
        histname["selmuon_fourmu_osv"].append("hselmuon_fourmu_osv_nstriphits")
        histtype[histname["selmuon_fourmu_osv"][-1]]="mustriphits"
        #
        histname["selmuon_fourmu_osv"].append("hselmuon_fourmu_osv_ntrackerlayers")
        histtype[histname["selmuon_fourmu_osv"][-1]]="mutrackerlayers"
        #
    ##
    # Di-muon
    histname["dimuon"] = []
    histname2d["dimuon"] = []
    histname["dimuon_osv"] = []
    histname2d["dimuon_osv"] = []
    if dimuon:
        #
        histname["dimuon"].append("hdimuon_mass")
        histtype[histname["dimuon"][-1]]="dimumass"
        #
        histname["dimuon"].append("hdimuon_pt")
        histtype[histname["dimuon"][-1]]="dimupt"
        #
        histname["dimuon"].append("hdimuon_lxy")
        histtype[histname["dimuon"][-1]]="lxy"
        #
        histname["dimuon"].append("hdimuon_dr")
        histtype[histname["dimuon"][-1]]="dimudr"
        #
        histname["dimuon"].append("hdimuon_dphi")
        histtype[histname["dimuon"][-1]]="dimudphi"
        #
        histname["dimuon"].append("hdimuon_deta")
        histtype[histname["dimuon"][-1]]="dimudeta"
        #
        histname["dimuon"].append("hdimuon_detadphiratio")
        histtype[histname["dimuon"][-1]]="dimudetadphiratio"
        #
        histname["dimuon"].append("hdimuon_3dangle")
        histtype[histname["dimuon"][-1]]="dimu3dangle"
        #
        histname["dimuon"].append("hdimuon_dphisv")
        histtype[histname["dimuon"][-1]]="dimudphisv"
        #
        histname["dimuon"].append("hdimuon_detasv")
        histtype[histname["dimuon"][-1]]="dimudetasv"
        #
        histname["dimuon"].append("hdimuon_detadphisvratio")
        histtype[histname["dimuon"][-1]]="dimudetadphisvratio"
        #
        histname["dimuon"].append("hdimuon_3danglesv")
        histtype[histname["dimuon"][-1]]="dimu3danglesv"
        #
        histname["dimuon"].append("hdimuon_uphi_dr")
        histtype[histname["dimuon"][-1]]="dimuupdr"
        #
        histname["dimuon"].append("hdimuon_uphi_dphi")
        histtype[histname["dimuon"][-1]]="dimuupdphi"
        #
        histname["dimuon"].append("hdimuon_uphi_deta")
        histtype[histname["dimuon"][-1]]="dimuupdeta"
        #
        histname["dimuon"].append("hdimuon_uphi_detadphiratio")
        histtype[histname["dimuon"][-1]]="dimuupdetadphiratio"
        #
        histname["dimuon"].append("hdimuon_uphi_3dangle")
        histtype[histname["dimuon"][-1]]="dimuup3dangle"
        #
        histname["dimuon"].append("hdimuon_uphi_dphisv")
        histtype[histname["dimuon"][-1]]="dimuupdphisv"
        #
        histname["dimuon"].append("hdimuon_uphi_detasv")
        histtype[histname["dimuon"][-1]]="dimuupdetasv"
        #
        histname["dimuon"].append("hdimuon_uphi_detadphisvratio")
        histtype[histname["dimuon"][-1]]="dimuupdetadphisvratio"
        #
        histname["dimuon"].append("hdimuon_uphi_3danglesv")
        histtype[histname["dimuon"][-1]]="dimuup3danglesv"
        #
        histname["dimuon"].append("hdimuon_detamindphimusvratio")
        histtype[histname["dimuon"][-1]]="dimudetamindphimusvratio"
        #
        histname["dimuon"].append("hdimuon_detasvmindphimusvratio")
        histtype[histname["dimuon"][-1]]="dimudetasvmindphimusvratio"
        #
        histname["dimuon"].append("hdimuon_sdphisvlxy")
        histtype[histname["dimuon"][-1]]="dimusdphisvlxy"
        #
        histname["dimuon"].append("hdimuon_s3danglesvl3d")
        histtype[histname["dimuon"][-1]]="dimus3danglesvl3d"
        #
        histname["dimuon"].append("hdimuon_uphi_detamindphimusvratio")
        histtype[histname["dimuon"][-1]]="dimuupdetamindphimusvratio"
        #
        histname["dimuon"].append("hdimuon_uphi_detasvmindphimusvratio")
        histtype[histname["dimuon"][-1]]="dimuupdetasvmindphimusvratio"
        #
        histname["dimuon"].append("hdimuon_uphi_sdphisvlxy")
        histtype[histname["dimuon"][-1]]="dimuupsdphisvlxy"
        #
        histname["dimuon"].append("hdimuon_uphi_s3danglesvl3d")
        histtype[histname["dimuon"][-1]]="dimuups3danglesvl3d"
        #
        histname["dimuon"].append("hdimuon_hitsbeforesv")
        histtype[histname["dimuon"][-1]]="totalmuhitsbeforesv"
        #
        histname["dimuon"].append("hdimuon_isocategory")
        histtype[histname["dimuon"][-1]]="dimuisocat"
        #
        histname["dimuon"].append("hdimuon_isgenmatched")
        histtype[histname["dimuon"][-1]]="isgen"
        #
        histname["dimuon"].append("hdimuon_genmatchdr")
        histtype[histname["dimuon"][-1]]="dimugenmatchingdr"
        #
        histname["dimuon"].append("hdimuon_gen_genlxy")
        histtype[histname["dimuon"][-1]]="llplxy"
        #
        histname["dimuon"].append("hdimuon_gen_recolxy")
        histtype[histname["dimuon"][-1]]="lxy"
        #
        histname["dimuon"].append("hdimuon_gen_deltalxy")
        histtype[histname["dimuon"][-1]]="deltalxy"
        #
        histname["dimuon"].append("hdimuon_gen_recomass")
        histtype[histname["dimuon"][-1]]="dimumass"
        #
        histname["dimuon"].append("hdimuon_genjpsi_genlxy")
        histtype[histname["dimuon"][-1]]="jpsilxy"
        #
        histname["dimuon"].append("hdimuon_genjpsi_recolxy")
        histtype[histname["dimuon"][-1]]="lxy"
        #
        histname["dimuon"].append("hdimuon_genjpsi_recomass")
        histtype[histname["dimuon"][-1]]="dimumass"
        #
        histname2d["dimuon"].append("hdimuon_gen_lxycomp")
        histtype2d[histname2d["dimuon"][-1]]="lxyvslxygen"
        #
        histname2d["dimuon"].append("hdimuon_genjpsi_lxycomp")
        histtype2d[histname2d["dimuon"][-1]]="lxyvslxygen"
        #
        histname["dimuon"].append("hdimuon_umass")
        histtype[histname["dimuon"][-1]]="dimuumass"
        #
        histname["dimuon"].append("hdimuon_cowboy")
        histtype[histname["dimuon"][-1]]="cowboyumass"
        #
        histname["dimuon"].append("hdimuon_seagull")
        histtype[histname["dimuon"][-1]]="seagullumass"
        ##
        # Di-muon from overlapping SV
        #
        #
        histname["dimuon_osv"].append("hdimuon_osv_mass")
        histtype[histname["dimuon_osv"][-1]]="dimumass"
        #
        histname["dimuon_osv"].append("hdimuon_osv_pt")
        histtype[histname["dimuon_osv"][-1]]="dimupt"
        #
        histname["dimuon_osv"].append("hdimuon_osv_lxy")
        histtype[histname["dimuon_osv"][-1]]="lxy"
        #
        histname["dimuon_osv"].append("hdimuon_osv_dr")
        histtype[histname["dimuon_osv"][-1]]="dimudr"
        #
        histname["dimuon_osv"].append("hdimuon_osv_dphi")
        histtype[histname["dimuon_osv"][-1]]="dimudphi"
        #
        histname["dimuon_osv"].append("hdimuon_osv_deta")
        histtype[histname["dimuon_osv"][-1]]="dimudeta"
        #
        histname["dimuon_osv"].append("hdimuon_osv_detadphiratio")
        histtype[histname["dimuon_osv"][-1]]="dimudetadphiratio"
        #
        histname["dimuon_osv"].append("hdimuon_osv_3dangle")
        histtype[histname["dimuon_osv"][-1]]="dimu3dangle"
        #
        histname["dimuon_osv"].append("hdimuon_osv_dphisv")
        histtype[histname["dimuon_osv"][-1]]="dimudphisv"
        #
        histname["dimuon_osv"].append("hdimuon_osv_detasv")
        histtype[histname["dimuon_osv"][-1]]="dimudetasv"
        #
        histname["dimuon_osv"].append("hdimuon_osv_detadphisvratio")
        histtype[histname["dimuon_osv"][-1]]="dimudetadphisvratio"
        #
        histname["dimuon_osv"].append("hdimuon_osv_3danglesv")
        histtype[histname["dimuon_osv"][-1]]="dimu3danglesv"
        #
        histname["dimuon_osv"].append("hdimuon_osv_uphi_dr")
        histtype[histname["dimuon_osv"][-1]]="dimuupdr"
        #
        histname["dimuon_osv"].append("hdimuon_osv_uphi_dphi")
        histtype[histname["dimuon_osv"][-1]]="dimuupdphi"
        #
        histname["dimuon_osv"].append("hdimuon_osv_uphi_deta")
        histtype[histname["dimuon_osv"][-1]]="dimuupdeta"
        #
        histname["dimuon_osv"].append("hdimuon_osv_uphi_detadphiratio")
        histtype[histname["dimuon_osv"][-1]]="dimuupdetadphiratio"
        #
        histname["dimuon_osv"].append("hdimuon_osv_uphi_3dangle")
        histtype[histname["dimuon_osv"][-1]]="dimuup3dangle"
        #
        histname["dimuon_osv"].append("hdimuon_osv_uphi_dphisv")
        histtype[histname["dimuon_osv"][-1]]="dimuupdphisv"
        #
        histname["dimuon_osv"].append("hdimuon_osv_uphi_detasv")
        histtype[histname["dimuon_osv"][-1]]="dimuupdetasv"
        #
        histname["dimuon_osv"].append("hdimuon_osv_uphi_detadphisvratio")
        histtype[histname["dimuon_osv"][-1]]="dimuupdetadphisvratio"
        #
        histname["dimuon_osv"].append("hdimuon_osv_uphi_3danglesv")
        histtype[histname["dimuon_osv"][-1]]="dimuup3danglesv"
        #
        histname["dimuon_osv"].append("hdimuon_osv_detamindphimusvratio")
        histtype[histname["dimuon_osv"][-1]]="dimudetamindphimusvratio"
        #
        histname["dimuon_osv"].append("hdimuon_osv_detasvmindphimusvratio")
        histtype[histname["dimuon_osv"][-1]]="dimudetasvmindphimusvratio"
        #
        histname["dimuon_osv"].append("hdimuon_osv_sdphisvlxy")
        histtype[histname["dimuon_osv"][-1]]="dimusdphisvlxy"
        #
        histname["dimuon_osv"].append("hdimuon_osv_s3danglesvl3d")
        histtype[histname["dimuon_osv"][-1]]="dimus3danglesvl3d"
        #
        histname["dimuon_osv"].append("hdimuon_osv_uphi_detamindphimusvratio")
        histtype[histname["dimuon_osv"][-1]]="dimuupdetamindphimusvratio"
        #
        histname["dimuon_osv"].append("hdimuon_osv_uphi_detasvmindphimusvratio")
        histtype[histname["dimuon_osv"][-1]]="dimuupdetasvmindphimusvratio"
        #
        histname["dimuon_osv"].append("hdimuon_osv_uphi_sdphisvlxy")
        histtype[histname["dimuon_osv"][-1]]="dimuupsdphisvlxy"
        #
        histname["dimuon_osv"].append("hdimuon_osv_uphi_s3danglesvl3d")
        histtype[histname["dimuon_osv"][-1]]="dimuups3danglesvl3d"
        #
        histname["dimuon_osv"].append("hdimuon_osv_hitsbeforesv")
        histtype[histname["dimuon_osv"][-1]]="totalmuhitsbeforesv"
        #
        histname["dimuon_osv"].append("hdimuon_osv_isocategory")
        histtype[histname["dimuon_osv"][-1]]="dimuisocat"
        #
        histname["dimuon_osv"].append("hdimuon_osv_isgenmatched")
        histtype[histname["dimuon_osv"][-1]]="isgen"
        #
        histname["dimuon_osv"].append("hdimuon_osv_genmatchdr")
        histtype[histname["dimuon_osv"][-1]]="dimugenmatchingdr"
        #
        histname["dimuon_osv"].append("hdimuon_gen_osv_lxy")
        histtype[histname["dimuon_osv"][-1]]="llplxy"
        #
        histname2d["dimuon_osv"].append("hdimuon_gen_osv_lxycomp")
        histtype2d[histname2d["dimuon_osv"][-1]]="lxyvslxygen"
        #
        histname["dimuon_osv"].append("hdimuon_genjpsi_osv_lxy")
        histtype[histname["dimuon_osv"][-1]]="jpsilxy"
        #
        histname2d["dimuon_osv"].append("hdimuon_genjpsi_osv_lxycomp")
        histtype2d[histname2d["dimuon_osv"][-1]]="lxyvslxygen"
        #

    ##
    # Four-muon from overlapping SV
    histname["fourmuon_osv"] = []
    histname2d["fourmuon_osv"] = []
    if fourmuonosv:
        #
        histname["fourmuon_osv"].append("hfourmuon_osv_mass")
        histtype[histname["fourmuon_osv"][-1]]="fourmumass"
        #
        histname["fourmuon_osv"].append("hfourmuon_osv_pt")
        histtype[histname["fourmuon_osv"][-1]]="fourmupt"
        #
        histname["fourmuon_osv"].append("hfourmuon_osv_lxy")
        histtype[histname["fourmuon_osv"][-1]]="lxy"
        #
        histname["fourmuon_osv"].append("hfourmuon_osv_mindr")
        histtype[histname["fourmuon_osv"][-1]]="fourmumindr"
        #
        histname["fourmuon_osv"].append("hfourmuon_osv_maxdr")
        histtype[histname["fourmuon_osv"][-1]]="fourmumaxdr"
        #
        histname["fourmuon_osv"].append("hfourmuon_osv_mindphi")
        histtype[histname["fourmuon_osv"][-1]]="fourmumindphi"
        #
        histname["fourmuon_osv"].append("hfourmuon_osv_maxdphi")
        histtype[histname["fourmuon_osv"][-1]]="fourmumaxdphi"
        #
        histname["fourmuon_osv"].append("hfourmuon_osv_mindeta")
        histtype[histname["fourmuon_osv"][-1]]="fourmumindeta"
        #
        histname["fourmuon_osv"].append("hfourmuon_osv_maxdeta")
        histtype[histname["fourmuon_osv"][-1]]="fourmumaxdeta"
        #
        histname["fourmuon_osv"].append("hfourmuon_osv_mindetadphiratio")
        histtype[histname["fourmuon_osv"][-1]]="fourmumindetadphiratio"
        #
        histname["fourmuon_osv"].append("hfourmuon_osv_maxdetadphiratio")
        histtype[histname["fourmuon_osv"][-1]]="fourmumaxdetadphiratio"
        #
        histname["fourmuon_osv"].append("hfourmuon_osv_min3dangle")
        histtype[histname["fourmuon_osv"][-1]]="fourmumin3dangle"
        #
        histname["fourmuon_osv"].append("hfourmuon_osv_max3dangle")
        histtype[histname["fourmuon_osv"][-1]]="fourmumax3dangle"
        #
        histname["fourmuon_osv"].append("hfourmuon_osv_dphisv")
        histtype[histname["fourmuon_osv"][-1]]="fourmudphisv"
        #
        histname["fourmuon_osv"].append("hfourmuon_osv_detasv")
        histtype[histname["fourmuon_osv"][-1]]="fourmudetasv"
        #
        histname["fourmuon_osv"].append("hfourmuon_osv_detadphisvratio")
        histtype[histname["fourmuon_osv"][-1]]="fourmudetadphisvratio"
        #
        histname["fourmuon_osv"].append("hfourmuon_osv_3danglesv")
        histtype[histname["fourmuon_osv"][-1]]="fourmu3danglesv"
        #
        histname["fourmuon_osv"].append("hfourmuon_osv_uphi_mindr")
        histtype[histname["fourmuon_osv"][-1]]="fourmuupmindr"
        #
        histname["fourmuon_osv"].append("hfourmuon_osv_uphi_maxdr")
        histtype[histname["fourmuon_osv"][-1]]="fourmuupmaxdr"
        #
        histname["fourmuon_osv"].append("hfourmuon_osv_uphi_mindphi")
        histtype[histname["fourmuon_osv"][-1]]="fourmuupmindphi"
        #
        histname["fourmuon_osv"].append("hfourmuon_osv_uphi_maxdphi")
        histtype[histname["fourmuon_osv"][-1]]="fourmuupmaxdphi"
        #
        histname["fourmuon_osv"].append("hfourmuon_osv_uphi_mindeta")
        histtype[histname["fourmuon_osv"][-1]]="fourmuupmindeta"
        #
        histname["fourmuon_osv"].append("hfourmuon_osv_uphi_maxdeta")
        histtype[histname["fourmuon_osv"][-1]]="fourmuupmaxdeta"
        #
        histname["fourmuon_osv"].append("hfourmuon_osv_uphi_mindetadphiratio")
        histtype[histname["fourmuon_osv"][-1]]="fourmuupmindetadphiratio"
        #
        histname["fourmuon_osv"].append("hfourmuon_osv_uphi_maxdetadphiratio")
        histtype[histname["fourmuon_osv"][-1]]="fourmuupmaxdetadphiratio"
        #
        histname["fourmuon_osv"].append("hfourmuon_osv_uphi_min3dangle")
        histtype[histname["fourmuon_osv"][-1]]="fourmuupmin3dangle"
        #
        histname["fourmuon_osv"].append("hfourmuon_osv_uphi_max3dangle")
        histtype[histname["fourmuon_osv"][-1]]="fourmuupmax3dangle"
        #
        histname["fourmuon_osv"].append("hfourmuon_osv_uphi_dphisv")
        histtype[histname["fourmuon_osv"][-1]]="fourmuupdphisv"
        #
        histname["fourmuon_osv"].append("hfourmuon_osv_uphi_detasv")
        histtype[histname["fourmuon_osv"][-1]]="fourmuupdetasv"
        #
        histname["fourmuon_osv"].append("hfourmuon_osv_uphi_detadphisvratio")
        histtype[histname["fourmuon_osv"][-1]]="fourmuupdetadphisvratio"
        #
        histname["fourmuon_osv"].append("hfourmuon_osv_uphi_3danglesv")
        histtype[histname["fourmuon_osv"][-1]]="fourmuup3danglesv"
        #
        histname["fourmuon_osv"].append("hfourmuon_osv_detamindphimusvratio")
        histtype[histname["fourmuon_osv"][-1]]="fourmudetamindphimusvratio"
        #
        histname["fourmuon_osv"].append("hfourmuon_osv_detasvmindphimusvratio")
        histtype[histname["fourmuon_osv"][-1]]="fourmudetasvmindphimusvratio"
        #
        histname["fourmuon_osv"].append("hfourmuon_osv_sdphisvlxy")
        histtype[histname["fourmuon_osv"][-1]]="fourmusdphisvlxy"
        #
        histname["fourmuon_osv"].append("hfourmuon_osv_s3danglesvl3d")
        histtype[histname["fourmuon_osv"][-1]]="fourmus3danglesvl3d"
        #
        histname["fourmuon_osv"].append("hfourmuon_osv_uphi_detamindphimusvratio")
        histtype[histname["fourmuon_osv"][-1]]="fourmuupdetamindphimusvratio"
        #
        histname["fourmuon_osv"].append("hfourmuon_osv_uphi_detasvmindphimusvratio")
        histtype[histname["fourmuon_osv"][-1]]="fourmuupdetasvmindphimusvratio"
        #
        histname["fourmuon_osv"].append("hfourmuon_osv_uphi_sdphisvlxy")
        histtype[histname["fourmuon_osv"][-1]]="fourmuupsdphisvlxy"
        #
        histname["fourmuon_osv"].append("hfourmuon_osv_uphi_s3danglesvl3d")
        histtype[histname["fourmuon_osv"][-1]]="fourmuups3danglesvl3d"
        #
        histname["fourmuon_osv"].append("hfourmuon_osv_hitsbeforesv")
        histtype[histname["fourmuon_osv"][-1]]="totalmuhitsbeforesv"
        #
    ##
    # Four-muon
    histname["fourmuon"] = []
    histname2d["fourmuon"] = []
    if fourmuon:
        #
        histname["fourmuon"].append("hfourmuon_mass")
        histtype[histname["fourmuon"][-1]]="fourmumass"
        #
        histname["fourmuon"].append("hfourmuon_maxmass")
        histtype[histname["fourmuon"][-1]]="fourmumaxmass"
        #
        histname["fourmuon"].append("hfourmuon_minmass")
        histtype[histname["fourmuon"][-1]]="fourmuminmass"
        #
        histname["fourmuon"].append("hfourmuon_avgmass")
        histtype[histname["fourmuon"][-1]]="fourmuavgmass"
        #
        histname["fourmuon"].append("hfourmuon_reldmass")
        histtype[histname["fourmuon"][-1]]="fourmureldmass"
        #
        histname["fourmuon"].append("hfourmuon_pt")
        histtype[histname["fourmuon"][-1]]="fourmupt"
        #
        histname["fourmuon"].append("hfourmuon_minpt")
        histtype[histname["fourmuon"][-1]]="fourmuminpt"
        #
        histname["fourmuon"].append("hfourmuon_maxpt")
        histtype[histname["fourmuon"][-1]]="fourmumaxpt"
        #
        histname["fourmuon"].append("hfourmuon_minlxy")
        histtype[histname["fourmuon"][-1]]="minlxy"
        #
        histname["fourmuon"].append("hfourmuon_maxlxy")
        histtype[histname["fourmuon"][-1]]="maxlxy"
        #
        histname["fourmuon"].append("hfourmuon_mindr")
        histtype[histname["fourmuon"][-1]]="fourmumindr"
        #
        histname["fourmuon"].append("hfourmuon_maxdr")
        histtype[histname["fourmuon"][-1]]="fourmumaxdr"
        #
        histname["fourmuon"].append("hfourmuon_mindphi")
        histtype[histname["fourmuon"][-1]]="fourmumindphi"
        #
        histname["fourmuon"].append("hfourmuon_maxdphi")
        histtype[histname["fourmuon"][-1]]="fourmumaxdphi"
        #
        histname["fourmuon"].append("hfourmuon_mindeta")
        histtype[histname["fourmuon"][-1]]="fourmumindeta"
        #
        histname["fourmuon"].append("hfourmuon_maxdeta")
        histtype[histname["fourmuon"][-1]]="fourmumaxdeta"
        #
        histname["fourmuon"].append("hfourmuon_mindetadphiratio")
        histtype[histname["fourmuon"][-1]]="fourmumindetadphiratio"
        #
        histname["fourmuon"].append("hfourmuon_maxdetadphiratio")
        histtype[histname["fourmuon"][-1]]="fourmumaxdetadphiratio"
        #
        histname["fourmuon"].append("hfourmuon_min3dangle")
        histtype[histname["fourmuon"][-1]]="fourmumin3dangle"
        #
        histname["fourmuon"].append("hfourmuon_max3dangle")
        histtype[histname["fourmuon"][-1]]="fourmumax3dangle"
        #
        histname["fourmuon"].append("hfourmuon_mindphisv")
        histtype[histname["fourmuon"][-1]]="fourmumindphisv"
        #
        histname["fourmuon"].append("hfourmuon_maxdphisv")
        histtype[histname["fourmuon"][-1]]="fourmumaxdphisv"
        #
        histname["fourmuon"].append("hfourmuon_mindetasv")
        histtype[histname["fourmuon"][-1]]="fourmumindetasv"
        #
        histname["fourmuon"].append("hfourmuon_maxdetasv")
        histtype[histname["fourmuon"][-1]]="fourmumaxdetasv"
        #
        histname["fourmuon"].append("hfourmuon_mindetadphisvratio")
        histtype[histname["fourmuon"][-1]]="fourmumindetadphisvratio"
        #
        histname["fourmuon"].append("hfourmuon_maxdetadphisvratio")
        histtype[histname["fourmuon"][-1]]="fourmumaxdetadphisvratio"
        #
        histname["fourmuon"].append("hfourmuon_min3danglesv")
        histtype[histname["fourmuon"][-1]]="fourmumin3danglesv"
        #
        histname["fourmuon"].append("hfourmuon_max3danglesv")
        histtype[histname["fourmuon"][-1]]="fourmumax3danglesv"
        #
        histname["fourmuon"].append("hfourmuon_uphi_mindr")
        histtype[histname["fourmuon"][-1]]="fourmuupmindr"
        #
        histname["fourmuon"].append("hfourmuon_uphi_maxdr")
        histtype[histname["fourmuon"][-1]]="fourmuupmaxdr"
        #
        histname["fourmuon"].append("hfourmuon_uphi_mindphi")
        histtype[histname["fourmuon"][-1]]="fourmuupmindphi"
        #
        histname["fourmuon"].append("hfourmuon_uphi_maxdphi")
        histtype[histname["fourmuon"][-1]]="fourmuupmaxdphi"
        #
        histname["fourmuon"].append("hfourmuon_uphi_mindeta")
        histtype[histname["fourmuon"][-1]]="fourmuupmindeta"
        #
        histname["fourmuon"].append("hfourmuon_uphi_maxdeta")
        histtype[histname["fourmuon"][-1]]="fourmuupmaxdeta"
        #
        histname["fourmuon"].append("hfourmuon_uphi_mindetadphiratio")
        histtype[histname["fourmuon"][-1]]="fourmuupmindetadphiratio"
        #
        histname["fourmuon"].append("hfourmuon_uphi_maxdetadphiratio")
        histtype[histname["fourmuon"][-1]]="fourmuupmaxdetadphiratio"
        #
        histname["fourmuon"].append("hfourmuon_uphi_min3dangle")
        histtype[histname["fourmuon"][-1]]="fourmuupmin3dangle"
        #
        histname["fourmuon"].append("hfourmuon_uphi_max3dangle")
        histtype[histname["fourmuon"][-1]]="fourmuupmax3dangle"
        #
        histname["fourmuon"].append("hfourmuon_uphi_mindphisv")
        histtype[histname["fourmuon"][-1]]="fourmuupmindphisv"
        #
        histname["fourmuon"].append("hfourmuon_uphi_maxdphisv")
        histtype[histname["fourmuon"][-1]]="fourmuupmaxdphisv"
        #
        histname["fourmuon"].append("hfourmuon_uphi_mindetasv")
        histtype[histname["fourmuon"][-1]]="fourmuupmindetasv"
        #
        histname["fourmuon"].append("hfourmuon_uphi_maxdetasv")
        histtype[histname["fourmuon"][-1]]="fourmuupmaxdetasv"
        #
        histname["fourmuon"].append("hfourmuon_uphi_mindetadphisvratio")
        histtype[histname["fourmuon"][-1]]="fourmuupmindetadphisvratio"
        #
        histname["fourmuon"].append("hfourmuon_uphi_maxdetadphisvratio")
        histtype[histname["fourmuon"][-1]]="fourmuupmaxdetadphisvratio"
        #
        histname["fourmuon"].append("hfourmuon_uphi_min3danglesv")
        histtype[histname["fourmuon"][-1]]="fourmuupmin3danglesv"
        #
        histname["fourmuon"].append("hfourmuon_uphi_max3danglesv")
        histtype[histname["fourmuon"][-1]]="fourmuupmax3danglesv"
        #
        histname["fourmuon"].append("hfourmuon_mindetamindphimusvratio")
        histtype[histname["fourmuon"][-1]]="fourmumindetamindphimusvratio"
        #
        histname["fourmuon"].append("hfourmuon_maxdetamindphimusvratio")
        histtype[histname["fourmuon"][-1]]="fourmumaxdetamindphimusvratio"
        #
        histname["fourmuon"].append("hfourmuon_mindetasvmindphimusvratio")
        histtype[histname["fourmuon"][-1]]="fourmumindetasvmindphimusvratio"
        #
        histname["fourmuon"].append("hfourmuon_maxdetasvmindphimusvratio")
        histtype[histname["fourmuon"][-1]]="fourmumaxdetasvmindphimusvratio"
        #
        histname["fourmuon"].append("hfourmuon_minsdphisvlxy")
        histtype[histname["fourmuon"][-1]]="fourmuminsdphisvlxy"
        #
        histname["fourmuon"].append("hfourmuon_maxsdphisvlxy")
        histtype[histname["fourmuon"][-1]]="fourmumaxsdphisvlxy"
        #
        histname["fourmuon"].append("hfourmuon_mins3danglesvl3d")
        histtype[histname["fourmuon"][-1]]="fourmumins3danglesvl3d"
        #
        histname["fourmuon"].append("hfourmuon_maxs3danglesvl3d")
        histtype[histname["fourmuon"][-1]]="fourmumaxs3danglesvl3d"
        #
        histname["fourmuon"].append("hfourmuon_uphi_mindetamindphimusvratio")
        histtype[histname["fourmuon"][-1]]="fourmuupmindetamindphimusvratio"
        #
        histname["fourmuon"].append("hfourmuon_uphi_maxdetamindphimusvratio")
        histtype[histname["fourmuon"][-1]]="fourmuupmaxdetamindphimusvratio"
        #
        histname["fourmuon"].append("hfourmuon_uphi_mindetasvmindphimusvratio")
        histtype[histname["fourmuon"][-1]]="fourmuupmindetasvmindphimusvratio"
        #
        histname["fourmuon"].append("hfourmuon_uphi_maxdetasvmindphimusvratio")
        histtype[histname["fourmuon"][-1]]="fourmuupmaxdetasvmindphimusvratio"
        #
        histname["fourmuon"].append("hfourmuon_uphi_minsdphisvlxy")
        histtype[histname["fourmuon"][-1]]="fourmuupminsdphisvlxy"
        #
        histname["fourmuon"].append("hfourmuon_uphi_maxsdphisvlxy")
        histtype[histname["fourmuon"][-1]]="fourmuupmaxsdphisvlxy"
        #
        histname["fourmuon"].append("hfourmuon_uphi_mins3danglesvl3d")
        histtype[histname["fourmuon"][-1]]="fourmuupmins3danglesvl3d"
        #
        histname["fourmuon"].append("hfourmuon_uphi_maxs3danglesvl3d")
        histtype[histname["fourmuon"][-1]]="fourmuupmaxs3danglesvl3d"
        #
        histname["fourmuon"].append("hfourmuon_hitsbeforesv")
        histtype[histname["fourmuon"][-1]]="totalmuhitsbeforesv"
        #
    return histname,histtype,histname2d,histtype2d

def histInitialization(presel,dimuon,fourmuon,fourmuonosv):
    nbins    = dict()
    low      = dict()
    high     = dict()
    xtitle   = dict()
    ytitle   = dict()
    labels   = dict()
    variable = dict()
    hist1dDefinition(nbins, low, high, xtitle, ytitle, labels, variable)
    
    nbinsX      = dict()
    lowX        = dict()
    highX       = dict()
    xtitle2d    = dict()
    nbinsY      = dict()    
    lowY        = dict()
    highY       = dict()
    ytitle2d    = dict()
    ztitle2d    = dict()
    variablesXY = dict()
    hist2dDefinition(nbinsX, lowX, highX, xtitle2d, nbinsY, lowY, highY, ytitle2d, ztitle2d, variablesXY)

    histname = dict()
    histtype = dict()
    histname2d = dict()
    histtype2d = dict()
    histname, histtype, histname2d, histtype2d = histBooking(presel,dimuon, fourmuon, fourmuonosv)

    hists1d     = dict()
    variables1d = dict()
    for cat in histname.keys():
        hists1d[cat] = []
        for hn in histname[cat]:
            if histtype[hn] in labels.keys():
                th = H1(hn,nbins[histtype[hn]],low[histtype[hn]],high[histtype[hn]],xtitle[histtype[hn]],ytitle[histtype[hn]],labels[histtype[hn]])
            else:
                th = H1(hn,nbins[histtype[hn]],low[histtype[hn]],high[histtype[hn]],xtitle[histtype[hn]],ytitle[histtype[hn]])
            variables1d[hn] = variable[histtype[hn]]
            hists1d[cat].append(th)
    hists2d     = dict()
    variables2d = dict()
    for cat in histname2d.keys():
        hists2d[cat] = []
        for hn in histname2d[cat]:
            th = H2(hn,
                    nbinsX[histtype2d[hn]],lowX[histtype2d[hn]],highX[histtype2d[hn]],xtitle2d[histtype2d[hn]],
                    nbinsY[histtype2d[hn]],lowY[histtype2d[hn]],highY[histtype2d[hn]],ytitle2d[histtype2d[hn]],
                    ztitle2d[histtype2d[hn]])
            variables2d[hn] = variablesXY[histtype2d[hn]]
            hists2d[cat].append(th)
    return hists1d, variables1d, hists2d, variables2d
