CC=g++
#INCLUDE=-I. -I$${CMSSW_BASE}/src -I$${CMSSW_BASE}/../../../external/boost/1.78.0-850e5328ab465746724c19b2301f9b35/include
#INCLUDE=-I. -I${CMSSW_BASE}/src -I${CMSSW_BASE}/src/DataFormats/FWLite/interface
INCLUDE=-I. -I$${CMSSW_BASE}/src -I$${CMSSW_BASE}/../../../external/boost/1.78.0-850e5328ab465746724c19b2301f9b35/include -I${CMSSW_BASE}/src/DataFormats/FWLite/interface
LIBRARIES=-L$${CMSSW_BASE}/lib/$${SCRAM_ARCH} -lDataFormatsFWLite -lFWCoreUtilities -lDataFormatsCandidate -lDataFormatsCommon -lDataFormatsHepMCCandidate -lDataFormatsProvenance

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
$(OUT): $(OBJS) run3ScoutingLooper.C
	$(CC) $(OBJS) $(INCLUDE) $(LIBRARIES) -std=c++17 -Wno-attributes -o $(OUT) `root-config --cflags --glibs` -L/cvmfs/cms.cern.ch/el8_amd64_gcc10/external/gcc/10.3.0-84898dea653199466402e67d73657f10/lib64/ -lstdc++ -lpthread


rootDict : LinkDef.h
	rootcint -f rootDict.cc -c headerDict.h LinkDef.h

%.o : tools/%.cc tools/%.h
	$(CC) -c $< -o $@

rootDict.o : rootDict.cc
	$(CC) -I$../include -c $< -o $@ `root-config --cflags --glibs`
	
clean:
	rm main.exe *.o tools/*.o
