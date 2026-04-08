# Some instructions

## PU reweighting

To obtain the MC profiles we get them directly from CMSSW:
```
python3 scripts/makeMCPileupHist.py SimGeneral.MixingModule.mix_2022_25ns_RunIII2022Summer24_PoissonOOTPU_cfi --outputFilename MCPileupHistogram2022.root
python3 scripts/makeMCPileupHist.py SimGeneral.MixingModule.mix_2023_25ns_EraCD_PoissonOOTPU_cfi --outputFilename MCPileupHistogram2023.root
```

For the data instead:
```
```
