#!/bin/bash

usage() {
    echo ""
    echo "Usage:  sh condor/fillTuples_onCondor.sh ['notar'] <INDIR>"
    echo "        <INDIR> = looper output dir tag or full /ceph/cms/... path"
    echo ""
    exit 1
}

notar=0
indir=""
if [ "$1" == "notar" ]; then
    notar=1
    indir=$2
else
    indir=$1
fi
[ -z "$indir" ] && usage

# Normalize: accept a bare tag or a full path.
case "$indir" in
    /*) INDIR="$indir" ;;
    *)  INDIR="/ceph/cms/store/group/Run3Scouting/${indir}" ;;
esac
if [ ! -d "$INDIR" ]; then
    echo "ERROR: input dir not found: $INDIR"
    exit 1
fi

# Proxy for the xrootd/davs reads from the redirector.
cp $(voms-proxy-info -path) $HOME/x509proxy
export X509_USER_PROXY=$HOME/x509proxy

export STARTDIR=$PWD
export FILLTUPLES_INDIR="$INDIR"

export FILLTUPLES_TUPLEDIR="${FILLTUPLES_TUPLEDIR:-tuples_L1_info}"
export FILLTUPLES_COLLECTION="${FILLTUPLES_COLLECTION:-OR}"
mkdir -p condor/plotting_logs

ls "$INDIR"/output_*.root 2>/dev/null \
    | xargs -n1 basename 2>/dev/null \
    | sed -E 's/^output_(.*)_2024_([0-9]+To[0-9]+)\.root$/\1, \2/' \
    | sort -u > condor/fillTuples_samples.txt

if [ -n "${FILLTUPLES_SAMPLE_GREP:-}" ]; then
    grep -E "$FILLTUPLES_SAMPLE_GREP" condor/fillTuples_samples.txt > condor/fillTuples_samples.txt.tmp || true
    mv condor/fillTuples_samples.txt.tmp condor/fillTuples_samples.txt
    echo "Applied sample filter '$FILLTUPLES_SAMPLE_GREP'."
fi

njobs=$(wc -l < condor/fillTuples_samples.txt)
if [ "$njobs" -eq 0 ]; then
    echo "ERROR: no output_*.root files found in $INDIR"
    exit 1
fi
echo "Found $njobs file(s) to process in $INDIR (one job each):"
cat condor/fillTuples_samples.txt
echo ""
echo "Output tuple dir: $FILLTUPLES_TUPLEDIR   |   collection: $FILLTUPLES_COLLECTION"
echo ""

if [ ${notar} -eq 0 ]; then
    echo "Creating package_fillTuples.tar.gz ..."
    sh condor/fillTuples_create_package.sh
fi
if [ ! -f package_fillTuples.tar.gz ]; then
    echo "ERROR: package_fillTuples.tar.gz missing (run without 'notar' to build it)."
    exit 1
fi

condor_submit condor/fillTuples_onCondor.sub

# Print the per-sample merge command(s) to run once all jobs are done. The BDT keys
# on the single filename tuples_<sample>_2024.root, so the shards must be hadd'ed.
echo ""
echo "=== When all jobs finish, merge shards into the BDT-expected filename(s): ==="
cut -d, -f1 condor/fillTuples_samples.txt | sort -u | while read -r s; do
    s=$(echo "$s" | tr -d '[:space:]')
    echo "hadd -f ${FILLTUPLES_TUPLEDIR}/tuples_${s}_2024.root ${FILLTUPLES_TUPLEDIR}/tuples_${s}_2024_*To*.root"
done
