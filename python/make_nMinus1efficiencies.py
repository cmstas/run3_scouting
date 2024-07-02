import ROOT
import os,sys,json
import argparse
from datetime import date
import numpy as np
import copy
import math
sys.path.append('utils')
import plotUtils
from IPython.display import Image
import argparse
import os
import matplotlib.pyplot as plt
import mplhep as hep

ROOT.gStyle.SetOptStat(0)
parser = argparse.ArgumentParser()
parser.add_argument('directory', type=str)
args = parser.parse_args()
files = []
directory = args.directory

def getValues(histo):
	values = []
	bins = []
	for n in range(1,histo.GetNbinsX()+1):
		values.append(histo.GetBinContent(n))
		bins.append(histo.GetBinLowEdge(n))
	bins.append(histo.GetBinLowEdge(n) + histo.GetBinWidth(n))
	return np.array(values), np.array(bins)

if not os.path.exists('cuts_plots/'):
	os.mkdir('cuts_plots/')

sum_100mm_allCuts = {}
sum_10mm_allCuts = {}
sum_1mm_allCuts = {}
sum_100mm_noCuts = {}
sum_10mm_noCuts = {}
sum_1mm_noCuts = {}
sum_100mm_Cut1 = {}
sum_10mm_Cut1 = {}
sum_1mm_Cut1 = {}
sum_100mm_Cut2 = {}
sum_10mm_Cut2 = {}
sum_1mm_Cut2 = {}
sum_100mm_Cut3 = {}
sum_10mm_Cut3 = {}
sum_1mm_Cut3 = {}
sum_100mm_Cut4 = {}
sum_10mm_Cut4 = {}
sum_1mm_Cut4 = {}
for subdir  in os.listdir(directory):
	if 'Jun-14' in subdir:
		full_subdir_path = os.path.join(directory, subdir, '')
		files = os.listdir(full_subdir_path)
		for filename in files:
			if '_all' in filename:
				continue
			if '-2p0_' in filename:
				mass = 2
			elif '-7p0_' in filename:
				mass = 7
			elif '-10p0_' in filename:
				mass = 10
			elif '-20p0_' in filename:
				mass = 20
			elif '-30p0_' in filename:
				mass = 30
			else:
				continue
			file = ROOT.TFile.Open(full_subdir_path + filename)
			if 'allCuts' in subdir:
				if '100mm' in filename:
					ctau = '100mm'
					hdimuon_mass = file.Get("hdimuon_mass")
					n_hist_100mm_allCuts = hdimuon_mass.Integral()
					current_value_100mm_allCuts = sum_100mm_allCuts.get(mass, 0)
					updated_value_100mm_allCuts = current_value_100mm_allCuts + n_hist_100mm_allCuts
					sum_100mm_allCuts[mass] = updated_value_100mm_allCuts
					
				elif '10mm' in filename:
					ctau = '10mm'
					hdimuon_mass = file.Get("hdimuon_mass")
					n_hist_10mm_allCuts = hdimuon_mass.Integral()
					current_value_10mm_allCuts = sum_10mm_allCuts.get(mass, 0)
					updated_value_10mm_allCuts = current_value_10mm_allCuts + n_hist_10mm_allCuts
					sum_10mm_allCuts[mass] = updated_value_10mm_allCuts
				
				elif '1mm' in filename:
					ctau = '1mm'
					hdimuon_mass = file.Get("hdimuon_mass")
					n_hist_1mm_allCuts = hdimuon_mass.Integral()
					current_value_1mm_allCuts = sum_1mm_allCuts.get(mass, 0)
					updated_value_1mm_allCuts = current_value_1mm_allCuts + n_hist_1mm_allCuts
					sum_1mm_allCuts[mass] = updated_value_1mm_allCuts
						

			elif 'noCuts' in subdir:
				if '100mm' in filename:
					ctau = '100mm'
					hdimuon_mass = file.Get("hdimuon_mass")
					n_hist_100mm_noCuts = hdimuon_mass.Integral()
					current_value_100mm_noCuts = sum_100mm_noCuts.get(mass, 0)
					updated_value_100mm_noCuts = current_value_100mm_noCuts + n_hist_100mm_noCuts
					sum_100mm_noCuts[mass] = updated_value_100mm_noCuts

				elif '10mm' in filename:
					ctau = '10mm'
					hdimuon_mass = file.Get("hdimuon_mass")
					n_hist_10mm_noCuts = hdimuon_mass.Integral()
					current_value_10mm_noCuts = sum_10mm_noCuts.get(mass, 0)
					updated_value_10mm_noCuts = current_value_10mm_noCuts + n_hist_10mm_noCuts
					sum_10mm_noCuts[mass] = updated_value_10mm_noCuts

				elif '1mm' in filename:
					ctau = '1mm'
					hdimuon_mass = file.Get("hdimuon_mass")
					n_hist_1mm_noCuts = hdimuon_mass.Integral()
					current_value_1mm_noCuts = sum_1mm_noCuts.get(mass, 0)
					updated_value_1mm_noCuts = current_value_1mm_noCuts + n_hist_1mm_noCuts
					sum_1mm_noCuts[mass] = updated_value_1mm_noCuts	
			elif 'noDiMuonAngularSel' in subdir:
				if '100mm' in filename:
					ctau = '100mm'
					hdimuon_mass = file.Get("hdimuon_mass")
					n_hist_100mm_Cut1 = hdimuon_mass.Integral()
					current_value_100mm_Cut1 = sum_100mm_Cut1.get(mass, 0)
					updated_value_100mm_Cut1 = current_value_100mm_Cut1 + n_hist_100mm_Cut1
					sum_100mm_Cut1[mass] = updated_value_100mm_Cut1

				elif '10mm' in filename:
					ctau = '10mm'
					hdimuon_mass = file.Get("hdimuon_mass")
					n_hist_10mm_Cut1 = hdimuon_mass.Integral()
					current_value_10mm_Cut1 = sum_10mm_Cut1.get(mass, 0)
					updated_value_10mm_Cut1 = current_value_10mm_Cut1 + n_hist_10mm_Cut1
					sum_10mm_Cut1[mass] = updated_value_10mm_Cut1

				elif '1mm' in filename:
					ctau = '1mm'
					hdimuon_mass = file.Get("hdimuon_mass")
					n_hist_1mm_Cut1 = hdimuon_mass.Integral()
					current_value_1mm_Cut1 = sum_1mm_Cut1.get(mass, 0)
					updated_value_1mm_Cut1 = current_value_1mm_Cut1 + n_hist_1mm_Cut1
					sum_1mm_Cut1[mass] = updated_value_1mm_Cut1

			elif 'noMaterialVeto' in subdir:
				if '100mm' in filename:
					ctau = '100mm'
					hdimuon_mass = file.Get("hdimuon_mass")
					n_hist_100mm_Cut2 = hdimuon_mass.Integral()
					current_value_100mm_Cut2 = sum_100mm_Cut2.get(mass, 0)
					updated_value_100mm_Cut2 = current_value_100mm_Cut2 + n_hist_100mm_Cut2
					sum_100mm_Cut2[mass] = updated_value_100mm_Cut2

				elif '10mm' in filename:
					ctau = '10mm'
					hdimuon_mass = file.Get("hdimuon_mass")
					n_hist_10mm_Cut2 = hdimuon_mass.Integral()
					current_value_10mm_Cut2 = sum_10mm_Cut2.get(mass, 0)
					updated_value_10mm_Cut2 = current_value_10mm_Cut2 + n_hist_10mm_Cut2
					sum_10mm_Cut2[mass] = updated_value_10mm_Cut2

				elif '1mm' in filename:
					ctau = '1mm'
					hdimuon_mass = file.Get("hdimuon_mass")
					n_hist_1mm_Cut2 = hdimuon_mass.Integral()
					current_value_1mm_Cut2 = sum_1mm_Cut2.get(mass, 0)
					updated_value_1mm_Cut2 = current_value_1mm_Cut2 + n_hist_1mm_Cut2
					sum_1mm_Cut2[mass] = updated_value_1mm_Cut2


			elif 'noMuonHitSel' in subdir:
				if '100mm' in filename:
					ctau = '100mm'
					hdimuon_mass = file.Get("hdimuon_mass")
					n_hist_100mm_Cut3 = hdimuon_mass.Integral()
					current_value_100mm_Cut3 = sum_100mm_Cut3.get(mass, 0)
					updated_value_100mm_Cut3 = current_value_100mm_Cut3 + n_hist_100mm_Cut3
					sum_100mm_Cut3[mass] = updated_value_100mm_Cut3
				elif '10mm' in filename:
					ctau = '10mm'
					hdimuon_mass = file.Get("hdimuon_mass")
					n_hist_10mm_Cut3 = hdimuon_mass.Integral()
					current_value_10mm_Cut3 = sum_10mm_Cut3.get(mass, 0)
					updated_value_10mm_Cut3 = current_value_10mm_Cut3 + n_hist_10mm_Cut3
					sum_10mm_Cut3[mass] = updated_value_10mm_Cut3

				elif '1mm' in filename:
					ctau = '1mm'
					hdimuon_mass = file.Get("hdimuon_mass")
					n_hist_1mm_Cut3 = hdimuon_mass.Integral()
					current_value_1mm_Cut3 = sum_1mm_Cut3.get(mass, 0)
					updated_value_1mm_Cut3 = current_value_1mm_Cut3 + n_hist_1mm_Cut3
					sum_1mm_Cut3[mass] = updated_value_1mm_Cut3

			elif 'noMuonIPSel' in subdir:
				if '100mm' in filename:
					ctau = '100mm'
					hdimuon_mass = file.Get("hdimuon_mass")
					n_hist_100mm_Cut4 = hdimuon_mass.Integral()
					current_value_100mm_Cut4 = sum_100mm_Cut4.get(mass, 0)
					updated_value_100mm_Cut4 = current_value_100mm_Cut4 + n_hist_100mm_Cut4
					sum_100mm_Cut4[mass] = updated_value_100mm_Cut4
				elif '10mm' in filename:
					ctau = '10mm'
					hdimuon_mass = file.Get("hdimuon_mass")
					n_hist_10mm_Cut4 = hdimuon_mass.Integral()
					current_value_10mm_Cut4 = sum_10mm_Cut4.get(mass, 0)
					updated_value_10mm_Cut4 = current_value_10mm_Cut4 + n_hist_10mm_Cut4
					sum_10mm_Cut4[mass] = updated_value_10mm_Cut4

				elif '1mm' in filename:
					ctau = '1mm'
					hdimuon_mass = file.Get("hdimuon_mass")
					n_hist_1mm_Cut4 = hdimuon_mass.Integral()
					current_value_1mm_Cut4 = sum_1mm_Cut4.get(mass, 0)
					updated_value_1mm_Cut4 = current_value_1mm_Cut4 + n_hist_1mm_Cut4
					sum_1mm_Cut4[mass] = updated_value_1mm_Cut4


masses = [2,7,10,20,30]
ctaus =['1mm','10mm','100mm']

nbins = len(masses)*len(ctaus)
maxx = nbins
minx = 0

h_noCuts = ROOT.TH1F('h_noCuts', 'No cuts', nbins, minx, maxx)
h_allCuts = ROOT.TH1F('h_allCuts', 'All cuts', nbins, minx, maxx)
h_Cut1 = ROOT.TH1F('h_Cut1', 'Cut 1', nbins, minx, maxx)
h_Cut2 = ROOT.TH1F('h_Cut2', 'Cut 2', nbins, minx, maxx)
h_Cut3 = ROOT.TH1F('h_Cut3', 'Cut 3', nbins, minx, maxx)
h_Cut4 = ROOT.TH1F('h_Cut4', 'Cut 4', nbins, minx, maxx)
for massindex, mass in enumerate(masses):
        h_noCuts.Fill(massindex,sum_1mm_noCuts[mass]/sum_1mm_noCuts[mass])
        h_Cut1.Fill(massindex,sum_1mm_Cut1[mass]/sum_1mm_noCuts[mass])
        h_Cut2.Fill(massindex,sum_1mm_Cut2[mass]/sum_1mm_noCuts[mass])
        h_Cut3.Fill(massindex,sum_1mm_Cut3[mass]/sum_1mm_noCuts[mass])
        h_Cut4.Fill(massindex,sum_1mm_Cut4[mass]/sum_1mm_noCuts[mass])
        h_allCuts.Fill(massindex,sum_1mm_allCuts[mass]/sum_1mm_noCuts[mass])

        h_noCuts.Fill(massindex + len(masses),sum_10mm_noCuts[mass]/sum_10mm_noCuts[mass])
        h_Cut1.Fill(massindex + len(masses),sum_10mm_Cut1[mass]/sum_10mm_noCuts[mass])
        h_Cut2.Fill(massindex + len(masses),sum_10mm_Cut2[mass]/sum_10mm_noCuts[mass])
        h_Cut3.Fill(massindex + len(masses),sum_10mm_Cut3[mass]/sum_10mm_noCuts[mass])
        h_Cut4.Fill(massindex + len(masses),sum_10mm_Cut4[mass]/sum_10mm_noCuts[mass])
        h_allCuts.Fill(massindex + len(masses),sum_10mm_allCuts[mass]/sum_10mm_noCuts[mass])

        h_noCuts.Fill(massindex + 2*len(masses),sum_100mm_noCuts[mass]/sum_100mm_noCuts[mass])
        h_Cut1.Fill(massindex + 2*len(masses),sum_100mm_Cut1[mass]/sum_100mm_noCuts[mass])
        h_Cut2.Fill(massindex + 2*len(masses),sum_100mm_Cut2[mass]/sum_100mm_noCuts[mass])
        h_Cut3.Fill(massindex + 2*len(masses),sum_100mm_Cut3[mass]/sum_100mm_noCuts[mass])
        h_Cut4.Fill(massindex + 2*len(masses),sum_100mm_Cut4[mass]/sum_100mm_noCuts[mass])
        h_allCuts.Fill(massindex + 2*len(masses),sum_100mm_allCuts[mass]/sum_100mm_noCuts[mass])


values_noCuts, bins_noCuts = getValues(h_noCuts)
values_allCuts, bins_allCuts = getValues(h_allCuts)
values_Cut1, bins_Cut1 = getValues(h_Cut1)
values_Cut2, bins_Cut2 = getValues(h_Cut2)
values_Cut3, bins_Cut3 = getValues(h_Cut3)
values_Cut4, bins_Cut4 = getValues(h_Cut4)

hist_array = [values_noCuts, values_Cut1, values_Cut2, values_Cut3, values_Cut4, values_allCuts]
label_array = ['No cuts','No Dimuon Angular Selection','No Material Veto','No Muon Hit Selection','No Muon IP Selection','All cuts']
yearenergy="(2022, 13.6 TeV)"
bin_labels = []
j = -1
masses_plot = masses*3

hep.style.use("CMS")
fig, ax = plt.subplots(figsize=(10, 7.5))
hep.histplot(
	hist_array,
	stack = False,
	bins = bins_allCuts,
	histtype = "step",
	alpha = 1,
	label = label_array,
	ax = ax
)

legend_coords = (0.78,0.4)
ax.set_xlim(0, 15)
expoffset = 0.065
hep.cms.label(rlabel="")
ax.set_xticks(bins_allCuts)
j = -1
for i in range(len(masses_plot)):
    if i%len(masses) == 0:
        j+=1
    x = (bins_allCuts[i] + bins_allCuts[i+1]) / 2 - 0.45
    y = -0.07
    mass_label = f"{masses_plot[i]} GeV"
    ctau_label = f"{ctaus[j]}"
    plt.text(x, y, mass_label + "\n" + ctau_label, fontsize=10)

ax.set_xticks(bins_allCuts)
ax.set_xticklabels([''] * len(bins_allCuts))
ax.legend(loc='center', bbox_to_anchor=legend_coords, fontsize=15)
ax.text(1.01, 1 + expoffset, yearenergy, transform=ax.transAxes, verticalalignment='top', horizontalalignment='right', fontsize=25)
plt.ylabel("N - 1 Efficiency")
plt.savefig("cuts_plots/nMinus1efficiencies_goodplots.png")
plt.close()


c1 = ROOT.TCanvas('c1', '', 600, 500)
c1.cd()
h_noCuts.SetTitle("Efficiencies")
h_noCuts.SetMinimum(0)
h_noCuts.GetYaxis().SetTitleOffset(1.2)
h_noCuts.SetLineColor(ROOT.kOrange)
h_Cut1.SetLineColor(ROOT.kBlue)
h_Cut2.SetLineColor(ROOT.kGreen)
h_Cut3.SetLineColor(ROOT.kRed)
h_Cut4.SetLineColor(ROOT.kCyan)
h_allCuts.SetLineColor(ROOT.kBlack)


'''
leftMargin = 0.13
topMargin = 0.13
bottomMargin = 0.15
rightMargin = 0.13
r.gStyle.SetPadLeftMargin(leftMargin)   
r.gStyle.SetPadTopMargin(topMargin)   
r.gStyle.SetPadBottomMargin(bottomMargin)   
r.gStyle.SetHistTopMargin(0.)
r.gStyle.SetPadRightMargin(rightMargin)   
binw = (1.0 - leftMargin - rightMargin)/len(sorted_models)

xlabels = []
for n in range(len(masses)*len(ctaus)):
    xlabels.append(leftMargin + binw*(n + 0.5))
for n in range(len(x_labels)):

'''

j = 0
masses_plot = masses*3

for i, mass in enumerate(masses_plot):
    if i % len(masses) == 0:  
        label = f"m = {mass}, ctau = {ctaus[j]}"
        j += 1
    else:
        label = f"m = {mass}"
    h_noCuts.GetXaxis().SetBinLabel(i+1, label)

h_noCuts.Draw('HIST')
h_Cut1.Draw('HIST SAME')
h_Cut2.Draw('HIST SAME')
h_Cut3.Draw('HIST SAME')
h_Cut4.Draw('HIST SAME')
h_allCuts.Draw('HIST SAME')

legend = ROOT.TLegend(0.15,0.3,0.48,0.5)
legend.SetBorderSize(0)
legend.SetTextSize(0.035)
legend.AddEntry(h_noCuts,"No cuts","l")
legend.AddEntry(h_Cut1,"Dimuon Angular Selection","l")
legend.AddEntry(h_Cut2,"Material Veto","l")
legend.AddEntry(h_Cut3,"Muon Hit Selection","l")
legend.AddEntry(h_Cut4,"Muon IP Selection","l")
legend.AddEntry(h_allCuts,"All cuts","l")

legend.Draw()
c1.Update()

filename = 'efficiencies.png'
output_filename = f'cuts_plots/{filename}'
c1.SaveAs(output_filename)
Image(filename=output_filename)
'''
filename = "h_2GeV_100mm.png"
h_2GeV_100mm = ROOT.TH1F("h_2GeV_100mm", "mass = 2 GeV, ctau = 100mm", nbins, minx, maxx)

h_2GeV_100mm.SetTitle("mass = 2 GeV, ctau = 100mm")
h_2GeV_100mm.SetMinimum(0)

h_2GeV_100mm.Fill(0,1)
h_2GeV_100mm.Fill(1,sum_100mm_Cut1[2]/sum_100mm_noCuts[2])
h_2GeV_100mm.Fill(2,sum_100mm_Cut2[2]/sum_100mm_noCuts[2])
h_2GeV_100mm.Fill(3,sum_100mm_Cut3[2]/sum_100mm_noCuts[2])
h_2GeV_100mm.Fill(4,sum_100mm_Cut4[2]/sum_100mm_noCuts[2])
h_2GeV_100mm.Fill(5,sum_100mm_allCuts[2]/sum_100mm_noCuts[2])
#
h_2GeV_100mm.GetXaxis().SetBinLabel(1, "No cuts")
h_2GeV_100mm.GetXaxis().SetBinLabel(2, "noDiMuonAngularSel")
h_2GeV_100mm.GetXaxis().SetBinLabel(3, "noMaterialVeto")
h_2GeV_100mm.GetXaxis().SetBinLabel(4, "noMuonHitSel")
h_2GeV_100mm.GetXaxis().SetBinLabel(5, "noMuonIPSel")
h_2GeV_100mm.GetXaxis().SetBinLabel(6, "All cuts")

c1 = ROOT.TCanvas('c1', '', 600, 500)
c1.cd()
h_2GeV_100mm.Draw('HIST')

output_filename = f'cuts_plots/{filename}'
c1.SaveAs(output_filename)
Image(filename=output_filename)
#
#
filename = "h_7GeV_100mm.png"
h_7GeV_100mm = ROOT.TH1F("h_7GeV_100mm", "mass = 7 GeV, ctau = 100mm", nbins, minx, maxx)

h_7GeV_100mm.SetTitle("mass = 7 GeV, ctau = 100mm")
h_7GeV_100mm.SetMinimum(0)

h_7GeV_100mm.Fill(0,1)
h_7GeV_100mm.Fill(1,sum_100mm_Cut1[7]/sum_100mm_noCuts[7])
h_7GeV_100mm.Fill(2,sum_100mm_Cut2[7]/sum_100mm_noCuts[7])
h_7GeV_100mm.Fill(3,sum_100mm_Cut3[7]/sum_100mm_noCuts[7])
h_7GeV_100mm.Fill(4,sum_100mm_Cut4[7]/sum_100mm_noCuts[7])
h_7GeV_100mm.Fill(5,sum_100mm_allCuts[7]/sum_100mm_noCuts[7])
#
h_7GeV_100mm.GetXaxis().SetBinLabel(1, "No cuts")
h_7GeV_100mm.GetXaxis().SetBinLabel(2, "noDiMuonAngularSel")
h_7GeV_100mm.GetXaxis().SetBinLabel(3, "noMaterialVeto")
h_7GeV_100mm.GetXaxis().SetBinLabel(4, "noMuonHitSel")
h_7GeV_100mm.GetXaxis().SetBinLabel(5, "noMuonIPSel")
h_7GeV_100mm.GetXaxis().SetBinLabel(6, "All cuts")

c2 = ROOT.TCanvas('c2', '', 600, 500)
c2.cd()
h_7GeV_100mm.Draw('HIST')

output_filename = f'cuts_plots/{filename}'
c2.SaveAs(output_filename)
Image(filename=output_filename)
#
#
filename = "h_10GeV_100mm.png"
h_10GeV_100mm = ROOT.TH1F("h_10GeV_100mm", "mass = 10 GeV, ctau = 100mm", nbins, minx, maxx)

h_10GeV_100mm.SetTitle("mass = 10 GeV, ctau = 100mm")
h_10GeV_100mm.SetMinimum(0)

h_10GeV_100mm.Fill(0,1)
h_10GeV_100mm.Fill(1,sum_100mm_Cut1[10]/sum_100mm_noCuts[10])
h_10GeV_100mm.Fill(2,sum_100mm_Cut2[10]/sum_100mm_noCuts[10])
h_10GeV_100mm.Fill(3,sum_100mm_Cut3[10]/sum_100mm_noCuts[10])
h_10GeV_100mm.Fill(4,sum_100mm_Cut4[10]/sum_100mm_noCuts[10])
h_10GeV_100mm.Fill(5,sum_100mm_allCuts[10]/sum_100mm_noCuts[10])
#
h_10GeV_100mm.GetXaxis().SetBinLabel(1, "No cuts")
h_10GeV_100mm.GetXaxis().SetBinLabel(2, "noDiMuonAngularSel")
h_10GeV_100mm.GetXaxis().SetBinLabel(3, "noMaterialVeto")
h_10GeV_100mm.GetXaxis().SetBinLabel(4, "noMuonHitSel")
h_10GeV_100mm.GetXaxis().SetBinLabel(5, "noMuonIPSel")
h_10GeV_100mm.GetXaxis().SetBinLabel(6, "All cuts")

c3 = ROOT.TCanvas('c3', '', 600, 500)
c3.cd()
h_10GeV_100mm.Draw('HIST')

output_filename = f'cuts_plots/{filename}'
c3.SaveAs(output_filename)
Image(filename=output_filename)
#
#
filename = "h_20GeV_100mm.png"
h_20GeV_100mm = ROOT.TH1F("h_20GeV_100mm", "mass = 20 GeV, ctau = 100mm", nbins, minx, maxx)

h_20GeV_100mm.SetTitle("mass = 20 GeV, ctau = 100mm")
h_20GeV_100mm.SetMinimum(0)

h_20GeV_100mm.Fill(0,1)
h_20GeV_100mm.Fill(1,sum_100mm_Cut1[20]/sum_100mm_noCuts[20])
h_20GeV_100mm.Fill(2,sum_100mm_Cut2[20]/sum_100mm_noCuts[20])
h_20GeV_100mm.Fill(3,sum_100mm_Cut3[20]/sum_100mm_noCuts[20])
h_20GeV_100mm.Fill(4,sum_100mm_Cut4[20]/sum_100mm_noCuts[20])
h_20GeV_100mm.Fill(5,sum_100mm_allCuts[20]/sum_100mm_noCuts[20])
#
h_20GeV_100mm.GetXaxis().SetBinLabel(1, "No cuts")
h_20GeV_100mm.GetXaxis().SetBinLabel(2, "noDiMuonAngularSel")
h_20GeV_100mm.GetXaxis().SetBinLabel(3, "noMaterialVeto")
h_20GeV_100mm.GetXaxis().SetBinLabel(4, "noMuonHitSel")
h_20GeV_100mm.GetXaxis().SetBinLabel(5, "noMuonIPSel")
h_20GeV_100mm.GetXaxis().SetBinLabel(6, "All cuts")

c4 = ROOT.TCanvas('c4', '', 600, 500)
c4.cd()
h_20GeV_100mm.Draw('HIST')

output_filename = f'cuts_plots/{filename}'
c4.SaveAs(output_filename)
Image(filename=output_filename)
#
#
filename = "h_30GeV_100mm.png"
h_30GeV_100mm = ROOT.TH1F("h_30GeV_100mm", "mass = 30 GeV, ctau = 100mm", nbins, minx, maxx)

h_30GeV_100mm.SetTitle("mass = 30 GeV, ctau = 100mm")
h_30GeV_100mm.SetMinimum(0)

h_30GeV_100mm.Fill(0,1)
h_30GeV_100mm.Fill(1,sum_100mm_Cut1[30]/sum_100mm_noCuts[30])
h_30GeV_100mm.Fill(2,sum_100mm_Cut2[30]/sum_100mm_noCuts[30])
h_30GeV_100mm.Fill(3,sum_100mm_Cut3[30]/sum_100mm_noCuts[30])
h_30GeV_100mm.Fill(4,sum_100mm_Cut4[30]/sum_100mm_noCuts[30])
h_30GeV_100mm.Fill(5,sum_100mm_allCuts[30]/sum_100mm_noCuts[30])
#
h_30GeV_100mm.GetXaxis().SetBinLabel(1, "No cuts")
h_30GeV_100mm.GetXaxis().SetBinLabel(2, "noDiMuonAngularSel")
h_30GeV_100mm.GetXaxis().SetBinLabel(3, "noMaterialVeto")
h_30GeV_100mm.GetXaxis().SetBinLabel(4, "noMuonHitSel")
h_30GeV_100mm.GetXaxis().SetBinLabel(5, "noMuonIPSel")
h_30GeV_100mm.GetXaxis().SetBinLabel(6, "All cuts")

c5 = ROOT.TCanvas('c5', '', 600, 500)
c5.cd()
h_30GeV_100mm.Draw('HIST')

output_filename = f'cuts_plots/{filename}'
c5.SaveAs(output_filename)
Image(filename=output_filename)
#
#
#
#
filename = "h_2GeV_10mm.png"
h_2GeV_10mm = ROOT.TH1F("h_2GeV_10mm", "mass = 2 GeV, ctau = 10mm", nbins, minx, maxx)

h_2GeV_10mm.SetTitle("mass = 2 GeV, ctau = 10mm")
h_2GeV_10mm.SetMinimum(0)

h_2GeV_10mm.Fill(0,1)
h_2GeV_10mm.Fill(1,sum_10mm_Cut1[2]/sum_10mm_noCuts[2])
h_2GeV_10mm.Fill(2,sum_10mm_Cut2[2]/sum_10mm_noCuts[2])
h_2GeV_10mm.Fill(3,sum_10mm_Cut3[2]/sum_10mm_noCuts[2])
h_2GeV_10mm.Fill(4,sum_10mm_Cut4[2]/sum_10mm_noCuts[2])
h_2GeV_10mm.Fill(5,sum_10mm_allCuts[2]/sum_10mm_noCuts[2])
#
h_2GeV_10mm.GetXaxis().SetBinLabel(1, "No cuts")
h_2GeV_10mm.GetXaxis().SetBinLabel(2, "noDiMuonAngularSel")
h_2GeV_10mm.GetXaxis().SetBinLabel(3, "noMaterialVeto")
h_2GeV_10mm.GetXaxis().SetBinLabel(4, "noMuonHitSel")
h_2GeV_10mm.GetXaxis().SetBinLabel(5, "noMuonIPSel")
h_2GeV_10mm.GetXaxis().SetBinLabel(6, "All cuts")

c6 = ROOT.TCanvas('c6', '', 600, 500)
c6.cd()
h_2GeV_10mm.Draw('HIST')

output_filename = f'cuts_plots/{filename}'
c6.SaveAs(output_filename)
Image(filename=output_filename)
#
#
filename = "h_7GeV_10mm.png"
h_7GeV_10mm = ROOT.TH1F("h_7GeV_10mm", "mass = 7 GeV, ctau = 10mm", nbins, minx, maxx)

h_7GeV_10mm.SetTitle("mass = 7 GeV, ctau = 10mm")
h_7GeV_10mm.SetMinimum(0)

h_7GeV_10mm.Fill(0,1)
h_7GeV_10mm.Fill(1,sum_10mm_Cut1[7]/sum_10mm_noCuts[7])
h_7GeV_10mm.Fill(2,sum_10mm_Cut2[7]/sum_10mm_noCuts[7])
h_7GeV_10mm.Fill(3,sum_10mm_Cut3[7]/sum_10mm_noCuts[7])
h_7GeV_10mm.Fill(4,sum_10mm_Cut4[7]/sum_10mm_noCuts[7])
h_7GeV_10mm.Fill(5,sum_10mm_allCuts[7]/sum_10mm_noCuts[7])
#
h_7GeV_10mm.GetXaxis().SetBinLabel(1, "No cuts")
h_7GeV_10mm.GetXaxis().SetBinLabel(2, "noDiMuonAngularSel")
h_7GeV_10mm.GetXaxis().SetBinLabel(3, "noMaterialVeto")
h_7GeV_10mm.GetXaxis().SetBinLabel(4, "noMuonHitSel")
h_7GeV_10mm.GetXaxis().SetBinLabel(5, "noMuonIPSel")
h_7GeV_10mm.GetXaxis().SetBinLabel(6, "All cuts")

c7 = ROOT.TCanvas('c7', '', 600, 500)
c7.cd()
h_7GeV_10mm.Draw('HIST')

output_filename = f'cuts_plots/{filename}'
c7.SaveAs(output_filename)
Image(filename=output_filename)
#
#
filename = "h_10GeV_10mm.png"
h_10GeV_10mm = ROOT.TH1F("h_10GeV_10mm", "mass = 10 GeV, ctau = 10mm", nbins, minx, maxx)

h_10GeV_10mm.SetTitle("mass = 10 GeV, ctau = 10mm")
h_10GeV_10mm.SetMinimum(0)

h_10GeV_10mm.Fill(0,1)
h_10GeV_10mm.Fill(1,sum_10mm_Cut1[10]/sum_10mm_noCuts[10])
h_10GeV_10mm.Fill(2,sum_10mm_Cut2[10]/sum_10mm_noCuts[10])
h_10GeV_10mm.Fill(3,sum_10mm_Cut3[10]/sum_10mm_noCuts[10])
h_10GeV_10mm.Fill(4,sum_10mm_Cut4[10]/sum_10mm_noCuts[10])
h_10GeV_10mm.Fill(5,sum_10mm_allCuts[10]/sum_10mm_noCuts[10])
#
h_10GeV_10mm.GetXaxis().SetBinLabel(1, "No cuts")
h_10GeV_10mm.GetXaxis().SetBinLabel(2, "noDiMuonAngularSel")
h_10GeV_10mm.GetXaxis().SetBinLabel(3, "noMaterialVeto")
h_10GeV_10mm.GetXaxis().SetBinLabel(4, "noMuonHitSel")
h_10GeV_10mm.GetXaxis().SetBinLabel(5, "noMuonIPSel")
h_10GeV_10mm.GetXaxis().SetBinLabel(6, "All cuts")

c8 = ROOT.TCanvas('c8', '', 600, 500)
c8.cd()
h_10GeV_10mm.Draw('HIST')

output_filename = f'cuts_plots/{filename}'
c8.SaveAs(output_filename)
Image(filename=output_filename)
#
#
filename = "h_20GeV_10mm.png"
h_20GeV_10mm = ROOT.TH1F("h_20GeV_10mm", "mass = 20 GeV, ctau = 10mm", nbins, minx, maxx)

h_20GeV_10mm.SetTitle("mass = 20 GeV, ctau = 10mm")
h_20GeV_10mm.SetMinimum(0)

h_20GeV_10mm.Fill(0,1)
h_20GeV_10mm.Fill(1,sum_10mm_Cut1[20]/sum_10mm_noCuts[20])
h_20GeV_10mm.Fill(2,sum_10mm_Cut2[20]/sum_10mm_noCuts[20])
h_20GeV_10mm.Fill(3,sum_10mm_Cut3[20]/sum_10mm_noCuts[20])
h_20GeV_10mm.Fill(4,sum_10mm_Cut4[20]/sum_10mm_noCuts[20])
h_20GeV_10mm.Fill(5,sum_10mm_allCuts[20]/sum_10mm_noCuts[20])
#
h_20GeV_10mm.GetXaxis().SetBinLabel(1, "No cuts")
h_20GeV_10mm.GetXaxis().SetBinLabel(2, "noDiMuonAngularSel")
h_20GeV_10mm.GetXaxis().SetBinLabel(3, "noMaterialVeto")
h_20GeV_10mm.GetXaxis().SetBinLabel(4, "noMuonHitSel")
h_20GeV_10mm.GetXaxis().SetBinLabel(5, "noMuonIPSel")
h_20GeV_10mm.GetXaxis().SetBinLabel(6, "All cuts")

c9 = ROOT.TCanvas('c9', '', 600, 500)
c9.cd()
h_20GeV_10mm.Draw('HIST')

output_filename = f'cuts_plots/{filename}'
c9.SaveAs(output_filename)
Image(filename=output_filename)
#
#
filename = "h_30GeV_10mm.png"
h_30GeV_10mm = ROOT.TH1F("h_30GeV_10mm", "mass = 30 GeV, ctau = 10mm", nbins, minx, maxx)

h_30GeV_10mm.SetTitle("mass = 30 GeV, ctau = 10mm")
h_30GeV_10mm.SetMinimum(0)

h_30GeV_10mm.Fill(0,1)
h_30GeV_10mm.Fill(1,sum_10mm_Cut1[30]/sum_10mm_noCuts[30])
h_30GeV_10mm.Fill(2,sum_10mm_Cut2[30]/sum_10mm_noCuts[30])
h_30GeV_10mm.Fill(3,sum_10mm_Cut3[30]/sum_10mm_noCuts[30])
h_30GeV_10mm.Fill(4,sum_10mm_Cut4[30]/sum_10mm_noCuts[30])
h_30GeV_10mm.Fill(5,sum_10mm_allCuts[30]/sum_10mm_noCuts[30])
#
h_30GeV_10mm.GetXaxis().SetBinLabel(1, "No cuts")
h_30GeV_10mm.GetXaxis().SetBinLabel(2, "noDiMuonAngularSel")
h_30GeV_10mm.GetXaxis().SetBinLabel(3, "noMaterialVeto")
h_30GeV_10mm.GetXaxis().SetBinLabel(4, "noMuonHitSel")
h_30GeV_10mm.GetXaxis().SetBinLabel(5, "noMuonIPSel")
h_30GeV_10mm.GetXaxis().SetBinLabel(6, "All cuts")

c10 = ROOT.TCanvas('c10', '', 600, 500)
c10.cd()
h_30GeV_10mm.Draw('HIST')

output_filename = f'cuts_plots/{filename}'
c10.SaveAs(output_filename)
Image(filename=output_filename)
#
#
#
#
#
filename = "h_2GeV_1mm.png"
h_2GeV_1mm = ROOT.TH1F("h_2GeV_1mm", "mass = 2 GeV, ctau = 1mm", nbins, minx, maxx)

h_2GeV_1mm.SetTitle("mass = 2 GeV, ctau = 1mm")
h_2GeV_1mm.SetMinimum(0)

h_2GeV_1mm.Fill(0,1)
h_2GeV_1mm.Fill(1,sum_1mm_Cut1[2]/sum_1mm_noCuts[2])
h_2GeV_1mm.Fill(2,sum_1mm_Cut2[2]/sum_1mm_noCuts[2])
h_2GeV_1mm.Fill(3,sum_1mm_Cut3[2]/sum_1mm_noCuts[2])
h_2GeV_1mm.Fill(4,sum_1mm_Cut4[2]/sum_1mm_noCuts[2])
h_2GeV_1mm.Fill(5,sum_1mm_allCuts[2]/sum_1mm_noCuts[2])
#
h_2GeV_1mm.GetXaxis().SetBinLabel(1, "No cuts")
h_2GeV_1mm.GetXaxis().SetBinLabel(2, "noDiMuonAngularSel")
h_2GeV_1mm.GetXaxis().SetBinLabel(3, "noMaterialVeto")
h_2GeV_1mm.GetXaxis().SetBinLabel(4, "noMuonHitSel")
h_2GeV_1mm.GetXaxis().SetBinLabel(5, "noMuonIPSel")
h_2GeV_1mm.GetXaxis().SetBinLabel(6, "All cuts")

c11 = ROOT.TCanvas('c11', '', 600, 500)
c11.cd()
h_2GeV_1mm.Draw('HIST')

output_filename = f'cuts_plots/{filename}'
c11.SaveAs(output_filename)
Image(filename=output_filename)
#
#
filename = "h_7GeV_1mm.png"
h_7GeV_1mm = ROOT.TH1F("h_7GeV_1mm", "mass = 7 GeV, ctau = 1mm", nbins, minx, maxx)

h_7GeV_1mm.SetTitle("mass = 7 GeV, ctau = 1mm")
h_7GeV_1mm.SetMinimum(0)

h_7GeV_1mm.Fill(0,1)
h_7GeV_1mm.Fill(1,sum_1mm_Cut1[7]/sum_1mm_noCuts[7])
h_7GeV_1mm.Fill(2,sum_1mm_Cut2[7]/sum_1mm_noCuts[7])
h_7GeV_1mm.Fill(3,sum_1mm_Cut3[7]/sum_1mm_noCuts[7])
h_7GeV_1mm.Fill(4,sum_1mm_Cut4[7]/sum_1mm_noCuts[7])
h_7GeV_1mm.Fill(5,sum_1mm_allCuts[7]/sum_1mm_noCuts[7])
#
h_7GeV_1mm.GetXaxis().SetBinLabel(1, "No cuts")
h_7GeV_1mm.GetXaxis().SetBinLabel(2, "noDiMuonAngularSel")
h_7GeV_1mm.GetXaxis().SetBinLabel(3, "noMaterialVeto")
h_7GeV_1mm.GetXaxis().SetBinLabel(4, "noMuonHitSel")
h_7GeV_1mm.GetXaxis().SetBinLabel(5, "noMuonIPSel")
h_7GeV_1mm.GetXaxis().SetBinLabel(6, "All cuts")

c12 = ROOT.TCanvas('c12', '', 600, 500)
c12.cd()
h_7GeV_1mm.Draw('HIST')

output_filename = f'cuts_plots/{filename}'
c12.SaveAs(output_filename)
Image(filename=output_filename)
#
#
filename = "h_10GeV_1mm.png"
h_10GeV_1mm = ROOT.TH1F("h_10GeV_1mm", "mass = 10 GeV, ctau = 1mm", nbins, minx, maxx)

h_10GeV_1mm.SetTitle("mass = 10 GeV, ctau = 1mm")
h_10GeV_1mm.SetMinimum(0)

h_10GeV_1mm.Fill(0,1)
h_10GeV_1mm.Fill(1,sum_1mm_Cut1[10]/sum_1mm_noCuts[10])
h_10GeV_1mm.Fill(2,sum_1mm_Cut2[10]/sum_1mm_noCuts[10])
h_10GeV_1mm.Fill(3,sum_1mm_Cut3[10]/sum_1mm_noCuts[10])
h_10GeV_1mm.Fill(4,sum_1mm_Cut4[10]/sum_1mm_noCuts[10])
h_10GeV_1mm.Fill(5,sum_1mm_allCuts[10]/sum_1mm_noCuts[10])
#
h_10GeV_1mm.GetXaxis().SetBinLabel(1, "No cuts")
h_10GeV_1mm.GetXaxis().SetBinLabel(2, "noDiMuonAngularSel")
h_10GeV_1mm.GetXaxis().SetBinLabel(3, "noMaterialVeto")
h_10GeV_1mm.GetXaxis().SetBinLabel(4, "noMuonHitSel")
h_10GeV_1mm.GetXaxis().SetBinLabel(5, "noMuonIPSel")
h_10GeV_1mm.GetXaxis().SetBinLabel(6, "All cuts")

c13 = ROOT.TCanvas('c13', '', 600, 500)
c13.cd()
h_10GeV_1mm.Draw('HIST')

output_filename = f'cuts_plots/{filename}'
c13.SaveAs(output_filename)
Image(filename=output_filename)
#
#
filename = "h_20GeV_1mm.png"
h_20GeV_1mm = ROOT.TH1F("h_20GeV_1mm", "mass = 20 GeV, ctau = 1mm", nbins, minx, maxx)

h_20GeV_1mm.SetTitle("mass = 20 GeV, ctau = 1mm")
h_20GeV_1mm.SetMinimum(0)

h_20GeV_1mm.Fill(0,1)
h_20GeV_1mm.Fill(1,sum_1mm_Cut1[20]/sum_1mm_noCuts[20])
h_20GeV_1mm.Fill(2,sum_1mm_Cut2[20]/sum_1mm_noCuts[20])
h_20GeV_1mm.Fill(3,sum_1mm_Cut3[20]/sum_1mm_noCuts[20])
h_20GeV_1mm.Fill(4,sum_1mm_Cut4[20]/sum_1mm_noCuts[20])
h_20GeV_1mm.Fill(5,sum_1mm_allCuts[20]/sum_1mm_noCuts[20])
#
h_20GeV_1mm.GetXaxis().SetBinLabel(1, "No cuts")
h_20GeV_1mm.GetXaxis().SetBinLabel(2, "noDiMuonAngularSel")
h_20GeV_1mm.GetXaxis().SetBinLabel(3, "noMaterialVeto")
h_20GeV_1mm.GetXaxis().SetBinLabel(4, "noMuonHitSel")
h_20GeV_1mm.GetXaxis().SetBinLabel(5, "noMuonIPSel")
h_20GeV_1mm.GetXaxis().SetBinLabel(6, "All cuts")

c14 = ROOT.TCanvas('c14', '', 600, 500)
c14.cd()
h_20GeV_1mm.Draw('HIST')

output_filename = f'cuts_plots/{filename}'
c14.SaveAs(output_filename)
Image(filename=output_filename)
#
#
filename = "h_30GeV_1mm.png"
h_30GeV_1mm = ROOT.TH1F("h_30GeV_1mm", "mass = 30 GeV, ctau = 1mm", nbins, minx, maxx)

h_30GeV_1mm.SetTitle("mass = 30 GeV, ctau = 1mm")
h_30GeV_1mm.SetMinimum(0)

h_30GeV_1mm.Fill(0,1)
h_30GeV_1mm.Fill(1,sum_1mm_Cut1[30]/sum_1mm_noCuts[30])
h_30GeV_1mm.Fill(2,sum_1mm_Cut2[30]/sum_1mm_noCuts[30])
h_30GeV_1mm.Fill(3,sum_1mm_Cut3[30]/sum_1mm_noCuts[30])
h_30GeV_1mm.Fill(4,sum_1mm_Cut4[30]/sum_1mm_noCuts[30])
h_30GeV_1mm.Fill(5,sum_1mm_allCuts[30]/sum_1mm_noCuts[30])
#
h_30GeV_1mm.GetXaxis().SetBinLabel(1, "No cuts")
h_30GeV_1mm.GetXaxis().SetBinLabel(2, "noDiMuonAngularSel")
h_30GeV_1mm.GetXaxis().SetBinLabel(3, "noMaterialVeto")
h_30GeV_1mm.GetXaxis().SetBinLabel(4, "noMuonHitSel")
h_30GeV_1mm.GetXaxis().SetBinLabel(5, "noMuonIPSel")
h_30GeV_1mm.GetXaxis().SetBinLabel(6, "All cuts")



c15 = ROOT.TCanvas('c15', '', 600, 500)
c15.cd()
h_30GeV_1mm.Draw('HIST')

output_filename = f'cuts_plots/{filename}'
c15.SaveAs(output_filename)
Image(filename=output_filename)

'''


