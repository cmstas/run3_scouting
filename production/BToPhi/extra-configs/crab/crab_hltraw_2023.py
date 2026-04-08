from CRABClient.UserUtilities import config #, getUsernameFromSiteDB
from CRABAPI.RawCommand import crabCommand

datasets = []
datasets.append('/BToPhi_MPhi-0p25_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext3/fernance-private-GENSIM-2023-0742df3d9fa8c7daac18c31affb255d4/USER')
datasets.append('/BToPhi_MPhi-0p3_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext3/fernance-private-GENSIM-2023-459bedf957afe26ecce0842cbccf7e96/USER')
datasets.append('/BToPhi_MPhi-0p4_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext3/fernance-private-GENSIM-2023-5049402cb93126d63ef83412fc6498ca/USER')
datasets.append('/BToPhi_MPhi-0p5_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext3/fernance-private-GENSIM-2023-edd0d39992221ec83d09fdf693846f79/USER')
datasets.append('/BToPhi_MPhi-0p6_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext3/fernance-private-GENSIM-2023-0319c51656fe0a438e5f6f199d792bd9/USER')
datasets.append('/BToPhi_MPhi-0p7_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext3/fernance-private-GENSIM-2023-71cd160e08dd7b8f498b06a97ce6d712/USER')
datasets.append('/BToPhi_MPhi-0p9_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext3/fernance-private-GENSIM-2023-357549d65d68d9a4d3da413b55a07bfd/USER')
datasets.append('/BToPhi_MPhi-1p25_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext3/fernance-private-GENSIM-2023-5a5eab9048dd67d306114708c47e272b/USER')
datasets.append('/BToPhi_MPhi-1p5_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext3/fernance-private-GENSIM-2023-64d7832b9a7e05bee70d545fbbb54f14/USER')
datasets.append('/BToPhi_MPhi-2p0_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext3/fernance-private-GENSIM-2023-e05cdb4e8db9dd6324c5f533fdb7f940/USER')
datasets.append('/BToPhi_MPhi-2p85_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext3/fernance-private-GENSIM-2023-7459204128726bac01929c52a2b8a7fa/USER')
datasets.append('/BToPhi_MPhi-3p35_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext3/fernance-private-GENSIM-2023-7747c42f0a397aeddab898b6e5c64da7/USER')
datasets.append('/BToPhi_MPhi-4p0_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext3/fernance-private-GENSIM-2023-fc0179a06114250e5d057924e1545314/USER')
datasets.append('/BToPhi_MPhi-4p6_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext3/fernance-private-GENSIM-2023-e5fbac9f92e0b075b4237a1f731f5a20/USER')
"""
datasets.append('/BToPhi_MPhi-0p25_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext/fernance-private-GENSIM-2023-406cae102bd2d820388e035a1b180a31/USER')
datasets.append('/BToPhi_MPhi-0p3_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext/fernance-private-GENSIM-2023-a84d7485f01202a4d4125ff135dd6a1d/USER')
datasets.append('/BToPhi_MPhi-0p4_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext/fernance-private-GENSIM-2023-336d626a6c6039fb560cabd6eec957c5/USER')
datasets.append('/BToPhi_MPhi-0p5_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext/fernance-private-GENSIM-2023-d9e81283eef133ac063a33055c97c102/USER')
datasets.append('/BToPhi_MPhi-0p6_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext/fernance-private-GENSIM-2023-fae7c6578e86c9aa140d0ffcc6fc40df/USER')
datasets.append('/BToPhi_MPhi-0p7_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext/fernance-private-GENSIM-2023-fe86d8e2dc6931bbd96352725718bd7c/USER')
datasets.append('/BToPhi_MPhi-0p9_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext/fernance-private-GENSIM-2023-ef3ea3adf5e3559f05180d658fdf84d0/USER')
datasets.append('/BToPhi_MPhi-1p25_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext/fernance-private-GENSIM-2023-5ea3f94bd42dc1a2a520dd33f4f4ccca/USER')
datasets.append('/BToPhi_MPhi-1p5_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext/fernance-private-GENSIM-2023-6a9c6a2431fbda11512cc4941789d20d/USER')
datasets.append('/BToPhi_MPhi-2p0_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext/fernance-private-GENSIM-2023-a0d23fe082a969ff827cd12485196df2/USER')
datasets.append('/BToPhi_MPhi-2p85_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext/fernance-private-GENSIM-2023-cf2b293ed417c56b91c9c3d4c0d268bf/USER')
datasets.append('/BToPhi_MPhi-3p35_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext/fernance-private-GENSIM-2023-74172e2a59c3d6ea841a6b07250a6291/USER')
datasets.append('/BToPhi_MPhi-4p0_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext/fernance-private-GENSIM-2023-45bd1d4f49fc8fb9553e53b3eb85ac1f/USER')
datasets.append('/BToPhi_MPhi-4p6_ctau-0p1mm_TuneCP5_13p6TeV_pythia8_ext/fernance-private-GENSIM-2023-03349891db07d388acca7a19c82409bb/USER')
datasets.append('/BToPhi_MPhi-4p6_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext/fernance-private-GENSIM-2023-f97114777291a6678e5374120c400614/USER')
datasets.append('/BToPhi_MPhi-4p6_ctau-100mm_TuneCP5_13p6TeV_pythia8_ext/fernance-private-GENSIM-2023-0cd571e3aff0a0c5ba11a79e6cf26998/USER')
datasets.append('/BToPhi_MPhi-4p6_ctau-10mm_TuneCP5_13p6TeV_pythia8_ext/fernance-private-GENSIM-2023-248d8ef2193d1ca98e1dbfc8bfbe9347/USER')
datasets.append('/BToPhi_MPhi-4p6_ctau-1mm_TuneCP5_13p6TeV_pythia8_ext/fernance-private-GENSIM-2023-66aa00b377256ea04b249047e10e1a60/USER')
datasets.append('/BToPhi_MPhi-5p0_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext/fernance-private-GENSIM-2023-b50654b57893b01fcf285c26cc77706c/USER')
"""

for dataset in datasets:

    name = dataset.split('/')[1]

    conf = config()

    conf.General.requestName = 'crab_hltraw_%s_2023'%(name)
    conf.General.transferOutputs = True
    conf.General.transferLogs = False

    conf.JobType.pluginName = 'Analysis'
    conf.JobType.psetName = 'configs/hltraw_2023_cfg.py'
    conf.JobType.maxMemoryMB = 3000

    conf.Data.inputDataset = dataset
    conf.Data.splitting = 'FileBased'
    conf.Data.unitsPerJob = 1
    conf.Data.totalUnits = 3000
    conf.Data.outLFNDirBase = '/store/user/fernance/BToPhi-samples/'
    conf.Data.publication = True
    conf.Data.outputDatasetTag = 'private-HLTRAW-2023'
    conf.Data.ignoreLocality = True
    conf.Data.inputDBS = 'phys03'

    conf.Site.storageSite = 'T2_US_UCSD'

    conf.Site.blacklist = ['T2_US_MIT']
    conf.Site.whitelist = ['T2_US_Wisconsin','T2_US_Florida','T2_US_Nebraska','T2_US_Caltech','T2_US_Purdue']
    conf.section_("Debug")
    conf.Debug.extraJDL = ['My.CMS_ALLOW_OVERFLOW=False']

    print(conf)
    crabCommand('submit', config = conf, dryrun = False)
