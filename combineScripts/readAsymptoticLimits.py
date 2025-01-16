import os,sys
import ROOT

ROOT.gROOT.ProcessLine(".L cpp/helper.C+")

useSignalMC = False

if len(sys.argv)<3:
    print("Please, specify model and limit directory.")
    exit(1)

model = sys.argv[1]
limdir = sys.argv[2]
year = sys.argv[3]
if len(sys.argv)>4:
    outdir = sys.argv[4]
    if not os.path.exists(outdir):
        os.makedirs(outdir)
else:
    outdir = limdir

fout = open("%s/limits_%s_%s.txt"%(outdir,model,year),"w")

if useSignalMC:
    #masses =  [0.5, 0.7, 1.5, 2.0, 2.5, 5.0, 6.0, 7.0, 8.0, 12.0, 14.0, 16.0, 20.0, 22.0, 24.0, 30.0, 34.0, 40.0, 44.0, 50.0] # Full set of masses
    #masses =  [1.5, 2.0, 2.5, 5.0, 6.0, 7.0, 8.0, 14.0, 16.0, 20.0, 22.0, 24.0, 30.0, 34.0, 40.0, 44.0, 50.0]
    masses =  [5.0, 8.0]
    ctaus = [0.10, 0.16, 0.25, 0.40, 0.63, 1.00, 1.60, 2.50, 4.00, 6.30, 10.00, 16.00, 25.00, 40.00, 63.00, 100.00]
else:
    masses = []
    ctaus = [1, 10, 100] # Lifetimes for the grid
    with open('data/HZdZd_limitgrid.txt', 'r') as f:
        lmasses = f.readlines()
        for mass in lmasses:
            m = float(mass)
            masses.append(m)
            print(m)

f2bs = [0.0]
if model == "nomodel":
    f2bs = [0.0,0.01,0.05,0.1,0.25,0.5,0.75,0.9,0.95,0.99,1.0]
    fout.write("# mass,f2b,obs,exp,exp-2s,exp-1s,exp+1s,exp+1s\n")
else:
    fout.write("# model,mass,ctau,obs,exp,exp-2s,exp-1s,exp+1s,exp+1s\n")

for m in masses:
    for t in ctaus:
        for f in f2bs:
            obs = -1.0
            exp = -1.0
            m2s = -1.0
            m1s = -1.0
            p1s = -1.0
            p2s = -1.0
            if model != "nomodel":
                fname = "%s/lim_asymptotic_%s_m%.3f_ctau%.2f_%s.txt"%(limdir,model,m,t,year)
                print('Reading: ' + fname)
            else:
                fname = "%s/lim_asymptotic_f2b%.0f_m%.0f.txt"%(limdir,100.0*f,m)
            if not os.path.exists(fname):
                continue
            else:
                fin=open(fname,"r")
            for l in fin.readlines():
                if "Observed" in l:
                    obs = l.split()[len(l.split())-1]
                elif "Expected  2.5" in l:
                    m2s = l.split()[len(l.split())-1]
                elif "Expected 16" in l:
                    m1s = l.split()[len(l.split())-1]
                elif "Expected 50" in l:
                    exp = l.split()[len(l.split())-1]
                elif "Expected 84" in l:
                    p1s = l.split()[len(l.split())-1]
                elif "Expected 97.5" in l:
                    p2s = l.split()[len(l.split())-1]
            fin.close()
            if model != "nomodel":
                fout.write("%s,%.3f,%.2f,%s,%s,%s,%s,%s,%s\n"%(model,m,t,obs,exp,m2s,m1s,p1s,p2s))
            else:
                fout.write("%.0f,%.2f,%s,%s,%s,%s,%s,%s\n"%(m,f,obs,exp,m2s,m1s,p1s,p2s))

fout.close()
