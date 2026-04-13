from CRABClient.UserUtilities import config #, getUsernameFromSiteDB
from CRABAPI.RawCommand import crabCommand

datasets = []
#datasets.append('/BToPhi_MPhi-0p25_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext3/fernance-private-GENSIM-2022postEE-b3765a3f55e7d30c4d2e4a20b9e8cbb2/USER')
#datasets.append('/BToPhi_MPhi-0p3_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext3/fernance-private-GENSIM-2022postEE-c87c1b8424cfd35a61c99691abdfafcf/USER')
#datasets.append('/BToPhi_MPhi-0p4_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext3/fernance-private-GENSIM-2022postEE-c44c8ecb98bde8c6ca03831832181fcf/USER')
#datasets.append('/BToPhi_MPhi-0p5_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext3/fernance-private-GENSIM-2022postEE-6711c4e515f9bbed880e844b22a51f58/USER')
#datasets.append('/BToPhi_MPhi-0p6_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext3/fernance-private-GENSIM-2022postEE-bc0383b38076f439209907e2bdef3884/USER')
#datasets.append('/BToPhi_MPhi-0p7_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext3/fernance-private-GENSIM-2022postEE-6bc5956ba5270f751f08d9872e9ba0f0/USER')
#datasets.append('/BToPhi_MPhi-0p9_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext3/fernance-private-GENSIM-2022postEE-28f027021165d73241ff8129d8c1636b/USER')
#datasets.append('/BToPhi_MPhi-1p25_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext3/fernance-private-GENSIM-2022postEE-354cb1171df145cd4b5dbf2475eae022/USER')
#datasets.append('/BToPhi_MPhi-1p5_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext3/fernance-private-GENSIM-2022postEE-ccc54113a904e4ffd734df68a0eca381/USER')
#datasets.append('/BToPhi_MPhi-2p0_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext3/fernance-private-GENSIM-2022postEE-2b24228ed8ef919dac197e08540e1e3c/USER')
#datasets.append('/BToPhi_MPhi-2p85_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext3/fernance-private-GENSIM-2022postEE-74bd65d6e3fb1d60922f2bdf3b55e2fa/USER')
#datasets.append('/BToPhi_MPhi-3p35_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext3/fernance-private-GENSIM-2022postEE-a017280f2972cdfebe458f070f967b88/USER')
#datasets.append('/BToPhi_MPhi-4p0_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext3/fernance-private-GENSIM-2022postEE-e7c2ddb7e4dba442c588ae6b86b1b0ca/USER')
datasets.append('/BToPhi_MPhi-4p6_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext3/fernance-private-GENSIM-2022postEE-90ad4ee819623477cbb651f7e2a005a6/USER')
#datasets.append('/BToPhi_MPhi-5p0_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext3/fernance-private-GENSIM-2022postEE-91fec0ec137520888ea79674f83e330b/USER')
"""
datasets.append('/BToPhi_MPhi-0p25_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext/fernance-private-GENSIM-2022postEE-a42235e3939a3fe0af8012f53a567ebc/USER')
datasets.append('/BToPhi_MPhi-0p3_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext/fernance-private-GENSIM-2022postEE-09a9d0b43582aba69a1984b2be8fd1d3/USER')
datasets.append('/BToPhi_MPhi-0p4_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext/fernance-private-GENSIM-2022postEE-42e9f6c0fcab6aa7932d44b5cf41866c/USER')
datasets.append('/BToPhi_MPhi-0p5_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext/fernance-private-GENSIM-2022postEE-92e18f2f82bac1d5900c0d3a41623ee3/USER')
datasets.append('/BToPhi_MPhi-0p6_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext/fernance-private-GENSIM-2022postEE-abe0e179733e88d5823053c4c8c68d2f/USER')
datasets.append('/BToPhi_MPhi-0p7_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext/fernance-private-GENSIM-2022postEE-b75ea6b777c8bddfb4e9892dca998339/USER')
datasets.append('/BToPhi_MPhi-0p9_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext/fernance-private-GENSIM-2022postEE-c95164b423b113bf1b3b1d0eb47a5b50/USER')
datasets.append('/BToPhi_MPhi-1p25_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext/fernance-private-GENSIM-2022postEE-05028817197e124d4c127a6961e4aa81/USER')
datasets.append('/BToPhi_MPhi-1p5_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext/fernance-private-GENSIM-2022postEE-65560a9e89f3f9185da0fabc9522bef9/USER')
datasets.append('/BToPhi_MPhi-2p0_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext/fernance-private-GENSIM-2022postEE-8ef1a6bdbc2962246fbf03d8b6ecfbd4/USER')
datasets.append('/BToPhi_MPhi-2p85_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext/fernance-private-GENSIM-2022postEE-dd4ea29bd6e59bb50a07453749ae6b5c/USER')
datasets.append('/BToPhi_MPhi-3p35_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext/fernance-private-GENSIM-2022postEE-b88303f727b0b68ceaf932b906f8967d/USER')
datasets.append('/BToPhi_MPhi-4p0_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext/fernance-private-GENSIM-2022postEE-a84588d2652b7b9e9592aa9ca7e02407/USER')
datasets.append('/BToPhi_MPhi-4p6_ctau-0p1mm_TuneCP5_13p6TeV_pythia8_ext/fernance-private-GENSIM-2022postEE-4c0c7b2897225085fa82a2c3df9b608b/USER')
datasets.append('/BToPhi_MPhi-4p6_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext/fernance-private-GENSIM-2022postEE-ce209c75986142620045973eb8005664/USER')
datasets.append('/BToPhi_MPhi-4p6_ctau-100mm_TuneCP5_13p6TeV_pythia8_ext/fernance-private-GENSIM-2022postEE-95df6a68b463e6bd2081e6653c3fd5a4/USER')
datasets.append('/BToPhi_MPhi-4p6_ctau-10mm_TuneCP5_13p6TeV_pythia8_ext/fernance-private-GENSIM-2022postEE-680e327b4009571b92508e0ad5bd35fa/USER')
datasets.append('/BToPhi_MPhi-4p6_ctau-1mm_TuneCP5_13p6TeV_pythia8_ext/fernance-private-GENSIM-2022postEE-234f382350bf03c261006569c9bd5e4f/USER')
datasets.append('/BToPhi_MPhi-5p0_ctau-1000mm_TuneCP5_13p6TeV_pythia8_ext/fernance-private-GENSIM-2022postEE-b7effb16e300265b30ee59ad8ee68588/USER')
"""

for dataset in datasets:

    name = dataset.split('/')[1]

    conf = config()

    conf.General.requestName = 'crab_hltraw_%s_2022postEE'%(name)
    conf.General.transferOutputs = True
    conf.General.transferLogs = False

    conf.JobType.pluginName = 'Analysis'
    conf.JobType.psetName = 'configs/hltraw_2022postEE_cfg.py'
    conf.JobType.maxMemoryMB = 3000

    conf.Data.inputDataset = dataset
    conf.Data.splitting = 'FileBased'
    conf.Data.unitsPerJob = 1
    conf.Data.totalUnits = 3000
    conf.Data.outLFNDirBase = '/store/user/fernance/BToPhi-samples/'
    conf.Data.publication = True
    conf.Data.outputDatasetTag = 'private-HLTRAW-2022postEE'
    conf.Data.ignoreLocality = True
    conf.Data.inputDBS = 'phys03'

    conf.Site.storageSite = 'T2_US_UCSD'

    conf.Site.blacklist = ['T2_US_MIT']
    conf.Site.whitelist = ['T2_US_Wisconsin','T2_US_Florida','T2_US_Nebraska','T2_US_Caltech','T2_US_Purdue']
    conf.section_("Debug")
    conf.Debug.extraJDL = ['My.CMS_ALLOW_OVERFLOW=False']

    print(conf)
    crabCommand('submit', config = conf, dryrun = False)
