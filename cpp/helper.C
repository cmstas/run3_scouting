#include "TCanvas.h"
#include "TFile.h"
#include "TString.h"
#include "TTree.h"
#include "TH1F.h"
#include "TF1.h"
#include "TSpline.h"
#include "TMath.h"
#include "TSystem.h"

#include <map>
#include <iostream>
#include <iomanip>
#include <sys/stat.h>
#include <filesystem>
#include <string>

using namespace std;

bool passMassVeto(float mass) {  
    if ((mass > 0.43) && (mass < 0.49))
        return false;
    if ((mass > 0.52) && (mass < 0.58))
        return false;
    if ((mass > 0.73) && (mass < 0.84))
        return false;
    if ((mass > 0.96) && (mass < 1.08))
        return false;
    if ((mass > 2.91) && (mass < 3.27))
        return false;
    if ((mass > 3.47) && (mass < 3.89))
        return false;
    if ((mass > 8.99) && (mass < 9.87))
        return false;
    if ((mass > 9.61) && (mass < 10.39))
        return false;
    if ((mass > 9.87) && (mass < 10.77))
        return false;
    //  
    return true;
}
