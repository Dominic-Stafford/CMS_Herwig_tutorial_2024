import FWCore.ParameterSet.Config as cms

from Configuration.Generator.Herwig7Settings.Herwig7StableParticlesForDetector_cfi import *
from Configuration.Generator.Herwig7Settings.Herwig7CH3TuneSettings_cfi import *
from Configuration.Generator.Herwig7Settings.Herwig7_7p1SettingsFor7p2_cfi import *
from Configuration.Generator.Herwig7Settings.Herwig7LHECommonSettings_cfi import *
from Configuration.Generator.Herwig7Settings.Herwig7LHEPowhegSettings_cfi import *



externalLHEProducer = cms.EDProducer("ExternalLHEProducer",
    args = cms.vstring('/cvmfs/cms.cern.ch/phys_generator/gridpacks/slc6_amd64_gcc630/13TeV/Powheg/V2/RelValidation/TTBar/hvq_slc6_amd64_gcc630_CMSSW_9_3_9_patch1_ttbar_new.tgz'),
    nEvents = cms.untracked.uint32(5000),
    numberOfParameters = cms.uint32(1),
    outputFile = cms.string('cmsgrid_final.lhe'),
    scriptName = cms.FileInPath('GeneratorInterface/LHEInterface/data/run_generic_tarball_cvmfs.sh'),
    generateConcurrently = cms.untracked.bool(True),
    postGenerationCommand = cms.untracked.vstring('mergeLHE.py', '-n', '-i', 'thread*/cmsgrid_final.lhe', '-o', 'cmsgrid_final.lhe'),
)


generator = cms.EDFilter("Herwig7GeneratorFilter",
    herwig7StableParticlesForDetectorBlock,
    herwig7CH3SettingsBlock,
    herwig7LHECommonSettingsBlock,
    herwig7LHEPowhegSettingsBlock,
    herwig7p1SettingsFor7p2Block,
    configFiles = cms.vstring(),                                                                                                                                             
    parameterSets = cms.vstring('herwig7CH3PDF', 'herwig7CH3AlphaS', 'herwig7CH3MPISettings', 'hw_7p1SettingsFor7p2', 'herwig7StableParticlesForDetector', 'hw_lhe_common_settings', 'hw_lhe_powheg_settings'),
    crossSection = cms.untracked.double(-1),
    dataLocation = cms.string('${HERWIGPATH:-6}'),
    eventHandlers = cms.string('/Herwig/EventHandlers'),
    filterEfficiency = cms.untracked.double(1.0),
    generatorModule = cms.string('/Herwig/Generators/EventGenerator'),
    repository = cms.string('${HERWIGPATH}/HerwigDefaults.rpo'),
    run = cms.string('InterfaceMatchboxTest'),
    runModeList = cms.untracked.string("read,run"),
    seed = cms.untracked.int32(12345)
)


from GeneratorInterface.RivetInterface.rivetAnalyzer_cfi import rivetAnalyzer

rivetAnalyzer.AnalysisNames = cms.vstring(
    'MC_TTBAR', # MC analysis for lepton+jets
    'MC_PARTONICTOPS', # MC parton level top analysis
    'MC_TOPMASS_LJETS', # MC analysis for lepton+jets top mass
    'MC_FSPARTICLES', # MC generic analysis
    'MC_XS', # MC xs analysis
    'CMS_2016_I1491950',  # diff xs lepton+jets (2015 paper)
    'CMS_2018_I1620050',  # diff xs dilepton (2015 paper)
    'CMS_2018_I1663958',  # ttbar lepton+jets 13 TeV
)
rivetAnalyzer.OutputFile = cms.string("standalone_DY.yoda")

ProductionFilterSequence = cms.Sequence(generator*rivetAnalyzer)