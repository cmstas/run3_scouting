# HAHM production

The production takes as an example the existing HAHM hToZdZd simulation for Run 3 with $m_{Z_D} = 20$ GeV and $\epsilon = 1\cdot 10^{-8}$. Central fragment for this sample can be accessed through:

```
https://cms-pdmv.cern.ch/mcm/public/restapi/requests/get_fragment/EXO-Run3Summer22EEwmLHEGS-01017
```

Additional info:
McM record: https://cms-pdmv.cern.ch/mcm/requests?page=0&prepid=EXO-Run3Summer22EEwmLHEGS-01017

## Building the model

Each point is framed in a grid of $m_{Z_D}$ (mass of the dark photon) and $\epsilon$ (kinetix mixing). For the generation there are several parameters that need to be computed and set in the gridpacks/fragments:
- Lifetime $c\tau_{Z_D}$ (in mm): `ctau`
- Decay width $\Gamma_{Z_D}$ (in GeV): `gammaZd`
- Branching ratio to fermions including leptons and quarks

The characteristics of the model are documented in https://link.springer.com/article/10.1007/JHEP02(2015)157.

The `makeModel.py` script computes the parameters for a given set of $(m_{Z_D}, \epsilon)$ values. **Note: Branching ratios are not implemented yet.** It is executed by running:
```
python3 makeModel.py
```
after setting the `model_grid` variable with the $m_{Z_D}$ and $\epsilon$ choices.

The output is a `mass_epsilon_gamma_ctau.txt` file whose rows correspond with the final $m_{Z_D}$, $\epsilon$, $\Gamma_{Z_D}$ and $c\tau_{Z_D}$ values. The total width $\Gamma_{Z_D}$ is computed from the tabuled value of
$$\dfrac{\Gamma_{Z_D}}{\epsilon^2 \text{ (GeV)}}$$
which is available in `model-tables/HiggsedDarkPhoton_BrTableData.txt` and in [this reference](http://exotichiggs.physics.sunysb.edu/web/wopr/wp-content/uploads/2014/12/HiggsedDarkPhoton_BrTableData.txt). Then, the lifetime is computed by using
$$c\tau_{Z_D} = \dfrac{c\hbar}{\Gamma_{Z_D}}$$.

Last created file is available in `mass_epsilon_gamma_ctau.txt` and will be used as an input for the fragment generation (described later).

### Branching fraction calculation

The decay is driven by Pythia and the different branching fractions are set in the fragment (see below). These branching fractions need to be computed manually. The computation is done with Madgraph by following the steps specified below:

1) Get the model UFO from [insertar link], decompress it and copy the `HAHM_variableXX_UFO` folders in the Madgraph `models/` directory. Then, run Madgraph by doing:
```
./bin/mg5_aMC
```

2) Import the model from sw, define `f` for the fermions and generate the diagrams:
```
import model --modelname HAHM_variablesw_v3_UFO
define f = u c d s u~ c~ d~ s~ b b~ e+ e- m+ m- tt+ tt- ve vm vt ve~ vm~ vt~
generate zp > f f
```

3) Launch the computations and modify the model parameters accordingly:
```
launch
```
3.1) Set Pythia 8 for showering.
3.2) Set the `param_card.dat` accordingly for each point (remember to fix 400 GeV for $m_{s}$ and $k = 0.01$). For $m_{Z_D} = 10$ GeV and $\epsilon = 1\cdot 10^{-6}$ we would have:
```
###################################
## INFORMATION FOR HIDDEN
###################################
Block hidden
    1 1.000000e+01 # mZDinput
    2 4.000000e+02 # MHSinput
    3 1.000000e-06 # epsilon
    4 1.000000e-02 # kap
    5 1.279000e+02 # aXM1
```
3.3) Increase the number of generated events in the `run_card.dat` to `100000`.

Note: Madgraph can be used in lxplus by following the instructions of [this twiki](https://twiki.cern.ch/twiki/bin/view/Main/MadgraphOnLxPlus).

## Gridpack production

Template cards to make the gridpacks are found in ```card-templates/``` and are made from ones extracted from the central gridpack:
```
/cvmfs/cms.cern.ch/phys_generator/gridpacks/RunIII/13p6TeV/slc7_amd64_gcc10/madgraph/LL_HAHM_MS_400/LL_HAHM_MS_400_kappa_0p01_MZd_20_eps_1e-08_slc7_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz
```

To create the new cards for a predefined set of $(m_{Z_D}, \epsilon)$ values fist add the chosen points in ```makeCards.py``` with the following structure:
```
model_grid = {}
model_grid["5.0"] = ['1e-8', '2e-7']
```
and then run:
```
python3 makeCards.py
``` 
The output cards will be available in the ```hZdZd/``` dir.

To create the gridpacks the central generation repository should be cloned:
```
git clone https://github.com/cms-sw/genproductions.git
```
This would load the repository with the `master` configuration which now (Oct 4th) corresponds with:
- SCRAM ARCH: `slc7_amd64_gcc10` (used for central production)
- CMSSW version: `CMSSW_12_4_8` (used for central production)
- Madgraph5 version: 2.9.13 (central production used 2.9.9)

The new cards should be copied within the ```genproductions/bin/MadGraph5_aMCatNLO/cards``` folder. Then, in ```genproductions/bin/MadGraph5_aMCatNLO/``` the gridpacks are created by running:
```
./gridpack_generation.sh LL_HAHM_MS_400_kappa_0p01_MZd_5p0_eps_1e-8 cards/hZdZd/hZdZd_mZd_5p0_eps_1e-8/
```

Once created, test the output by going to the recently created folder and running ```runcmsgrid.sh```. For example:
```
cd LL_HAHM_MS_400_kappa_0p01_MZd_10_eps_1e-6/LL_HAHM_MS_400_kappa_0p01_MZd_10_eps_1e-6_gridpack/work/gridpack/
./runcmsgrid.sh 100 1 1
```

## Fragment production

(in progress)