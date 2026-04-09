import pickle
from hepdata_lib import Submission, Table, Variable, Uncertainty


ZERO_SUPPRESSION = True

def apply_zero_suppresion(x, ys):

    total = [sum(col) for col in zip(*ys)]
    filtered_x = [X for n, X in enumerate(x) if total[n]>0]
    filtered_ys = []
    for y in ys:
        filtered_ys.append([Y for n, Y in enumerate(y) if total[n]>0])
    
    return filtered_x, filtered_ys 

## Submission
submission = Submission()

#########################################################################################################################
######################################################################################################################### Figure 5a)
#########################################################################################################################
table_5a = Table("Figure 5a")
table_5a.description = ""
table_5a.location = ""
table_5a.keywords["observables"] = ["N"]
table_5a.add_image("paperPlots/Figure_005-a.pdf")

with open("paperPlots/hepdata_Figure_005-a.pkl", "rb") as f:

    data = pickle.load(f)

    if ZERO_SUPPRESSION:
        data["mass_binned_values"],[data["data_values"], data["data_unc"], data["Signal_HTo2ZdTo2mu2x_MZd-5p0_ctau-10.00mm"], data["Signal_ScenarioA_Mpi-2_MA-0p67_ctau-1.00mm"], data["Signal_ScenarioA_Mpi-5_MA-1p67_ctau-10.00mm"], data["Signal_ScenarioA_Mpi-7p50_MA-2p50_ctau-10.00mm"]] = apply_zero_suppresion(data["mass_binned_values"],
                                                                                                                                                                                                                                                                                                                       [data["data_values"],
                                                                                                                                                                                                                                                                                                                        data["data_unc"],
                                                                                                                                                                                                                                                                                                                        data["Signal_HTo2ZdTo2mu2x_MZd-5p0_ctau-10.00mm"],
                                                                                                                                                                                                                                                                                                                        data["Signal_ScenarioA_Mpi-2_MA-0p67_ctau-1.00mm"],
                                                                                                                                                                                                                                                                                                                        data["Signal_ScenarioA_Mpi-5_MA-1p67_ctau-10.00mm"],
                                                                                                                                                                                                                                                                                                                        data["Signal_ScenarioA_Mpi-7p50_MA-2p50_ctau-10.00mm"]])

    mass = Variable("$m_{4\mu}$", is_independent=True, is_binned=True, units="GeV")
    mass.values = data["mass_binned_values"]

    N_Data = Variable("Number of data events", is_independent=False, is_binned=False, units="")
    N_Data.values = data["data_values"]
    Data_unc = Uncertainty("Stat uncertainty", is_symmetric=True)
    Data_unc.values = data["data_unc"]
    N_Data.add_uncertainty(Data_unc)

    N_HAHM = Variable("Number of HAHM m = 8 GeV,  ctau = 1 cm events", is_independent=False, is_binned=False, units="")
    N_HAHM.values = data["Signal_HTo2ZdTo2mu2x_MZd-5p0_ctau-10.00mm"]

    DQCD1 = Variable("Number of ScenarioA $m_\pi$ = 2 GeV, $m_A$ = 0.67 GeV, ctau = 0.1 cm events", is_independent=False, is_binned=False, units="")
    DQCD1.values = data["Signal_ScenarioA_Mpi-2_MA-0p67_ctau-1.00mm"]

    DQCD2 = Variable("Number of ScenarioA $m_\pi$ = 5 GeV, $m_A$ = 1.67 GeV, ctau = 1 cm events", is_independent=False, is_binned=False, units="")
    DQCD2.values = data["Signal_ScenarioA_Mpi-5_MA-1p67_ctau-10.00mm"]

    DQCD3 = Variable("Number of ScenarioA $m_\pi$ = 7.5 GeV, $m_A$ = 2.5 GeV, ctau = 1 cm events", is_independent=False, is_binned=False, units="")
    DQCD3.values = data["Signal_ScenarioA_Mpi-7p50_MA-2p50_ctau-10.00mm"]

    table_5a.add_variable(mass)
    table_5a.add_variable(N_Data)
    table_5a.add_variable(N_HAHM)
    table_5a.add_variable(DQCD1)
    table_5a.add_variable(DQCD2)
    table_5a.add_variable(DQCD3)

submission.add_table(table_5a)


#######################################################################################################################
####################################################################################################################### Figure 5b)
#######################################################################################################################
table_5b = Table("Figure 5b")
table_5b.description = ""
table_5b.location = ""
table_5b.keywords["observables"] = ["N"]
table_5b.add_image("paperPlots/Figure_005-b.pdf")

with open("paperPlots/hepdata_Figure_005-b.pkl", "rb") as f:

    data = pickle.load(f)

    if ZERO_SUPPRESSION:
        data["mass_binned_values"],[data["data_values"], data["data_unc"], data["Signal_ScenarioB1_Mpi-2_MA-0p67_ctau-1.00mm"], data["Signal_ScenarioB1_Mpi-5_MA-1p67_ctau-1.00mm"], data["Signal_ScenarioB1_Mpi-7p50_MA-2p50_ctau-1.00mm"]] = apply_zero_suppresion(data["mass_binned_values"],
                                                                                                                                                                                                                                                                       [data["data_values"],
                                                                                                                                                                                                                                                                        data["data_unc"],
                                                                                                                                                                                                                                                                        data["Signal_ScenarioB1_Mpi-2_MA-0p67_ctau-1.00mm"],
                                                                                                                                                                                                                                                                        data["Signal_ScenarioB1_Mpi-5_MA-1p67_ctau-1.00mm"],
                                                                                                                                                                                                                                                                        data["Signal_ScenarioB1_Mpi-7p50_MA-2p50_ctau-1.00mm"]])

    mass = Variable("$m_{4\mu}$", is_independent=True, is_binned=True, units="GeV")
    mass.values = data["mass_binned_values"]

    N_Data = Variable("Number of data events", is_independent=False, is_binned=False, units="")
    N_Data.values = data["data_values"]
    Data_unc = Uncertainty("Stat uncertainty", is_symmetric=True)
    Data_unc.values = data["data_unc"]
    N_Data.add_uncertainty(Data_unc)

    DQCD1 = Variable("Number of ScenarioB1 $m_\pi$ = 2 GeV, $m_A$ = 0.67 GeV, ctau = 0.1 cm events", is_independent=False, is_binned=False, units="")
    DQCD1.values = data["Signal_ScenarioB1_Mpi-2_MA-0p67_ctau-1.00mm"]

    DQCD2 = Variable("Number of ScenarioB1 $m_\pi$ = 5 GeV, $m_A$ = 1.67 GeV, ctau = 0.1 cm events", is_independent=False, is_binned=False, units="")
    DQCD2.values = data["Signal_ScenarioB1_Mpi-5_MA-1p67_ctau-1.00mm"]

    DQCD3 = Variable("Number of ScenarioB1 $m_\pi$ = 7.5 GeV, $m_A$ = 2.5 GeV, ctau = 0.1 cm events", is_independent=False, is_binned=False, units="")
    DQCD3.values = data["Signal_ScenarioB1_Mpi-7p50_MA-2p50_ctau-1.00mm"]

    table_5b.add_variable(mass)
    table_5b.add_variable(N_Data)
    table_5b.add_variable(DQCD1)
    table_5b.add_variable(DQCD2)
    table_5b.add_variable(DQCD3)

submission.add_table(table_5b)

#########################################################################################################################
######################################################################################################################### Figure 10a)
#########################################################################################################################
table_10a = Table("Figure 10a")
table_10a.description = ""
table_10a.location = ""
table_10a.keywords["observables"] = ["N"]
table_10a.add_image("paperPlots/Figure_010-a.pdf")

with open("paperPlots/hepdata_Figure_010-a.pkl", "rb") as f:

    data = pickle.load(f)

    mass = Variable(r"$m_{\mu\mu}$", is_independent=True, is_binned=True, units="GeV")
    mass.values = data["mass_binned_values"]

    N_Data = Variable("Number of data events", is_independent=False, is_binned=False, units="")
    N_Data.values = data["data_values"]
    Data_unc = Uncertainty("Stat uncertainty", is_symmetric=False)
    Data_unc.values = [(-lo, hi) for lo, hi in zip(data["data_unc_low"], data["data_unc_high"])]
    N_Data.add_uncertainty(Data_unc)

    bkg_variables = []
    for pname in data["pdf_names"]:
        bkg_var = Variable("Background PDF (%s)" % pname, is_independent=False, is_binned=False, units="")
        bkg_var.values = data[pname]
        bkg_variables.append(bkg_var)

    table_10a.add_variable(mass)
    table_10a.add_variable(N_Data)
    for bkg_var in bkg_variables:
        table_10a.add_variable(bkg_var)

submission.add_table(table_10a)

#########################################################################################################################
######################################################################################################################### Figure 10b)
#########################################################################################################################
table_10b = Table("Figure 10b")
table_10b.description = ""
table_10b.location = ""
table_10b.keywords["observables"] = ["N"]
table_10b.add_image("paperPlots/Figure_010-b.pdf")

with open("paperPlots/hepdata_Figure_010-b.pkl", "rb") as f:

    data = pickle.load(f)

    mass = Variable(r"$m_{\mu\mu}$", is_independent=True, is_binned=True, units="GeV")
    mass.values = data["mass_binned_values"]

    N_MC = Variable("Number of signal simulation events", is_independent=False, is_binned=False, units="")
    N_MC.values = data["data_values"]
    MC_unc = Uncertainty("Stat uncertainty", is_symmetric=False)
    MC_unc.values = [(-lo, hi) for lo, hi in zip(data["data_unc_low"], data["data_unc_high"])]
    N_MC.add_uncertainty(MC_unc)

    Gauss = Variable("Gaussian component", is_independent=False, is_binned=False, units="")
    Gauss.values = data["Gaussian"]

    DCB = Variable("Double Crystal Ball component", is_independent=False, is_binned=False, units="")
    DCB.values = data["DoubleCrystalBall"]

    TotalFit = Variable("Total signal fit", is_independent=False, is_binned=False, units="")
    TotalFit.values = data["TotalSignalFit"]

    table_10b.add_variable(mass)
    table_10b.add_variable(N_MC)
    table_10b.add_variable(Gauss)
    table_10b.add_variable(DCB)
    table_10b.add_variable(TotalFit)

submission.add_table(table_10b)

# Final:
submission.create_files("example_output", remove_old=True)


