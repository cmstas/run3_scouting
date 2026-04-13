#!/bin/bash

indir=$1
cd "$indir" || exit 1

for tag in $(ls histograms_GEN_*.root | sed -E 's/histograms_GEN_([^_]+)_.*/\1/' | sort -u); do
    echo "Haciendo hadd para $tag ..."
    hadd -f histograms_GEN_${tag}.root histograms_GEN_${tag}_*.root
done

