import ROOT
import numpy
import copy
import os,sys,csv
from datetime import date
import mplhep as hep
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import MultipleLocator
from matplotlib.ticker import FixedLocator, FixedFormatter
import plotly.graph_objects as go
#import plotUtils

#########################

ROOT.gROOT.SetBatch(1)

user = os.environ.get("USER")
today= date.today().strftime("%b-%d-%Y")

sigModel = "HTo2ZdTo2mu2x" # HTo2ZdTo2mu2x : BToPhi

y = 2023

eras = {}
if y==2022:
    eras[2022] = ['2022', '2022postEE']
    inDir = '/ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Feb-07-2024_2022_wrapped'
else:
    eras[2023] = ['2023', '2023BPix']
    inDir = '/ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_2023_Feb-03-2025_wrapped'

# Signals
sigMasses = []
sigCTaus = []
if sigModel=="HTo2ZdTo2mu2x":
        sigMasses = [2.0, 2.5, 5.0, 7.0, 8.0, 14.0, 16.0, 20.0, 30.0, 40.0]
        sigCTaus = [1, 10, 100, 1000]

if sigModel=="BToPhi":
    sigMasses = [0.25, 0.3, 0.4, 0.6, 0.7, 0.9, 1.25, 1.5, 2.85, 3.35]
    sigCTaus = [0.1, 1, 10, 100]

#
#
### Loop to count
for era in eras[y]:
    nera = 0
    for m in sigMasses:
        for t in sigCTaus:
            sm = ('%.1f'%(m)).replace('.', 'p')
            st = '%.0f'%(t)
            file = inDir + '/' + 'output_Signal_%s_MZd-%s_ctau-%smm_%s_%i_0To99.root'%(sigModel, sm, st, era, y)
            tfile = ROOT.TFile(file)
            counts = tfile.Get("counts")
            nera += counts.GetEntries()
            print(file, counts.GetEntries())
    print(era, nera/(len(sigCTaus)*len(sigMasses)))
            
