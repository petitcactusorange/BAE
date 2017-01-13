# $Id: $
# Test your line(s) of the stripping
#  
# NOTE: Please make a copy of this file for your testing, and do NOT change this one!
#
'''
File used to rerun stripping 28 on 2012 MC  
Works with DaVinci v42r1
'''

LeptonType = "Muons" 

if LeptonType == "Muons" : 
    l = "mu"
    tuplename = "muon"
if LeptonType == "Electrons": 
    l = "e"
    tuplename = "electron"

print LeptonType 
print l 


from Gaudi.Configuration import *
from Configurables import DaVinci
from StrippingConf.Configuration import StrippingConf


from Configurables import EventNodeKiller, ProcStatusCheck 

# first kill the nodes 
event_node_killer = EventNodeKiller("StripKiller")
event_node_killer.Nodes = ["/Event/allStreams", "/Event/Strip","/Event/Leptonic" ]



# Specify the name of your configuration
confname='B2KLLXInclusive' #FOR USERS    

from StrippingSelections import buildersConf
confs = buildersConf()

#print confs
from StrippingSelections.Utils import lineBuilder, buildStreamsFromBuilder
streams = buildStreamsFromBuilder(confs,confname)

#clone lines for CommonParticles overhead-free timing

print "Creating line clones for timing"
for s in streams:
    for l in s.lines:
        if "_TIMING" not in l.name():
            cloned = l.clone(l.name().strip("Stripping")+"_TIMING")
            s.appendLines([cloned])

#define stream names
leptonicMicroDSTname   = 'Leptonic'
charmMicroDSTname      = 'Charm'
pidMicroDSTname        = 'PID'
bhadronMicroDSTname    = 'Bhadron'
mdstStreams = [ leptonicMicroDSTname,charmMicroDSTname,pidMicroDSTname,bhadronMicroDSTname ]
dstStreams  = [ "BhadronCompleteEvent", "CharmCompleteEvent", "Dimuon",
                "EW", "Semileptonic", "Calibration", "MiniBias", "Radiative" ]

stripTESPrefix = 'Strip'

from Configurables import ProcStatusCheck

sc = StrippingConf( HDRLocation = "SomeLocation",
                    Streams = streams,
                    MaxCandidates = 2000,
                    AcceptBadEvents = False,
                    BadEventSelection = ProcStatusCheck(),
                    TESPrefix = stripTESPrefix,
                    ActiveMDSTStream = True,
                    Verbose = True,
                    DSTStreams = dstStreams,
                    MicroDSTStreams = mdstStreams )

#
# Configure the dst writers for the output
#
enablePacking = True




from Configurables import DecayTreeTuple, FitDecayTrees, TupleToolRecoStats, TupleToolTrigger, TupleToolSubMass
from Configurables import TupleToolTISTOS, CondDB, SelDSTWriter
from Configurables import TupleToolTrackInfo, TupleToolRICHPid, TupleToolGeometry, TupleToolPid
from Configurables import TupleToolANNPID
from DecayTreeTuple.Configuration import *

tupleB = DecayTreeTuple("bae-"+tuplename+"-mc")


tupleB.Inputs = ["Phys/B2KLLXInclusive_InclKLLLine_NoHadronPID/Particles"]

#decay = ""
if LeptonType == "Muons" : 
    decay =  "[B+ -> ^(J/psi(1S) -> ^mu+ ^mu-) ^K+]CC"
    tupleB.addBranches ({
            "Kplus"  :  "[B+ -> ^K+ (J/psi(1S) -> mu+ mu-)]CC",
            "Jpsi"   :  "[B+ -> K+ ^(J/psi(1S) -> mu+ mu-)]CC",
            "lplus"  :  "[B+ -> K+ (J/psi(1S) -> ^mu+ mu-)]CC",
            "lminus" :  "[B+ -> K+ (J/psi(1S) -> mu+ ^mu-)]CC",
            "Bplus"  : "[B+ -> K+ J/psi(1S)]CC",
            })

if LeptonType == "Electrons":
    decay =  "[B+ -> ^(J/psi(1S) -> ^e+ ^e-) ^K+]CC"
    tupleB.addBranches ({
            "Kplus"  :  "[B+ -> ^K+ (J/psi(1S) -> e+ e-)]CC",
            "Jpsi"   :  "[B+ -> K+ ^(J/psi(1S) -> e+ e-)]CC",
            "lplus"  :  "[B+ -> K+ (J/psi(1S) -> ^e+ e-)]CC",
            "lminus" :  "[B+ -> K+ (J/psi(1S) -> e+ ^e-)]CC",
            "Bplus"  :  "[B+ -> K+ J/psi(1S)]CC",
            })
tupleB.Decay = decay



tupleB.ToolList =  [
      "TupleToolKinematic"
      , "TupleToolEventInfo"
      , "TupleToolRecoStats"
      ,"TupleToolMCBackgroundInfo",#comment out for data
      "TupleToolMCTruth", #comment out for data
      "TupleToolTrigger",
      "TupleToolPid",
      "TupleToolPrimaries",
      "TupleToolAngles",
      "TupleToolEventInfo",
      "TupleToolGeometry",
      "TupleToolKinematic",
      "TupleToolPropertime",
      "TupleToolRecoStats",
      "TupleToolTrackInfo",
      "TupleToolTISTOS",
      "TupleToolBremInfo",
      "TupleToolPhotonInfo"#,
      ,"TupleToolTrackIsolation"
      , "TupleToolANNPID"
      
] # Probably need to add many more Tools.




LoKi_All=tupleB.addTupleTool("LoKi::Hybrid::TupleTool/LoKi_All")
LoKi_All.Variables = {
        'MINIPCHI2' : "MIPCHI2DV(PRIMARY)",
        'MINIP' : "MIPDV(PRIMARY)",
        'IPCHI2_OWNPV' : "BPVIPCHI2()",
        'IP_OWNPV' : "BPVIP()"
}



LoKi_lplus=tupleB.lplus.addTupleTool("LoKi::Hybrid::TupleTool/LoKi_lplus")
LoKi_lplus.Variables = {
       'PIDmu' : "PIDmu",
       'ghost' : "TRGHP",
       'TRACK_CHI2' : "TRCHI2DOF",
       'NNK' : "PPINFO(PROBNNK)",
       'NNpi' : "PPINFO(PROBNNpi)",
       'NNmu' : "PPINFO(PROBNNmu)", 
       
}

LoKi_Kplus=tupleB.Kplus.addTupleTool("LoKi::Hybrid::TupleTool/LoKi_Kplus")
LoKi_Kplus.Variables = {
       'PIDmu' : "PIDmu",
       'PIDK' : "PIDK",
       'ghost' : "TRGHP",
       'TRACK_CHI2' : "TRCHI2DOF",
       'NNK' : "PPINFO(PROBNNK)",
       'NNpi' : "PPINFO(PROBNNpi)",
       'NNmu' : "PPINFO(PROBNNmu)"
}
LoKi_lminus=tupleB.lminus.addTupleTool("LoKi::Hybrid::TupleTool/LoKi_lminus")
LoKi_lminus.Variables = {
       'PIDmu' : "PIDmu",
       'ghost' : "TRGHP",
       'TRACK_CHI2' : "TRCHI2DOF",
       'NNK' : "PPINFO(PROBNNK)",
       'NNpi' : "PPINFO(PROBNNpi)",
       'NNmu' : "PPINFO(PROBNNmu)"
}

LoKi_B=tupleB.Bplus.addTupleTool("LoKi::Hybrid::TupleTool/LoKi_B")
LoKi_B.Variables = {
       'DTF_CHI2' : "DTF_CHI2NDOF(True)",
       'TAU' : "BPVLTIME()",
       'DIRA_OWNPV' : "BPVDIRA",
       'FD_CHI2' : "BPVVDCHI2",
       'ENDVERTEX_CHI2' : "VFASPF(VCHI2/VDOF)",
       'PVX' : "BPV(VX)",
       'PVY' : "BPV(VY)",
       'PVZ' : "BPV(VZ)",
       'VX' : "VFASPF(VX)",
       'VY' : "VFASPF(VY)",
       'VZ' : "VFASPF(VZ)",
       'X_travelled' : "VFASPF(VX)-BPV(VX)",
       'Y_travelled' : "VFASPF(VY)-BPV(VY)",
       'Z_travelled' : "VFASPF(VZ)-BPV(VZ)",
       'P_Parallel' : "BPVDIRA*P",
       'P_Perp' : "sin(acos(BPVDIRA))*P",
       'Corrected_Mass' : "BPVCORRM"
}


TriggerListL0 = [
    "L0ElectronDecision",
    "L0HadronDecision",
    "L0MuonDecision",
    "L0DiMuonDecision"
  ]

TriggerListHlt =[   
    "Hlt1TrackAllL0Decision",
    "Hlt1DiMuonLowMassDecision",
    "Hlt1DiMuonHighMassDecision",
    "Hlt1MuTrackDecision",
    "Hlt1TrackMuonDecision",
    "Hlt2Topo2BodyBBDTDecision",
    "Hlt2Topo3BodyBBDTDecision",
    "Hlt2Topo4BodyBBDTDecision",
    "Hlt2TopoE2BodyBBDTDecision",
    "Hlt2TopoE3BodyBBDTDecision",
    "Hlt2TopoE4BodyBBDTDecision",
    "Hlt2TopoMu2BodyBBDTDecision",
    "Hlt2TopoMu3BodyBBDTDecision",
    "Hlt2TopoMu4BodyBBDTDecision",
    "Hlt2RadiativeTopoTrackTOSDecision",
    "Hlt2RadiativeTopoPhotonL0Decision",
    "Hlt2SingleMuonDecision",
    "Hlt2DiMuonDetachedDecision"
]



tupleB.Bplus.ToolList += [ "TupleToolTISTOS" ]
tupleB.Bplus.addTool( TupleToolTISTOS, name = "TupleToolTISTOS" )
tupleB.Bplus.TupleToolTISTOS.Verbose = True
tupleB.Bplus.TupleToolTISTOS.TriggerList = TriggerListL0
tupleB.Bplus.TupleToolTISTOS.TriggerList += TriggerListHlt

tupleB.Bplus.TupleToolTISTOS.Verbose = True
tupleB.Bplus.TupleToolTISTOS.VerboseL0= True
tupleB.Bplus.TupleToolTISTOS.VerboseHlt1= True
tupleB.Bplus.TupleToolTISTOS.VerboseHlt2= True




tupleB.Jpsi.ToolList += [ "TupleToolTISTOS" ]
tupleB.Jpsi.addTool( TupleToolTISTOS, name = "TupleToolTISTOS" )
tupleB.Jpsi.TupleToolTISTOS.Verbose = True
tupleB.Jpsi.TupleToolTISTOS.TriggerList =TriggerListL0
tupleB.Jpsi.TupleToolTISTOS.TriggerList += TriggerListHlt

tupleB.Jpsi.TupleToolTISTOS.Verbose = True
tupleB.Jpsi.TupleToolTISTOS.VerboseL0= True
tupleB.Jpsi.TupleToolTISTOS.VerboseHlt1= True
tupleB.Jpsi.TupleToolTISTOS.VerboseHlt2= True


tupleB.addTool(TupleToolTrackInfo, name = "TupleToolTrackInfo")
tupleB.TupleToolTrackInfo.Verbose=True
tupleB.addTool(TupleToolRICHPid, name="TupleToolRICHPid")
tupleB.TupleToolRICHPid.Verbose=True
tupleB.addTool(TupleToolRecoStats, name="TupleToolRecoStats")
tupleB.TupleToolRecoStats.Verbose=True
tupleB.addTool(TupleToolGeometry, name="TupleToolGeometry")
tupleB.TupleToolGeometry.Verbose=True
tupleB.addTool(TupleToolPid, name="TupleToolPid")
tupleB.TupleToolPid.Verbose=True

tupleB.addTool(TupleToolANNPID, name = "TupleToolANNPID")
tupleB.TupleToolANNPID.ANNPIDTunes = ['MC12TuneV2', 'MC12TuneV3', "MC12TuneV4"]


tupleB.Bplus.addTupleTool( 'TupleToolSubMass' )
tupleB.Bplus.ToolList += [ "TupleToolSubMass" ]

tupleB.Bplus.TupleToolSubMass.Substitution += ["K+ => pi+"]
tupleB.Bplus.TupleToolSubMass.Substitution += ["K+ => p+"]


tupleB.lplus.addTupleTool( 'TupleToolL0Calo', name = "lplusL0ECalo" )
tupleB.lplus.ToolList += [ "TupleToolL0Calo/lplusL0ECalo" ]
tupleB.lplus.lplusL0ECalo.WhichCalo = "ECAL"
tupleB.lminus.addTupleTool( 'TupleToolL0Calo', name = "lminusL0ECalo" )
tupleB.lminus.ToolList += [ "TupleToolL0Calo/lminusL0ECalo" ]
tupleB.lminus.lminusL0ECalo.WhichCalo = "ECAL"

tupleB.lplus.addTupleTool( 'TupleToolL0Calo', name = "lplusL0HCalo" )
tupleB.lplus.ToolList += [ "TupleToolL0Calo/lplusL0HCalo" ]
tupleB.lplus.lplusL0HCalo.WhichCalo = "HCAL"
tupleB.lminus.addTupleTool( 'TupleToolL0Calo', name = "lminusL0HCalo" )
tupleB.lminus.ToolList += [ "TupleToolL0Calo/lminusL0HCalo" ]
tupleB.lminus.lminusL0HCalo.WhichCalo = "HCAL"

tupleB.Kplus.addTupleTool( 'TupleToolL0Calo', name = "KaonL0Calo" )
tupleB.Kplus.ToolList += [ "TupleToolL0Calo/KaonL0Calo" ]
tupleB.Kplus.KaonL0Calo.WhichCalo = "HCAL"


tupleB.Bplus.addTupleTool( 'TupleToolDecayTreeFitter', name = "DTF" )
tupleB.Bplus.addTupleTool( tupleB.Bplus.DTF.clone( "DTF_PV",
                                             constrainToOriginVertex = True ) )
tupleB.Bplus.ToolList += [ "TupleToolDecayTreeFitter/DTF_PV" ]
tupleB.Bplus.addTupleTool( tupleB.Bplus.DTF.clone( "DTF_Jpsi",
                                             constrainToOriginVertex = False,
                                             daughtersToConstrain = [ "J/psi(1S)" ] ) )
tupleB.Bplus.ToolList += [ "TupleToolDecayTreeFitter/DTF_Jpsi" ]
tupleB.Bplus.addTupleTool( tupleB.Bplus.DTF.clone( "DTF_psi2S",
                                             constrainToOriginVertex = False,
                                             Substitutions = { "[ [B+]cc -> ^J/psi(1S) K+ ]CC" : "psi(2S)" },
                                             daughtersToConstrain = [ "psi(2S)" ] ) )
tupleB.Bplus.ToolList += [ "TupleToolDecayTreeFitter/DTF_psi2S" ]

tupleB.addTool(TupleToolTrackInfo, name = "TupleToolTrackInfo")
tupleB.TupleToolTrackInfo.Verbose=True
tupleB.addTool(TupleToolRICHPid, name="TupleToolRICHPid")
tupleB.TupleToolRICHPid.Verbose=True
tupleB.addTool(TupleToolRecoStats, name="TupleToolRecoStats")
tupleB.TupleToolRecoStats.Verbose=True
tupleB.addTool(TupleToolGeometry, name="TupleToolGeometry")
tupleB.TupleToolGeometry.Verbose=True
tupleB.addTool(TupleToolPid, name="TupleToolPid")
tupleB.TupleToolPid.Verbose=True

tupleB.addTool(TupleToolANNPID, name = "TupleToolANNPID")
tupleB.TupleToolANNPID.ANNPIDTunes = ['MC12TuneV2', 'MC12TuneV3', "MC12TuneV4"]



tupleB.addTupleTool('TupleToolMCTruth')
tupleB.TupleToolMCTruth.ToolList = ["MCTupleToolKinematic", "MCTupleToolHierarchy"]

# rerun the Calo reconstruction 
importOptions("$APPCONFIGOPTS/DaVinci/DV-RedoCaloPID-Stripping21.py")

#Configure DaVinci


DaVinci().HistogramFile = 'xdummy.root'
DaVinci().EvtMax = -1
DaVinci().PrintFreq = 2000
DaVinci().appendToMainSequence( [ sc.sequence() ] )
DaVinci().appendToMainSequence([tupleB])


DaVinci().DataType  = "2012"
DaVinci().InputType = "DST"
DaVinci().Simulation = True
DaVinci().Lumi = False

DaVinci().TupleFile = "bae-"+str(tuplename)+"-mc.root"

MessageSvc().Format = "% F%60W%S%7W%R%T %0W%M"
# database


DaVinci().DDDBtag   = "dddb-20150522-2"
DaVinci().CondDBtag = "sim-20150522-vc-md100"

#input file
importOptions("$HOME/BAEO/BAE/davinci_scripts/B2Kmm.py")
