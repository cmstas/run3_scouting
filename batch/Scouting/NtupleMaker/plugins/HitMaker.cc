#include "Scouting/NtupleMaker/plugins/HitMaker.h" 
#include "TMath.h"

using namespace edm;
using namespace std;

namespace {

  Surface::RotationType rotation(const GlobalVector& zDir) {
    GlobalVector zAxis = zDir.unit();
    GlobalVector yAxis(zAxis.y(), -zAxis.x(), 0);
    GlobalVector xAxis = yAxis.cross(zAxis);
    return Surface::RotationType(xAxis, yAxis, zAxis);
  }


}

HitMaker::HitMaker(const edm::ParameterSet& iConfig):
magFieldToken_(esConsumes()),
trackingGeometryToken_(esConsumes()),
measurementTrackerToken_(esConsumes()),
trackerTopologyToken_(esConsumes()),
propagatorToken_(esConsumes(edm::ESInputTag("", "PropagatorWithMaterial")))
{
    muonToken_ = consumes<Run3ScoutingMuonCollection>(iConfig.getParameter<InputTag>("muonInputTag"));
    dvToken_ = consumes<Run3ScoutingVertexCollection>(iConfig.getParameter<InputTag>("dvInputTag"));
    measurementTrackerEventToken_ = consumes<MeasurementTrackerEvent>(iConfig.getParameter<InputTag>("measurementTrackerEventInputTag"));
    vtxIndxToken_ = mayConsume<std::vector<std::vector<int>>>(iConfig.getParameter<InputTag>("vtxIndxInputTag"));

    produces<vector<vector<vector<bool> > > >("isbarrel").setBranchAlias("Muon_hit_barrel");
    produces<vector<vector<vector<bool> > > >("ispixel").setBranchAlias("Muon_hit_pixel");
    produces<vector<vector<vector<bool> > > >("isactive").setBranchAlias("Muon_hit_active");
    produces<vector<vector<vector<int> > > >("layernum").setBranchAlias("Muon_hit_layer");
    produces<vector<vector<vector<int> > > >("ndet").setBranchAlias("Muon_hit_ndet");
    produces<vector<vector<vector<float> > > >("x").setBranchAlias("Muon_hit_x");
    produces<vector<vector<vector<float> > > >("y").setBranchAlias("Muon_hit_y");
    produces<vector<vector<vector<float> > > >("z").setBranchAlias("Muon_hit_z");
    produces<vector<vector<int> > >("nhitsbeforesv").setBranchAlias("Muon_nHitsBeforeSV");
    produces<vector<vector<int> > >("nexpectedhits").setBranchAlias("Muon_nExpectedPixelHits");
    produces<vector<vector<int> > >("ncompatible").setBranchAlias("Muon_nCompatiblePixelLayers");
    produces<vector<vector<int> > >("nexpectedhitsmultiple").setBranchAlias("Muon_nExpectedPixelHitsMultiple");
    produces<vector<vector<int> > >("ncompatibletotal").setBranchAlias("Muon_nCompatibleTrackerLayers");
    produces<vector<vector<int> > >("nexpectedhitsmultipletotal").setBranchAlias("Muon_nExpectedTrackerHitsMultiple");
    produces<vector<vector<int> > >("nexpectedhitstotal").setBranchAlias("Muon_nExpectedTrackerHits");
    produces<vector<vector<float> > >("pxatdv").setBranchAlias("Muon_pxatdv");
    produces<vector<vector<float> > >("pyatdv").setBranchAlias("Muon_pyatdv");
    produces<vector<vector<float> > >("pzatdv").setBranchAlias("Muon_pzatdv");
    produces<vector<bool> >("dvonmodule").setBranchAlias("Vertex_onModule");
    produces<vector<bool> >("dvonmodulewithinunc").setBranchAlias("Vertex_onModule_withinUnc");
    produces<vector<float> >("dvmindfromdet").setBranchAlias("Vertex_minDistanceFromDet");
    produces<vector<float> >("dvmindfromdetx").setBranchAlias("Vertex_minDistanceFromDet_x");
    produces<vector<float> >("dvmindfromdety").setBranchAlias("Vertex_minDistanceFromDet_y");
    produces<vector<float> >("dvmindfromdetz").setBranchAlias("Vertex_minDistanceFromDet_z");
    produces<vector<float> >("dvdetxmind").setBranchAlias("Vertex_closestDet_x");
    produces<vector<float> >("dvdetymind").setBranchAlias("Vertex_closestDet_y");
    produces<vector<float> >("dvdetzmind").setBranchAlias("Vertex_closestDet_z");
}

HitMaker::~HitMaker(){
}

void HitMaker::beginJob(){}

void HitMaker::endJob(){}

void HitMaker::beginRun(const edm::Run& iRun, const edm::EventSetup& iSetup){}

std::vector<float> HitMaker::getMinDetDistance(const GeomDet *det, Local3DPoint point, GlobalPoint& retPoint){

  float mindistance=100000;
  float mindistance_x=100000;
  float mindistance_y=100000;
  float mindistance_z=100000;
  float xy[4][2];
  float dz;
  const Bounds *b = &((det->surface()).bounds());

  if (const TrapezoidalPlaneBounds *b2 = dynamic_cast<const TrapezoidalPlaneBounds *>(b)) {
    // See sec. "TrapezoidalPlaneBounds parameters" in doc/reco-geom-notes.txt
    std::array<const float, 4> const &par = b2->parameters();
    xy[0][0] = -par[0];
    xy[0][1] = -par[3];
    xy[1][0] = -par[1];
    xy[1][1] = par[3];
    xy[2][0] = par[1];
    xy[2][1] = par[3];
    xy[3][0] = par[0];
    xy[3][1] = -par[3];
    dz = par[2];
  } else if (const RectangularPlaneBounds *b2 = dynamic_cast<const RectangularPlaneBounds *>(b)) {
    // Rectangular
    float dx = b2->width() * 0.5;   // half width
    float dy = b2->length() * 0.5;  // half length
    xy[0][0] = -dx;
    xy[0][1] = -dy;
    xy[1][0] = -dx;
    xy[1][1] = dy;
    xy[2][0] = dx;
    xy[2][1] = dy;
    xy[3][0] = dx;
    xy[3][1] = -dy;
    dz = b2->thickness() * 0.5;  // half thickness
  }
  for (int i = 0; i < 4; ++i) {
    Local3DPoint lp1(xy[i][0], xy[i][1], -dz);
    Local3DPoint lp2(xy[i][0], xy[i][1], dz);
    if((point-lp1).mag()<mindistance) {mindistance=(point-lp1).mag(); mindistance_x=(point-lp1).x(); mindistance_y=(point-lp1).y(); mindistance_z=(point-lp1).z(); retPoint=det->surface().toGlobal(lp1);}
    if((point-lp2).mag()<mindistance) {mindistance=(point-lp2).mag(); mindistance_x=(point-lp2).x(); mindistance_y=(point-lp2).y(); mindistance_z=(point-lp2).z(); retPoint=det->surface().toGlobal(lp2);}
  }
  std::vector<float> mind;
  mind.push_back(mindistance);
  mind.push_back(mindistance_x);
  mind.push_back(mindistance_y);
  mind.push_back(mindistance_z);
  return mind;

}

void HitMaker::produce(edm::Event& iEvent, const edm::EventSetup& iSetup){

    bool debug = false;

    propagatorHandle_ = iSetup.getHandle(propagatorToken_);
    magfield_ = iSetup.getHandle(magFieldToken_);
    theGeo_ = iSetup.getHandle(trackingGeometryToken_);
    measurementTracker_ = iSetup.getHandle(measurementTrackerToken_);
    const TrackerTopology* const ttopo_ = &iSetup.getData(trackerTopologyToken_);

    auto const& searchGeom = *(*measurementTracker_).geometricSearchTracker();
    auto const& prop = *propagatorHandle_;

    edm::Handle<MeasurementTrackerEvent> measurementTrackerEvent;
    iEvent.getByToken(measurementTrackerEventToken_, measurementTrackerEvent);

    edm::Handle<Run3ScoutingMuonCollection> muonHandle;
    iEvent.getByToken(muonToken_, muonHandle);

    edm::Handle<Run3ScoutingVertexCollection> dvHandle;
    iEvent.getByToken(dvToken_, dvHandle);

    edm::Handle<std::vector<std::vector<int>>> vtxIndxHandle;
    iEvent.getByToken(vtxIndxToken_, vtxIndxHandle);

    if (debug) {
        std::cout << std::endl;
        std::cout << "------- Run " << iEvent.id().run() << " Lumi " << iEvent.luminosityBlock() << " Event " << iEvent.id().event() << " -------" << std::endl;
    }

    // nlohmann::json j;

    unique_ptr<vector<vector<vector<bool> > > > v_isbarrel(new vector<vector<vector<bool> > >);
    unique_ptr<vector<vector<vector<bool> > > > v_ispixel(new vector<vector<vector<bool> > >);
    unique_ptr<vector<vector<vector<bool> > > > v_isactive(new vector<vector<vector<bool> > >);
    unique_ptr<vector<vector<vector<int> > > > v_layernum(new vector<vector<vector<int> > >);
    unique_ptr<vector<vector<vector<int> > > > v_ndet(new vector<vector<vector<int> > >);
    unique_ptr<vector<vector<vector<float> > > > v_hitx(new vector<vector<vector<float> > >);
    unique_ptr<vector<vector<vector<float> > > > v_hity(new vector<vector<vector<float> > >);
    unique_ptr<vector<vector<vector<float> > > > v_hitz(new vector<vector<vector<float> > >);
    unique_ptr<vector<vector<int> > > v_nhitsbeforesv(new vector<vector<int> >);
    unique_ptr<vector<vector<int> > > v_nexpectedhits(new vector<vector<int> >);
    unique_ptr<vector<vector<int> > > v_ncompatible(new vector<vector<int> >);
    unique_ptr<vector<vector<int> > > v_nexpectedhitsmultiple(new vector<vector<int> >);
    unique_ptr<vector<vector<int> > > v_nexpectedhitstotal(new vector<vector<int> >);
    unique_ptr<vector<vector<int> > > v_ncompatibletotal(new vector<vector<int> >);
    unique_ptr<vector<vector<int> > > v_nexpectedhitsmultipletotal(new vector<vector<int> >);
    unique_ptr<vector<vector<float> > > v_pxatdv(new vector<vector<float> >);
    unique_ptr<vector<vector<float> > > v_pyatdv(new vector<vector<float> >);
    unique_ptr<vector<vector<float> > > v_pzatdv(new vector<vector<float> >);
    unique_ptr<vector<bool> > dv_onmodule(new vector<bool>);
    unique_ptr<vector<bool> > dv_onmodule_withinunc(new vector<bool>);
    unique_ptr<vector<float> > dv_mindfromdet(new vector<float>);
    unique_ptr<vector<float> > dv_mindfromdet_x(new vector<float>);
    unique_ptr<vector<float> > dv_mindfromdet_y(new vector<float>);
    unique_ptr<vector<float> > dv_mindfromdet_z(new vector<float>);
    unique_ptr<vector<float> > dv_detxmind(new vector<float>);
    unique_ptr<vector<float> > dv_detymind(new vector<float>);
    unique_ptr<vector<float> > dv_detzmind(new vector<float>);

    if(debug){
    GlobalPoint myPoint(0,0,0);
    GlobalError myErr(0.1,0,0.1,0,0,0.1);
    for (auto const& detL : searchGeom.allLayers()){
        auto const& components = detL->basicComponents();
        int ncomp=0;
        for (auto const& comp: components){
            std::cout << "component NN " << ncomp <<"/" << components.size() <<" from "<< detL->subDetector() << ", isLEAF  "<< comp->isLeaf() << std::endl;
            std::cout <<" length "<< comp->surface().bounds().length() << " width "<< comp->surface().bounds().width() << " thickness " << comp->surface().bounds().thickness() << std::endl;
            ncomp++;
            if(!comp->isLeaf()){
              std::cout << " subcomp --- " << comp->components().size() << std::endl;
              for (auto const& subcomp: comp->components()){
                  std::cout << "subLEAF "<<subcomp->isLeaf() << std::endl;
                  std::cout <<" length "<< subcomp->surface().bounds().length() << " width "<< subcomp->surface().bounds().width() << " thickness " << subcomp->surface().bounds().thickness() << std::endl;
                  Local3DPoint myLocalPoint = subcomp->surface().toLocal(myPoint);
                  std::cout << " L_x " << myLocalPoint.x() << " L_y " << myLocalPoint.y() << " L_z "<< myLocalPoint.z() << std::endl;             
                  std::cout << " 0_x " << subcomp->position().x() << " 0_y " << subcomp->position().y() << " 0_z "<< subcomp->position().z() << std::endl;
                  std::cout << " inside " << subcomp->surface().bounds().inside(myLocalPoint)<< std::endl;              
              }
            }
            else{
 
                Local3DPoint myLocalPoint = comp->surface().toLocal(myPoint);
                LocalError myLocalErr = ErrorFrameTransformer().transform( myErr, comp->surface());
                std::cout << " L_x " << myLocalPoint.x() << " L_y " << myLocalPoint.y() << " L_z "<< myLocalPoint.z() << std::endl;
                std::cout << " 0_x " << comp->position().x() << " 0_y " << comp->position().y() << " 0_z "<< comp->position().z() << std::endl;
                std::cout << " inside " << comp->surface().bounds().inside(myLocalPoint)<< std::endl;
                GlobalPoint refCenterG(comp->position().x(),comp->position().y(),comp->position().z());
                Local3DPoint refCenterGL = comp->surface().toLocal(refCenterG);
                std::cout << " L_x " << refCenterGL.x() << " L_y " << refCenterGL.y() << " L_z "<< refCenterGL.z() << std::endl;
                std::cout << " inside GL " << comp->surface().bounds().inside(refCenterGL)<< std::endl;
                std::cout << " inside GLE " << comp->surface().bounds().inside(refCenterGL,myLocalErr)<< std::endl;
            }
         }
    }
    }
    
    for (auto const& vertex : *dvHandle) {
        bool vertex_onmodule = false;
        bool vertex_onmodule_withinunc = false;
        GlobalPoint closestDetV(0,0,0);
        float mindistance=10E6;
        float mindistance_x=10E6;
        float mindistance_y=10E6;
        float mindistance_z=10E6;
        GlobalPoint myPoint(vertex.x(),vertex.y(),vertex.z());
        GlobalError myErr(vertex.xError(),0,vertex.yError(),0,0,vertex.zError()); // cov missing
        for (auto const& detL : searchGeom.allLayers()){
            auto const& components = detL->basicComponents();
            for (auto const& comp: components){
                if(!comp->isLeaf()){
                   for (auto const& subcomp: comp->components()){ 
                       // not going further down beacause this level should be enough to separate all components (check above)
                       Local3DPoint myLocalPoint = subcomp->surface().toLocal(myPoint);
                       LocalError myLocalErr = ErrorFrameTransformer().transform( myErr, subcomp->surface());
                       vertex_onmodule=subcomp->surface().bounds().inside(myLocalPoint);
                       vertex_onmodule_withinunc=subcomp->surface().bounds().inside(myLocalPoint,myLocalErr);
                       GlobalPoint retPoint(0,0,0);
                       std::vector<float> mindist_temp=getMinDetDistance(subcomp, myLocalPoint, retPoint);
                       if(mindist_temp[0]<mindistance){mindistance=mindist_temp[0]; mindistance_x=mindist_temp[1]; mindistance_y=mindist_temp[2]; mindistance_z=mindist_temp[3]; closestDetV=retPoint;}
                   }
                }
                else{
                   Local3DPoint myLocalPoint = comp->surface().toLocal(myPoint);
                   LocalError myLocalErr = ErrorFrameTransformer().transform( myErr, comp->surface());
                   vertex_onmodule=comp->surface().bounds().inside(myLocalPoint);
                   vertex_onmodule_withinunc=comp->surface().bounds().inside(myLocalPoint,myLocalErr);
                   GlobalPoint retPoint(0,0,0);
                   std::vector<float> mindist_temp=getMinDetDistance(comp, myLocalPoint, retPoint);
                   if(mindist_temp[0]<mindistance){mindistance=mindist_temp[0]; mindistance_x=mindist_temp[1]; mindistance_y=mindist_temp[2]; mindistance_z=mindist_temp[3]; closestDetV=retPoint;}
                }
            }
            if(vertex_onmodule && vertex_onmodule_withinunc) break;     
        }
        dv_onmodule->push_back(vertex_onmodule);
        dv_onmodule_withinunc->push_back(vertex_onmodule_withinunc);
        dv_mindfromdet->push_back(mindistance);
        dv_mindfromdet_x->push_back(mindistance_x);
        dv_mindfromdet_y->push_back(mindistance_y);
        dv_mindfromdet_z->push_back(mindistance_z);
        dv_detxmind->push_back(closestDetV.x());
        dv_detymind->push_back(closestDetV.y());
        dv_detzmind->push_back(closestDetV.z());
        if (debug){
            std::cout << " -- " << myPoint.x() << "  -- "<< myPoint.y() << " -- " << myPoint.z() << std::endl;
            std::cout << " -- " << vertex_onmodule << " -- " << mindistance << std::endl;
            std::cout << " -- " << closestDetV.x() << " -- " << closestDetV.y() <<" -- " << closestDetV.z() << std::endl;
        }
    }
   
    for (unsigned int imu = 0; imu < muonHandle->size(); ++imu) {
        auto const& muon = (*muonHandle)[imu];

	vector<int> dv_nhitsbeforesv;
	vector<vector<bool>> dv_isbarrel;
	vector<vector<bool>> dv_ispixel;
	vector<vector<bool>> dv_isactive;
	vector<vector<int>> dv_layernum;
	vector<vector<int>> dv_ndet;
	vector<vector<float>> dv_hitx;
	vector<vector<float>> dv_hity;
	vector<vector<float>> dv_hitz;
    vector<int> dv_nexpectedhits;
	vector<int> dv_ncompatible;
	vector<int> dv_nexpectedhitsmultiple;
	vector<int> dv_nexpectedhitstotal;
	vector<int> dv_ncompatibletotal;
	vector<int> dv_nexpectedhitsmultipletotal;
	vector<float> dv_pxatdv;
	vector<float> dv_pyatdv;
	vector<float> dv_pzatdv;

        TLorentzVector lv;
        lv.SetPtEtaPhiM(muon.pt(), muon.eta(), muon.phi(), 0.10566);

        // Muon track
        float track_px = lv.Px();
        float track_py = lv.Py();
        float track_pz = lv.Pz();
        float track_phi = muon.trk_phi();
        float track_dz = muon.trk_dz();
        float track_dxy = muon.trk_dxy();
        float track_dsz = muon.trk_dsz();
        float track_lambda = muon.trk_lambda();
        float track_qoverpError = muon.trk_qoverpError();
        float track_lambdaError = muon.trk_lambdaError();
        float track_phiError = muon.trk_phiError();
        float track_dxyError = muon.trk_dxyError();
        float track_dszError = muon.trk_dszError();
        int track_charge = muon.charge();
        int nvalidpixelhits = muon.nValidPixelHits();

        /* Compute track reference point position. This is where the momentum is reported.
         * Invert this to solve:
         * / dxy \   / -sin(phi)              cos(phi)              0           \ / vx \
         * | dsz | = | -cos(phi)*sin(lambda)  -sin(phi)*sin(lambda) cos(lambda) | | vy |
         * \  dz /   \ 0                      0                     1           / \ vz /
         * Based on DataFormats/TrackReco/interface/TrackBase.h
         */
        float sinphi = sin(track_phi);
        float cosphi = cos(track_phi);
        float sinlmb = sin(track_lambda);
        float coslmb = cos(track_lambda);
        float tanlmb = sinlmb/coslmb;
        float track_vz = track_dz;
        float track_vx = -sinphi*track_dxy - (cosphi/sinlmb)*track_dsz + (cosphi/tanlmb)*track_vz;
        float track_vy =  cosphi*track_dxy - (sinphi/sinlmb)*track_dsz + (sinphi/tanlmb)*track_vz;

        // Covariance matrix
        reco::TrackBase::CovarianceMatrix track_cov;
        track_cov(0,0) = pow(track_qoverpError,2);
        track_cov(1,1) = pow(track_lambdaError,2);
        track_cov(2,2) = pow(track_phiError,2);
        track_cov(3,3) = pow(track_dxyError,2);
        track_cov(4,4) = pow(track_dszError,2);

        CurvilinearTrajectoryError err(track_cov);
        // Loop over the vertices
        vector<int> vertex_indices = vtxIndxHandle.isValid() ? (*vtxIndxHandle)[imu] : muon.vtxIndx();
        for (auto idx : vertex_indices) {
            if (!(idx >= 0 && idx < (int)(*dvHandle).size())) 
                continue;
        
	    Run3ScoutingVertex dv = (*dvHandle).at(idx);

	    //float chi2_=dv.chi2();
	    //int ndof_=dv.ndof();
	    //float prob_ = TMath::Prob(chi2_,ndof_);
	    float dv_x = dv.x();
	    float dv_y = dv.y();
	    float dv_z = dv.z();

	    // Is track reference point inside a cylinder with the DV? This should always be true from what I've seen.
	    bool track_ref_inside_dv = (track_vx*track_vx+track_vy*track_vy) < (dv_x*dv_x+dv_y*dv_y);

	    // Get the hit pattern of the muon and count the number of hits in a cylinder with the DV
	    int nhitsbeforesv = 0; // counter
	    Run3ScoutingHitPatternPOD hitPattern = muon.trk_hitPattern();
	    reco::HitPattern theHitPattern(hitPattern);
	    const TrackingGeometry::DetContainer& dets = theGeo_->dets();
	    for (int i = 0; i < theHitPattern.numberOfAllHits(reco::HitPattern::TRACK_HITS); i++) {
	      uint16_t hit = theHitPattern.getHitPattern(reco::HitPattern::TRACK_HITS, i);
	      if (!theHitPattern.validHitFilter(hit))
		continue;
	      uint16_t subDet = theHitPattern.getSubStructure(hit);
	      uint16_t layer = theHitPattern.getLayer(hit);
	      std::pair<uint16_t, uint16_t> detInfo(subDet, layer);
	      for (unsigned int i = 0; i < dets.size(); i++) {
		auto detId = dets[i]->geographicalId();
		if (subDet==detId.subdetId() && layer==ttopo_->layer(detId)) {
		  if(subDet==1 || subDet==3 || subDet==5) {
		    if ((dets[i]->position().perp()*dets[i]->position().perp()) < (dv_x*dv_x+dv_y*dv_y)) {
		      //std::cout << "subDet: " << subDet << ", Rho: " << dets[i]->position().perp() << std::endl; 
		      nhitsbeforesv++;
		    }
		  } else {
		    if (std::abs(dets[i]->position().z()) < std::abs(dv_z)) {
		      //std::cout << "subDet: " << subDet << ", Z: " << dets[i]->position().z() << std::endl; 
		      nhitsbeforesv++;
		    }
		  }
		  break;
		}
	      }
	    }
	    dv_nhitsbeforesv.push_back(nhitsbeforesv);
	    //std::cout << "Number of hits: " << nhitsbeforesv << "\t, and pt: " << muon.pt() << std::endl;

	    if (debug) {
		std::cout << "=== Muon "
		    << " nDV=" << vertex_indices.size()
		    << " (pt,eta,phi)=(" << muon.pt() << "," << muon.eta() << "," << muon.phi() << ")"
		    << " (px,py,pz)=(" << track_px << "," << track_py << "," << track_pz << ")"
		    << " (dvx,dvy,dvz)=(" << dv_x << "," << dv_y << "," << dv_z << ")"
		    << " (tvx,tvy,tvz)=(" << track_vx << "," << track_vy << "," << track_vz << ")"
		    << " trkindv=" << track_ref_inside_dv
		    << " q=" << track_charge
		    << " nvalid=" << nvalidpixelhits
		    << std::endl;

		// j["event"] = iEvent.id().event();
		// j["nMuon"] = (*muonHandle).size();
		// j["nDV"] = (*dvHandle).size();
		// j["Muon_pt"] = muon.pt();
		// j["Muon_eta"] = muon.eta();
		// j["Muon_phi"] = muon.phi();
		// j["Muon_px"] = track_px;
		// j["Muon_py"] = track_py;
		// j["Muon_pz"] = track_pz;
		// j["Muon_nDV"] = vertex_indices.size();
		// j["Muon_dvx"] = dv_x;
		// j["Muon_dvy"] = dv_y;
		// j["Muon_dvz"] = dv_z;
		// j["Muon_tvx"] = track_vx;
		// j["Muon_tvy"] = track_vy;
		// j["Muon_tvz"] = track_vz;
		// j["Muon_trkindv"] = track_ref_inside_dv;
		// j["Muon_charge"] = track_charge;
		// j["Muon_nvalid"] = nvalidpixelhits;
	    }

	    // Default parameters according to https://github.com/cms-sw/cmssw/blob/master/TrackingTools/KalmanUpdators/interface/Chi2MeasurementEstimatorParams.h
	    Chi2MeasurementEstimator estimator(30., 3., 0.5, 2.0, 0.5, 1.e12);

	    GlobalVector startingMomentum(track_px, track_py, track_pz);
	    GlobalPoint startingPosition;
	    if (track_ref_inside_dv) {
		startingPosition = GlobalPoint(track_vx, track_vy, track_vz);
	    } else {
		// If the ref point is outside the DV cylinder (due to rounding issues or DV not corresponding to the right muon), just use the DV cylinder
		startingPosition = GlobalPoint(dv_x, dv_y, dv_z);
	    }

	    PlaneBuilder pb;
	    auto startingPlane = pb.plane(startingPosition, rotation(startingMomentum));

	    TrajectoryStateOnSurface startingStateP(
		    GlobalTrajectoryParameters(startingPosition, startingMomentum, track_charge, magfield_.product()),
		    err, *startingPlane
		    );

	    // float cylx = dv_x;
	    // float cyly = dv_y;
	    // float cylz = dv_z;

	    if (track_ref_inside_dv) {
		float dv_rho = sqrt(dv_x*dv_x+dv_y*dv_y);
		if (debug) {
		    std::cout << "   Before propagating trk ref to DV cyl POS/MOM: " << startingStateP.globalPosition() << "/" << startingStateP.globalMomentum() << std::endl;
		}
		// https://github.com/cms-sw/cmssw/blob/949a7b9d2c1bfde1458e01da1c14da0cd53a0ccf/HLTriggerOffline/Muon/src/PropagateToMuon.cc#L159
		// https://github.com/cms-sw/cmssw/blob/c9b012f3388a39f64eb05980e3732d0484539f14/DataFormats/GeometrySurface/interface/Cylinder.h
		double valid_distance = prop.propagateWithPath(startingStateP, Cylinder(dv_rho)).second;
		if(valid_distance<=0)  //rarely (test 24 muons in 105181 evts, 5893 passing filters) the propagation seems to give seg faults
				       //since this is very rare (0.2% of muons, assuming 2 per evt) I just check the distance and use dummy values 
		{
		    if (debug) std::cout << "UNSUCCESFUL propagation to the starting point" << std::endl;
		    dv_isbarrel.push_back(vector<bool>());
		    dv_ispixel.push_back(vector<bool>());
		    dv_isactive.push_back(vector<bool>());
		    dv_layernum.push_back(vector<int>());
		    dv_ndet.push_back(vector<int>());
		    dv_hitx.push_back(vector<float>());
		    dv_hity.push_back(vector<float>());
		    dv_hitz.push_back(vector<float>());
		    dv_nexpectedhits.push_back(-1);
		    dv_ncompatible.push_back(-1);
		    dv_nexpectedhitsmultiple.push_back(-1);
		    dv_nexpectedhitstotal.push_back(-1);
		    dv_ncompatibletotal.push_back(-1);
		    dv_nexpectedhitsmultipletotal.push_back(-1);
		    dv_pxatdv.push_back(0);
		    dv_pyatdv.push_back(0);
		    dv_pzatdv.push_back(0);
		    continue;//skip the rest for the given vertex, it should happend very rarely
		}

		startingStateP = prop.propagate(startingStateP, Cylinder(dv_rho));
		// cylx = startingStateP.globalPosition().x();
		// cyly = startingStateP.globalPosition().y();
		// cylz = startingStateP.globalPosition().z();
		if (debug) {
		    std::cout << "   After propagating trk ref to DV cyl POS/MOM: " << startingStateP.globalPosition() << "/" << startingStateP.globalMomentum() << std::endl;
		    // j["Muon_dvcylx"] = cylx;
		    // j["Muon_dvcyly"] = cyly;
		    // j["Muon_dvcylz"] = cylz;
		}
	    }

	    float pxatdv = startingStateP.globalMomentum().x();
	    float pyatdv = startingStateP.globalMomentum().y();
	    float pzatdv = startingStateP.globalMomentum().z();

	    // or could get searchGeom.allLayers() and require layer->subDetector() enum is PixelBarrel/PixelEndcap 
	    //vector<DetLayer const*> layers_pixel;
	    //for (auto layer : searchGeom.pixelBarrelLayers()) layers_pixel.push_back(layer);
	    //for (auto layer : searchGeom.negPixelForwardLayers()) layers_pixel.push_back(layer);
	    //for (auto layer : searchGeom.posPixelForwardLayers()) layers_pixel.push_back(layer);
	    vector<bool> isbarrel;
	    vector<bool> ispixel;
	    vector<bool> isactive;
	    vector<int> layernum;
	    vector<int> ndet;
	    vector<float> hitx;
	    vector<float> hity;
	    vector<float> hitz;
	    int nexpectedhits = 0;
	    int nexpectedhitsmultiple = 0;
	    int nexpectedhitsmultipleraw = 0;
	    int nexpectedhitstotal = 0;
	    int nexpectedhitsmultipletotal = 0;
	    auto tsos = startingStateP;
	    int ncompatible = 0;
	    int ncompatibletotal = 0;
	    for (auto const& layer : searchGeom.allLayers()) {
		if(debug) std::cout << (int)layer->subDetector() << " " << layer->subDetector() << " layers subdet" << std::endl;
		bool pixel=((int)layer->subDetector())<2; // pixel barrel = 0, endcap = 1
		bool compatible = layer->compatible(tsos, prop, estimator).first;
		if (debug) std::cout << "compatible=" << compatible << std::endl;
		if (pixel) ncompatible += compatible;
		ncompatibletotal += compatible;
		// auto tsos = startingStateP;
		// /cvmfs/cms.cern.ch/slc6_amd64_gcc700/cms/cmssw/CMSSW_10_2_5/src/TrackingTools/DetLayers/src/BarrelDetLayer.cc
		auto const& detWithState = layer->compatibleDets(tsos, prop, estimator);
		if (debug) std::cout << "detWithState.size()=" << detWithState.size() << std::endl;
		if (!detWithState.size()) continue;
		tsos = detWithState.front().second;
		DetId did = detWithState.front().first->geographicalId();
		MeasurementDetWithData measDet = measurementTracker_->idToDet(did, *measurementTrackerEvent);
		bool active = measDet.isActive() && measDet.isValid(); // From what I see, isValid is always true, but just be safe.
		bool barrel = layer->isBarrel();
		int seq = layer->seqNum();
		int sdet = detWithState.size();
		auto pos = tsos.globalPosition();
		if (debug) {
		    std::cout << "HIT subdet=" << layer->subDetector()
			<< " layer=" << seq 
			<< " detSize=" << sdet
			<< " pos=" << pos
			<< " active=" << active 
			<< std::endl;
		}
		for (auto ds : detWithState) {
		    auto did2 = ds.first->geographicalId();
		    auto md = measurementTracker_->idToDet(did2, *measurementTrackerEvent);
		    if (debug) std::cout << "   subhit active=" << md.isActive() << " valid=" << md.isValid() << std::endl;
		    if (pixel) nexpectedhitsmultiple += md.isActive()*md.isValid();
		    nexpectedhitsmultipletotal += md.isActive()*md.isValid();
		    nexpectedhitsmultipleraw += 1;
		}
		isbarrel.push_back(barrel);
		ispixel.push_back(pixel);
		isactive.push_back(active);
		layernum.push_back(seq);
		ndet.push_back(sdet);
		hitx.push_back(pos.x());
		hity.push_back(pos.y());
		hitz.push_back(pos.z());
		if (pixel) nexpectedhits += active;
		nexpectedhitstotal += active;
	    }
	    dv_isbarrel.push_back(isbarrel);
	    dv_ispixel.push_back(ispixel);
	    dv_isactive.push_back(isactive);
	    dv_layernum.push_back(layernum);
	    dv_ndet.push_back(ndet);
	    dv_hitx.push_back(hitx);
	    dv_hity.push_back(hity);
	    dv_hitz.push_back(hitz);
	    dv_nexpectedhits.push_back(nexpectedhits);
	    dv_ncompatible.push_back(ncompatible);
	    dv_nexpectedhitsmultiple.push_back(nexpectedhitsmultiple);
	    dv_nexpectedhitstotal.push_back(nexpectedhitstotal);
	    dv_ncompatibletotal.push_back(ncompatibletotal);
	    dv_nexpectedhitsmultipletotal.push_back(nexpectedhitsmultipletotal);
	    dv_pxatdv.push_back(pxatdv);
	    dv_pyatdv.push_back(pyatdv);
	    dv_pzatdv.push_back(pzatdv);

	    if (debug) {
		std::cout <<  " valid: " << nvalidpixelhits <<  " exp: " << nexpectedhits <<  " expmultiple: " << nexpectedhitsmultiple 
			  <<  " valid-exp: " << nvalidpixelhits-nexpectedhits <<  " valid-expmultiple: " << nvalidpixelhits-nexpectedhitsmultiple <<  std::endl;
		// j["Muon_expected"] = nexpectedhits;
		// j["Muon_expectedmultiple"] = nexpectedhitsmultiple;
		// j["Muon_expectedmultipleraw"] = nexpectedhitsmultipleraw;

	    }

        }
	v_isbarrel->push_back(dv_isbarrel);
	v_ispixel->push_back(dv_ispixel);
	v_isactive->push_back(dv_isactive);
	v_layernum->push_back(dv_layernum);
	v_ndet->push_back(dv_ndet);
	v_hitx->push_back(dv_hitx);
	v_hity->push_back(dv_hity);
	v_hitz->push_back(dv_hitz);
        v_nhitsbeforesv->push_back(dv_nhitsbeforesv);
	v_nexpectedhits->push_back(dv_nexpectedhits);
	v_ncompatible->push_back(dv_ncompatible);
	v_nexpectedhitsmultiple->push_back(dv_nexpectedhitsmultiple);
	v_nexpectedhitstotal->push_back(dv_nexpectedhitstotal);
	v_ncompatibletotal->push_back(dv_ncompatibletotal);
	v_nexpectedhitsmultipletotal->push_back(dv_nexpectedhitsmultipletotal);
	v_pxatdv->push_back(dv_pxatdv);
	v_pyatdv->push_back(dv_pyatdv);
	v_pzatdv->push_back(dv_pzatdv);
        if (debug) {
            // std::cout << "JSON: " << j.dump(-1) << std::endl;
        }
    }

    iEvent.put(std::move(v_isbarrel), "isbarrel");
    iEvent.put(std::move(v_ispixel), "ispixel");
    iEvent.put(std::move(v_isactive), "isactive");
    iEvent.put(std::move(v_layernum), "layernum");
    iEvent.put(std::move(v_ndet), "ndet");
    iEvent.put(std::move(v_hitx), "x");
    iEvent.put(std::move(v_hity), "y");
    iEvent.put(std::move(v_hitz), "z");
    iEvent.put(std::move(v_nhitsbeforesv), "nhitsbeforesv");
    iEvent.put(std::move(v_nexpectedhits), "nexpectedhits");
    iEvent.put(std::move(v_ncompatible), "ncompatible");
    iEvent.put(std::move(v_nexpectedhitsmultiple), "nexpectedhitsmultiple");
    iEvent.put(std::move(v_nexpectedhitstotal), "nexpectedhitstotal");
    iEvent.put(std::move(v_ncompatibletotal), "ncompatibletotal");
    iEvent.put(std::move(v_nexpectedhitsmultipletotal), "nexpectedhitsmultipletotal");
    iEvent.put(std::move(v_pxatdv), "pxatdv");
    iEvent.put(std::move(v_pyatdv), "pyatdv");
    iEvent.put(std::move(v_pzatdv), "pzatdv");
    iEvent.put(std::move(dv_onmodule), "dvonmodule");
    iEvent.put(std::move(dv_onmodule_withinunc), "dvonmodulewithinunc");
    iEvent.put(std::move(dv_mindfromdet), "dvmindfromdet");
    iEvent.put(std::move(dv_mindfromdet_x), "dvmindfromdetx");
    iEvent.put(std::move(dv_mindfromdet_y), "dvmindfromdety");
    iEvent.put(std::move(dv_mindfromdet_z), "dvmindfromdetz");
    iEvent.put(std::move(dv_detxmind), "dvdetxmind");
    iEvent.put(std::move(dv_detymind), "dvdetymind");
    iEvent.put(std::move(dv_detzmind), "dvdetzmind");
}

DEFINE_FWK_MODULE(HitMaker);
