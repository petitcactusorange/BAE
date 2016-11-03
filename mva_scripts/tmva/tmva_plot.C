#include <TMVA/Factory.h>
#include <TTree.h>
#include <TFile.h>
#include <TMVA/Types.h>

void tmva_plot(TString infilename) {

	// don't change the order of the function calls, some don't
	// work otherwise (no idea why)
	
	//TMVA::TMVAGui(infilename);

	// HistType 3 is overtraining plot
	TMVA::mvas(infilename,static_cast<TMVA::HistType>(3));
	TMVA::efficiencies(infilename);
	TMVA::correlations(infilename);
	TMVA::variables(infilename);
}
