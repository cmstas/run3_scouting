import os,sys
import ROOT

ROOT.gROOT.ProcessLine(".L cpp/helper.C+")

if len(sys.argv)<3:
    print("Please, specify model and limit directory.")
    exit(1)

var = sys.argv[1]
model = sys.argv[2]
limdir = sys.argv[3]
year = sys.argv[4]
if len(sys.argv)>5:
    outdir = sys.argv[5]
    if not os.path.exists(outdir):
        os.makedirs(outdir)
else:
    outdir = limdir

fout = open("%s/limits_%s_asymptotic_%s.txt"%(outdir,model,year),"w")

if model=="HTo2ZdTo2mu2x":
    if var=='ctau':
        #masses =  [0.5, 0.7, 1.5, 2.0, 2.5, 5.0, 6.0, 7.0, 8.0, 12.0, 14.0, 16.0, 20.0, 22.0, 24.0, 30.0, 34.0, 40.0, 44.0, 50.0] # Full set of masses
        masses =  [1.5, 2.0, 2.5, 5.0, 7.0, 8.0, 14.0, 16.0, 20.0, 22.0, 24.0, 30.0, 34.0, 40.0, 44.0, 50.0]
        masses =  [1.5, 2.0, 2.5, 5.0, 12.0, 20.0, 30.0, 40.0, 50.0]
        #masses =  [20.0, 30.0, 40.0, 50.0]
        #masses =  [40.000, 50.000]
        ctaus = [0.10, 0.16, 0.25, 0.40, 0.63, 1.00, 1.60, 2.50, 4.00, 6.30, 10.00, 16.00, 25.00, 40.00, 63.00, 100.00, 160.00, 250.00, 400.00, 630.00, 1000.00]
    elif var=='mass':
        masses = []
        ctaus = [1, 10, 100, 1000] # Lifetimes for the grid
        with open('data/sigmasses_HTo2ZdTo2mu2x_fine.txt', 'r') as f:
            lmasses = f.readlines()
            for mass in lmasses:
                m = float(mass)
                masses.append(m)
                print(m)
elif model=="BToPhi": 
    if var=='ctau':
        #masses =  [0.25, 0.30, 0.40, 0.50, 0.60, 0.70, 0.90, 1.25, 1.50, 2.0, 2.85, 3.35, 4.00, 5.00] # Just full set of masses
        masses =  [1.25, 1.50, 2.0] # Just full set of masses
        ctaus = [0.10, 0.16, 0.25, 0.40, 0.63, 1.00, 1.60, 2.50, 4.00, 6.30, 10.00, 16.00, 25.00, 40.00, 63.00, 100.0]
    elif var=='mass':
        masses = []
        ctaus = [1, 10, 100] # Lifetimes for the grid
        with open('data/BToPhi_limitgrid.txt', 'r') as f:
            lmasses = f.readlines()
            for mass in lmasses:
                m = float(mass)
                masses.append(m)
                print(m)
elif model=="ScenarioA": 
    if var=='ctau':
        masses =  [] 
        #masses.append([1,0.33])
        masses.append([2,0.67])
        masses.append([4,1.33])
        masses.append([5,1.67])
        #masses.append([3.33,0.33])
        masses.append([6.,2.])
        masses.append([7.5,2.5])
        masses.append([12.,1.20])
        ctaus = [0.10, 0.25, 0.60, 1.00, 2.50, 6.00, 10.00, 25.00, 60.00, 100.00]
        ctaus = [1000.0]
    elif var=='mass':
        print("No mass grid supported for this model")
elif model=="ScenarioB1": 
    if var=='ctau':
        masses =  [] 
        #masses.append([1,0.33])
        masses.append([2,0.67])
        masses.append([4,1.33])
        masses.append([5,1.67])
        #masses.append([3.33,0.33])
        masses.append([6.,2.])
        masses.append([7.5,2.5])
        masses.append([12.,1.20])
        #ctaus = [0.10, 0.25, 0.60, 1.00, 2.50, 6.00, 10.00, 25.00, 60.00, 100.00]
        ctaus = [1000.0]
    elif var=='mass':
        print("No mass grid supported for this model")


f2bs = [0.0]
if model == "nomodel":
    f2bs = [0.0,0.01,0.05,0.1,0.25,0.5,0.75,0.9,0.95,0.99,1.0]
    fout.write("# mass,f2b,obs,exp,exp-2s,exp-1s,exp+1s,exp+1s\n")
else:
    if "Scenario" not in model:
        fout.write("# model,mass,ctau,obs,exp,exp-2s,exp-1s,exp+1s,exp+1s\n")
    else:
        fout.write("# model,mass1,mass2,ctau,obs,exp,exp-2s,exp-1s,exp+1s,exp+1s\n")

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
                if "Scenario" not in model:
                    fname = "%s/lim_asymptotic_%s_m%.3f_ctau%.2f_%s.txt"%(limdir,model,m,t,year)
                else:
                    fname = "%s/lim_asymptotic_%s_m%.3f_M%.3f_ctau%.2f_%s.txt"%(limdir,model,m[0],m[1],t,year)
                print('Reading: ' + fname)
            else:
                fname = "%s/lim_asymptotic_f2b%.0f_m%.0f.txt"%(limdir,100.0*f,m)
            if not os.path.exists(fname):
                continue
                print(">>> Missing point: %.3f GeV, %.2f mm"%(m, t))
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
            if float(obs) > -1 and float(exp) > -1:
                if model != "nomodel":
                    if "Scenario" not in model:
                        fout.write("%s,%.3f,%.2f,%s,%s,%s,%s,%s,%s\n"%(model,m,t,obs,exp,m2s,m1s,p1s,p2s))
                    else:
                        fout.write("%s,%.3f,%.3f,%.2f,%s,%s,%s,%s,%s,%s\n"%(model,m[0],m[1],t,obs,exp,m2s,m1s,p1s,p2s))
                else:
                    fout.write("%.0f,%.2f,%s,%s,%s,%s,%s,%s\n"%(m,f,obs,exp,m2s,m1s,p1s,p2s))

fout.close()
