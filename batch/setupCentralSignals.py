import os

## This script put the crab output in the corresponding ceph area and creates the files to run the looper and plotter

# To be modified by user:
sourceDir = "/ceph/cms/store/group/Run3Scouting/RAWScouting_5c"
finalDir = "/ceph/cms/store/group/Run3Scouting/Run3ScoutingSamples/Feb-03-2024/CentralSignal"
sourceDir = "/ceph/cms/store/group/Run3Scouting/RAWScouting_BToPhi_2023_v7p0"
modeto = False # Set to True if moving files it is necessary
selected_era = '2023BPix'

### File with central datasets fr looper input
fout_ = open("centralDatasets.txt", "w")

### File with condor launcher for looper
f2out_ = open("runScoutingLooper_onCondor_CentralSignal.sub", "w") 
f2out_.write("executable      = $ENV(STARTDIR)/condor/condorLooper_executable.sh\n")
f2out_.write("output          = $ENV(STARTDIR)/condor/plotting_logs/job.$(ClusterId).$(ProcId).out\n")
f2out_.write("error           = $ENV(STARTDIR)/condor/plotting_logs/job.$(ClusterId).$(ProcId).err\n")
f2out_.write("log             = $ENV(STARTDIR)/condor/plotting_logs/job.$(ClusterId).$(ProcId).log\n")
f2out_.write("\n")
f2out_.write("getenv = True\n")
f2out_.write("+JobFlavour = 'workday'\n")
f2out_.write("+DESIRED_Sites = 'T2_US_UCSD'\n")
f2out_.write("transfer_input_files = $ENV(STARTDIR)/package.tar.gz\n")
f2out_.write("should_transfer_files = YES\n")
f2out_.write("when_to_transfer_output = ON_EXIT\n")
f2out_.write("x509userproxy=$ENV(X509_USER_PROXY)\n")
f2out_.write("use_x509userproxy = True\n")
f2out_.write("\n")
f2out_.write("queue arguments from (\n")

### File with condor launcher for histos
f3out_ = open("runScoutingHistos_onCondor_CentralSignal.sub", "w") 
f3out_.write("executable      = $ENV(STARTDIR)/condor/condorHistos_executable.sh\n")
f3out_.write("output          = $ENV(STARTDIR)/condor/plotting_logs/job.$(ClusterId).$(ProcId).out\n")
f3out_.write("error           = $ENV(STARTDIR)/condor/plotting_logs/job.$(ClusterId).$(ProcId).err\n")
f3out_.write("log             = $ENV(STARTDIR)/condor/plotting_logs/job.$(ClusterId).$(ProcId).log\n")
f3out_.write("\n")
f3out_.write("RequestCpus   = 2\n")
f3out_.write("RequestMemory = 8000\n")
f3out_.write("\n")
f3out_.write("getenv = True\n")
f3out_.write("+JobFlavour = 'workday'\n")
f3out_.write("+DESIRED_Sites = 'T2_US_UCSD'\n")
f3out_.write("transfer_input_files = $ENV(STARTDIR)/package.tar.gz\n")
f3out_.write("should_transfer_files = YES\n")
f3out_.write("when_to_transfer_output = ON_EXIT\n")
f3out_.write("x509userproxy=$ENV(X509_USER_PROXY)\n")
f3out_.write("use_x509userproxy = True\n")
f3out_.write("\n")
f3out_.write("queue arguments from (\n")

for sample in os.listdir(sourceDir):
    if '.' in sample:
        continue
    tag = sample.split('_TuneCP5_')[0]
    source = sourceDir + '/' + sample + '/' 
    for campaign in os.listdir(source):
        isource = source + '/' + campaign + '/'
        isource += os.listdir(isource)[-1] + '/'
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
        fout_.write(line)
        f2out_.write("$ENV(SCOUTINGOUTPUTDIR) {} {} 0 100\n".format(year, 'Signal_' + tag + '_' + era))
        f3out_.write("$ENV(SCOUTINGINPUTDIR) $ENV(SCOUTINGOUTPUTDIR) --condor --signal --inSample {} --splitIndex 0 --splitPace 1000000 $ENV(SCOUTINGARGS)\n".format('Signal_' + tag + '_' + era))
f2out_.write(")\n")
f3out_.write(")\n")
fout_.close()
f2out_.close()
