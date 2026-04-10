from CRABClient.UserUtilities import config
config = config()

config.General.requestName = 'gensim_5p0_1000mm_2022postEE'
config.General.transferOutputs = True
config.General.transferLogs = False

config.JobType.pluginName = 'PrivateMC'
config.JobType.psetName = 'configs/gensim_5p0_1000mm_2022postEE_cfg.py'

config.Data.outputPrimaryDataset = 'BToPhi_MPhi-5p0_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext3'
config.Data.splitting = 'EventBased'
config.Data.unitsPerJob = 1000
NJOBS = 3000
config.Data.totalUnits = config.Data.unitsPerJob * NJOBS

config.Data.outLFNDirBase = '/store/user/fernance/BToPhi-samples/'
config.Data.publication = True
config.Data.outputDatasetTag = 'private-GENSIM-2022postEE'

config.Site.storageSite = 'T2_US_UCSD'

config.Site.blacklist = ['T2_US_MIT']
config.Site.whitelist = ['T2_US_UCSD','T2_US_Wisconsin','T2_US_Florida']
config.section_("Debug")
config.Debug.extraJDL = ['My.CMS_ALLOW_OVERFLOW=False']
