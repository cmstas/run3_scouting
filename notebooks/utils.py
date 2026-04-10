import ROOT
import os,sys,json
import argparse
from datetime import date    
import numpy as np
import copy
import math
import mplhep as hep
import matplotlib.pyplot as plt

def getValues(histo, overflow = False):
    values = []
    bins = []
    for n in range(1, histo.GetNbinsX()+1):
        values.append(histo.GetBinContent(n))
        bins.append(histo.GetBinLowEdge(n))
    bins.append(histo.GetBinLowEdge(n) + histo.GetBinWidth(n))
    if overflow:
        values[-1] = values[-1] + histo.GetBinContent(histo.GetNbinsX()+1)
    return np.array(values), np.array(bins)

def getValues2D(histo):
    nbins_x = histo.GetNbinsX()
    nbins_y = histo.GetNbinsY()
    x_edges = np.array([histo.GetXaxis().GetBinLowEdge(i) for i in range(1, nbins_x + 2)])
    y_edges = np.array([histo.GetYaxis().GetBinLowEdge(i) for i in range(1, nbins_y + 2)])
    values = np.array([[histo.GetBinContent(i, j) for j in range(1, nbins_y + 1)] for i in range(1, nbins_x + 1)])
    return values, x_edges, y_edges
