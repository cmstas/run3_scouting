import ROOT
import os,sys,json,copy
from datetime import date    
import numpy as np
import argparse
from tqdm import tqdm
from DataFormats.FWLite import Events, Handle
import mplhep as hep
import matplotlib.pyplot as plt
import correctionlib.schemav2 as cs

MUON_MASS = 0.10566
user = os.environ.get("USER")
today= date.today().strftime("%b-%d-%Y")
hep.style.use("CMS")

def getValues(histo):
    values = []
    bins = []
    for n in range(1, histo.GetNbinsX()+1):
        values.append(histo.GetBinContent(n))
        bins.append(histo.GetBinLowEdge(n))
    bins.append(histo.GetBinLowEdge(n) + histo.GetBinWidth(n))
    return np.array(values), np.array(bins)

def get2DValues(histo):
    nbins_x = histo.GetNbinsX()
    nbins_y = histo.GetNbinsY()
    values = np.zeros((nbins_x, nbins_y))
    x_edges = np.zeros(nbins_x + 1)
    y_edges = np.zeros(nbins_y + 1)
    for i in range(1, nbins_x + 1):
        for j in range(1, nbins_y + 1):
            values[i-1,j-1] = histo.GetBinContent(i,j)
    for i in range(1, nbins_x+1):
        x_edges[i-1] = histo.GetXaxis().GetBinLowEdge(i)
    for j in range(1, nbins_y+1):
        y_edges[j-1] = histo.GetYaxis().GetBinLowEdge(j)
    x_edges[-1] = histo.GetXaxis().GetBinUpEdge(nbins_x)
    y_edges[-1] = histo.GetYaxis().GetBinUpEdge(nbins_y)
    return values, x_edges, y_edges

### From Pythia
inDir = '/ceph/cms/store/user/$USER/Run3ScoutingOutput/B-Studies'
listOfFiles = []
listOfFiles.append(f'{inDir}/histograms_GEN_0p3.root')
listOfFiles.append(f'{inDir}/histograms_GEN_0p4.root')
listOfFiles.append(f'{inDir}/histograms_GEN_0p5.root')
listOfFiles.append(f'{inDir}/histograms_GEN_0p6.root')
listOfFiles.append(f'{inDir}/histograms_GEN_0p7.root')
listOfFiles.append(f'{inDir}/histograms_GEN_0p9.root')
listOfFiles.append(f'{inDir}/histograms_GEN_1p25.root')
listOfFiles.append(f'{inDir}/histograms_GEN_1p5.root')
listOfFiles.append(f'{inDir}/histograms_GEN_2p0.root')
listOfFiles.append(f'{inDir}/histograms_GEN_2p85.root')
listOfFiles.append(f'{inDir}/histograms_GEN_3p35.root')
listOfFiles.append(f'{inDir}/histograms_GEN_4p0.root')
for p,path in enumerate(listOfFiles):
    file_pythia = ROOT.TFile(path)
    if p==0:
        h_bhadron_pt_filtered = copy.deepcopy(file_pythia.Get('h_bhadron_pt_filtered').Clone())
        h_bhadron_pt = copy.deepcopy(file_pythia.Get('h_bhadron_pt').Clone())
        h_bhadron_eta = copy.deepcopy(file_pythia.Get('h_bhadron_eta').Clone())
    else:
        h_bhadron_pt_filtered.Add(file_pythia.Get('h_bhadron_pt_filtered'))
        h_bhadron_pt.Add(file_pythia.Get('h_bhadron_pt'))
        h_bhadron_eta.Add(file_pythia.Get('h_bhadron_eta'))


#file_pythia = ROOT.TFile('/home/users/fernance/Run3-Analyses/SnT-Scouting/Code/Final/run3_scouting/plotsGeneration_Aug-19-2025/histograms_GEN_2p0.root')
#h_bhadron_pt_filtered = file_pythia.Get('h_bhadron_pt_filtered')
#h_bhadron_pt = file_pythia.Get('h_bhadron_pt')
#h_bhadron_eta = file_pythia.Get('h_bhadron_eta')

h_bhadron_pt_filtered.Scale(1./h_bhadron_pt_filtered.GetEntries())
h_bhadron_pt.Scale(4.46e8/h_bhadron_pt.GetEntries())
h_bhadron_eta.Scale(4.46e8/h_bhadron_eta.GetEntries())

### From FONLL (inclusive)
# ebeam1 = 6800, ebeam2 = 6800
# PDF set = NNPDF30_nlo_as_0118
# ptmin = 0
# ptmax = 300
# etamin = -8
# etamax = 8
# Uncertainties from scales
# cross section is ds/dpt (pb/GeV)

# PT:
ipt = np.array([
0.0000, 0.5008, 1.0017, 1.5025, 2.0033, 2.5042, 3.0050, 3.5058, 4.0067, 4.5075,
5.0083, 5.5092, 6.0100, 6.5109, 7.0117, 7.5125, 8.0134, 8.5142, 9.0150, 9.5159,
10.0167, 10.5175, 11.0184, 11.5192, 12.0200, 12.5209, 13.0217, 13.5225, 14.0234,
14.5242, 15.0250, 15.5259, 16.0267, 16.5275, 17.0284, 17.5292, 18.0301, 18.5309,
19.0317, 19.5326, 20.0334, 20.5342, 21.0351, 21.5359, 22.0367, 22.5376, 23.0384,
23.5392, 24.0401, 24.5409, 25.0417, 25.5426, 26.0434, 26.5442, 27.0451, 27.5459,
28.0467, 28.5476, 29.0484, 29.5492, 30.0501, 30.5509, 31.0518, 31.5526, 32.0534,
32.5543, 33.0551, 33.5559, 34.0568, 34.5576, 35.0584, 35.5593, 36.0601, 36.5609,
37.0618, 37.5626, 38.0634, 38.5643, 39.0651, 39.5659, 40.0668
])

icentral = np.array([
0.0000e+00, 2.1895e+07, 4.0966e+07, 5.4774e+07, 6.3155e+07, 6.6895e+07, 6.6960e+07,
6.4348e+07, 5.9977e+07, 5.4627e+07, 4.8904e+07, 4.3233e+07, 3.7882e+07, 3.2995e+07,
2.8632e+07, 2.4796e+07, 2.1459e+07, 1.8576e+07, 1.6095e+07, 1.3967e+07, 1.2142e+07,
1.0577e+07, 9.2347e+06, 8.0822e+06, 7.0963e+06, 6.2399e+06, 5.4994e+06, 4.8584e+06,
4.3025e+06, 3.8198e+06, 3.3986e+06, 3.0300e+06, 2.7069e+06, 2.4231e+06, 2.1734e+06,
1.9532e+06, 1.7588e+06, 1.5865e+06, 1.4336e+06, 1.2975e+06, 1.1763e+06, 1.0681e+06,
9.7131e+05, 8.8463e+05, 8.0688e+05, 7.3698e+05, 6.7405e+05, 6.1730e+05, 5.6605e+05,
5.1969e+05, 4.7771e+05, 4.3963e+05, 4.0505e+05, 3.7361e+05, 3.4498e+05, 3.1889e+05,
2.9508e+05, 2.7331e+05, 2.5340e+05, 2.3517e+05, 2.1845e+05, 2.0311e+05, 1.8901e+05,
1.7604e+05, 1.6411e+05, 1.5311e+05, 1.4296e+05, 1.3360e+05, 1.2494e+05, 1.1694e+05,
1.0953e+05, 1.0266e+05, 9.6288e+04, 9.0376e+04, 8.4885e+04, 7.9780e+04, 7.5031e+04,
7.0610e+04, 6.6491e+04, 6.2651e+04, 5.9069e+04
])

iminv = np.array([
0.0000e+00, 1.1418e+07, 2.1956e+07, 3.0072e+07, 3.5494e+07, 3.8449e+07, 3.9329e+07,
3.8598e+07, 3.6732e+07, 3.4153e+07, 3.1203e+07, 2.8140e+07, 2.5137e+07, 2.2280e+07,
1.9629e+07, 1.7286e+07, 1.5303e+07, 1.3449e+07, 1.1777e+07, 1.0331e+07, 9.0821e+06,
7.9902e+06, 7.0378e+06, 6.1807e+06, 5.4447e+06, 4.8035e+06, 4.2474e+06, 3.7644e+06,
3.3444e+06, 2.9785e+06, 2.6583e+06, 2.3773e+06, 2.1301e+06, 1.9124e+06, 1.7203e+06,
1.5504e+06, 1.3999e+06, 1.2662e+06, 1.1471e+06, 1.0409e+06, 9.4602e+05, 8.6109e+05,
7.8494e+05, 7.1656e+05, 6.5506e+05, 5.9964e+05, 5.4961e+05, 5.0439e+05, 4.6346e+05,
4.2635e+05, 3.9267e+05, 3.6206e+05, 3.3420e+05, 3.0882e+05, 2.8566e+05, 2.6452e+05,
2.4517e+05, 2.2747e+05, 2.1124e+05, 1.9634e+05, 1.8266e+05, 1.7009e+05, 1.5851e+05,
1.4785e+05, 1.3802e+05, 1.2894e+05, 1.2056e+05, 1.1281e+05, 1.0563e+05, 9.8985e+04,
9.2822e+04, 8.7104e+04, 8.1794e+04, 7.6859e+04, 7.2269e+04, 6.7996e+04, 6.4017e+04,
6.0308e+04, 5.6848e+04, 5.3619e+04, 5.0602e+04
])

imaxv = np.array([
0.0000e+00, 3.3011e+07, 6.0776e+07, 7.9950e+07, 9.0991e+07, 9.5638e+07, 9.5452e+07,
9.1744e+07, 8.5639e+07, 7.8122e+07, 7.0003e+07, 6.1890e+07, 5.4183e+07, 4.7114e+07,
4.0784e+07, 3.5213e+07, 3.0367e+07, 2.6184e+07, 2.2594e+07, 1.9520e+07, 1.6893e+07,
1.4648e+07, 1.2730e+07, 1.1089e+07, 9.6913e+06, 8.4822e+06, 7.4413e+06, 6.5438e+06,
5.7690e+06, 5.0990e+06, 4.5172e+06, 4.0102e+06, 3.5677e+06, 3.1807e+06, 2.8415e+06,
2.5437e+06, 2.2817e+06, 2.0506e+06, 1.8462e+06, 1.6651e+06, 1.5044e+06, 1.3614e+06,
1.2340e+06, 1.1203e+06, 1.0186e+06, 9.2748e+05, 8.4575e+05, 7.7230e+05, 7.0618e+05,
6.4657e+05, 5.9276e+05, 5.4409e+05, 5.0003e+05, 4.6008e+05, 4.2382e+05, 3.9084e+05,
3.6083e+05, 3.3347e+05, 3.0850e+05, 2.8568e+05, 2.6482e+05, 2.4571e+05, 2.2820e+05,
2.1213e+05, 1.9737e+05, 1.8380e+05, 1.7131e+05, 1.5980e+05, 1.4918e+05, 1.3939e+05,
1.3033e+05, 1.2196e+05, 1.1421e+05, 1.0703e+05, 1.0038e+05, 9.4200e+04, 8.8466e+04,
8.3136e+04, 7.8180e+04, 7.3568e+04, 6.9272e+04
])

# ETA:
ieta = np.array([
   -8.0000, -7.8400, -7.6800, -7.5200, -7.3600, -7.2000, -7.0400, -6.8800,
   -6.7200, -6.5600, -6.4000, -6.2400, -6.0800, -5.9200, -5.7600, -5.6000,
   -5.4400, -5.2800, -5.1200, -4.9600, -4.8000, -4.6400, -4.4800, -4.3200,
   -4.1600, -4.0000, -3.8400, -3.6800, -3.5200, -3.3600, -3.2000, -3.0400,
   -2.8800, -2.7200, -2.5600, -2.4000, -2.2400, -2.0800, -1.9200, -1.7600,
   -1.6000, -1.4400, -1.2800, -1.1200, -0.9600, -0.8000, -0.6400, -0.4800,
   -0.3200, -0.1600,  0.0000,  0.1600,  0.3200,  0.4800,  0.6400,  0.8000,
    0.9600,  1.1200,  1.2800,  1.4400,  1.6000,  1.7600,  1.9200,  2.0800,
    2.2400,  2.4000,  2.5600,  2.7200,  2.8800,  3.0400,  3.2000,  3.3600,
    3.5200,  3.6800,  3.8400,  4.0000,  4.1600,  4.3200,  4.4800,  4.6400,
    4.8000,  4.9600,  5.1200,  5.2800,  5.4400,  5.6000,  5.7600,  5.9200,
    6.0800,  6.2400,  6.4000,  6.5600,  6.7200,  6.8800,  7.0400,  7.2000,
    7.3600,  7.5200,  7.6800,  7.8400,  8.0000
])

icentral_eta = np.array([
   6.4930e+05, 8.5290e+05, 1.1100e+06, 1.4360e+06, 1.8490e+06, 2.3590e+06,
   2.9690e+06, 3.6870e+06, 4.5160e+06, 5.4620e+06, 6.5420e+06, 7.7550e+06,
   9.0930e+06, 1.0550e+07, 1.2130e+07, 1.3810e+07, 1.5570e+07, 1.7410e+07,
   1.9320e+07, 2.1270e+07, 2.4020e+07, 2.5250e+07, 2.7250e+07, 2.9240e+07,
   3.1180e+07, 3.3100e+07, 3.4960e+07, 3.6770e+07, 3.8500e+07, 4.0140e+07,
   4.1690e+07, 4.3130e+07, 4.4450e+07, 4.5610e+07, 4.6610e+07, 4.7410e+07,
   4.7990e+07, 4.8340e+07, 4.8440e+07, 4.8280e+07, 4.7860e+07, 4.7190e+07,
   4.6300e+07, 4.5220e+07, 4.4030e+07, 4.2790e+07, 4.1590e+07, 4.0530e+07,
   3.9700e+07, 3.9170e+07, 3.8980e+07, 3.9170e+07, 3.9700e+07, 4.0530e+07,
   4.1590e+07, 4.2790e+07, 4.4030e+07, 4.5220e+07, 4.6300e+07, 4.7190e+07,
   4.7860e+07, 4.8280e+07, 4.8440e+07, 4.8340e+07, 4.7990e+07, 4.7410e+07,
   4.6610e+07, 4.5610e+07, 4.4450e+07, 4.3130e+07, 4.1690e+07, 4.0140e+07,
   3.8500e+07, 3.6770e+07, 3.4960e+07, 3.3100e+07, 3.1180e+07, 2.9240e+07,
   2.7250e+07, 2.5250e+07, 2.4020e+07, 2.1270e+07, 1.9320e+07, 1.7410e+07,
   1.5570e+07, 1.3810e+07, 1.2130e+07, 1.0550e+07, 9.0930e+06, 7.7550e+06,
   6.5420e+06, 5.4620e+06, 4.5160e+06, 3.6870e+06, 2.9690e+06, 2.3590e+06,
   1.8490e+06, 1.4360e+06, 1.1100e+06, 8.5290e+05, 6.4930e+05
])

iminv_eta = np.array([
   4.7500e+05, 6.1250e+05, 7.9820e+05, 1.0350e+06, 1.3270e+06, 1.6860e+06,
   2.1140e+06, 2.6160e+06, 3.1920e+06, 3.8420e+06, 4.5770e+06, 5.3980e+06,
   6.2960e+06, 7.2680e+06, 8.3120e+06, 9.4120e+06, 1.0550e+07, 1.1730e+07,
   1.2940e+07, 1.4160e+07, 1.5390e+07, 1.6610e+07, 1.7820e+07, 1.9000e+07,
   2.0160e+07, 2.1280e+07, 2.2360e+07, 2.3390e+07, 2.4370e+07, 2.5300e+07,
   2.6170e+07, 2.6980e+07, 2.7720e+07, 2.8390e+07, 2.8970e+07, 2.9440e+07,
   2.9800e+07, 3.0030e+07, 3.0120e+07, 3.0070e+07, 2.9870e+07, 2.9520e+07,
   2.9040e+07, 2.8460e+07, 2.7790e+07, 2.7090e+07, 2.6410e+07, 2.5810e+07,
   2.5600e+07, 2.5290e+07, 2.5180e+07, 2.5290e+07, 2.5600e+07, 2.5810e+07,
   2.6410e+07, 2.7090e+07, 2.7790e+07, 2.8460e+07, 2.9040e+07, 2.9520e+07,
   2.9870e+07, 3.0070e+07, 3.0120e+07, 3.0030e+07, 2.9800e+07, 2.9440e+07,
   2.8970e+07, 2.8390e+07, 2.7720e+07, 2.6980e+07, 2.6170e+07, 2.5300e+07,
   2.4370e+07, 2.3390e+07, 2.2360e+07, 2.1280e+07, 2.0160e+07, 1.9000e+07,
   1.7820e+07, 1.6610e+07, 1.5390e+07, 1.4160e+07, 1.2940e+07, 1.1730e+07,
   1.0550e+07, 9.4120e+06, 8.3120e+06, 7.2680e+06, 6.2960e+06, 5.3980e+06,
   4.5770e+06, 3.8420e+06, 3.1920e+06, 2.6160e+06, 2.1140e+06, 1.6860e+06,
   1.3270e+06, 1.0350e+06, 7.9820e+05, 6.1250e+05, 4.7500e+05
])

imaxv_eta = np.array([
   9.8270e+05, 1.2880e+06, 1.6720e+06, 2.1570e+06, 2.7680e+06, 3.5210e+06,
   4.4190e+06, 5.7520e+06, 6.6880e+06, 8.0700e+06, 9.6410e+06, 1.1410e+07,
   1.3340e+07, 1.5440e+07, 1.7710e+07, 2.0110e+07, 2.2630e+07, 2.5260e+07,
   2.7970e+07, 3.0740e+07, 3.3550e+07, 3.6370e+07, 3.9180e+07, 4.1980e+07,
   4.4740e+07, 4.7430e+07, 5.0020e+07, 5.2530e+07, 5.4940e+07, 5.7230e+07,
   5.9380e+07, 6.1370e+07, 6.3180e+07, 6.4770e+07, 6.6130e+07, 6.7210e+07,
   6.7980e+07, 6.8420e+07, 6.8510e+07, 6.8230e+07, 6.7590e+07, 6.6590e+07,
   6.5290e+07, 6.3730e+07, 6.2000e+07, 6.0220e+07, 5.8500e+07, 5.6980e+07,
   5.5790e+07, 5.5030e+07, 5.4760e+07, 5.5030e+07, 5.5790e+07, 5.6980e+07,
   5.8500e+07, 6.0220e+07, 6.2000e+07, 6.3730e+07, 6.5290e+07, 6.6590e+07,
   6.7590e+07, 6.8230e+07, 6.8510e+07, 6.8420e+07, 6.7980e+07, 6.7210e+07,
   6.6130e+07, 6.4770e+07, 6.3180e+07, 6.1370e+07, 5.9380e+07, 5.7230e+07,
   5.4940e+07, 5.2530e+07, 5.0020e+07, 4.7430e+07, 4.4740e+07, 4.1980e+07,
   3.9180e+07, 3.6370e+07, 3.3550e+07, 3.0740e+07, 2.7970e+07, 2.5260e+07,
   2.2630e+07, 2.0110e+07, 1.7710e+07, 1.5440e+07, 1.3340e+07, 1.1410e+07,
   9.6410e+06, 8.0700e+06, 6.6880e+06, 5.7520e+06, 4.4190e+06, 3.5210e+06,
   2.7680e+06, 2.1570e+06, 1.6720e+06, 1.2880e+06, 9.8270e+05
])

### From FONLL (fiducial)
# ebeam1 = 6800, ebeam2 = 6800
# PDF set = NNPDF30_nlo_as_0118
# ptmin = 5.5
# ptmax = 39.5
# etamin = -2.8
# etamax = 2.8
# Uncertainties from scales
# cross section is ds/dpt (pb/GeV)

pt = np.array([
    5.5, 6.5, 7.5, 8.5, 9.5, 10.5, 11.5, 12.5, 13.5, 14.5,
    15.5, 16.5, 17.5, 18.5, 19.5, 20.5, 21.5, 22.5, 23.5, 24.5,
    25.5, 26.5, 27.5, 28.5, 29.5, 30.5, 31.5, 32.5, 33.5, 34.5,
    35.5, 36.5, 37.5, 38.5, 39.5
])
#
central = np.array([
    2.7222e+07, 2.1760e+07, 1.6947e+07, 1.3064e+07, 1.0056e+07,
    7.7682e+06, 6.0379e+06, 4.7283e+06, 3.7309e+06, 2.9684e+06,
    2.3802e+06, 1.9222e+06, 1.5635e+06, 1.2806e+06, 1.0555e+06,
    8.7522e+05, 7.2988e+05, 6.1199e+05, 5.1576e+05, 4.3674e+05,
    3.7152e+05, 3.1739e+05, 2.7227e+05, 2.3449e+05, 2.0270e+05,
    1.7584e+05, 1.5305e+05, 1.3364e+05, 1.1705e+05, 1.0282e+05,
    9.0582e+04, 8.0014e+04, 7.0862e+04, 6.2912e+04, 5.5986e+04
])
#
minv = np.array([
    1.7020e+07, 1.4214e+07, 1.1489e+07, 9.2396e+06, 7.2856e+06,
    5.7610e+06, 4.5618e+06, 3.6319e+06, 2.8915e+06, 2.3153e+06,
    1.8679e+06, 1.5176e+06, 1.2415e+06, 1.0224e+06, 8.4709e+05,
    7.0589e+05, 5.9146e+05, 4.9817e+05, 4.2163e+05, 3.5848e+05,
    3.0612e+05, 2.6249e+05, 2.2597e+05, 1.9526e+05, 1.6932e+05,
    1.4732e+05, 1.2860e+05, 1.1260e+05, 9.8881e+04, 8.7081e+04,
    7.6898e+04, 6.8082e+04, 6.0427e+04, 5.3759e+04, 4.7937e+04
])
#
maxv = np.array([
    3.8933e+07, 3.1053e+07, 2.4058e+07, 1.8409e+07, 1.4051e+07,
    1.0755e+07, 8.2816e+06, 6.4252e+06, 5.0234e+06, 3.9611e+06,
    3.1490e+06, 2.5222e+06, 2.0352e+06, 1.6543e+06, 1.3538e+06,
    1.1149e+06, 9.2371e+05, 7.6968e+05, 6.4485e+05, 5.4303e+05,
    4.5949e+05, 3.9057e+05, 3.3343e+05, 2.8584e+05, 2.4602e+05,
    2.1253e+05, 1.8426e+05, 1.6030e+05, 1.3990e+05, 1.2248e+05,
    1.0754e+05, 9.4697e+04, 8.3615e+04, 7.4023e+04, 6.5696e+04
])


### Get weights for normalization and plots
#
fig, ax = plt.subplots(1, 1, figsize=(11, 8))
hep.cms.label("", data=False, year='', com='13.6', ax=ax)
hist, edges = getValues(h_bhadron_pt)
ax.plot(ipt, icentral, color='#e42536', label="FONLL central")
ax.fill_between(ipt, iminv, imaxv, color='#e42536', label=r'FONLL central uncertainty', zorder=1, alpha=0.3) 
hep.histplot(hist, edges, color='#5790fc', histtype="step", ax=ax, label="Pythia")
ax.set_yscale('log')
ax.set_xlabel(r'B-hadron $p_{T}$ (GeV)')
ax.set_ylabel(r'$d\sigma/dp_{T}$ (pb/GeV)')
ax.text(25, 5e6, 'Inclusive', fontsize=22, fontstyle='italic')
ax.set_xlim(0, 40)
ax.legend()
fig.savefig("python/B-norm/B-hadron_inclusive_pt.png", dpi=140)
#
fig, ax = plt.subplots(1, 1, figsize=(11, 8))
hep.cms.label("", data=False, year='', com='13.6', ax=ax)
hist, edges = getValues(h_bhadron_eta)
ax.plot(ieta, icentral_eta, color='#e42536', label="FONLL central")
ax.fill_between(ieta, iminv_eta, imaxv_eta, color='#e42536', label=r'FONLL central uncertainty', zorder=1, alpha=0.3) 
hep.histplot(hist, edges, color='#5790fc', histtype="step", ax=ax, label="Pythia")
ax.set_yscale('log')
ax.set_xlabel(r'B-hadron $p_{T}$ (GeV)')
ax.set_ylabel(r'$d\sigma/dp_{T}$ (pb/GeV)')
ax.text(6, 5e6, 'Inclusive', fontsize=22, fontstyle='italic')
ax.set_xlim(-8, 8)
ax.legend()
fig.savefig("python/B-norm/B-hadron_inclusive_eta.png", dpi=140)
#

## Normalization for efficiency(m) of the gen filter
# h_counts_1b
# h_counts_sel1b
masses = [0.3, 0.4, 0.5, 0.6, 0.7, 0.9, 1.25, 1.5, 2.0, 2.85, 3.35, 4.0]
efficiencies = []
for p,path in enumerate(listOfFiles):
    file_pythia = ROOT.TFile(path)
    den = file_pythia.Get("h_counts_1b").GetEntries()
    num = file_pythia.Get("h_counts_sel1b").GetEntries()
    print(den, num, num/den)
    efficiencies.append(num/den)
#
masses.append(4.6)
efficiencies.append(0.5748189563275079) # Assuming linearity with the previous two points
print(masses)
print(efficiencies)
fig, ax = plt.subplots(1, 1, figsize=(11, 8))
hep.cms.label("", data=False, year='', com='13.6', ax=ax)
hist, edges = getValues(h_bhadron_eta)
ax.plot(masses, efficiencies, color='darkgoldenrod')
ax.set_xlabel(r'$\phi$ mass (GeV)')
ax.set_ylabel(r'Kinematic gen-filter efficiency $\epsilon(m)$')
ax.text(0.5, 0.5, '$p_{T}^{B}$ > 5 GeV, $|\eta^{B}|$ < 2.8', fontsize=22)
ax.set_xlim(0.0, 5.0)
ax.set_ylim(0.0, 1.0)
ax.legend()
fig.savefig("python/B-norm/B-hadron_genFilter-efficiency.png", dpi=140)


### Import reweighting in correctionlib defining the weights

XSEC_FID = 1.289e8

fig, ax = plt.subplots(1, 1, figsize=(11, 8))
hep.cms.label("", data=False, year='', com='13.6', ax=ax)
hist, edges = getValues(h_bhadron_pt_filtered)
ax.fill_between(pt, minv/XSEC_FID, maxv/XSEC_FID, color='#e42536', label=r'FONLL central uncertainty', zorder=1, alpha=0.3) 
ax.plot(pt, central/XSEC_FID, color='#e42536', label="FONLL central")
hep.histplot(hist, edges, color='#5790fc', histtype="step", ax=ax, label="Pythia")
ax.set_xlabel(r'B-hadron $p_{T}$ (GeV)')
ax.set_ylabel(r'Shape $d\sigma/dp_{T}$ (GeV$^{-1}$)')
ax.text(20, 0.20, '$p_{T}^{B}$ > 5 GeV, $|\eta^{B}|$ < 2.8', fontsize=22)
ax.set_xlim(5, 40)
ax.legend()
fig.savefig("python/B-norm/B-hadron_shape-only.png", dpi=140)
#
fig, ax = plt.subplots(1, 1, figsize=(11, 8))
hep.cms.label("", data=False, year='', com='13.6', ax=ax)
hist, edges = getValues(h_bhadron_pt_filtered)
ax.fill_between(pt, minv/XSEC_FID/(hist), maxv/XSEC_FID/(hist), color='#e42536', label=r'FONLL central uncertainty', zorder=1, alpha=0.3) 
hep.histplot((central/XSEC_FID)/(hist), edges, color='red', histtype="step", ax=ax, label="FONLL central/Pythia")
ax.set_xlabel(r'B-hadron $p_{T}$ (GeV)')
ax.set_ylabel(r'Weight function $w(p_T)$')
ax.set_xlim(5, 40)
ax.set_ylim(0.0, 2.5)
ax.text(20, 1.75, '$p_{T}^{B}$ > 5 GeV, $|\eta^{B}|$ < 2.8', fontsize=22)
ax.legend()
fig.savefig("python/B-norm/B-hadron_weights.png", dpi=140)

# Acceptance plots
#
def plotHistogram2D(name, histo, label, xaxis = '', yaxis=''):  
    plt.style.use(hep.style.CMS)  
    values, x_edges, y_edges = get2DValues(histo)
    fig, ax = plt.subplots(figsize=(10, 7))
    #im = ax.imshow(
    #    values.T, 
    #    extent=[x_edges[0], x_edges[-1], y_edges[0], y_edges[-1]],
    #    origin='lower',
    #    cmap="viridis"
    #)
    #cbar = fig.colorbar(im, ax=ax, pad=0.01)
    #cbar.set_label("Yield", fontsize=18)
    #cbar.ax.tick_params(labelsize=14, width=1.5)
    #cbar.outline.set_linewidth(1.5)

    X, Y = np.meshgrid(x_edges, y_edges, indexing="ij")
    pcm = ax.pcolormesh(X, Y, values, cmap="viridis")

    cbar = fig.colorbar(pcm, ax=ax, pad=0.01)
    cbar.set_label("Entries", fontsize=16)
    
    hep.cms.label("", data=False, year='', com='13.6', ax=ax)
    ax.set_xlabel(xaxis, fontsize=18, labelpad=10)
    ax.set_ylabel(yaxis, fontsize=18, labelpad=10)
    ax.tick_params(axis='both', which='major', labelsize=14, width=1.5)  # Ticks principales
    ax.tick_params(axis='both', which='minor', labelsize=14, width=1.5)
    ax.legend(title=label, fontsize=12, frameon=True, loc='lower right', title_fontsize=12)
    ax.spines["left"].set_linewidth(1.5)
    ax.spines["right"].set_linewidth(1.5)
    ax.spines["top"].set_linewidth(1.5)
    ax.spines["bottom"].set_linewidth(1.5)
    fig.savefig('python/B-norm/'+name+".png", dpi=140)
#
masses = [0.3, 0.4, 0.5, 0.6, 0.7, 0.9, 1.25, 1.5, 2.0, 2.85, 3.35, 4.0]
masses = [2.0]
efficiencies = []
histos = []
histos.append("acc_parent_pt_eta_level1")
histos.append("acc_nonparent_pt_eta_level1")
histos.append("acc_parent_pt_eta_level2")
histos.append("acc_nonparent_pt_eta_level2")
histos.append("acc_parent_pt_eta_level3")
histos.append("acc_nonparent_pt_eta_level3")
for p,path in enumerate([f'{inDir}/histograms_GEN_2p0.root']):
    file_pythia = ROOT.TFile(path)
    for h in histos:
        plot = file_pythia.Get(h)
        plotHistogram2D(h + "_%.2f"%masses[p], plot, '', xaxis = r'B-hadron $p_{T}$ (GeV)', yaxis='B-hadron $|\eta|$')

    plot = file_pythia.Get('acc_summary')
    fig, ax = plt.subplots(1, 1, figsize=(11, 8))
    hep.cms.label("", data=False, year='', com='13.6', ax=ax)
    histi, edgesi = getValues(plot)
    hep.histplot(histi, edgesi, color='#5790fc', histtype="step", ax=ax)
    ax.set_xlabel(r'B-hadron category (0 = 1 in acc, 1 = 2 in acc)')
    ax.set_ylabel(r'Number of events')
    fig.savefig("python/B-norm/B-hadron_acceptance.png", dpi=140)


pt_edges = [x for x in edges] + [1e9]
w_nom = [x for x in ((central/XSEC_FID)/(hist)) ] + [((central/XSEC_FID)/(hist))[-1]]
w_up = [x for x in ((maxv/XSEC_FID)/(hist)) ] + [((maxv/XSEC_FID)/(hist))[-1]]
w_down = [x for x in ((minv/XSEC_FID)/(hist)) ] + [((minv/XSEC_FID)/(hist))[-1]]

def binning(values):
    return cs.Binning(
        nodetype="binning",
        input="pt",
        edges=pt_edges,
        content=values,
        flow="clamp"   # usa el borde más cercano fuera de rango
    )

corr = cs.Correction(
    name="PT_weight",
    description="Scale factor 1D vs pt for b-hadron",
    version=1,
    inputs=[
        cs.Variable(name="pt", type="real"),
        cs.Variable(name="variation", type="string", description="nominal/up/down"),
    ],
    output=cs.Variable(name="weight", type="real"),
    data=cs.Category(
        nodetype="category",
        input="variation",
        content=[
            cs.CategoryItem(key="nominal", value=binning(w_nom)),
            cs.CategoryItem(key="up",      value=binning(w_up)),
            cs.CategoryItem(key="down",    value=binning(w_down)),
        ]
    )
)

cset = cs.CorrectionSet(schema_version=2, corrections=[corr])
with open("python/B-norm/pt_weights.json", "w") as f:
    f.write(cset.json(exclude_unset=True))

# Test the json:
import correctionlib
cset = correctionlib.CorrectionSet.from_file("python/B-norm/pt_weights.json")
for pt in pt_edges:
    print(f"Weight for pt={pt} = {cset['PT_weight'].evaluate(pt, 'nominal')}")

