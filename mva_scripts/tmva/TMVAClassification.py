#!/usr/bin/env python
# @(#)root/tmva $Id$#
# Standard python import
import sys    # exit
import time   # time accounting
import getopt # command line parser

# --------------------------------------------

# Default settings for command line arguments
DEFAULT_OUTFNAME = "TMVA.root"
DEFAULT_INFNAMEBKG  =  '../../Paris-14112016/BAE-small-data.root'
DEFAULT_INFNAMESIG  = '../../Paris-14112016/K1mumu-mc-2012-reduced.root'


#DEFAULT_TREESIG  = "bae-muon-MC/DecayTree"
DEFAULT_TREESIG  = "DecayTree"
DEFAULT_TREEBKG  = "bae-muon-data/DecayTree"

DEFAULT_METHODS  =  "BDTG"#

# Print usage help
def usage():
    print " "
    print "Usage: python %s [options]" % sys.argv[0]
    print "  -m | --methods    : gives methods to be run (default: all methods)"
    print "  -is | --inputfile signal  : name of input ROOT file (default: '%s')" %  DEFAULT_INFNAMESIG
    print "  -ib | --inputfile background : name of input ROOT file (default: '%s')" % DEFAULT_INFNAMEBKG

    print "  -o | --outputfile : name of output ROOT file containing results (default: '%s')" % DEFAULT_OUTFNAME
    print "  -t | --inputtrees signal : input ROOT Trees for signal and background (default: '%s %s')" % DEFAULT_TREESIG

    print "  -t | --inputtrees : input ROOT Trees for signal and background (default: '%s %s')" % DEFAULT_TREEBKG
    print "  -v | --verbose"
    print "  -? | --usage      : print this help message"
    print "  -h | --help       : print this help message"
    print " "

# Main routine
def main():

    try:
        # retrive command line options
        shortopts  = "m:is:ib:ts:tb:o:vh?"
        longopts   = ["methods=", "inputfile_signal=","inputfile_background=" , "inputtree_signal=", "inputtree_background=",  "outputfile=", "verbose", "help", "usage"]
        opts, args = getopt.getopt( sys.argv[1:], shortopts, longopts )

    except getopt.GetoptError:
        # print help information and exit:
        print "ERROR: unknown options in argument %s" % sys.argv[1:]
        usage()
        sys.exit(1)

    infnameSig     = DEFAULT_INFNAMESIG
    infnameBkg     = DEFAULT_INFNAMEBKG
    treeNameSig = DEFAULT_TREESIG
    treeNameBkg = DEFAULT_TREEBKG
    outfname    = DEFAULT_OUTFNAME
    methods     = DEFAULT_METHODS
    verbose     = False
    for o, a in opts:
        if o in ("-?", "-h", "--help", "--usage"):
            usage()
            sys.exit(0)
        elif o in ("-m", "--methods"):
            methods = a
        elif o in ("-is", "--inputfile_signal"):
            infnameSig = a
        elif o in ("-ib", "--inputfile_background"):
            infnameBkg = a
        elif o in ("-o", "--outputfile"):
            outfname = a
        elif o in ("-ts", "--inputree_signal"):
            treeNameSig = a
        elif o in ("-tb", "--inputtree_background"):
            treeNameBkg = a
        elif o in ("-v", "--verbose"):
            verbose = True

    # Print methods
    mlist = methods.replace(' ',',').split(',')
    print "=== TMVAClassification: use method(s)..."
    for m in mlist:
        if m.strip() != '':
            print "=== - <%s>" % m.strip()

    # Import ROOT classes
    from ROOT import gSystem, gROOT, gApplication, TFile, TTree, TCut

    # check ROOT version, give alarm if 5.18
    if gROOT.GetVersionCode() >= 332288 and gROOT.GetVersionCode() < 332544:
        print "*** You are running ROOT version 5.18, which has problems in PyROOT such that TMVA"
        print "*** does not run properly (function calls with enums in the argument are ignored)."
        print "*** Solution: either use CINT or a C++ compiled version (see TMVA/macros or TMVA/examples),"
        print "*** or use another ROOT version (e.g., ROOT 5.19)."
        sys.exit(1)

    # Logon not automatically loaded through PyROOT (logon loads TMVA library) load also GUI
    gROOT.SetMacroPath( "./" )
    gROOT.Macro       ( "./TMVAlogon.C" )
    gROOT.LoadMacro   ( "./TMVAGui.C" )

    # Import TMVA classes from ROOT
    from ROOT import TMVA

    # Output file
    outputFile = TFile( outfname, 'RECREATE' )

    # Create instance of TMVA factory (see TMVA/macros/TMVAClassification.C for more factory options)
    # All TMVA output can be suppressed by removing the "!" (not) in
    # front of the "Silent" argument in the option string
    factory = TMVA.Factory( "TMVAClassification", outputFile,
                            "!V:!Silent:Color:DrawProgressBar:Transformations=I;D;P;G,D:AnalysisType=Classification" )

    # Set verbosity
    factory.SetVerbose( verbose )


    #B+ variables
    factory.AddVariable( "Bplus_P", "Bplus_P", "" , 'D' )
    factory.AddVariable( "Bplus_PT", "Bplus_PT", "" , 'D' )
    factory.AddVariable( "acos(Bplus_DIRA_OWNPV)",                "acos(Bplus_DIRAOWNPV)", "", 'D' )
    factory.AddVariable( "Bplus_FD_CHI2",                "Bplus_FD_CHI2", "", 'D' )
    factory.AddVariable( "Bplus_ENDVERTEX_CHI2",                "Bplus_ENDVERTEX_CHI2", "", 'D' )




    #Dimuon variables
    factory.AddVariable( "Jpsi_PT",   "Jpsi_PT", "" , 'D' )

    #muons variables
    factory.AddVariable ("log(muplus_IPCHI2_OWNPV)", "log(muplus_IPCHI2_OWNPV)", "", "D")
    factory.AddVariable ("log(muminus_IPCHI2_OWNPV)", "log(muminus_IPCHI2_OWNPV)", "", "D")


    #Kaon variables
    factory.AddVariable( "Kplus_P",   "Kplus_P", "" , 'D' )
    factory.AddVariable(  "Kplus_PT",   "Kplus_PT", "" , 'D' )
    factory.AddVariable ("log(Kplus_IPCHI2_OWNPV)", "log(Kplus_IPCHI2_OWNPV)", "", "D")


    input_signal = TFile.Open( infnameSig )
    input_background = TFile.Open( infnameBkg )

    # Get the signal and background trees for training
    signal      = input_signal.Get( treeNameSig )
    background  = input_background.Get( treeNameBkg )
    signalWeight     = 1.0
    backgroundWeight = 1.0

    print 'is this modern hell ? '

    print input_signal
    print input_background
    print signal
    print background



    factory.AddSignalTree    ( signal,     signalWeight     )
    factory.AddBackgroundTree( background, backgroundWeight )

    # These are the spectators
    factory.AddSpectator ("Bplus_MM", "Bplus_MM", "",2000, 7000)
    factory.AddSpectator ("Jpsi_MM", "Jpsi_MM", "",2000, 7000)

    # A collection of cuts to apply
    Sanity = TCut (" Bplus_ENDVERTEX_CHI2>0  && Bplus_P < 5e5 && Bplus_PT < 5e5 && Bplus_ENDVERTEX_CHI2 < 5 && Bplus_FD_CHI2 < 1e5 && Kplus_MINIPCHI2 > 9")

    #Trigger
    L0 = TCut ("Bplus_L0HadronDecisionTOS || Bplus_L0MuonDecision || Bplus_L0DiMuonDecision")
    HLT1 = TCut("Bplus_Hlt1TrackMuonDecisionTOS")
    HLT2 = TCut("Bplus_Hlt2DiMuonDetachedDecisionTOS ||  Bplus_Hlt2DiMuonDetachedHeavyDecisionTOS")
    Trigger = L0 and HLT1 and HLT2
    #PID
    PIDK = TCut ("(Kplus_ProbNNk - Kplus_ProbNNpi)>0.1 && Kplus_ProbNNk > 0.2")
    PIDMu = TCut("muplus_ProbNNmu > 0.25 && muminus_ProbNNmu > 0.25") #change to NNK NNPi
    PID = PIDK and PIDMu
    #upper side band
    UpperSideBand = TCut ("Bplus_MM > 5500 ")
    #total signal cut
    SignalCut = TCut ("")
    SignalCut += Sanity
    #total background cut
    BackgroundCut = TCut("")
    BackgroundCut +=Sanity
    BackgroundCut +=UpperSideBand
    BackgroundCut += PID


    print  "Dump the total Signal cut just for checking ..."
    print SignalCut
    print "Dump the total Background cut just for checking ..."
    print BackgroundCut


    # Here, the relevant variables are copied over in new, slim trees that are
    # used for TMVA training and testing
    # "SplitMode=Random" means that the input events are randomly shuffled before
    # splitting them into training and test samples
    factory.PrepareTrainingAndTestTree( SignalCut, BackgroundCut,
                                            "nTrain_Signal=0:nTrain_Background=0:SplitMode=Random:NormMode=NumEvents:!V" )


   # --------------------------------------------------------------------------------------------------
   # ---- Book MVA methods
   #
   # Boosted Decision Trees
    if "BDTG" in mlist:
        factory.BookMethod( TMVA.Types.kBDT, "BDTG",
                           "!H:!V:NTrees=1000:MinNodeSize=1.5%:BoostType=Grad:Shrinkage=0.10:UseBaggedBoost:BaggedSampleFraction=0.5:nCuts=20:MaxDepth=2" )
    if "BDT" in mlist:
      factory.BookMethod( TMVA.Types.kBDT, "BDT",
                           "!H:!V:NTrees=200:MinNodeSize=5.0%:MaxDepth=3:BoostType=AdaBoost:AdaBoostBeta=0.5:UseBaggedBoost:BaggedSampleFraction=0.5:SeparationType=GiniIndex:nCuts=-1" )
    # Train MVAs
    factory.TrainAllMethods()
    # Test MVAs
    factory.TestAllMethods()
    # Evaluate MVAs
    factory.EvaluateAllMethods()
    # Save the output.
    outputFile.Close()

    print "=== wrote root file %s\n" % outfname
    print "=== TMVAClassification is done!\n"

# ----------------------------------------------------------

if __name__ == "__main__":
    main()
