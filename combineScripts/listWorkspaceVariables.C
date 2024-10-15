#include <RooWorkspace.h>
#include <RooRealVar.h>
#include <TFile.h>
#include <iostream>

void listWorkspaceVariables() {
    const char* filename = "/home/users/fernance/Run3-Analyses/SnT-Scouting/Code/Looper8p0/run3_scouting/datacards_all_Jul-31-2024_2022/card_ch3_HTo2ZdTo2mu2x_M2.0_ctau1_2022.root";
    TFile *file = TFile::Open(filename, "READ");
    if (!file || file->IsZombie()) {
        std::cerr << "Error opening file " << filename << std::endl;
        return;
    }

    RooWorkspace *w = (RooWorkspace*)file->Get("w");
    if (!w) {
        std::cerr << "Error getting RooWorkspace from file " << filename << std::endl;
        file->Close();
        return;
    }

    // Obtain the list of variables in the workspace
    std::cout << "Variables in the workspace:\n";
    TIterator* iter = w->componentIterator();
    for (RooAbsArg* arg = (RooAbsArg*)iter->Next(); arg != nullptr; arg = (RooAbsArg*)iter->Next()) {
        RooRealVar* var = dynamic_cast<RooRealVar*>(arg);
        if (var) {
            double min = var->getMin();
            double max = var->getMax();
            if (min != max && min < max && min > -1e+30 && max < 1e+30) {
                std::cout << "Variable: " << var->GetName() 
                          << ", Min: " << min 
                          << ", Max: " << max 
                          << " (Ranges are defined)" << std::endl;
            } else {
                std::cout << "Variable: " << var->GetName() 
                          << ", Min: " << min 
                          << ", Max: " << max 
                          << " (Ranges are not properly defined)" << std::endl;
            }
        }
    }

    file->Close();
}

int main() {
    listWorkspaceVariables();
    return 0;
}

