import FWCore.ParameterSet.Config as cms

from Configuration.Generator.Herwig7Settings.Herwig7StableParticlesForDetector_cfi import *
from Configuration.Generator.Herwig7Settings.Herwig7CH3TuneSettings_cfi import *
from Configuration.Generator.Herwig7Settings.Herwig7_7p1SettingsFor7p2_cfi import *
from Configuration.Generator.Herwig7Settings.Herwig7CommonMergingSettings_cfi import *


externalLHEProducer = cms.EDProducer("ExternalLHEProducer",
    args = cms.vstring('/afs/cern.ch/user/d/dstaffor/public/CMS_Herwig_tutorial_24_gridpacks/DYJetsToLL_M-50_13TeV-madgraphMLM-herwig7_slc7_amd64_gcc820_CMSSW_9_3_16_tarball.tar.xz'),
    nEvents = cms.untracked.uint32(5000),
    numberOfParameters = cms.uint32(1),
    outputFile = cms.string('cmsgrid_final.lhe'),
    scriptName = cms.FileInPath('GeneratorInterface/LHEInterface/data/run_generic_tarball_cvmfs.sh'),
    generateConcurrently = cms.untracked.bool(True),
    postGenerationCommand = cms.untracked.vstring('mergeLHE.py', '-n', '-i', 'thread*/cmsgrid_final.lhe', '-o', 'cmsgrid_final.lhe'),
)


generator = cms.EDFilter("Herwig7HadronizerFilter",
    herwig7StableParticlesForDetectorBlock,
    herwig7CH3SettingsBlock,
    herwig7CommonMergingSettingsBlock,
    herwig7p1SettingsFor7p2Block,
    configFiles = cms.vstring(),
    lo_merging_settings = cms.vstring(
        'set FxFxHandler:MergeMode TreeMG5',
        'set FxFxHandler:njetsmax  2',
        # Turn off MPI to speed up generation for this tutorial:
        'set /Herwig/EventHandlers/EventHandler:CascadeHandler:MPIHandler NULL'
    ),                                                                                                                                         
    parameterSets = cms.vstring('herwig7CH3PDF', 'herwig7CH3AlphaS', 'herwig7CH3MPISettings', 'hw_7p1SettingsFor7p2', 'herwig7StableParticlesForDetector', 'hw_common_merging_settings', 'lo_merging_settings'),
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
    "CMS_2018_I1667854",
    "MC_ZINC",
    "MC_ZJETS",
    "MC_XS",
    "MC_GENERIC"
)
rivetAnalyzer.OutputFile = cms.string("standalone_DY.yoda")

ProductionFilterSequence = cms.Sequence(generator*rivetAnalyzer)