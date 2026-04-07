import os

## This script put the crab output in the corresponding ceph area and creates the files to run the looper and plotter

# To be modified by user:
sourceDir = "/ceph/cms/store/group/Run3Scouting/RAWScouting_5c"
#finalDir = "/ceph/cms/store/group/Run3Scouting/Run3ScoutingSamples/Feb-03-2024/CentralSignal"
sourceDir = "/ceph/cms/store/group/Run3Scouting/RAWScouting_HTo2ZdTo2mu2x_2023_vhahm_7p0"
sourceDir = "/ceph/cms/store/group/Run3Scouting/RAWScouting_privQCD_vdqcd_preliminar_7p0"
sourceDir = "/ceph/cms/store/group/Run3Scouting/RAWScouting_privQCD_vvdqcd_final_8p0"
### These are for BToPhi
#sourceDir = "/ceph/cms/store/group/Run3Scouting/RAWScouting_BToPhi_2023_vbtophi_final_8p0"
#sourceDir = "/ceph/cms/store/group/Run3Scouting/RAWScouting_BToPhi_2022_vbtophi_final_8p0"
#sourceDir = "/ceph/cms/store/group/Run3Scouting/RAWScouting_BToPhiExtra_2022_vbtophi_extra_8p0/"
#sourceDir = "/ceph/cms/store/group/Run3Scouting/RAWScouting_BToPhiExtra_2023_vbtophi_extra_8p0/"
sourceDir = "/ceph/cms/store/group/Run3Scouting/RAWScouting_BToPhiExtra_2022_vvdqcd_final_8p0/"
sourceDir = "/ceph/cms/store/group/Run3Scouting/RAWScouting_BToPhiExtra_2023_vvdqcd_final_8p0/"
modeto = False # Set to True if moving files it is necessary
selected_era = '2023BPix'
filter = 'BToPhi'

### File with central datasets fr looper input
fout_ = open("centralDatasets_%s_%s.txt"%(filter, selected_era), "w")

### File with condor launcher for looper
f2out_ = open("runScoutingLooper_onCondor_%s_%s.sub"%(filter, selected_era), "w") 
#f2out_.write("executable      = $ENV(STARTDIR)/condor/condorLooper_executable.sh\n")
#f2out_.write("output          = $ENV(STARTDIR)/condor/plotting_logs/job.$(ClusterId).$(ProcId).out\n")
#f2out_.write("error           = $ENV(STARTDIR)/condor/plotting_logs/job.$(ClusterId).$(ProcId).err\n")
#f2out_.write("log             = $ENV(STARTDIR)/condor/plotting_logs/job.$(ClusterId).$(ProcId).log\n")
#f2out_.write("\n")
#f2out_.write("getenv = True\n")
#f2out_.write("+JobFlavour = 'workday'\n")
#f2out_.write("+DESIRED_Sites = 'T2_US_UCSD'\n")
#f2out_.write("transfer_input_files = $ENV(STARTDIR)/package.tar.gz\n")
#f2out_.write("should_transfer_files = YES\n")
#f2out_.write("when_to_transfer_output = ON_EXIT\n")
#f2out_.write("x509userproxy=$ENV(X509_USER_PROXY)\n")
#f2out_.write("use_x509userproxy = True\n")
#f2out_.write("\n")
#f2out_.write("queue arguments from (\n")

### File with condor launcher for histos
f3out_ = open("runScoutingHistos_onCondor_%s_%s.sub"%(filter, selected_era), "w") 
#f3out_.write("executable      = $ENV(STARTDIR)/condor/condorHistos_executable.sh\n")
#f3out_.write("output          = $ENV(STARTDIR)/condor/plotting_logs/job.$(ClusterId).$(ProcId).out\n")
#f3out_.write("error           = $ENV(STARTDIR)/condor/plotting_logs/job.$(ClusterId).$(ProcId).err\n")
#f3out_.write("log             = $ENV(STARTDIR)/condor/plotting_logs/job.$(ClusterId).$(ProcId).log\n")
#f3out_.write("\n")
#f3out_.write("RequestCpus   = 2\n")
#f3out_.write("RequestMemory = 8000\n")
#f3out_.write("\n")
#f3out_.write("getenv = True\n")
#f3out_.write("+JobFlavour = 'workday'\n")
#f3out_.write("+DESIRED_Sites = 'T2_US_UCSD'\n")
#f3out_.write("transfer_input_files = $ENV(STARTDIR)/package.tar.gz\n")
#f3out_.write("should_transfer_files = YES\n")
#f3out_.write("when_to_transfer_output = ON_EXIT\n")
#f3out_.write("x509userproxy=$ENV(X509_USER_PROXY)\n")
#f3out_.write("use_x509userproxy = True\n")
#f3out_.write("\n")
#f3out_.write("queue arguments from (\n")

for sample in os.listdir(sourceDir):
    print(sample)
    if '.' in sample:
        continue
    tag = sample.split('_TuneCP5_')[0]
    if filter not in tag:
        continue
    print('passed filter')
    if 'scenario' in tag:
        tag = tag.replace('scenario', 'Scenario')
        tag = tag.replace('mpi_', 'Mpi-')
        tag = tag.replace('mA_', 'MA-')
        tag = tag + 'mm'
        #tag = tag.replace('_%s'%selected_era, 'mm_%s'%selected_era)
        print(tag)
        # remove after reprocessing
        if '1000mm' not in tag:
            continue
    source = sourceDir + '/' + sample + '/' 
    for campaign in os.listdir(source):
        isource = source + '/' + campaign + '/'
        isource += sorted(os.listdir(isource))[-1] + '/'
        isource += '0000/' # Don't expect signals to contain more than 1000 files
        if "2022postEE" in isource:
            era = "2022postEE"
            year = "2022"
        elif "2022" in isource:
            era = "2022"
            year = "2022"
        elif "2023BPix" in isource:
            era = "2023BPix"
            year = "2023"
        elif "2023" in isource:
            era = "2023"
            year = "2023"
        if era!=selected_era:
            continue
        #destination = finalDir + '/Signal_' + tag + '_' + era + '/'
        #if not os.path.exists(destination):
        #    os.mkdir(destination)
        #os.system("mv {}*.root {}".format(isource, destination))
        #print("mv {}*.root {}".format(isource, destination))
        #line = "{},{}\n".format('Signal_' + tag + '_' + era, destination)
        line = "{},{}\n".format('Signal_' + tag + '_' + era, isource)
        print(line)
        fout_.write(line)
        f2out_.write("$ENV(SCOUTINGOUTPUTDIR) {} {} 0 100\n".format(year, 'Signal_' + tag + '_' + era))
        f3out_.write("$ENV(SCOUTINGINPUTDIR) $ENV(SCOUTINGOUTPUTDIR) --condor --signal --noSeed L1_DoubleMu_12_5 --inSample {} --splitIndex 0 --splitPace 1000000 $ENV(SCOUTINGARGS)\n".format('Signal_' + tag + '_' + era))
f2out_.write(")\n")
f3out_.write(")\n")
fout_.close()
f2out_.close()
os.system('sort -t, -k1,1 centralDatasets_%s_%s.txt > centralDatasets_%s_%ssorted.txt'%(filter, selected_era, filter, selected_era))
os.system('sort -k8,8 runScoutingHistos_onCondor_%s_%s.sub > runScoutingHistos_onCondor_%s_%s_sorted.sub'%(filter, selected_era, filter, selected_era))
print('sort -k8,8 runScoutingHistos_onCondor_%s_%s.sub > runScoutingHistos_onCondor_%s_%s_sorted.sub'%(filter, selected_era, filter, selected_era))
os.system('sort -t, -k1,1 runScoutingLooper_onCondor_%s_%s.sub > runScoutingLooper_onCondor_%s_%s_sorted.sub'%(filter, selected_era, filter, selected_era))
