#!/bin/env python3                                                                                                                                               
import ROOT, array, random, copy                                                                                                    
from ROOT import TCanvas, TFile, TH1, TH1F, TF1, gSystem                                                                                        
import ROOT, array, random, copy                                                                                        
from ROOT import RooCmdArg, RooArgSet, kFALSE, RooLinkedList, kBlue, kRed, kBlack, kOpenStar, kWhite, kGray                                    
from ROOT import gStyle, TStyle, TGraph, TGraphErrors, TMath, TMultiGraph, TLine, gPad, TGaxis, TLegend, TText, TLatex, TColor, TPaveText      
from ROOT import TAttFill, TLegend, TRatioPlot, TPad, THStack, TFileCollection                                                      
from ROOT import kBlue, kRed, kBlack, kWhite, kAzure, kOrange, kPink, kGreen, kYellow, kCyan, kMagenta                                         
from ROOT import RooRealVar, RooDataHist, RooCBShape, RooDoubleCBFast, RooGaussian, RooExponential, RooAddPdf, RooFit, RooArgList, RooPolynomial, RooGenericPdf, RooBernsteinFast, RooBernstein
from ROOT import RooCmdArg, RooArgSet, RooLinkedList, kFALSE, kBlue, kRed, kBlack, kGray
from ROOT import gStyle, TCanvas, TLatex, TLegend, TFile
import math                                                                                                                             
import os                                                                                                            
import argparse                                                                                                                         
import sys
from datetime import date
import numpy as np
import mplhep as hep
import matplotlib.pyplot as plt
                                                                                                       

ROOT.gROOT.SetBatch()                                                                                          
ROOT.gStyle.SetOptStat(0)                                                                                    
ROOT.gStyle.SetOptTitle(0)

def getValues(histo):
    values = []
    bins = []
    for n in range(1, histo.GetNbinsX()+1):
        values.append(histo.GetBinContent(n))
        bins.append(histo.GetBinLowEdge(n))
    bins.append(histo.GetBinLowEdge(n) + histo.GetBinWidth(n))
    return np.array(values), np.array(bins)

def fitDataset(name, dataset, mass, fit_range=(2.6, 3.6), outDir="output", year=2022, lumi=1.0, nBins=100, bOnly=False):

    # Loop over pdfs:
    #for pdf in ["exp", "power", "bern"]:
    for pdf in ["exp"]:
        ## Frame
        mfit = RooRealVar("mfit", "mfit", fit_range[0], fit_range[1])
        data = dataset.reduce(mfit, "%f < mfit && mfit < %f"%(fit_range[0], fit_range[1]))
        data.Print()
        x = data.get().find("mfit")
        x.setRange("fitRange", fit_range[0], fit_range[1])
        #nBins = 100
        histogram = data.createHistogram("mfit", nBins) 
        data_hist = RooDataHist("data_hist", "Binned data", RooArgSet(x), histogram)
        ## Background pdfs
        # Background exponential
        if pdf=="exp":
            expo_slope  = RooRealVar("expo_slope","expo_slope",-0.1,-20.0,20.0)
            background = RooExponential("background_exponential", "background_exponential",x,expo_slope)
        elif pdf=="power":
            plaw_power  = RooRealVar("plaw_power","plaw_power",-3.0,-25.0,25.0)
            background = RooGenericPdf("background_powerlaw", "background_powerlaw", "TMath::Power(@0,@1)",RooArgList(x,plaw_power))
        elif pdf=="bern":
            par0 = RooRealVar("pbern0_order2", "pbern0_order2", 0.0, 0.0, 10.0)
            par1 = RooRealVar("pbern1_order2", "pbern1_order2", 0.0, 0.0, 10.0)
            par2 = RooRealVar("pbern2_order2", "pbern2_order2", 0.0, 0.0, 10.0)
            background = RooBernstein("background_bernstein_order2","background_bernstein_order2",x,RooArgList(par0,par1,par2))
        #b0 = RooRealVar("b0", "constant term", 1.0, 0.0, 10.0)
        #b1 = RooRealVar("b1", "linear term", 0.0, -1.0, 1.0)
        #background = RooPolynomial("background", "background", x, RooArgList(b0, b1))
        #
        if "Upsilon" not in name:
            # Signal parameters initialization
            stddev = 0.02*mass
            minstddev = 0.001
            maxstddev = 2.0*stddev
            #
            mean = mass
            minmean = max([fit_range[0], 0.7*mean])
            maxmean = min([fit_range[1], 1.3*mean])
            #
            alphaR = 1.1;
            minalphaR = 1.0;
            maxalphaR = 10.0;
            #
            alphaL = 1.1;
            minalphaL = 1.0;
            maxalphaL = 10.0;
            #
            nR = 1.1;
            minnR = 1.0;
            maxnR = 5.0;
            #
            nL = 1.1;
            minnL = 1.0;
            maxnL = 5.0;
            #
            ## Signal pdfs
            mean_ = RooRealVar("mean", "mean of crystal ball", mean, minmean, maxmean)
            sigma_ = RooRealVar("sigma", "width of crystal ball", stddev, minstddev, maxstddev)
            gauss = RooGaussian("gauss", "gauss", x, mean_, sigma_)
            #
            alphaL_ = RooRealVar("alphaL", "alphaL", alphaL, minalphaL, maxalphaL)
            alphaR_ = RooRealVar("alphaR", "alphaR", alphaR, minalphaR, maxalphaR)
            nL_ = RooRealVar("nL", "nL", nL, minnL, maxnL)
            nR_ = RooRealVar("nR", "nR", nR, minnR, maxnR)
            dcb = RooDoubleCBFast("dcb", "dcb", x, mean_, sigma_, alphaL_, nL_, alphaR_, nR_)
            #
            #
            # Combine the models
            frac_gauss = RooRealVar("frac_gauss", "fraction of Gaussian", 0.1, 0.0, 1.0)
            frac_dcb = RooRealVar("frac_dcb", "fraction of crystal ball", 0.1, 0.0, 1.0)
            model = RooAddPdf("model", "DCB + Gaussian + Background", RooArgList(dcb, gauss, background), RooArgList(frac_dcb, frac_gauss))
        else:
            # Gaussian 1S
            mean1_ = RooRealVar("mean1", "mean of gaussian 1", 9.23, 9.33, 9.63)
            sigma1_ = RooRealVar("sigma1", "width of gaussian 1", 0.08, 0.001, 0.1)
            gauss1 = RooGaussian("gauss1", "gauss", x, mean1_, sigma1_)
            # Gaussian 2S
            mean2_ = RooRealVar("mean2", "mean of gaussian 2", 10.0, 9.90, 10.10)
            sigma2_ = RooRealVar("sigma2", "width of gaussian 2", 0.08, 0.001, 0.1)
            gauss2 = RooGaussian("gauss2", "gauss", x, mean2_, sigma2_)
            # Gaussian 3S
            mean3_ = RooRealVar("mean3", "mean of gaussian 3", 10.32, 10.20, 10.40)
            sigma3_ = RooRealVar("sigma3", "width of gaussian 3", 0.08, 0.001, 0.1)
            gauss3 = RooGaussian("gauss3", "gauss", x, mean3_, sigma3_)
            # Combine the models
            frac_g1 = RooRealVar("frac_g1", "fraction of Gaussian 1", 0.01, 0.0, 1.0)
            frac_g2 = RooRealVar("frac_g2", "fraction of Gaussian 2", 0.01, 0.0, 1.0)
            frac_g3 = RooRealVar("frac_g3", "fraction of Gaussian 3", 0.01, 0.0, 1.0)
            model = RooAddPdf("model", "DCB + Gaussian + Background", RooArgList(gauss1, gauss2, gauss3, background), RooArgList(frac_g1, frac_g2, frac_g3))

        # Fit
        if bOnly:
            model = background
        nMaxFitAttempts = 1
        nFits = 0
        while (nFits < nMaxFitAttempts):
            fit_result = model.fitTo(data_hist, RooFit.Range(fit_range[0], fit_range[1]), RooFit.Save())
            nFits+=1
            if fit_result.status()==0:
                break

        # Create a frame to plot the fit result
        frame = x.frame(RooFit.Title("Mass"))
        data_hist.plotOn(frame)
        model.plotOn(frame)
        #
        frame.SetXTitle("Mass [GeV]")
        frame.GetXaxis().SetTitleOffset(1.3)
        frame.SetYTitle("Events / 0.01 GeV")

        # Get Chi2 and normalize by ndof and number of bins
        chi2 = frame.chiSquare(fit_result.floatParsFinal().getSize())  # chi^2
        ndof = fit_result.floatParsFinal().getSize()  # Number of degrees of freedom
        chi2_over_ndof = chi2 / (nBins - ndof)
        print("----------------------------------------")
        print("nBins = ", nBins)
        print("chi2_over_ndof = ", chi2_over_ndof)
        print("----------------------------------------")    

        ## Plotting
        histo, bins = getValues(histogram)
        binw = histogram.GetBinLowEdge(2)-histogram.GetBinLowEdge(1)
        y_err = histo**0.5
        xval = np.linspace(fit_range[0], fit_range[1], 200)
        vbkg = []  
        vdcb = []  
        vgaus = []  
        vmodel = []
        vsignal = []
        vg1 = []
        vg2 = []
        vg3 = []
        bkg_integral_value = background.createIntegral(RooArgSet(x)).getVal()
        model_integral_value = model.createIntegral(RooArgSet(x)).getVal()
        if "Upsilon" not in name:
            gauss_integral_value = gauss.createIntegral(RooArgSet(x)).getVal()
            dcb_integral_value = dcb.createIntegral(RooArgSet(x)).getVal()
        else:
            g1_integral_value = gauss1.createIntegral(RooArgSet(x)).getVal()
            g2_integral_value = gauss2.createIntegral(RooArgSet(x)).getVal()
            g3_integral_value = gauss3.createIntegral(RooArgSet(x)).getVal()
        #    
        for val in xval:
            x.setVal(val)
            if not bOnly:
                if "Upsilon" not in name:
                    frac_bkg = 1.0 - frac_dcb.getVal()-frac_gauss.getVal()
                    vbkg.append(background.getVal()*data.sumEntries()*binw*(frac_bkg)/bkg_integral_value)
                    vdcb.append(dcb.getVal()*data.sumEntries()*binw*frac_dcb.getVal()/dcb_integral_value)
                    vgaus.append(gauss.getVal()*data.sumEntries()*binw*frac_gauss.getVal()/gauss_integral_value)
                    vmodel.append(vbkg[-1]+vdcb[-1]+vgaus[-1])
                    vsignal.append(vdcb[-1]+vgaus[-1])
                else:
                    frac_bkg = 1.0 - frac_g1.getVal()-frac_g2.getVal()-frac_g3.getVal()
                    vbkg.append(background.getVal()*data.sumEntries()*binw*(frac_bkg)/bkg_integral_value)
                    vg1.append(gauss1.getVal()*data.sumEntries()*binw*frac_g1.getVal()/g1_integral_value)
                    vg2.append(gauss2.getVal()*data.sumEntries()*binw*frac_g2.getVal()/g2_integral_value)
                    vg3.append(gauss3.getVal()*data.sumEntries()*binw*frac_g3.getVal()/g3_integral_value)
                    vmodel.append(vbkg[-1]+vg1[-1]+vg2[-1]+vg3[-1])
            else:
                vmodel.append(model.getVal()*data.sumEntries()*binw/model_integral_value)
        residuals = []
        masses = []
        for i in range(0, len(bins)-1):
            masses.append(0.5*(bins[i] + bins[i+1]))
            x.setVal(masses[-1])
            if histo[i] > 0:
                if not bOnly:
                    residuals.append((histo[i]-(background.getVal()*data.sumEntries()*binw*(frac_bkg)/bkg_integral_value))/y_err[i])
                else:
                    residuals.append((histo[i]-(model.getVal()*data.sumEntries()*binw/model_integral_value))/y_err[i])
            else:
                residuals.append(0.0)
        #
        plt.style.use(hep.style.CMS)
        #fig, (ax, ax_residuals) = plt.subplots(2, 1, gridspec_kw={'height_ratios': [4, 1], 'hspace': 0.05}, sharex=True, figsize=(10, 10))
        fig, ax = plt.subplots(1,1, figsize=(10, 7.5))
        # Main plot
        ax.set_ylabel(r'Events / %.5f GeV'%((fit_range[1]-fit_range[0])/nBins), fontsize=24)
        ax.set_xlabel('')
        ax.set_xlim(fit_range[0], fit_range[1])
        hep.cms.label("Preliminary", data=True, year=year, com='13.6', ax=ax)
        ax.set_ylim(0.0,1.45*max(histo))
        llabel = ''
        if '0p0to0p2' in name:
            llabel = '[0.0, 0.2] cm'
        if '0p2to1p0' in name:
            llabel = '[0.2, 1.0] cm'
        if '1p0to2p4' in name:
            llabel = '[1.0, 2.4] cm'
        if '2p4to3p1' in name:
            llabel = '[2.4, 3.1] cm'
        if '3p1to7p0' in name:
            llabel = '[3.1, 7.0] cm'
        if '7p0to11p0' in name:
            llabel = '[7.0, 11.0] cm'
        if '11p0to16p0' in name:
            llabel = '[11.0, 16.0] cm'
        if '16p0to70p0' in name:
            llabel = '[16.0, 70.0] cm'
        ax.errorbar(masses, histo, yerr=y_err, fmt='o', capsize=5, label='Data (%s)'%(llabel), color='k', markersize=8)
        ax.axvline(x=3.55, color='orange', linestyle='--')
        #if not bOnly:
        #    ax.plot(xval, vbkg, label='Background (%s)'%(pdf), color='slateblue', lw = 3, linestyle='--')
        #    ax.plot(xval, vmodel, label='Signal + Background', color='tab:red', lw = 3)
        #else:
        #    ax.plot(xval, vmodel, label='Background (%s)'%(pdf), color='tab:red', lw = 3)
        #ax.text(0.63, 0.95, 'Fit parameters', fontsize=18, color='black', horizontalalignment='left', verticalalignment='top', transform=ax.transAxes, fontweight='bold')
        #if not bOnly:
        #    if "Upsilon" not in name:
        #        ax.text(0.63, 0.9, r'Mean = %.2f GeV'%(mean_.getVal()), fontsize=18, color='black', horizontalalignment='left', verticalalignment='top', transform=ax.transAxes)
        #        ax.text(0.63, 0.86, r'$\sigma =$ %.1f MeV'%(sigma_.getVal()*1000.0), fontsize=18, color='black', horizontalalignment='left', verticalalignment='top', transform=ax.transAxes)
        #        ax.text(0.63, 0.82, r'$\chi^2/ndof =$ %.3f'%(chi2_over_ndof), fontsize=18, color='black', horizontalalignment='left', verticalalignment='top', transform=ax.transAxes)
        #    else:
        #        ax.text(0.63, 0.9, r'Mean (1S) = %.2f GeV'%(mean1_.getVal()), fontsize=18, color='black', horizontalalignment='left', verticalalignment='top', transform=ax.transAxes)
        #        ax.text(0.63, 0.86, r'$\sigma (1S) =$ %.1f MeV'%(sigma1_.getVal()*1000.0), fontsize=18, color='black', horizontalalignment='left', verticalalignment='top', transform=ax.transAxes)
        #        ax.text(0.63, 0.82, r'Mean (2S) = %.2f GeV'%(mean2_.getVal()), fontsize=18, color='black', horizontalalignment='left', verticalalignment='top', transform=ax.transAxes)
        #        ax.text(0.63, 0.78, r'$\sigma (2S) =$ %.1f MeV'%(sigma2_.getVal()*1000.0), fontsize=18, color='black', horizontalalignment='left', verticalalignment='top', transform=ax.transAxes)
        #        ax.text(0.63, 0.74, r'Mean (3S) = %.2f GeV'%(mean3_.getVal()), fontsize=18, color='black', horizontalalignment='left', verticalalignment='top', transform=ax.transAxes)
        #        ax.text(0.63, 0.70, r'$\sigma (3S) =$ %.1f MeV'%(sigma3_.getVal()*1000.0), fontsize=18, color='black', horizontalalignment='left', verticalalignment='top', transform=ax.transAxes)
        #        ax.text(0.63, 0.66, r'$\chi^2/ndof =$ %.3f'%(chi2_over_ndof), fontsize=18, color='black', horizontalalignment='left', verticalalignment='top', transform=ax.transAxes)
        #else:
        #    ax.text(0.63, 0.9, r'$\chi^2/ndof =$ %.3f'%(chi2_over_ndof), fontsize=18, color='black', horizontalalignment='left', verticalalignment='top', transform=ax.transAxes)
        if 'short' in name:
            ax.text(0.05, 0.74, r'$l_{xy} \in [0, 2.4]$ cm', fontsize=18, color='black', horizontalalignment='left', verticalalignment='top', transform=ax.transAxes)
        elif 'medium' in name:
            ax.text(0.05, 0.74, r'$l_{xy} \in [2.4, 11.0]$ cm', fontsize=18, color='black', horizontalalignment='left', verticalalignment='top', transform=ax.transAxes)
        elif 'high' in name:
            ax.text(0.05, 0.74, r'$l_{xy} \in [11.0, 70.0]$ cm', fontsize=18, color='black', horizontalalignment='left', verticalalignment='top', transform=ax.transAxes)
        ax.legend(loc='upper left', fontsize = 18, frameon = True, ncol=1)
        # Residual subplot
        #ax_residuals.stairs(np.array(residuals), bins, color="red", alpha=0.3)
        #ax_residuals.fill_between(bins[:-1], residuals, 0, color="red", alpha=0.3, step="post")
        #ax_residuals.set_ylabel(r"$\mathrm{\frac{Data - Fit_{Bkg}}{\sigma_{Data}}}$")
        #ax_residuals.set_xlabel("Dimuon Mass [GeV]")
        fig.savefig('%s/%s_%s_fit.png'%(outDir,name,pdf), dpi=140) 

if __name__=="__main__":

    # Year
    year = 2022
    lumi = 27 if year==2022 else 35
    # Inclusive regions for fitting
    sdNames = {}
    
    sdNames["d_Dimuon_lxy0p0to0p2_inclusive"] = ["d_Dimuon_lxy0p0to0p2_inclusive"]
    sdNames["d_Dimuon_lxy0p2to1p0_inclusive"] = ["d_Dimuon_lxy0p2to1p0_inclusive"]
    sdNames["d_Dimuon_lxy1p0to2p4_inclusive"] = ["d_Dimuon_lxy1p0to2p4_inclusive"]
    sdNames["d_Dimuon_lxy2p4to3p1_inclusive"] = ["d_Dimuon_lxy2p4to3p1_inclusive"]
    sdNames["d_Dimuon_lxy3p1to7p0_inclusive"] = ["d_Dimuon_lxy3p1to7p0_inclusive"]
    sdNames["d_Dimuon_lxy7p0to11p0_inclusive"] = ["d_Dimuon_lxy7p0to11p0_inclusive"]
    sdNames["d_Dimuon_lxy11p0to16p0_inclusive"] = ["d_Dimuon_lxy11p0to16p0_inclusive"]
    sdNames["d_Dimuon_lxy16p0to70p0_inclusive"] = ["d_Dimuon_lxy16p0to70p0_inclusive"]
    
    #sdNames["d_Dimuon_inclusive"] = ["d_Dimuon_lxy0p0to0p2_inclusive",
    #                                 "d_Dimuon_lxy0p2to1p0_inclusive",
    #                                 "d_Dimuon_lxy1p0to2p4_inclusive", 
    #                                 "d_Dimuon_lxy2p4to3p1_inclusive",
    #                                 "d_Dimuon_lxy3p1to7p0_inclusive",
    #                                 "d_Dimuon_lxy7p0to11p0_inclusive",
    #                                 "d_Dimuon_lxy11p0to16p0_inclusive",
    #                                 "d_Dimuon_lxy16p0to70p0_inclusive"]
    #sdNames["d_Dimuon_short"] = ["d_Dimuon_lxy0p0to0p2_inclusive", "d_Dimuon_lxy0p2to1p0_inclusive"]
    #sdNames["d_Dimuon_medium"] = ["d_Dimuon_lxy1p0to2p4_inclusive", "d_Dimuon_lxy2p4to3p1_inclusive", "d_Dimuon_lxy3p1to7p0_inclusive", "d_Dimuon_lxy7p0to11p0_inclusive"]
    #sdNames["d_Dimuon_short"] = ["d_Dimuon_lxy0p0to0p2_inclusive", "d_Dimuon_lxy0p2to1p0_inclusive", "d_Dimuon_lxy1p0to2p4_inclusive"]
    #sdNames["d_Dimuon_medium"] = ["d_Dimuon_lxy2p4to3p1_inclusive", "d_Dimuon_lxy3p1to7p0_inclusive", "d_Dimuon_lxy7p0to11p0_inclusive"]
    #sdNames["d_Dimuon_high"] = ["d_Dimuon_lxy11p0to16p0_inclusive", "d_Dimuon_lxy16p0to70p0_inclusive"]
    #dNames = []
    #dNames.append("d_Dimuon_lxy0p0to0p2_inclusive")
    #dNames.append("d_Dimuon_lxy0p2to1p0_inclusive")
    #dNames.append("d_Dimuon_lxy1p0to2p4_inclusive")
    #dNames.append("d_Dimuon_lxy2p4to3p1_inclusive")
    #dNames.append("d_Dimuon_lxy3p1to7p0_inclusive")
    #dNames.append("d_Dimuon_lxy7p0to11p0_inclusive")
    #dNames.append("d_Dimuon_lxy11p0to16p0_inclusive")
    #dNames.append("d_Dimuon_lxy16p0to70p0_inclusive")
    #
    # Resonances to fit: {Resonance : center, fit_range}
    resonances = {}
    #resonances['TT'] = [3.55, (3.54, 3.56)]
    #resonances['TT'] = [3.55, (3.53, 3.57)]
    #resonances['TT'] = [3.55, (3.52, 3.58)]
    #resonances['TT'] = [3.55, (3.50, 3.60)]
    resonances['TT'] = [3.525, (3.515, 3.535)]
    #resonances['TT'] = [3.835, (3.810, 3.860)]
    #
    # Input
    #inDir = "/ceph/cms/store/user/fernance/Run3ScoutingOutput/outputHistograms_Sep-25-2024_RooDatasets_unblind"
    #inDir = "/ceph/cms/store/user/fernance/Run3ScoutingOutput/outputHistograms_Oct-30-2024_2022_unblind_noMuonIPSel"
    #inDir = "/ceph/cms/store/user/fernance/Run3ScoutingOutput/outputHistograms_Oct-30-2024_unblind_allCuts"
    inDir = "/ceph/cms/store/user/fernance/Run3ScoutingOutput/outputHistograms_Dec-03-2024_2022_complete"
    #inDir = "/ceph/cms/store/user/fernance/Run3ScoutingOutput/outputHistograms_Dec-03-2024_2023_complete"
    #inDir = "/ceph/cms/store/user/fernance/Run3ScoutingOutput/outputHistograms_Nov-11-2024_MinBias_fixed_noIP"
    files = os.listdir(inDir)
    #
    eras = []
    if year==2022:
        eras.append("DataC")
        eras.append("DataD")
        eras.append("DataE")
        eras.append("DataF")
        eras.append("DataG")
    elif year==2023:
        eras.append("DataC")
        eras.append("DataD")
    #eras = ["DileptonMinBias"] # Remove if you want to run on Data

    #
    today = date.today().strftime("%b-%d-%Y")
    outDir = "plotsMasking_%i_%s"%(year,today)
    if not os.path.exists(outDir):
        os.makedirs(outDir)
    #
    # Loop:
    for p in resonances:
        for sr in sdNames.keys():
            sdataset = 0
            for d_,d in enumerate(sdNames[sr]):
                for e,era in enumerate(eras):
                    if e==0:
                        fin = ROOT.TFile.Open("%s/%s"%(inDir,files[0]))
                        dataset = fin.Get(d).Clone()
                    for f,file in enumerate(files):
                        if era in file:
                            if e==0 and f==0:
                                continue
                            print("Reading %s"%(file))
                            fin = ROOT.TFile.Open("%s/%s"%(inDir,file))
                            tds = fin.Get(d).Clone()
                            dataset.append(tds)
                print(dataset.numEntries())
                if d_==0:
                    sdataset = dataset
                else:
                    sdataset.append(dataset)
            # Fitting:
            fitDataset("%s_%s_bOnly"%(p,sr), sdataset, mass = resonances[p][0], fit_range=resonances[p][1], outDir=outDir, year=year, lumi=lumi, nBins=70, bOnly=True)
            #if 'medium' in sr:
            #    print("Using 80 bins...")
            #    fitDataset("%s_%s"%(p,sr), sdataset, mass = resonances[p][0], fit_range=resonances[p][1], outDir=outDir, year=year, lumi=lumi, nBins=80)
            #    fitDataset("%s_%s_bOnly"%(p,sr), sdataset, mass = resonances[p][0], fit_range=resonances[p][1], outDir=outDir, year=year, lumi=lumi, nBins=80, bOnly=True)
            #elif 'high' in sr:
            #    print("Using 60 bins...")
            #    fitDataset("%s_%s"%(p,sr), sdataset, mass = resonances[p][0], fit_range=resonances[p][1], outDir=outDir, year=year, lumi=lumi, nBins=50)
            #    fitDataset("%s_%s_bOnly"%(p,sr), sdataset, mass = resonances[p][0], fit_range=resonances[p][1], outDir=outDir, year=year, lumi=lumi, nBins=50, bOnly=True)
            #else:
            #    print("Using 100 bins...")
            #    fitDataset("%s_%s_bOnly"%(p,sr), sdataset, mass = resonances[p][0], fit_range=resonances[p][1], outDir=outDir, year=year, lumi=lumi, nBins=100, bOnly=False)



