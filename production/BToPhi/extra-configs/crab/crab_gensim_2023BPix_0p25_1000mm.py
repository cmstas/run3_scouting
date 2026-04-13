from CRABClient.UserUtilities import config
config = config()

config.General.requestName = 'gensim_0p25_1000mm_2023BPix'
config.General.transferOutputs = True
config.General.transferLogs = False

config.JobType.pluginName = 'PrivateMC'
config.JobType.psetName = 'configs/gensim_0p25_1000mm_2023BPix_cfg.py'

config.Data.outputPrimaryDataset = 'BToPhi_MPhi-0p25_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext3'
config.Data.splitting = 'EventBased'
config.Data.unitsPerJob = 1000
NJOBS = 3000
config.Data.totalUnits = config.Data.unitsPerJob * NJOBS

config.Data.outLFNDirBase = '/store/user/fernance/BToPhi-samples/'
config.Data.publication = True
config.Data.outputDatasetTag = 'private-GENSIM-2023BPix'

config.Site.storageSite = 'T2_US_UCSD'

config.Site.blacklist = ['T2_US_MIT']
config.Site.whitelist = ['T2_US_UCSD','T2_US_Wisconsin','T2_US_Florida']
config.section_("Debug")
config.Debug.extraJDL = ['My.CMS_ALLOW_OVERFLOW=False']
