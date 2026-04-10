from CRABClient.UserUtilities import config #, getUsernameFromSiteDB
from CRABAPI.RawCommand import crabCommand

datasets = []
datasets.append('/BToPhi_MPhi-0p25_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext3/fernance-private-GENSIM-2022-04ac24cc914538e1ae648b825991958c/USER')
datasets.append('/BToPhi_MPhi-0p3_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext3/fernance-private-GENSIM-2022-733d7ae6d825ac3be0dbdc31622c814c/USER')
datasets.append('/BToPhi_MPhi-0p4_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext3/fernance-private-GENSIM-2022-9cb6a6b04164b65db1152fa2db6fb840/USER')
datasets.append('/BToPhi_MPhi-0p5_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext3/fernance-private-GENSIM-2022-57481f9648c9bd6db7b576aa9cf6ed02/USER')
datasets.append('/BToPhi_MPhi-0p6_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext3/fernance-private-GENSIM-2022-9456211164498abc89c2695943041607/USER')
datasets.append('/BToPhi_MPhi-0p7_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext3/fernance-private-GENSIM-2022-eb5bc8ab1b3a441c016ff6d6930d53f0/USER')
datasets.append('/BToPhi_MPhi-0p9_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext3/fernance-private-GENSIM-2022-c3792532399b9d9637b460341239dee4/USER')
datasets.append('/BToPhi_MPhi-1p25_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext3/fernance-private-GENSIM-2022-b532698ed6c5dc807a8980e66b3e4015/USER')
datasets.append('/BToPhi_MPhi-1p5_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext3/fernance-private-GENSIM-2022-397743000c5d12defb6cceaae780e7fe/USER')
datasets.append('/BToPhi_MPhi-2p0_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext3/fernance-private-GENSIM-2022-4fdcaf1f9c86ad4529d027dcbb12f8f4/USER')
datasets.append('/BToPhi_MPhi-2p85_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext3/fernance-private-GENSIM-2022-d25a0f82c40710a755e8e01e5d6fbc96/USER')
datasets.append('/BToPhi_MPhi-3p35_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext3/fernance-private-GENSIM-2022-0d637169376e8540a6b09fea8bd3c3f7/USER')
datasets.append('/BToPhi_MPhi-4p0_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext3/fernance-private-GENSIM-2022-c71dc2accf0d170f261ebd1ff9bdd5f1/USER')
datasets.append('/BToPhi_MPhi-4p6_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext3/fernance-private-GENSIM-2022-1ebeb5b44623aeec087802ad1c36dbb1/USER')
#datasets.append('/BToPhi_MPhi-5p0_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext3/fernance-private-GENSIM-2022-f939d517ac47067a527b961f6dd9f8fb/USER')
"""
datasets.append('/BToPhi_MPhi-0p25_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext/fernance-private-GENSIM-2022-5c915998ee1069ded75095b8212228c1/USER')
datasets.append('/BToPhi_MPhi-0p3_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext/fernance-private-GENSIM-2022-cb54fb30bedad5633ce72342fbc0bd6e/USER')
datasets.append('/BToPhi_MPhi-0p4_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext/fernance-private-GENSIM-2022-577cc66b15a1fef183e121e9bbe960be/USER')
datasets.append('/BToPhi_MPhi-0p5_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext/fernance-private-GENSIM-2022-870ef76932d7ffd8996d26e58022e015/USER')
datasets.append('/BToPhi_MPhi-0p6_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext/fernance-private-GENSIM-2022-884b48ee195c98f15e5d75d930a92b15/USER')
datasets.append('/BToPhi_MPhi-0p7_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext/fernance-private-GENSIM-2022-7dfb03475b59e4b3b28a19cfca5f8592/USER')
datasets.append('/BToPhi_MPhi-0p9_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext/fernance-private-GENSIM-2022-a90503e8b36a77385d21df0273a3c826/USER')
datasets.append('/BToPhi_MPhi-1p25_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext/fernance-private-GENSIM-2022-aeae921ae49576802bb6688dcd88b241/USER')
datasets.append('/BToPhi_MPhi-1p5_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext/fernance-private-GENSIM-2022-9438471406b2ff8547387dabc83418be/USER')
datasets.append('/BToPhi_MPhi-2p0_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext/fernance-private-GENSIM-2022-a8c5aca69ec1389eb030d1be0556e275/USER')
datasets.append('/BToPhi_MPhi-2p85_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext/fernance-private-GENSIM-2022-684e930d1db377afe44d7e9e1a2f420e/USER')
datasets.append('/BToPhi_MPhi-3p35_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext/fernance-private-GENSIM-2022-a9a9b77b60bfafd9d83847b28f91e2bc/USER')
datasets.append('/BToPhi_MPhi-4p0_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext/fernance-private-GENSIM-2022-0bdc8fd3877738bb798c7901aa7287e8/USER')
datasets.append('/BToPhi_MPhi-4p6_ctau-0p1mm_TuneCP5_13p6TeV_pythia8_ext/fernance-private-GENSIM-2022-fbd93a619dbc09d7f395a97754aad09c/USER')
datasets.append('/BToPhi_MPhi-4p6_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext/fernance-private-GENSIM-2022-e8ce38d90ef8c18051bdde8a9c9b2b6b/USER')
datasets.append('/BToPhi_MPhi-4p6_ctau-100mm_TuneCP5_13p6TeV_pythia8_ext/fernance-private-GENSIM-2022-2f2ff8a10ed81d37f8b2a391e20cc473/USER')
datasets.append('/BToPhi_MPhi-4p6_ctau-10mm_TuneCP5_13p6TeV_pythia8_ext/fernance-private-GENSIM-2022-ef58a9af2d47d320c61f1e68ba5e361b/USER')
datasets.append('/BToPhi_MPhi-4p6_ctau-1mm_TuneCP5_13p6TeV_pythia8_ext/fernance-private-GENSIM-2022-1c837fc6169ec6440dadf9ea4c3b3541/USER')
datasets.append('/BToPhi_MPhi-5p0_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext/fernance-private-GENSIM-2022-27c1bcc2479f06471d0247e63728c231/USER')
"""

for dataset in datasets:

    name = dataset.split('/')[1]

    conf = config()

    conf.General.requestName = 'crab_hltraw_%s_2022'%(name)
    conf.General.transferOutputs = True
    conf.General.transferLogs = False

    conf.JobType.pluginName = 'Analysis'
    conf.JobType.psetName = 'configs/hltraw_2022_cfg.py'
    conf.JobType.maxMemoryMB = 3000

    conf.Data.inputDataset = dataset
    conf.Data.splitting = 'FileBased'
    conf.Data.unitsPerJob = 1
    conf.Data.totalUnits = -1
    conf.Data.outLFNDirBase = '/store/user/fernance/BToPhi-samples/'
    conf.Data.publication = True
    conf.Data.outputDatasetTag = 'private-HLTRAW-2022'
    conf.Data.ignoreLocality = True
    conf.Data.inputDBS = 'phys03'

    conf.Site.storageSite = 'T2_US_UCSD'

    conf.Site.blacklist = ['T2_US_MIT']
    conf.Site.whitelist = ['T2_US_Wisconsin','T2_US_Florida','T2_US_Nebraska','T2_US_Caltech','T2_US_Purdue']
    conf.section_("Debug")
    conf.Debug.extraJDL = ['My.CMS_ALLOW_OVERFLOW=False']

    print(conf)
    crabCommand('submit', config = conf, dryrun = False)
