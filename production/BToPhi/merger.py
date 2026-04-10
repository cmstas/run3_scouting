import os
import sys

basedir = '/ceph/cms/store/group/Run3Scouting/GENScouting_noFilter_v1/'

signals = []
signals.append('BToPhi_MPhi-0p3_ctau-1mm')
signals.append('BToPhi_MPhi-0p4_ctau-1mm')
signals.append('BToPhi_MPhi-0p5_ctau-1mm')
signals.append('BToPhi_MPhi-0p6_ctau-1mm')
signals.append('BToPhi_MPhi-0p7_ctau-1mm')
signals.append('BToPhi_MPhi-0p9_ctau-1mm')
signals.append('BToPhi_MPhi-1p25_ctau-1mm')
signals.append('BToPhi_MPhi-1p5_ctau-1mm')
signals.append('BToPhi_MPhi-2p0_ctau-1mm')
signals.append('BToPhi_MPhi-2p85_ctau-1mm')
signals.append('BToPhi_MPhi-3p35_ctau-1mm')
signals.append('BToPhi_MPhi-4p0_ctau-1mm')
signals.append('BToPhi_MPhi-5p0_ctau-1mm')

for signal in signals:
    signaldir = basedir + signal + '-pythia8/'
    os.chdir(signaldir)
    datadir_ = [d for d in os.listdir(signaldir)][-1]
    datadir = signaldir + datadir_ + '/'
    datedir_ = [d for d in os.listdir(datadir)][-1]
    datedir = datadir + datedir_ + '/'
    target = datedir + '0000/'
    os.chdir(target)
    # hadd
    roots = [d for d in os.listdir(target) if 'root' in d]
    for i in range(0,10):
        if i<9:
            iroots = roots[i*100:(i+1)*100]
        else:
            iroots = roots[900:-1]
        tomerge = ''
        for root in iroots:
            tomerge = tomerge + root + ' '
        tomerge = tomerge[:-1] # no coma
        #print('>>>> hadd target_%i.root %s'%(i, tomerge))
        os.system("$PWD")
        os.system('hadd -f target_%i.root %s'%(i, tomerge))
    os.system('mv target*.root %s'%(datedir))
    os.system("""echo "%s" >> %s/finalpaths.txt"""%(target, basedir))
