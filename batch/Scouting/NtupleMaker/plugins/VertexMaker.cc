#include "Scouting/NtupleMaker/plugins/VertexMaker.h" 
#include "TMath.h"

using namespace edm;
using namespace std;

VertexMaker::VertexMaker(const edm::ParameterSet& iConfig):
theTransientTrackBuilderToken_{esConsumes(edm::ESInputTag("", "TransientTrackBuilder"))}
{
    muonVtxToken_ = consumes<Run3ScoutingMuonCollection>(iConfig.getParameter<InputTag>("muonVtxInputTag"));

    produces<std::vector<Run3ScoutingVertex>>("verticesVtx");
    produces<std::vector<vector<int> > >("vtxIndxVtx").setBranchAlias("MuonVtx_vtxIndx");

}

VertexMaker::~VertexMaker(){
}

void VertexMaker::beginJob(){}

void VertexMaker::endJob(){}

void VertexMaker::beginRun(const edm::Run& iRun, const edm::EventSetup& iSetup){}

reco::TrackBase::CovarianceMatrix VertexMaker::getCovariance(const Run3ScoutingMuon mu){

    reco::TrackBase::CovarianceMatrix cov = reco::TrackBase::CovarianceMatrix();

    cov(0,0) = mu.trk_qoverpError()*mu.trk_qoverpError();
    cov(1,1) = mu.trk_lambdaError()*mu.trk_lambdaError();
    cov(2,2) = mu.trk_phiError()*mu.trk_phiError();
    cov(3,3) = mu.trk_dxyError()*mu.trk_dxyError();
    cov(4,4) = mu.trk_dszError()*mu.trk_dszError();

    cov(0,1) = mu.trk_qoverp_lambda_cov();
    cov(1,0) = mu.trk_qoverp_lambda_cov();
    cov(0,2) = mu.trk_qoverp_phi_cov();
    cov(2,0) = mu.trk_qoverp_phi_cov();
    cov(0,3) = mu.trk_qoverp_dxy_cov();
    cov(3,0) = mu.trk_qoverp_dxy_cov();
    cov(0,4) = mu.trk_qoverp_dsz_cov();
    cov(4,0) = mu.trk_qoverp_dsz_cov();

    cov(1,2) = mu.trk_lambda_phi_cov();
    cov(2,1) = mu.trk_lambda_phi_cov();
    cov(1,3) = mu.trk_lambda_dxy_cov();
    cov(3,1) = mu.trk_lambda_dxy_cov();
    cov(1,4) = mu.trk_lambda_dsz_cov();
    cov(4,1) = mu.trk_lambda_dsz_cov();

    cov(2,3) = mu.trk_phi_dxy_cov();
    cov(3,2) = mu.trk_phi_dxy_cov();
    cov(2,4) = mu.trk_phi_dsz_cov();
    cov(4,2) = mu.trk_phi_dsz_cov();

    cov(3,4) = mu.trk_dxy_dsz_cov();
    cov(4,3) = mu.trk_dxy_dsz_cov();

    return cov;

}

void VertexMaker::produce(edm::Event& iEvent, const edm::EventSetup& iSetup){

    bool debug = false;

    const auto& theTransientTrackBuilder = iSetup.getData(theTransientTrackBuilderToken_);

    edm::Handle<Run3ScoutingMuonCollection> muonVtxHandle;
    iEvent.getByToken(muonVtxToken_, muonVtxHandle);

    if (debug) {
        std::cout << std::endl;
        std::cout << "------- Run " << iEvent.id().run() << " Lumi " << iEvent.luminosityBlock() << " Event " << iEvent.id().event() << " -------" << std::endl;
    }

    // event ptrs
    unique_ptr<vector<Run3ScoutingVertex> > v_vertexVtx(new vector<Run3ScoutingVertex >);
    unique_ptr<vector<vector<int>>> v_muonVtxIndices(new vector<vector<int>>(muonVtxHandle->size()));

    for (unsigned int i = 0; i < muonVtxHandle->size(); ++i) {
        for (unsigned int j = i + 1; j < muonVtxHandle->size(); ++j) {

            // track i
            const auto& imu = muonVtxHandle->at(i);
            reco::TrackBase::Vector imomentum(imu.trk_pt() * std::cos(imu.trk_phi()), imu.trk_pt() * std::sin(imu.trk_phi()), imu.trk_pt() * std::sinh(imu.trk_eta()));
            reco::TrackBase::Point irefPoint(imu.trk_vx(), imu.trk_vy(), imu.trk_vz());
            reco::TrackBase::CovarianceMatrix icov = getCovariance(imu);
            reco::Track itrack(imu.trk_chi2(), imu.trk_ndof(), irefPoint, imomentum, imu.charge(), icov, reco::TrackBase::undefAlgorithm, reco::TrackBase::undefQuality);
            reco::TransientTrack ittrack = theTransientTrackBuilder.build(itrack);

            // track j
            const auto& jmu = muonVtxHandle->at(j);
            reco::TrackBase::Vector jmomentum(jmu.trk_pt() * std::cos(jmu.trk_phi()), jmu.trk_pt() * std::sin(jmu.trk_phi()), jmu.trk_pt() * std::sinh(jmu.trk_eta()));
            reco::TrackBase::Point jrefPoint(jmu.trk_vx(), jmu.trk_vy(), jmu.trk_vz());
            reco::TrackBase::CovarianceMatrix jcov = getCovariance(jmu);
            reco::Track jtrack(jmu.trk_chi2(), jmu.trk_ndof(), jrefPoint, jmomentum, jmu.charge(), jcov, reco::TrackBase::undefAlgorithm, reco::TrackBase::undefQuality);
            reco::TransientTrack jttrack = theTransientTrackBuilder.build(jtrack);

            // Build vertex
            std::vector<reco::TransientTrack> ttracks = {ittrack, jttrack};
            KalmanVertexFitter kvf(true);
            TransientVertex tv = kvf.vertex(ttracks);

            // Build Run3ScoutingVertex and include it if valid
            if (tv.isValid()) {

                GlobalPoint pos = tv.position();
                GlobalError err = tv.positionError();
                
                Run3ScoutingVertex sv(
                    pos.x(),
                    pos.y(),
                    pos.z(),
                    err.cxx(),
                    err.cyy(),
                    err.czz(),
                    2,
                    tv.totalChiSquared(),
                    tv.degreesOfFreedom(),
                    tv.isValid(),
                    err.cyx(),
                    err.czx(),
                    err.czy()
                );

                v_vertexVtx->push_back(sv);

                (*v_muonVtxIndices)[i].push_back(v_vertexVtx->size() - 1);
                (*v_muonVtxIndices)[j].push_back(v_vertexVtx->size() - 1);

            }

        }
    }

    if (debug){
        std::cout << "Number of sv vertices = " << v_vertexVtx->size() << std::endl;
        for (unsigned int i = 0; i < muonVtxHandle->size(); ++i) {
            std::cout << "Muon " << i << " = " << (*v_muonVtxIndices)[i].size() << std::endl;
        }
    }

    // Event fill
    iEvent.put(std::move(v_vertexVtx), "verticesVtx");
    iEvent.put(std::move(v_muonVtxIndices), "vtxIndxVtx");

}

DEFINE_FWK_MODULE(VertexMaker);
