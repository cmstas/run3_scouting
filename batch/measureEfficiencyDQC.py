import os
import subprocess

os.system("""dasgoclient --query="dataset=/scenario*_mpi_*_mA_*_ctau_*/fernance-AODSIM_2023-final-*/USER instance=prod/phys03" > tmp.txt""")

with open("tmp.txt", 'r') as f:
    listOfDatasets = f.readlines()

print("Datasets to measure efficiencies:")
print(listOfDatasets)
print(f"Total: {len(listOfDatasets)}")

outfile = open("efficiencies.txt", 'w')

for dataset in listOfDatasets:
    dataset = dataset.replace('\n', '')
    os.system("""/cvmfs/cms.cern.ch/common/dasgoclient --query="dataset={0} instance=prod/phys03 | grep dataset.nfiles" > tmp_nfiles.txt""".format(dataset))
    with open('tmp_nfiles.txt','r') as f:
        nfiles = f.readlines()
        nfiles = [line for line in nfiles if line!=' \n']
        nfiles = nfiles[0]
        nfiles = nfiles.replace(' \n', '')
    nfiles = int(nfiles)
    os.system("""/cvmfs/cms.cern.ch/common/dasgoclient --query="dataset={0} instance=prod/phys03 | grep dataset.nevents" > tmp_nevents.txt""".format(dataset))
    with open('tmp_nevents.txt','r') as f:
        nevents = f.readlines()
        nevents = [line for line in nevents if line!=' \n']
        nevents = nevents[0]
        nevents = nevents.replace(' \n', '')
    nevents = int(nevents)
    sample = dataset.split('/')[1]
    mpi = sample.split('_mpi_')[1].split('_')[0]
    mA = sample.split('_mA_')[1].split('_')[0]
    ctau = sample.split('_ctau_')[1].split('_')[0]
    if 'scenarioA' in sample:
        tag = 'ScenarioA'
    if 'scenarioB1' in sample:
        tag = 'ScenarioB1'
    sampleName = f"Signal_{tag}_Mpi-{mpi}_MA-{mA}_ctau-{ctau}mm"
    print(f'>>>> {dataset}')
    print(f'> {sampleName}')
    print(f'> {nfiles}')
    print(f'> {nevents}')
    efficiency = float(nevents) / float(nfiles * 1000) 
    print(f'> {efficiency}')
    outfile.write(f'{sampleName},{efficiency}\n')

outfile.close()