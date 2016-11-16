
#include "TFile.h"
#include "TCut.h"
#include "TTree.h"
#include <iostream>

// What do we do : this is a little script to reduce the data for MVA input
// and count the luminosity just because we can.

void FirstReduction(){

  TFile * f = new TFile ("bu2jpsiK-mc-2012.root");
  TTree * tree = (TTree*)f->Get("bae-muon-MC/DecayTree");

  cout << "Total number of entries : "  << tree->GetEntries () << endl;



  TCut MCTruth =("Bplus_BKGCAT < 51");
  //Apply Trigger cuts

  //  TCut ApplyThis = LambdastarW && ElectronID && ProtonID && KaonID && UpperSideBand;
  TCut ApplyThis = MCTruth ;



  cout <<"For now we use the following cuts : " << ApplyThis << endl;
  TFile * signal_file = new TFile("bu2jpsiK-mc-2012-reduced.root", "recreate");



  TTree * signal_copy = tree->CopyTree( ApplyThis);
  signal_copy->Write();
  cout << "We are done with the first reduction :-) " << endl;
  return;
}
