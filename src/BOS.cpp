//
//  BOS.cpp
//  LandBOS
//
//  Created by Andrew Ning on 3/10/14.
//  Copyright (c) 2014 NREL. All rights reserved.
//

#include "BOS.h"
#include <math.h>


BOS::BOS(double machineRating, double rotorDiameter, double hubHeight,
         int nTurbines, double interconnectVoltage, double distToInterconnect,
         double turbineCapitalCosts, double towerTopMass,
         SiteTerrain siteTerrain, TurbineLayout turbineLayout,
         SoilCondition soilCondition){

    rating = machineRating;
    diameter = rotorDiameter;
    hubHt = hubHeight;
    nTurb = nTurbines;
    voltage = interconnectVoltage;
    distInter = distToInterconnect;
    tcc = turbineCapitalCosts;
    topMass = towerTopMass;
    terrain = siteTerrain;
    layout = turbineLayout;
    soil = soilCondition;
    
    farmSize = rating * nTurb / 1000.0;

}



double BOS::transportationCost(double transportationDistance) const{
    
    double cost = tcc * rating * nTurb;
    
    if (rating < 2500 && hubHt < 100) {
        cost += 1349*pow(transportationDistance, 0.746) * nTurb;
    } else {
        cost += 1867*pow(transportationDistance, 0.726) * nTurb;
    }
    
    return cost;
}


double BOS::engineeringCost() const{
    
    double cost = 7188.5 * nTurb;
    
    cost += round(3.4893*log(nTurb)-7.3049);
    
    double multiplier = 1.0;
    if (farmSize > 200) multiplier = 2.0;
    cost += multiplier * 161675;
    
    cost += 4000;
    
    return cost;
}


double BOS::powerPerformanceCost() const{
    
    int permanent;
    if (farmSize < 100){
        permanent = 1;
    } else if (farmSize < 200){
        permanent = 2;
    } else{
        permanent = int(farmSize/100.0);
    }
    
    int temporary = round(farmSize/75.0);
    
    double multiplier1 = 290000;
    double multiplier2 = 116800;
    if (hubHt < 90) {
        multiplier1 = 232600;
        multiplier2 = 92600;
    }

    double cost = 200000 + permanent*multiplier1 + temporary*multiplier2;

    return cost;    
}


double BOS::roadsCost() const{
    
    double cost = 0.0;
    
    if (layout == SIMPLE){
        if (terrain == FLAT_TO_ROLLING){
            cost = 6671648;
        } else if (terrain == RIDGE_TOP){
            cost = 7729995;
        } else if (terrain == MOUNTAINOUS){
            cost = 8412705;
        }
    
    } else if (layout == COMPLEX){
        if (terrain == FLAT_TO_ROLLING){
            cost = 8074668;
        } else if (terrain == RIDGE_TOP){
            cost = 9312692;
        } else if (terrain == MOUNTAINOUS){
            cost = 10224911;
        }
    }

    return cost;
}


double BOS::siteCompoundCost() const{
 
    int accessRoadEntrances = fmax(1, round(nTurb/20.0));
    
    int constructionTime = round(0.0001*nTurb*nTurb + 0.0963*nTurb + 2.7432);
    
    return siteCompoundCost(accessRoadEntrances, constructionTime);
    
}


double BOS::siteCompoundCost(int accessRoadEntrances, int constructionTime) const{
    
    
    double cost = 9825.0*accessRoadEntrances + 29850.0*constructionTime;
    
    double multiplier;
    if (farmSize > 100){
        multiplier = 10.0;
    } else if (farmSize > 30){
        multiplier = 5.0;
    } else{
        multiplier = 3.0;
    }
    
    cost += multiplier * 30000;
    
    
    if (farmSize > 30){
        cost += 90000;
    }
    
    cost += farmSize*60 + 62400;
    
    return cost;
}


double BOS::buildingCost() const{
    
    double buildingSize;
    if (farmSize < 200){
        buildingSize = 3000;
    } else if (farmSize < 500){
        buildingSize = 5000;
    } else if (farmSize < 800){
        buildingSize = 7000;
    } else if (farmSize < 1000){
        buildingSize = 9000;
    } else{
        buildingSize = 12000;
    }
    
    return buildingCost(buildingSize);
}


double BOS::buildingCost(double buildingSize) const{
    
    double cost = buildingSize*125 + 176125;
    
    return cost;
    
}