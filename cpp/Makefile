CC=g++
#INCLUDE=-I. -I$${CMSSW_BASE}/src -I$${CMSSW_BASE}/../../../external/boost/1.78.0-850e5328ab465746724c19b2301f9b35/include
#INCLUDE=-I. -I${CMSSW_BASE}/src -I${CMSSW_BASE}/src/DataFormats/FWLite/interface
INCLUDE=-I. -I$${CMSSW_BASE}/src -I$${CMSSW_RELEASE_BASE}/src -I$${CMSSW_BASE}/../../../external/boost/1.78.0-850e5328ab465746724c19b2301f9b35/include -I${CMSSW_RELEASE_BASE}/src/DataFormats/FWLite/interface
ifeq ($(SCRAM_ARCH),el9_amd64_gcc12)
INCLUDE=-I. -I$${CMSSW_BASE}/src -I$${CMSSW_RELEASE_BASE}/src -I$${CMSSW_BASE}/../../../external/boost/1.80.0-ee7655da280415252b8b334e18473a5c/include -I/cvmfs/cms.cern.ch/el9_amd64_gcc12/external/fmt/10.2.1-e35fd1db5eb3abc8ac0452e8ee427196/include -I${CMSSW_RELEASE_BASE}/src/DataFormats/FWLite/interface
endif
ifeq ($(SCRAM_ARCH),el8_amd64_gcc12)
INCLUDE=-I. -I$${CMSSW_BASE}/src -I$${CMSSW_RELEASE_BASE}/src -I/cvmfs/cms.cern.ch/el8_amd64_gcc12/external/boost/1.80.0-f9d55d46c162407ba3033b506563d0e2/include -I/cvmfs/cms.cern.ch/el8_amd64_gcc12/external/fmt/10.2.1-e35fd1db5eb3abc8ac0452e8ee427196/include -I${CMSSW_RELEASE_BASE}/src/DataFormats/FWLite/interface
endif
LIBRARIES=-L$${CMSSW_BASE}/lib/$${SCRAM_ARCH} -L$${CMSSW_RELEASE_BASE}/lib/$${SCRAM_ARCH} -lDataFormatsFWLite -lFWCoreUtilities -lDataFormatsCandidate -lDataFormatsCommon -lDataFormatsHepMCCandidate -lDataFormatsProvenance -lPhysicsToolsUtilities -lSimDataFormatsPileupSummaryInfo

SOURCES=$(wildcard tools/*.cc)
OUT=main.exe 
OBJS=main.cc rootDict.o $(SOURCES:.cc=.o)

all : $(OUT)

#$(OUT): $(OBJS) run3ScoutingLooper.C
#	$(CC) $(OBJS) $(INCLUDE) $(LIBRARIES) -std=c++11 -Wno-attributes -o $(OUT) `root-config --cflags --glibs` -lstdc++ -lpthread
#$(OUT): $(OBJS) run3ScoutingLooper.C
#	$(CC) $(OBJS) $(INCLUDE) $(LIBRARIES) -std=c++11 -Wno-attributes -o $(OUT) `root-config --cflags --glibs` -static-libstdc++ -lpthread
#$(OUT): $(OBJS) run3ScoutingLooper.C
#	$(CC) $(OBJS) $(INCLUDE) $(LIBRARIES) -std=c++11 -Wno-attributes -o $(OUT) `root-config --cflags --glibs` -lpthread
#$(OUT): $(OBJS) run3ScoutingLooper.C
#	$(CC) $(OBJS) $(INCLUDE) $(LIBRARIES) -std=c++17 -Wno-attributes -o $(OUT) `root-config --cflags --glibs` -L/cvmfs/cms.cern.ch/el8_amd64_gcc10/external/gcc/10.3.0-84898dea653199466402e67d73657f10/lib64/ -lstdc++ -lpthread
#$(OUT): $(OBJS) run3ScoutingLooper.C
#$(CC) $(OBJS) $(INCLUDE) $(LIBRARIES) -std=c++17 -Wno-attributes -o $(OUT) `root-config --cflags --glibs` -static-libstdc++ -lpthread
#$(OUT): $(OBJS) run3ScoutingLooper.C
#	$(CC) $(OBJS) $(INCLUDE) $(LIBRARIES) -std=c++17 -Wno-attributes -o $(OUT) `root-config --cflags --glibs` -lpthread
# Knows to work
ifeq ($(SCRAM_ARCH),el9_amd64_gcc12)
$(OUT): $(OBJS) run3ScoutingLooper.C
	$(CC) $(OBJS) $(INCLUDE) $(LIBRARIES) -std=c++17 -Wno-attributes -o $(OUT) `root-config --cflags --glibs` -L/cvmfs/cms.cern.ch/el9_amd64_gcc12/external/gcc/12.3.1-40d504be6370b5a30e3947a6e575ca28/lib64/ -lstdc++ -lpthread
else ifeq ($(SCRAM_ARCH),el8_amd64_gcc12)
$(OUT): $(OBJS) run3ScoutingLooper.C
	$(CC) $(OBJS) $(INCLUDE) $(LIBRARIES) -std=c++17 -Wno-attributes -o $(OUT) `root-config --cflags --glibs` -lstdc++ -lpthread
else
$(OUT): $(OBJS) run3ScoutingLooper.C
	$(CC) $(OBJS) $(INCLUDE) $(LIBRARIES) -std=c++17 -Wno-attributes -o $(OUT) `root-config --cflags --glibs` -L/cvmfs/cms.cern.ch/el8_amd64_gcc10/external/gcc/10.3.0-84898dea653199466402e67d73657f10/lib64/ -lstdc++ -lpthread
endif


rootDict : LinkDef.h
	rootcint -f rootDict.cc -c headerDict.h LinkDef.h

%.o : tools/%.cc tools/%.h
	$(CC) -c $< -o $@

rootDict.o : rootDict.cc
	$(CC) -I$../include -c $< -o $@ `root-config --cflags --glibs`
	
clean:
	rm -f main.exe *.o tools/*.o
