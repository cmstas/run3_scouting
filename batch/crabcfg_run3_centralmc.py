from CRABClient.UserUtilities import config #, getUsernameFromSiteDB
from CRABAPI.RawCommand import crabCommand

# https://twiki.cern.ch/twiki/bin/view/CMSPublic/CRAB3ConfigurationFile
#config = config()

import sys

era = sys.argv[1] # [2022, 2022postEE, 2023 or 2023BPix]
signal = sys.argv[2] # [HTo2ZdTo2mu2x, BToPhi, ScenarioB1]

year=0
if ("2022") in era:
    year=2022
elif ("2023") in era:
    year=2023
else:
    quit()

# This is only MC, should not be used to run on data
data=False

# ntuple version defined now
ntuple_version = "6p1"

# Setup working environment
import os
base = os.environ["CMSSW_BASE"]
print(base)
#if not os.path.exists(base + '/src/centralTasks'):
#
#    os.mkdir(base + '/src/centralTasks')

# List of datasets
config_list = []
extras = []
if (len(sys.argv)>2):
    mass_points = []
    config = config()
    config.General.workArea = base+'/../'
    config.General.transferLogs = True
    config.JobType.pluginName = 'Analysis'
    config.JobType.psetName = 'Scouting/NtupleMaker/test/producer_Run3.py'
    config.Data.splitting = 'EventAwareLumiBased'
    config.Data.unitsPerJob = int(10e4)
    config.Data.publication = False # By defailt but set to true below
    config.Site.storageSite = "T2_US_UCSD"
    if "HTo2ZdTo2mu2x" in sys.argv[2]:
        config.Data.outLFNDirBase = "/store/group/Run3Scouting/RAWScouting_HTo2ZdTo2mu2x_" + str(year) + "_v"+ntuple_version # DB no
        config.Data.inputDBS = 'global'
        config.Data.publication = True
        # Set the points to produce
        mass_points.append(['0p5', '1'])
        mass_points.append(['0p5', '10'])
        mass_points.append(['0p7', '1'])
        mass_points.append(['0p7', '10'])
        mass_points.append(['1p5', '1'])
        mass_points.append(['1p5', '10'])
        mass_points.append(['1p5', '100'])
        mass_points.append(['2p0', '1'])
        mass_points.append(['2p0', '10'])
        mass_points.append(['2p0', '100'])
        mass_points.append(['2p5', '1'])
        mass_points.append(['2p5', '10'])
        mass_points.append(['2p5', '100'])
        mass_points.append(['3p0', '1'])
        mass_points.append(['3p0', '10'])
        mass_points.append(['3p0', '100'])
        mass_points.append(['4p0', '1'])
        mass_points.append(['4p0', '10'])
        mass_points.append(['4p0', '100'])
        mass_points.append(['5p0', '1'])
        mass_points.append(['5p0', '10'])
        mass_points.append(['5p0', '100'])
        mass_points.append(['6p0', '1'])
        mass_points.append(['6p0', '10'])
        mass_points.append(['6p0', '100'])
        mass_points.append(['7p0', '1'])
        mass_points.append(['7p0', '10'])
        mass_points.append(['7p0', '100'])
        mass_points.append(['8p0', '1'])
        mass_points.append(['8p0', '10'])
        mass_points.append(['8p0', '100'])
        mass_points.append(['10p0', '1'])
        mass_points.append(['10p0', '10'])
        mass_points.append(['10p0', '100'])
        mass_points.append(['12p0', '1'])
        mass_points.append(['12p0', '10'])
        mass_points.append(['12p0', '100'])
        mass_points.append(['14p0', '1'])
        mass_points.append(['14p0', '10'])
        mass_points.append(['14p0', '100'])
        mass_points.append(['16p0', '1'])
        mass_points.append(['16p0', '10'])
        mass_points.append(['16p0', '100'])
        mass_points.append(['20p0', '1'])
        mass_points.append(['20p0', '10'])
        mass_points.append(['20p0', '100'])
        mass_points.append(['22p0', '1'])
        mass_points.append(['22p0', '10'])
        mass_points.append(['22p0', '100'])
        mass_points.append(['24p0', '1'])
        mass_points.append(['24p0', '10'])
        mass_points.append(['24p0', '100'])
        mass_points.append(['30p0', '1'])
        mass_points.append(['30p0', '10'])
        mass_points.append(['30p0', '100'])
        mass_points.append(['30p0', '1000'])
        mass_points.append(['34p0', '1'])
        mass_points.append(['34p0', '10'])
        mass_points.append(['34p0', '100'])
        mass_points.append(['34p0', '1000'])
        mass_points.append(['40p0', '1'])
        mass_points.append(['40p0', '10'])
        mass_points.append(['40p0', '100'])
        mass_points.append(['40p0', '1000'])
        mass_points.append(['44p0', '1'])
        mass_points.append(['44p0', '10'])
        mass_points.append(['44p0', '100'])
        mass_points.append(['44p0', '1000'])
        mass_points.append(['50p0', '1'])
        mass_points.append(['50p0', '10'])
        mass_points.append(['50p0', '100'])
        mass_points.append(['50p0', '1000'])
        
        for [m,t] in mass_points:
            config_list.append(config)
            config_list[-1].JobType.pyCfgParams=["era={}".format(era),"data=False",]
            if era=="2022":
                dataset_name = '/HTo2ZdTo2mu2x_MZd-{}_ctau-{}mm_TuneCP5_13p6TeV_madgraph-pythia8/Run3Summer22DRPremix-124X_mcRun3_2022_realistic_v12-v2/AODSIM'.format(m, t)
                config_list[-1].Data.inputDataset = dataset_name
            elif era=="2022postEE":
                dataset_name = '/HTo2ZdTo2mu2x_MZd-{}_ctau-{}mm_TuneCP5_13p6TeV_madgraph-pythia8/Run3Summer22EEDRPremix-124X_mcRun3_2022_realistic_postEE_v1-v2/AODSIM'.format(m, t)
                config_list[-1].Data.inputDataset = dataset_name
            elif era=="2023":
                dataset_name = '/HTo2ZdTo2mu2x_MZd-{}_ctau-{}mm_TuneCP5_13p6TeV_madgraph-pythia8/Run3Summer23DRPremix-130X_mcRun3_2023_realistic_v14-v2/AODSIM'.format(m, t)
                config_list[-1].Data.inputDataset = dataset_name
            elif era=="2023BPix":
                dataset_name = '/HTo2ZdTo2mu2x_MZd-{}_ctau-{}mm_TuneCP5_13p6TeV_madgraph-pythia8/Run3Summer23BPixDRPremix-130X_mcRun3_2023_realistic_postBPix_v2-v2/AODSIM'.format(m, t)
                config_list[-1].Data.inputDataset = dataset_name
            config_list[-1].General.requestName = 'centralSkim__{}_{}_m-{}_ctau-{}mm_{}'.format(signal, era, m, t, ntuple_version)
            print(config)
            #crabCommand('submit', config = config, dryrun = False) ## dryrun = True for local test
    elif "BToPhi" in sys.argv[2]:
        config.Data.outLFNDirBase = "/store/group/Run3Scouting/RAWScouting_BToPhi_" + str(year) + "_v"+ntuple_version 
        config.Data.inputDBS = 'global'
        config.Data.publication = True
        # Set the points to produce
        mass_points.append(['0p25', '0p0'])
        mass_points.append(['0p25', '0p1'])
        mass_points.append(['0p25', '100'])
        mass_points.append(['0p25', '10'])
        mass_points.append(['0p25', '1'])
        mass_points.append(['0p3', '0p0'])
        mass_points.append(['0p3', '0p1'])
        mass_points.append(['0p3', '100'])
        mass_points.append(['0p3', '10'])
        mass_points.append(['0p3', '1'])
        mass_points.append(['0p4', '0p0'])
        mass_points.append(['0p4', '0p1'])
        mass_points.append(['0p4', '100'])
        mass_points.append(['0p4', '10'])
        mass_points.append(['0p4', '1'])
        mass_points.append(['0p5', '0p0'])
        mass_points.append(['0p5', '0p1'])
        mass_points.append(['0p5', '100'])
        mass_points.append(['0p5', '10'])
        mass_points.append(['0p5', '1'])
        mass_points.append(['0p6', '0p0'])
        mass_points.append(['0p6', '0p1'])
        mass_points.append(['0p6', '100'])
        mass_points.append(['0p6', '10'])
        mass_points.append(['0p6', '1'])
        mass_points.append(['0p7', '0p0'])
        mass_points.append(['0p7', '0p1'])
        mass_points.append(['0p7', '100'])
        mass_points.append(['0p7', '10'])
        mass_points.append(['0p7', '1'])
        mass_points.append(['0p9', '0p0'])
        mass_points.append(['0p9', '0p1'])
        mass_points.append(['0p9', '100'])
        mass_points.append(['0p9', '10'])
        mass_points.append(['0p9', '1'])
        mass_points.append(['1p25', '0p0'])
        mass_points.append(['1p25', '0p1'])
        mass_points.append(['1p25', '100'])
        mass_points.append(['1p25', '10'])
        mass_points.append(['1p25', '1'])
        mass_points.append(['1p5', '0p0'])
        mass_points.append(['1p5', '0p1'])
        mass_points.append(['1p5', '100'])
        mass_points.append(['1p5', '10'])
        mass_points.append(['1p5', '1'])
        mass_points.append(['2p0', '0p0'])
        mass_points.append(['2p0', '0p1'])
        mass_points.append(['2p0', '100'])
        mass_points.append(['2p0', '10'])
        mass_points.append(['2p0', '1'])
        mass_points.append(['2p85', '0p0'])
        mass_points.append(['2p85', '0p1'])
        mass_points.append(['2p85', '100'])
        mass_points.append(['2p85', '10'])
        mass_points.append(['2p85', '1'])
        mass_points.append(['3p35', '0p0'])
        mass_points.append(['3p35', '0p1'])
        mass_points.append(['3p35', '100'])
        mass_points.append(['3p35', '10'])
        mass_points.append(['3p35', '1'])
        mass_points.append(['4p0', '0p0'])
        mass_points.append(['4p0', '0p1'])
        mass_points.append(['4p0', '100'])
        mass_points.append(['4p0', '10'])
        mass_points.append(['4p0', '1'])
        mass_points.append(['5p0', '0p0'])
        mass_points.append(['5p0', '0p1'])
        mass_points.append(['5p0', '100'])
        mass_points.append(['5p0', '10'])
        mass_points.append(['5p0', '1'])
        for [m,t] in mass_points:
            config_list.append(config)
            config_list[-1].JobType.pyCfgParams=["era={}".format(era),"data=False",]
            if era=="2022":
                dataset_name = '/BToPhi_MPhi-{}_ctau-{}mm_TuneCP5_13p6TeV_pythia8/Run3Summer22DRPremix-124X_mcRun3_2022_realistic_v12-v2/AODSIM'.format(m, t)
                config_list[-1].Data.inputDataset = dataset_name
            elif era=="2022postEE":
                dataset_name = '/BToPhi_MPhi-{}_ctau-{}mm_TuneCP5_13p6TeV_pythia8/Run3Summer22EEDRPremix-124X_mcRun3_2022_realistic_postEE_v1-v2/AODSIM'.format(m, t)
                config_list[-1].Data.inputDataset = dataset_name
            # No 2023 eras for the moment, when adding them, you have to run . install_cmssw.sh 2023central first
            config_list[-1].General.requestName = 'centralSkim__{}_{}_m-{}_ctau-{}mm_{}'.format(signal, era, m, t, ntuple_version)
            print(config)
            #crabCommand('submit', config = config, dryrun = False) ## dryrun = True for local test
    elif "DQCD" in sys.argv[2]:
        config.Data.outLFNDirBase = '/store/group/Run3Scouting/RAWScouting_privQCD_v'+ntuple_version # DB no
        config.Data.inputDBS = 'phys03'
        config.Data.splitting = 'FileBased'
        config.Data.publication = True
        config.Data.unitsPerJob = int(10) # Increased to match 10 jobs per file aprox
        config.Data.outputDatasetTag = "private-Skim_{era}-v2".format(era=era)
        if era=="2022":
            inputfile = 'data/datasets_dqcd_2022.txt'
        if era=="2022postEE":
            inputfile = 'data/datasets_dqcd_2022postEE.txt'
        with open(inputfile,'r') as f:
            dataset_list = f.readlines()
        for dataset_name in dataset_list:
            config_list.append(config)
            config_list[-1].JobType.pyCfgParams=["era={}".format(era),"data=False",]
            print(dataset_name)
            config_list[-1].Data.inputDataset = dataset_name[:-1]
            model_name = 'S'+dataset_name.split('_')[0][2:]
            mpi = dataset_name.split('mpi_')[1].split('_')[0]
            mA = dataset_name.split('mA_')[1].split('_')[0]
            t = dataset_name.split('ctau_')[1].split('/')[0]
            config_list[-1].General.requestName = 'centralSkim__{}_{}_mpi-{}_mA-{}_ctau-{}mm_{}'.format(model_name, era, mpi, mA, t, ntuple_version)
            print(config)
            try:
                crabCommand('submit', config = config, dryrun = False) ## dryrun = True for local test
            except:
                print('centralSkim__{}_{}_mpi-{}_mA-{}_ctau-{}mm_{} cant be launched! Skipping...'.format(model_name, era, mpi, mA, t, ntuple_version))
    elif "ScenarioA" in sys.argv[2]:
        config.Data.outLFNDirBase = '/store/group/Run3Scouting/RAWScouting_privScenarioA_v'+ntuple_version # DB no
        config.Data.inputDBS = 'phys03'
        config.Data.splitting = 'FileBased'
        config.Data.publication = True
        config.Data.unitsPerJob = int(10) # Increased to match 10 jobs per file aprox
        config.Data.outputDatasetTag = "private-Skim_{era}-v2".format(era=era)
        mass_points.append(['1', '0p25', '0p1'])
        mass_points.append(['1', '0p25', '1p0'])
        mass_points.append(['1', '0p25', '10'])
        mass_points.append(['1', '0p25', '100'])
        mass_points.append(['1', '0p33', '0p1'])
        mass_points.append(['1', '0p33', '1p0'])
        mass_points.append(['1', '0p33', '10'])
        mass_points.append(['1', '0p33', '100'])
        mass_points.append(['1', '0p45', '0p1'])
        mass_points.append(['1', '0p45', '1p0'])
        mass_points.append(['1', '0p45', '10'])
        mass_points.append(['1', '0p45', '100'])
        mass_points.append(['2', '0p25', '0p1'])
        mass_points.append(['2', '0p25', '1p0'])
        mass_points.append(['2', '0p25', '10'])
        mass_points.append(['2', '0p25', '100'])
        mass_points.append(['2', '0p40', '0p1'])
        mass_points.append(['2', '0p40', '1p0'])
        mass_points.append(['2', '0p40', '10'])
        mass_points.append(['2', '0p40', '100'])
        mass_points.append(['2', '0p50', '0p1'])
        mass_points.append(['2', '0p50', '1p0'])
        mass_points.append(['2', '0p50', '10'])
        mass_points.append(['2', '0p50', '100'])
        mass_points.append(['2', '0p67', '0p1'])
        mass_points.append(['2', '0p67', '1p0'])
        mass_points.append(['2', '0p67', '10'])
        mass_points.append(['2', '0p67', '100'])
        mass_points.append(['2', '0p90', '0p1'])
        mass_points.append(['2', '0p90', '1p0'])
        mass_points.append(['2', '0p90', '10'])
        mass_points.append(['2', '0p90', '100'])
        mass_points.append(['4', '0p25', '0p1'])
        mass_points.append(['4', '0p25', '1p0'])
        mass_points.append(['4', '0p25', '10'])
        mass_points.append(['4', '0p25', '100'])
        mass_points.append(['4', '0p40', '0p1'])
        mass_points.append(['4', '0p40', '1p0'])
        mass_points.append(['4', '0p40', '10'])
        mass_points.append(['4', '0p40', '100'])
        mass_points.append(['4', '0p80', '0p1'])
        mass_points.append(['4', '0p80', '1p0'])
        mass_points.append(['4', '0p80', '10'])
        mass_points.append(['4', '0p80', '100'])
        mass_points.append(['4', '1p30', '0p1'])
        mass_points.append(['4', '1p30', '1p0'])
        mass_points.append(['4', '1p30', '10'])
        mass_points.append(['4', '1p30', '100'])
        mass_points.append(['4', '1p90', '0p1'])
        mass_points.append(['4', '1p90', '1p0'])
        mass_points.append(['4', '1p90', '10'])
        mass_points.append(['4', '1p90', '100'])
        mass_points.append(['5', '0p50', '0p1'])
        mass_points.append(['5', '0p50', '1p0'])
        mass_points.append(['5', '0p50', '10'])
        mass_points.append(['5', '0p50', '100'])
        mass_points.append(['5', '1p00', '0p1'])
        mass_points.append(['5', '1p00', '1p0'])
        mass_points.append(['5', '1p00', '10'])
        mass_points.append(['5', '1p00', '100'])
        mass_points.append(['5', '1p67', '0p1'])
        mass_points.append(['5', '1p67', '1p0'])
        mass_points.append(['5', '1p67', '10'])
        mass_points.append(['5', '1p67', '100'])
        mass_points.append(['5', '2p40', '0p1'])
        mass_points.append(['5', '2p40', '1p0'])
        mass_points.append(['5', '2p40', '10'])
        mass_points.append(['5', '2p40', '100'])
        mass_points.append(['10', '1p00', '0p1'])
        mass_points.append(['10', '1p00', '1p0'])
        mass_points.append(['10', '1p00', '10'])
        mass_points.append(['10', '1p00', '100'])
        mass_points.append(['10', '2p00', '0p1'])
        mass_points.append(['10', '2p00', '1p0'])
        mass_points.append(['10', '2p00', '10'])
        mass_points.append(['10', '2p00', '100'])
        mass_points.append(['10', '3p33', '0p1'])
        mass_points.append(['10', '3p33', '1p0'])
        mass_points.append(['10', '3p33', '10'])
        mass_points.append(['10', '3p33', '100'])
        mass_points.append(['10', '4p90', '0p1'])
        mass_points.append(['10', '4p90', '1p0'])
        mass_points.append(['10', '4p90', '10'])
        mass_points.append(['10', '4p90', '100'])
        for [mpi,mA,t] in mass_points:
            config_list.append(config)
            config_list[-1].JobType.pyCfgParams=["era={}".format(era),"data=False",]
            if era=="2022":
                dataset_name = '/scenarioA_mpi_{}_mA_{}_ctau_{}/jleonhol-AODSIM_2022_ext-bd8711905ed05b0226f084d42f06d7ac/USER'.format(mpi, mA, t)
                config_list[-1].Data.inputDataset = dataset_name
            elif era=="2022postEE":
                dataset_name = '/scenarioA_mpi_{}_mA_{}_ctau_{}/tafoyava-AODSIM_2022-6c55dbd4f99ed6c824b000a7a99348b1/USER'.format(mpi, mA, t)
                config_list[-1].Data.inputDataset = dataset_name
            # No 2023 eras for the moment, when adding them, you have to run . install_cmssw.sh 2023central first
            config_list[-1].General.requestName = 'centralSkim__{}_{}_mpi-{}_mA-{}_ctau-{}mm_{}'.format(signal, era, mpi, mA, t, ntuple_version)
            print(config)
            crabCommand('submit', config = config, dryrun = False) ## dryrun = True for local test
    elif "ScenarioB1" in sys.argv[2]:
        config.Data.outLFNDirBase = '/store/group/Run3Scouting/RAWScouting_privScenarioA_v'+ntuple_version # DB no
        config.Data.inputDBS = 'phys03'
        config.Data.splitting = 'FileBased'
        config.Data.publication = True
        config.Data.unitsPerJob = int(10) # Increased to match 10 jobs per file aprox
        config.Data.outputDatasetTag = "private-Skim_{era}-v2".format(era=era)
        mass_points.append(['1', '0p40', '0p1'])
        mass_points.append(['1', '0p40', '1p0'])
        mass_points.append(['1', '0p40', '10'])
        mass_points.append(['1', '0p40', '100'])
        mass_points.append(['2', '0p33', '0p1'])
        mass_points.append(['2', '0p33', '1p0'])
        mass_points.append(['2', '0p33', '10'])
        mass_points.append(['2', '0p33', '100'])
        mass_points.append(['2', '0p90', '0p1'])
        mass_points.append(['2', '0p90', '1p0'])
        mass_points.append(['2', '0p90', '10'])
        mass_points.append(['2', '0p90', '100'])
        mass_points.append(['4', '0p67', '0p1'])
        mass_points.append(['4', '0p67', '1p0'])
        mass_points.append(['4', '0p67', '10'])
        mass_points.append(['4', '0p67', '100'])
        mass_points.append(['4', '1p90', '0p1'])
        mass_points.append(['4', '1p90', '1p0'])
        mass_points.append(['4', '1p90', '10'])
        mass_points.append(['4', '1p90', '100'])
        mass_points.append(['5', '0p83', '0p1'])
        mass_points.append(['5', '0p83', '1p0'])
        mass_points.append(['5', '0p83', '10'])
        mass_points.append(['5', '0p83', '100'])
        mass_points.append(['5', '1p00', '0p1'])
        mass_points.append(['5', '1p00', '1p0'])
        mass_points.append(['5', '1p00', '10'])
        mass_points.append(['5', '1p00', '100'])
        mass_points.append(['5', '1p67', '0p1'])
        mass_points.append(['5', '1p67', '1p0'])
        mass_points.append(['5', '1p67', '10'])
        mass_points.append(['5', '1p67', '100'])
        mass_points.append(['5', '2p40', '0p1'])
        mass_points.append(['5', '2p40', '1p0'])
        mass_points.append(['5', '2p40', '10'])
        mass_points.append(['5', '2p40', '100'])
        for [mpi,mA,t] in mass_points:
            config_list.append(config)
            config_list[-1].JobType.pyCfgParams=["era={}".format(era),"data=False",]
            if era=="2022":
                os.system("""dasgoclient -query="/scenarioB1_mpi_{}_mA_{}_ctau_{}/jleonhol-AODSIM_2022_ext*bd8711905ed05b0226f084d42f06d7ac/USER instance=prod/phys03" > temp.txt""".format(mpi, mA, t))
                with open('temp.txt', 'r') as file:
                    dataset_name = file.readlines()[-1]
                #dataset_name = '/scenarioB1_mpi_{}_mA_{}_ctau_{}/jleonhol-AODSIM_2022_ext-bd8711905ed05b0226f084d42f06d7ac/USER'.format(mpi, mA, t)
                config_list[-1].Data.inputDataset = dataset_name
            elif era=="2022postEE":
                os.system("""dasgoclient -query="/scenarioB1_mpi_{}_mA_{}_ctau_{}/tafoyava-AODSIM_2022-6c55dbd4f99ed6c824b000a7a99348b1/USER instance=prod/phys03" > temp.txt""".format(mpi, mA, t))
                with open('temp.txt', 'r') as file:
                    dataset_name = file.readlines()[-1]
                #dataset_name = '/scenarioB1_mpi_{}_mA_{}_ctau_{}/tafoyava-AODSIM_2022-6c55dbd4f99ed6c824b000a7a99348b1/USER'.format(mpi, mA, t)
                config_list[-1].Data.inputDataset = dataset_name
            # No 2023 eras for the moment, when adding them, you have to run . install_cmssw.sh 2023central first
            config_list[-1].General.requestName = 'centralSkim__{}_{}_mpi-{}_mA-{}_ctau-{}mm_{}'.format(signal, era, mpi, mA, t, ntuple_version)
            print(config)
            #crabCommand('submit', config = config, dryrun = False) ## dryrun = True for local test

    elif "ScenarioB1priv" in sys.argv[2]:
        # This setup is provisional as it is tested with private signal crab produced samples
        #   -> Will be replaced by central datasets when done
        config.Data.outLFNDirBase = '/store/group/Run3Scouting/RAWScouting_privScenarioB1_v'+ntuple_version # DB no
        config.Data.inputDBS = 'phys03'
        config.Data.splitting = 'FileBased'
        config.Data.publication = True
        config.Data.unitsPerJob = int(100) # Increased to match 10 jobs per file aprox
        config.Data.outputDatasetTag = "private-Skim_{era}-v1".format(era=era)
        if era=="2022":
            mass_points.append(['ScenarioB1_mpi_4_mA_1p33_ctau_0p1', '/scenarioB1_mpi_4_mA_1p33_ctau_0p1/jleonhol-AODSIM_2022-bd8711905ed05b0226f084d42f06d7ac/USER'])
            mass_points.append(['ScenarioB1_mpi_4_mA_1p33_ctau_1p0', '/scenarioB1_mpi_4_mA_1p33_ctau_1p0/jleonhol-AODSIM_2022-bd8711905ed05b0226f084d42f06d7ac/USER'])
            mass_points.append(['ScenarioB1_mpi_4_mA_1p33_ctau_10', '/scenarioB1_mpi_4_mA_1p33_ctau_10/jleonhol-AODSIM_2022-bd8711905ed05b0226f084d42f06d7ac/USER'])
            mass_points.append(['ScenarioB1_mpi_4_mA_1p33_ctau_100', '/scenarioB1_mpi_4_mA_1p33_ctau_100/jleonhol-AODSIM_2022-bd8711905ed05b0226f084d42f06d7ac/USER'])
        elif era=="2022postEE":
            mass_points.append(['ScenarioB1_mpi_4_mA_1p33_ctau_0p1', '/scenarioB1_mpi_4_mA_1p33_ctau_0p1/jleonhol-AODSIM_2022-bd8711905ed05b0226f084d42f06d7ac/USER'])
            mass_points.append(['ScenarioB1_mpi_4_mA_1p33_ctau_1p0', '/scenarioB1_mpi_4_mA_1p33_ctau_1p0/jleonhol-AODSIM_2022-bd8711905ed05b0226f084d42f06d7ac/USER'])
            mass_points.append(['ScenarioB1_mpi_4_mA_1p33_ctau_10', '/scenarioB1_mpi_4_mA_1p33_ctau_10/jleonhol-AODSIM_2022-bd8711905ed05b0226f084d42f06d7ac/USER'])
            mass_points.append(['ScenarioB1_mpi_4_mA_1p33_ctau_100', '/scenarioB1_mpi_4_mA_1p33_ctau_100/jleonhol-AODSIM_2022-bd8711905ed05b0226f084d42f06d7ac/USER'])
        for [signal_name,dataset_name] in mass_points:
            config_list.append(config)
            config_list[-1].JobType.pyCfgParams=["era={}".format(era),"data=False",]
            config_list[-1].Data.inputDataset = dataset_name
            config_list[-1].General.requestName = 'centralSkim_{}_{}_{}'.format(signal_name, era, ntuple_version)
            print(config_list[-1])
            crabCommand('submit', config = config_list[-1], dryrun = False) ## dryrun = True for local test
            #print(config)
            #crabCommand('submit', config = config, dryrun = False) ## dryrun = True for local test
    #elif "[signal]" in sys.argv[2]: (<--- Add additional signals here)
    else:
        quit()
    
else:
    quit()



