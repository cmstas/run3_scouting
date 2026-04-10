import FWCore.ParameterSet.Config as cms
from Configuration.StandardSequences.Eras import eras
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunesRun3ECM13p6TeV.PythiaCP5Settings_cfi import *

# Production Info
configurationMetadata = cms.untracked.PSet(
        version = cms.untracked.string('$1.0$'),
        name = cms.untracked.string('$Generic BBbar with a long-lived scalar resonance, m=0.9 GeV, ctau=1 mm$'),
        annotation = cms.untracked.string('Generic BBbar with a long-lived scalar resonance, m=0.9 GeV, ctau=1 mm')
)

generator = cms.EDFilter("Pythia8ConcurrentGeneratorFilter",
    PythiaParameters = cms.PSet(
            pythia8CommonSettingsBlock,
            pythia8CP5SettingsBlock,
            processParameters = cms.vstring(
                    'SoftQCD:nonDiffractive = on',
                    'PTFilter:filter = on',  
                    'PTFilter:quarkToFilter = 5',  
                    'PTFilter:scaleToFilter = 1.0',  
                    'ParticleDecays:limitTau0 = off',
                    '6000211:all = GeneralResonance void 0 0 0 0.9 0.001 0.0 0.0 1',
                    '6000211:oneChannel = 1 1.0 101 13 -13',
                    '521:addChannel = 1 1 1 6000211 321',
                    '511:addChannel = 1 1 1 6000211 311',
                    '531:addChannel = 1 1 1 6000211 333', 
                    '541:addChannel = 1 1 1 6000211 431',
                    '5122:addChannel = 1 1 1 6000211 3122',
            ),
            parameterSets = cms.vstring('pythia8CommonSettings',
                                        'pythia8CP5Settings',
                                        'processParameters'),
    ),
    comEnergy = cms.double(13600),
    crossSection = cms.untracked.double(1),
    filterEfficiency = cms.untracked.double(-1),
    maxEventsToPrint = cms.untracked.int32(0),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    pythiaPylistVerbosity = cms.untracked.int32(0)
)


### Filters
llphitomumukingenfilter = cms.EDFilter("PythiaDauVFilter",
                                       verbose         = cms.untracked.int32(1),
                                       NumberDaughters = cms.untracked.int32(2), 
                                       ParticleID      = cms.untracked.int32(6000211),  
                                       DaughterIDs     = cms.untracked.vint32(13, -13), 
                                       MinPt           = cms.untracked.vdouble( 2.0, 2.0), 
                                       MinEta          = cms.untracked.vdouble(-3.0,-3.0), 
                                       MaxEta          = cms.untracked.vdouble( 3.0, 3.0)
                               )

llphigenfilter = cms.EDFilter("PythiaDauFilter",
                              MinPt = cms.untracked.double(2.0),
                              MinEta = cms.untracked.double(-3.0),
                              MaxEta = cms.untracked.double( 3.0),
                              ParticleID = cms.untracked.int32(6000211),
                              DaughterIDs = cms.untracked.vint32(-13,13),
                              NumberDaughters = cms.untracked.int32(2)
                      )


### Production+filter sequence
#ProductionFilterSequence = cms.Sequence(generator*llphitomumukingenfilter)
#ProductionFilterSequence = cms.Sequence(generator*llphigenfilter)
ProductionFilterSequence = cms.Sequence(generator)
