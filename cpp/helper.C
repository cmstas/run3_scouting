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
    if ((mass > 0.41) && (mass < 0.50))
        return false;
    if ((mass > 0.51) && (mass < 0.59))
        return false;
    if ((mass > 0.73) && (mass < 0.83))
        return false;
    if ((mass > 0.96) && (mass < 1.08))
        return false;
    //if ((mass > 2.91) && (mass < 3.27))
    //    return false;
    //if ((mass > 3.47) && (mass < 3.89))
    //    return false;
    //if ((mass > 8.99) && (mass < 9.91))
    //    return false;
    //if ((mass > 9.64) && (mass < 10.56))
    //    return false;
    //if ((mass > 9.90) && (mass < 10.78))
    //    return false;
    //  
    return true;
}
