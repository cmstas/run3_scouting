import ROOT
import os,sys,json
import argparse
from datetime import date
import numpy as np
import copy
import math
sys.path.append('utils')
#import plotUtils
from IPython.display import Image
import argparse
import os

ROOT.gStyle.SetOptStat(0)
ROOT.gROOT.SetBatch(1)

user = os.environ.get("USER")
#today = date.today().strftime("%b-%d-%Y")

parser = argparse.ArgumentParser()
parser.add_argument('directory', type=str)
args = parser.parse_args()
files = []
directory = args.directory
indir = directory
hname = 'histograms'
year = '2022'
luminosity = 3.51
#
latex = ROOT.TLatex()
latex.SetTextFont(42)
latex.SetTextAlign(31)
latex.SetTextSize(0.04)
latex.SetNDC(True)
#
latexCMS = ROOT.TLatex()
latexCMS.SetTextFont(61)
latexCMS.SetTextSize(0.055)
latexCMS.SetNDC(True)
#
latexCMSExtra = ROOT.TLatex()
latexCMSExtra.SetTextFont(52)
latexCMSExtra.SetTextSize(0.04)
latexCMSExtra.SetNDC(True)
#
latexExtra = ROOT.TLatex()
latexExtra.SetTextFont(42)
latexExtra.SetTextSize(0.034)
latexExtra.SetNDC(True)
#
latexExtraBold = ROOT.TLatex()
latexExtraBold.SetTextFont(62)
latexExtraBold.SetTextSize(0.034)
latexExtraBold.SetNDC(True)
#
cmsExtra = "Preliminary"
yearenergy = "%.2f fb^{-1} (%s, 13.6 TeV)"%(luminosity,year)
#directory = '/ceph/cms/store/user/garciaja/Run3ScoutingOutput/outputHistograms_Jun-06-2024_JPsi_lxy0p0to0p2/'
#directory = '/home/users/garciaja/run3Scouting/run3_scouting/outputHistograms_Jun-06-2024/'

for subdir in os.listdir(directory):
	if 'Jul-02' in subdir:
		full_subdir_path = os.path.join(directory, subdir, '')
		files = os.listdir(full_subdir_path)
		data_files = []
		summed_histogram_mass = None
		summed_histogram_umass = None
		summed_histogram_cowboy = None
		summed_histogram_seagull = None

		for filename in files:
			if 'Data' in filename:
				data_files.append(filename)

		for filename in data_files:
		#for filename in files:
			file = ROOT.TFile.Open(full_subdir_path + filename)
			hdimuon_mass = file.Get("hdimuon_mass")
			hdimuon_umass = file.Get("hdimuon_umass")
			hdimuon_cowboy = file.Get("hdimuon_cowboy")
			hdimuon_seagull = file.Get("hdimuon_seagull")
			if summed_histogram_mass is None:
				summed_histogram_mass = hdimuon_mass.Clone("summed_histogram_mass")
				summed_histogram_mass.SetDirectory(0)
			else:
				summed_histogram_mass.Add(hdimuon_mass)
			if summed_histogram_umass is None:
				summed_histogram_umass = hdimuon_umass.Clone("summed_histogram_umass")
				summed_histogram_umass.SetDirectory(0)
			else:
				summed_histogram_umass.Add(hdimuon_umass)
			if summed_histogram_cowboy is None:
				summed_histogram_cowboy = hdimuon_cowboy.Clone("summed_histogram_cowboy")
				summed_histogram_cowboy.SetDirectory(0)
			else:
				summed_histogram_cowboy.Add(hdimuon_cowboy)
			if summed_histogram_seagull is None:
				summed_histogram_seagull = hdimuon_seagull.Clone("summed_histogram_seagull")
				summed_histogram_seagull.SetDirectory(0)
			else:
				summed_histogram_seagull.Add(hdimuon_seagull)

		if '0p0to0p2' in subdir:
			ymax = 220000
			title = 'lxy = 0.0 cm to 0.2 cm'
			name = '0p0to0p2'
			xCMS = 0.2
		if '0p2to1p0' in subdir:
			ymax = 130000
			title = 'lxy = 0.2 cm to 1.0 cm'
			name = '0p2to1p0'
			xCMS = 0.2
		if '1p0to2p4' in subdir:
			ymax = 10000
			title = 'lxy = 1.0 cm to 2.4 cm'
			name = '1p0to2p4'
			xCMS = 0.115
		if '2p4to3p1' in subdir:
			ymax = 300
			title = 'lxy = 2.4 cm to 3.1 cm'
			name = '2p4to3p1'
			xCMS = 0.115
		if '3p1to7p0' in subdir:
			ymax = 130
			title = 'lxy = 3.1 cm to 7.0 cm'
			name = '3p1to7p0'
			xCMS = 0.115
		if '3p1to11p0' in subdir:
			ymax = 130
			title = 'lxy = 3.1 cm to 11.0 cm'
			name = '3p1to11p0'
			xCMS = 0.115
		if '7p0to11p0' in subdir:
			ymax = 7
			title = 'lxy = 7.0 cm to 11.0 cm'
			name = '7p0to11p0'
			xCMS = 0.115
		if '11p0to16p0' in subdir: 
			ymax = 5
			title = 'lxy = 11.0 cm to 16.0 cm'
			name = '11p0to16p0'
			xCMS = 0.115
		if '16p0to70p0' in subdir:
			ymax = 20
			title = 'lxy = 16.0 cm to 70.0 cm'
			name = '16p0to70p0'
			xCMS = 0.115	


		if not os.path.exists('JPsiPlots/'):
			os.mkdir('JPsiPlots/')

		c1 = ROOT.TCanvas('c1', '', 600, 500)
		c1.cd()
		summed_histogram_mass.GetXaxis().SetRangeUser(2.6,3.6)
		summed_histogram_mass.GetYaxis().SetRangeUser(0, ymax)
		summed_histogram_mass.SetLineColor(ROOT.kBlack)
		#summed_histogram_mass.SetTitle(title)
		#c1.SetLogy(True)
		summed_histogram_mass.Draw('HIST')
		summed_histogram_umass.SetLineColor(ROOT.kRed)
		summed_histogram_umass.Draw('HIST SAME')
		summed_histogram_seagull.SetLineColor(ROOT.kCyan)
		summed_histogram_seagull.Draw('HIST SAME')
		summed_histogram_cowboy.SetLineColor(ROOT.kOrange)
		summed_histogram_cowboy.Draw('HIST SAME')
		#ROOT.gStyle.SetOptTitle(0)
		#latex = ROOT.TLatex()
		#latex.SetTextSize(0.04)
		#latex.DrawLatexNDC(0.38, 0.92, title)
		'''
		box = ROOT.TBox (3.27, ymax*0.78, 3.59, ymax*0.85)
		box.SetFillStyle(0)
		box.SetLineColor(1)
		box.SetLineWidth(1)
		box.Draw()
		text = ROOT.TLatex(3.28,ymax*0.8, title)
		text.SetTextSize(0.03)
		text.SetTextFont(42)
		text.Draw()

		'''		
		legend = ROOT.TLegend(0.15, 0.6, 0.35, 0.8)
		legend.SetTextSize(0.04)
		legend.SetBorderSize(0) 
		legend.AddEntry(summed_histogram_mass, "Corrected mass", "l")
		legend.AddEntry(summed_histogram_umass, "Uncorrected mass", "l")
		legend.AddEntry(summed_histogram_seagull, "Seagull", "l")
		legend.AddEntry(summed_histogram_cowboy, "Cowboy", "l")
		legend.Draw()
		latexCMS.DrawLatex(xCMS,0.91,"CMS");
		latexCMSExtra.DrawLatex(xCMS + 0.12,0.91, cmsExtra);
		latex = ROOT.TLatex()
		latex.SetTextSize(0.04)
		latexExtra.DrawLatex(0.62, 0.91, yearenergy);


		output_filename = f'JPsiPlots/lxy_{name}.png'
		c1.SaveAs(output_filename)
		Image(filename=output_filename)
		#file.close()
'''

	if '-6p0_ctau-' in filename:
		file = ROOT.TFile.Open(directory + filename)
		#file = ROOT.TFile.Open(filename)
		#if '100mm' in filename:
		#	file.ls()

		hdimuon_mass = file.Get("hdimuon_mass")
		hdimuon_umass = file.Get("hdimuon_umass")
		if not os.path.exists('comparisonPlots/'):
			os.mkdir('comparisonPlots/')

		if '100mm' in filename:
			ymax = 3
			if 'post' in filename:
				title = 'Dimuon mass comparison. ctau = 100mm, postEE'
			else:
				title = 'Dimuon mass comparison. ctau = 100mm'
		elif '10mm' in filename:
			ymax = 10
			if 'post' in filename:
				title = 'Dimuon mass comparison. ctau = 10mm, postEE'
			else:
				title = 'Dimuon mass comparison. ctau = 10mm'
		elif '1mm' in filename:
			ymax = 21
			if 'post' in filename:
				title = 'Dimuon mass comparison. ctau = 1mm, postEE'
			else:
				title = 'Dimuon mass comparison. ctau = 1mm'
		
		c1 = ROOT.TCanvas('c1', '', 600, 500)
		c1.cd()
		hdimuon_mass.GetXaxis().SetRangeUser(4,8)
		hdimuon_mass.GetYaxis().SetRangeUser(0, ymax)
		hdimuon_mass.GetXaxis().SetTitle("Mass (GeV)")
		hdimuon_mass.GetYaxis().SetTitle("Events/0.05")
		hdimuon_mass.SetLineColor(ROOT.kRed)
		hdimuon_mass.SetTitle(title)
		#c1.SetLogy()
		hdimuon_mass.Draw('HIST')
		hdimuon_umass.SetLineColor(ROOT.kBlue)
		hdimuon_umass.Draw('HIST, SAME')
		legend = ROOT.TLegend(0.15, 0.7, 0.35, 0.8)
		legend.AddEntry(hdimuon_mass, "Corrected mass", "l")
		legend.AddEntry(hdimuon_umass, "Uncorrected mass", "l")
		legend.Draw()
		
		filename = filename.replace('.root', '')
		output_filename = f'comparisonPlots/hdimuon_mass_comparison_{filename}.png'
		c1.SaveAs(output_filename)
		Image(filename=output_filename)

	
'''
