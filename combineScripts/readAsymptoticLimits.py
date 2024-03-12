import os,sys

useSignalMC = False

if len(sys.argv)<3:
    print("Please, specify model and limit directory.")
    exit(1)

model = sys.argv[1]
limdir = sys.argv[2]
if len(sys.argv)>3:
    outdir = sys.argv[3]
    if not os.path.exists(outdir):
        os.makedirs(outdir)
else:
    outdir = limdir

fout = open("%s/limits_%s.txt"%(outdir,model),"w")

masses =  [0.5, 0.7, 1.5, 2.0, 2.5, 5.0, 6.0, 7.0, 8.0, 12.0, 14.0, 16.0, 20.0, 22.0, 24.0, 30.0, 34.0, 40.0, 44.0, 50.0]
ctaus = [1, 10, 100]

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
                fname = "%s/lim_asymptotic_%s_m%.1f_ctau%i.txt"%(limdir,model,m,t)
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
                fout.write("%s,%.1f,%i,%s,%s,%s,%s,%s,%s\n"%(model,m,t,obs,exp,m2s,m1s,p1s,p2s))
            else:
                fout.write("%.0f,%.2f,%s,%s,%s,%s,%s,%s\n"%(m,f,obs,exp,m2s,m1s,p1s,p2s))

fout.close()
