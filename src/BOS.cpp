//
//  BOS.cpp
//  LandBOS
//
//  Created by Andrew Ning on 3/10/14.
//  Copyright (c) 2014 NREL. All rights reserved.
//

#include "BOS.h"


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

    // --- set default values that can be overridden ---

    // Construction Time (months)
    constructionTime = round(0.0001*nTurb*nTurb + 0.0963*nTurb + 2.7432);

    // Access road entrances
    accessRoadEntrances = fmax(1, round(nTurb/20.0));

    // O&M Building Size (ft2)
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

    // Quantity of Temporary Meteorological Towers for Testing
    temporary = round(farmSize/75.0);

    // Quantity of Permanent Meteorological Towers for Testing
    if (farmSize < 100){
        permanent = 1;
    } else if (farmSize < 200){
        permanent = 2;
    } else{
        permanent = int(farmSize/100.0);
    }

    // Wind/Weather delay days
    weatherDelayDays = round(nTurb/5.0);

    // Crane breakdowns
    craneBreakdowns = round(nTurb/20.0);

    // ---------------------------------


}


void BOS::setConstructionTime(int months){
    constructionTime = months;
}

void BOS::setAccessRoadEntrances(int number){
    accessRoadEntrances = number;
}

void BOS::setBuildingSize(double sqft){
    buildingSize = sqft;
}

void BOS::setTempTowers(double towers){
    temporary = towers;
}

void BOS::setPermanentTowers(double towers){
    permanent = towers;
}

void BOS::setWeatherDelays(int days){
    weatherDelayDays = days;
}

void BOS::setCraneBreakdowns(int number){
    craneBreakdowns = number;
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

    double cost = buildingSize*125 + 176125;

    return cost;

}

double BOS::foundationCost() const{

    double cost = rating*diameter*topMass/1000.0
        + 163421.5*pow(nTurb, 0.1458) + (hubHt-80)*500;

    if (soil == BOUYANT){
        cost += 20000;
    }

    cost *= nTurb;

    return cost;
}


double BOS::erectionCosts(bool deliveryAssistRequired) const{

    double cost = (37*rating + 27000*pow(nTurb, -0.42145) + (hubHt-80)*500)*nTurb;

    if (deliveryAssistRequired){
        cost += 60000*nTurb;
    }

    cost += 20000*weatherDelayDays + 35000*craneBreakdowns + 181*nTurb + 1834;

    return cost;
}


double BOS::electricalMaterialsCost() const{

    double cost = 0.0;

    if (layout == SIMPLE){
        if (terrain == FLAT_TO_ROLLING){
            cost = 13097685;
        } else if (terrain == RIDGE_TOP){
            cost = 13675685;
        } else if (terrain == MOUNTAINOUS){
            cost = 13712382;
        }

    } else if (layout == COMPLEX){
        if (terrain == FLAT_TO_ROLLING){
            cost = 14675585;
        } else if (terrain == RIDGE_TOP){
            cost = 15254685;
        } else if (terrain == MOUNTAINOUS){
            cost = 15372585;
        }
    }

    return cost;
}


double BOS::electricalInstallationCost() const{

    double cost = 0.0;

    if (layout == SIMPLE){
        if (terrain == FLAT_TO_ROLLING){
            cost = 5193910;
        } else if (terrain == RIDGE_TOP){
            cost = 7791830;
        } else if (terrain == MOUNTAINOUS){
            cost = 9260880;
        }

    } else if (layout == COMPLEX){
        if (terrain == FLAT_TO_ROLLING){
            cost = 7757730;
        } else if (terrain == RIDGE_TOP){
            cost = 11434480;
        } else if (terrain == MOUNTAINOUS){
            cost = 12780880;
        }
    }

    return cost;
}


double BOS::substationCost() const{

    double cost = 11652*(voltage+farmSize) + 11795*pow(farmSize, 0.3549) + 1526800;

    return cost;
}


double BOS::transmissionCost(bool newSwitchyardRequired) const{

    double cost = 0.0;

    if (distInter != 0){
        cost = (1176*voltage + 218257)*pow(distInter, 0.8937);
    }

    if (newSwitchyardRequired){
        cost += 18115*voltage + 165944;
    }

    return cost;
}


double BOS::constructionMgmtCost() const{

    double cost = round(0.0001*nTurb*nTurb + 0.0963*nTurb + 2.7432);

    return cost;
}


double BOS::projectMgmtCost(int constructionTime) const{

    double cost;
    if (constructionTime < 28){
        cost = (53.333*constructionTime*constructionTime - 3442*constructionTime
            + 209542)*(constructionTime + 2);
    } else{
        cost = (constructionTime + 2)*155000;
    }

    return cost;
}


double BOS::developmentCost(double developmentFee) const{

    return developmentFee*1000000;
}


std::pair<double, double> BOS::insuranceMultiplierAndCosts(double foundationCost,
    bool performanceBond) const{

    double alpha = 3.5 + 0.7 + 0.4 + 1.0;
    double cost = (0.7 + 0.4 + 1.0) * tcc * farmSize;

    if (performanceBond){
        alpha += 10.0;
        cost += 10.0 * tcc * farmSize;
    }

    alpha /= 1000.0;
    cost += 0.02*foundationCost + 20000;

    double multiplier = 1.0/(1-alpha);

    return std::make_pair(multiplier, cost);
}

//double BOS::insuranceMultiplier(bool performanceBond) const{
//
//    double alpha = 3.5 + 0.7 + 0.4 + 1.0;
//
//    if (performanceBond){
//        alpha += 10.0;
//    }
//
//    alpha /= 1000.0;
//
//    double multiplier = 1.0/(1-alpha);
//
//    return multiplier;
//}
//
//double BOS::insuranceFixedCosts(double foundationCost, bool performanceBond) const{
//
//    double cost = (0.7 + 0.4 + 1.0) * tcc * farmSize;
//
//    if (performanceBond){
//        cost += 10.0 * tcc * farmSize;
//    }
//
//    cost += 0.02*foundationCost + 20000;
//
//    return cost;
//}

std::pair<double, double> BOS::markupMultiplierAndCosts(double transportationCost,
    double contingency, double warranty, double useTax, double overhead,
    double profitMargin) const{

    double alpha = (contingency + warranty + useTax + overhead + profitMargin)/100.0;

    double cost = -alpha * transportationCost;

    double multiplier = 1.0/(1-alpha);

    return std::make_pair(multiplier, cost);
}