from CRABClient.UserUtilities import config #, getUsernameFromSiteDB
from CRABAPI.RawCommand import crabCommand

datasets = []
datasets.append('/BToPhi_MPhi-0p25_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext3/fernance-private-GENSIM-2023BPix-3d91ed39f2cfd773a40fc8d070ab32d2/USER')
datasets.append('/BToPhi_MPhi-0p3_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext3/fernance-private-GENSIM-2023BPix-e4905580243087eeae10f67ccdab59c7/USER')
datasets.append('/BToPhi_MPhi-0p4_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext3/fernance-private-GENSIM-2023BPix-c24a138b9064821d3eac7dcbb371695b/USER')
datasets.append('/BToPhi_MPhi-0p5_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext3/fernance-private-GENSIM-2023BPix-533606d803123c2fe60c6e5c04a26a50/USER')
datasets.append('/BToPhi_MPhi-0p6_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext3/fernance-private-GENSIM-2023BPix-be5a3c2fd81c6a6656087b5c87be1d60/USER')
datasets.append('/BToPhi_MPhi-0p7_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext3/fernance-private-GENSIM-2023BPix-95c58363e93eaafbad48334480c296a4/USER')
datasets.append('/BToPhi_MPhi-0p9_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext3/fernance-private-GENSIM-2023BPix-beb090edafb07242ca67f36624ff0174/USER')
datasets.append('/BToPhi_MPhi-1p25_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext3/fernance-private-GENSIM-2023BPix-c09906154d6715097842ffbc3b37abc0/USER')
datasets.append('/BToPhi_MPhi-1p5_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext3/fernance-private-GENSIM-2023BPix-62a6a233a7cbdeaf0807ed2008e89a3e/USER')
datasets.append('/BToPhi_MPhi-2p0_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext3/fernance-private-GENSIM-2023BPix-e4079e9a105caaac73771c664afe3684/USER')
datasets.append('/BToPhi_MPhi-2p85_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext3/fernance-private-GENSIM-2023BPix-8cffcc3f2c4c9993194ce044e235efea/USER')
datasets.append('/BToPhi_MPhi-3p35_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext3/fernance-private-GENSIM-2023BPix-9737681ca2dc545356468a2a46a53881/USER')
datasets.append('/BToPhi_MPhi-4p0_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext3/fernance-private-GENSIM-2023BPix-168d55adf4bf075181415c4acbc9d2f5/USER')
datasets.append('/BToPhi_MPhi-4p6_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext3/fernance-private-GENSIM-2023BPix-6cb70ccc44dc3279e001e98528e4b3eb/USER')
"""
datasets.append('/BToPhi_MPhi-0p25_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext/fernance-private-GENSIM-2023BPix-696e05f2d65ae5ce769cbe4752339317/USER')
datasets.append('/BToPhi_MPhi-0p3_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext/fernance-private-GENSIM-2023BPix-2891148643b9c27b59fcbd01cb9e92c0/USER')
datasets.append('/BToPhi_MPhi-0p4_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext/fernance-private-GENSIM-2023BPix-635e57f5ea541783be416aaeffb27612/USER')
datasets.append('/BToPhi_MPhi-0p5_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext/fernance-private-GENSIM-2023BPix-82fa98534f59dbef78d113e9abe90605/USER')
datasets.append('/BToPhi_MPhi-0p6_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext/fernance-private-GENSIM-2023BPix-aca3c760a3a4902c0f853c7a47cb7968/USER')
datasets.append('/BToPhi_MPhi-0p7_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext/fernance-private-GENSIM-2023BPix-37b314f63c2d4784e56b0852d048f50d/USER')
datasets.append('/BToPhi_MPhi-0p9_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext/fernance-private-GENSIM-2023BPix-fb231e09828c16f1ff1c8fddda555aa1/USER')
datasets.append('/BToPhi_MPhi-1p25_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext/fernance-private-GENSIM-2023BPix-17c7ea8b5984403f9a043aab30b21d2c/USER')
datasets.append('/BToPhi_MPhi-1p5_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext/fernance-private-GENSIM-2023BPix-38d40396b9c87e50690129c1e7b4ddb7/USER')
datasets.append('/BToPhi_MPhi-2p0_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext/fernance-private-GENSIM-2023BPix-a3b30e8b37d31169c7c114244a84c64c/USER')
datasets.append('/BToPhi_MPhi-2p85_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext/fernance-private-GENSIM-2023BPix-577932d239866d54a7aa22801d6a70ef/USER')
datasets.append('/BToPhi_MPhi-3p35_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext/fernance-private-GENSIM-2023BPix-986aa562dff28a1dbb92ecdec6d12bfa/USER')
datasets.append('/BToPhi_MPhi-4p0_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext/fernance-private-GENSIM-2023BPix-69160f53ec488138deaed3af2531f570/USER')
datasets.append('/BToPhi_MPhi-4p6_ctau-0p1mm_TuneCP5_13p6TeV_pythia8_ext/fernance-private-GENSIM-2023BPix-faf49bc90f3afc018be43ddc13781b8a/USER')
datasets.append('/BToPhi_MPhi-4p6_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext/fernance-private-GENSIM-2023BPix-e0dd2d3be4d57d5f3803b548bed7fd09/USER')
datasets.append('/BToPhi_MPhi-4p6_ctau-100mm_TuneCP5_13p6TeV_pythia8_ext/fernance-private-GENSIM-2023BPix-98ba354cdeab1bfeab4b23d1d4992f99/USER')
datasets.append('/BToPhi_MPhi-4p6_ctau-10mm_TuneCP5_13p6TeV_pythia8_ext/fernance-private-GENSIM-2023BPix-541138f8ba858ae980e92e06474b36c1/USER')
datasets.append('/BToPhi_MPhi-4p6_ctau-1mm_TuneCP5_13p6TeV_pythia8_ext/fernance-private-GENSIM-2023BPix-74882c457b66589a77e8592e02530404/USER')
datasets.append('/BToPhi_MPhi-5p0_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext/fernance-private-GENSIM-2023BPix-12cc4d97f0dd385bd81558c4337b9852/USER')
"""

for dataset in datasets:

    name = dataset.split('/')[1]

    conf = config()

    conf.General.requestName = 'crab_hltraw_%s_2023BPix'%(name)
    conf.General.transferOutputs = True
    conf.General.transferLogs = False

    conf.JobType.pluginName = 'Analysis'
    conf.JobType.psetName = 'configs/hltraw_2023BPix_cfg.py'
    conf.JobType.maxMemoryMB = 3000

    conf.Data.inputDataset = dataset
    conf.Data.splitting = 'FileBased'
    conf.Data.unitsPerJob = 1
    conf.Data.totalUnits = 3000
    conf.Data.outLFNDirBase = '/store/user/fernance/BToPhi-samples/'
    conf.Data.publication = True
    conf.Data.outputDatasetTag = 'private-HLTRAW-2023BPix'
    conf.Data.ignoreLocality = True
    conf.Data.inputDBS = 'phys03'

    conf.Site.storageSite = 'T2_US_UCSD'

    conf.Site.blacklist = ['T2_US_MIT']
    conf.Site.whitelist = ['T2_US_Wisconsin','T2_US_Florida','T2_US_Nebraska','T2_US_Caltech','T2_US_Purdue']
    conf.section_("Debug")
    conf.Debug.extraJDL = ['My.CMS_ALLOW_OVERFLOW=False']

    print(conf)
    crabCommand('submit', config = conf, dryrun = False)
