#!/usr/bin/env python
# @(#)root/tmva $Id$#
# Standard python import
import sys    # exit
import time   # time accounting
import getopt # command line parser

# --------------------------------------------

# Default settings for command line arguments
DEFAULT_OUTFNAME = "TMVA.root"
DEFAULT_INFNAMEBKG  =  '../../data.root'

DEFAULT_INFNAMESIG  = '../../mc.root'

DEFAULT_TREESIG  = "bae-muon-MC/DecayTree"
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

    # If you wish to modify default settings
    # (please check "src/Config.h" to see all available global options)
    #    gConfig().GetVariablePlotting()).fTimesRMS = 8.0
    #    gConfig().GetIONames()).fWeightFileDir = "myWeightDirectory"

    # Define the input variables that shall be used for the classifier training
    # note that you may also use variable expressions, such as: "3*var1/var2*abs(var3)"
    # [all types of expressions that can also be parsed by TTree::Draw( "expression" )]
    #factory.AddVariable( "myvar1 := var1+var2", 'F' )
    #factory.AddVariable( "myvar2 := var1-var2", "Expression 2", "", 'F' )
    #factory.AddVariable( "var3",                "Variable 3", "units", 'F' )
    #factory.AddVariable( "var4",                "Variable 4", "units", 'F' )
    #factory.AddVariable ("Polarity", "", "" , 'F')
    #factory.AddVariable ("GpsTime", "", "" , 'F')

    #Lb variables

    #Apply preselection cuts
    factory.AddVariable( "Bplus_P", "Bplus_P", "" , 'F' )
    factory.AddVariable( "Bplus_PT", "Bplus_PT", "" , 'F' )

    factory.AddVariable( "Bplus_DIRA_OWNPV",                "Bplus_DIRAOWNPV", "", 'F' )
    factory.AddVariable( "Bplus_FD_CHI2",                "Bplus_FD_CHI2", "", 'F' )
    factory.AddVariable( "Bplus_ENDVERTEX_CHI2",                "Bplus_ENDVERTEX_CHI2", "", 'F' )
    factory.AddVariable ("Bplus_IPCHI2_OWNPV", "Bplus_IPCHI2_OWNPV", "", "F")




    factory.AddVariable( "Jpsi_PT",   "Jpsi_PT", "" , 'F' )

    #factory.AddVariable( "Jpsi_FDCHI2_ORIVX",                "Jpsi_FDCHI2_ORIVX", "", 'F' )
    factory.AddVariable( "Jpsi_ENDVERTEX_CHI2",                "Jpsi_ENDVERTEX_CHI2", "", 'F' )
    factory.AddVariable( "Jpsi_IPCHI2_OWNPV",                "Jpsi_IPCHI2_OWNPV", "", 'F' )

    factory.AddVariable ("muplus_IPCHI2_OWNPV", "muplus_IPCHI2_OWNPV", "", "F")
    factory.AddVariable ("muminus_IPCHI2_OWNPV", "muminus_IPCHI2_OWNPV", "", "F")
    factory.AddVariable ("Jpsi_IPCHI2_OWNPV", "Jpsi_IPCHI2_OWNPV", "", "F")


    factory.AddVariable( "Kplus_P",   "Kplus_P", "" , 'F' )
    factory.AddVariable ("Kplus_IPCHI2_OWNPV", "Kplus_IPCHI2_OWNPV", "", "F")


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

    #add trigger selection



    L0 = TCut ("Bplus_L0HadronDecisionTOS || Bplus_L0MuonDecision || Bplus_L0DiMuonDecision")
    HLT1 = TCut("")
    HLT2 = TCut("")
    Trigger = L0 and HLT1 and HLT2

    PIDK = TCut ("(Kplus_ProbNNk - Kplus_ProbNNpi)>0.1 && Kplus_ProbNNk > 0.2")
    PIDMu = TCut("muplus_ProbNNmu > 0.25 && muminus_ProbNNmu > 0.25") #change to NNK NNPi

    PID = PIDK and PIDMu

    UpperSideBand = TCut ("Bplus_MM > 5400 ")

    MCTruth = TCut("Bplus_BKGCAT < 50")
    mycutSig = PID and MCTruth  #
    mycutBkg = PID and UpperSideBand  #upper sideband

    # Here, the relevant variables are copied over in new, slim trees that are
    # used for TMVA training and testing
    # "SplitMode=Random" means that the input events are randomly shuffled before
    # splitting them into training and test samples
    #factory.PrepareTrainingAndTestTree( mycutSig, mycutBkg,
#                                        "nTrain_Signal=1000:nTrain_Background=1000:SplitMode=Random:NormMode=NumEvents:!V" )
#

   #   factory->PrepareTrainingAndTestTree( mycut,
 #                                           "NSigTrain=3000:NBkgTrain=3000:NSigTest=3000:NBkgTest=3000:SplitMode=Random:!V" );
 #   factory.PrepareTrainingAndTestTree( mycutSig, mycutBkg,
  #                                      "nTrain_Signal=0:nTrain_Background=0:SplitMode=Random:NormMode=NumEvents:!V" )

    # --------------------------------------------------------------------------------------------------

    # ---- Book MVA methods
    #


    # Boosted Decision Trees
    if "BDTG" in mlist:
        factory.BookMethod( TMVA.Types.kBDT, "BDTG",
                           "!H:!V:NTrees=1000:MinNodeSize=1.5%:BoostType=Grad:Shrinkage=0.10:UseBaggedBoost:BaggedSampleFraction=0.5:nCuts=20:MaxDepth=2" )




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

    # open the GUI for the result macros
    #gROOT.ProcessLine( "TMVAGui(\"%s\")" % outfname )

    # keep the ROOT thread running
    gApplication.Run()

# ----------------------------------------------------------

if __name__ == "__main__":
    main()
