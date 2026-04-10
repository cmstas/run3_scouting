//
//// Function to get the results of the (AsymptoticLimits) limit
//
// Environment variables created:
// - LIM0 => 2.5% quantile
// - LIM1 => 16.0% quantile
// - LIM2 => 50.0% quantile
// - LIM3 => 84.0% quantile
// - LIM4 => 97.5% quantile
// - LIM5 => Observed
//
//

void getLimitResults(const char* fname) {
    TFile* f = TFile::Open(fname);
    TTree* t = (TTree*)f->Get("limit");  // reemplaza con el nombre real
    double var;
    t->SetBranchAddress("limit", &var);      // cambia "mass" por la variable que quieras
    for (int i = 0; i < 6; ++i) {
      t->GetEntry(i);
      std::cout << "LIM" << i << "=" << var << std::endl;
    }
  }