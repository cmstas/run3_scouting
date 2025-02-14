import FWCore.ParameterSet.Config as cms

externalLHEProducer = cms.EDProducer("ExternalLHEProducer",
    args = cms.vstring('{GRIDPACK}'),
    nEvents = cms.untracked.uint32(5000),
    numberOfParameters = cms.uint32(1),
    outputFile = cms.string('cmsgrid_final.lhe'),
    generateConcurrently = cms.untracked.bool(True),
    scriptName = cms.FileInPath('GeneratorInterface/LHEInterface/data/run_generic_tarball_cvmfs.sh')
)
CROSS_SECTION = 1 # pb
MASS_Zd = {ZDMASS} # in GeV
LIFETIME_Zd_inMM = {LIFETIME} # in mm
WIDTH_Zd = (1000./LIFETIME_Zd_inMM)*0.19733e-15 # in GeV
EPSILON_Zd =  {EPSILON}

BR_MUMU = {BR_MUMU}
BR_EE = {BR_EE}
BR_TAUTAU = {BR_TAUTAU}

BR_UUBAR = {BR_UUBAR}
BR_DDBAR = {BR_DDBAR}
BR_SSBAR = {BR_SSBAR}

BR_CCBAR = {BR_CCBAR}
BR_BBBAR = {BR_BBBAR}

BR_MUNUMUNUBAR = {BR_MUNUMUNUBAR}
BR_ENUENUBAR = {BR_ENUENUBAR}
BR_TAUNUTAUNUBAR = {BR_TAUNUTAUNUBAR}

import re
EPSILON_Zdmod = str(EPSILON_Zd)
EPSILON_Zdmod = re.sub("\.","p",EPSILON_Zdmod)

import FWCore.ParameterSet.Config as cms
from Configuration.Generator.Pythia8CommonSettings_cfi import *

from Configuration.Generator.MCTunesRun3ECM13p6TeV.PythiaCP5Settings_cfi import *
from Configuration.Generator.PSweightsPythia.PythiaPSweightsSettings_cfi import *

generator = cms.EDFilter("Pythia8ConcurrentHadronizerFilter",
    pythiaPylistVerbosity = cms.untracked.int32(1),
    filterEfficiency = cms.untracked.double(1),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    comEnergy = cms.double(13600.),
    crossSection = cms.untracked.double(CROSS_SECTION),
    maxEventsToPrint = cms.untracked.int32(10),
    PythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CP5SettingsBlock,
        pythia8PSweightsSettingsBlock,
        processParameters = cms.vstring(
            'SLHA:useDecayTable = off', # use pythia8 decay mode instead of decays defined in LH accord
            'LesHouches:setLifetime = 2',
            "1023:new = Zd Zdbar 3 0 0",
            "1023:m0 = %s" % MASS_Zd,
            "1023:mWidth = %s" % WIDTH_Zd,
            "1023:tau0 = %s" % LIFETIME_Zd_inMM,
            "1023:isResonance = on",
            "1023:mayDecay = on",
            "1023:oneChannel = 1  %s 100 -2 2" %BR_UUBAR,
            "1023:addChannel = 1  %s 100 -4 4" %BR_CCBAR,
            "1023:addChannel = 1  %s 100 -13 13" %BR_MUMU,
            "1023:addChannel = 1  %s 100 -11 11" %BR_EE,
            "1023:addChannel = 1  %s 100 -15 15" %BR_TAUTAU,
            "1023:addChannel = 1  %s 100 -3 3" %BR_SSBAR,
            "1023:addChannel = 1  %s 100 1 -1" %BR_DDBAR,
            "1023:addChannel = 1  %s 100 -5 5" %BR_BBBAR,
            "1023:addChannel = 1  %s 100 16 -16" %BR_TAUNUTAUNUBAR,
            "1023:addChannel = 1  %s 100 14 -14" %BR_MUNUMUNUBAR,
            "1023:addChannel = 1  %s 100 12 -12" %BR_ENUENUBAR
        ),
        parameterSets = cms.vstring(
            'pythia8CommonSettings',
            'pythia8CP5Settings',
            'pythia8PSweightsSettings',
            'processParameters'
        )
    )
)

# -- Require at least one muon in the final state. Muon from taus and HF decays are not considered.
MuMuFilter = cms.EDFilter("MCParticlePairFilter",
                          Status = cms.untracked.vint32(1, 1),
                          MinPt = cms.untracked.vdouble(2.5, 2.5),
                          MaxEta = cms.untracked.vdouble(2.5, 2.5),
                          MinEta = cms.untracked.vdouble(-2.5, -2.5),
                          ParticleID1 = cms.untracked.vint32(13,-13),
                          )

MuFilter = cms.EDFilter("PythiaFilter",
    Status = cms.untracked.int32(0),
    MotherID = cms.untracked.int32(1023),
    MinPt = cms.untracked.double(2.5),
    ParticleID = cms.untracked.int32(13),
    MaxEta = cms.untracked.double(2.5),
    MinEta = cms.untracked.double(-2.5)
)
ProductionFilterSequence = cms.Sequence(generator*MuMuFilter*MuFilter)


# Link to generator fragment:
# genFragments/Generator/Pythia/HTo2ZdTo2mu2x/13p6TeV/HTo2ZdTo2mu2x_MZd-20_Epsilon-1e-08_TuneCP5_13p6TeV_pythia8_cff.py
