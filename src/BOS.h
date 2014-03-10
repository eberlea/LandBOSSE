//
//  BOS.h
//  LandBOS
//
//  Created by Andrew Ning on 3/10/14.
//  Copyright (c) 2014 NREL. All rights reserved.
//

#ifndef __LandBOS__BOS__
#define __LandBOS__BOS__

//#include <iostream>

#endif /* defined(__LandBOS__BOS__) */


enum SiteTerrain {FLAT_TO_ROLLING, RIDGE_TOP, MOUNTAINOUS};
enum TurbineLayout {SIMPLE, COMPLEX};
enum SoilCondition {STANDARD, BOUYANT};

class BOS {
    double rating;  // machine rating (kW)
    double diameter;  // rotor diameter (m)
    double hubHt;  // hub height (m)
    int nTurb;  // number of turbines
    double voltage;  // interconnect voltage (kV)
    double distInter;  // distance to interconnect (mi)
    SiteTerrain terrain;
    TurbineLayout layout;
    SoilCondition soil;

    double tcc;  // Turbine Capital Cost ($/kW)
    double topMass;  // Tower Top Mass (Tonnes)
    
    double farmSize;  // wind farm size (MW)
    
    
public:
    
    BOS(double machineRating, double rotorDiameter, double hubHeight, int nTurbines,
        double interconnectVoltage, double distToInterconnect,
        double turbineCapitalCosts, double towerTopMass,
        SiteTerrain terrain, TurbineLayout layout, SoilCondition soil);
    
    // transportation costs
    double transportationCost(double transportationDistance) const;
    
    // engineering costs
    double engineeringCost() const;
    
    // met masts and power performance costs
    double powerPerformanceCost() const;
    
    // access roads and site improvement costs
    double roadsCost() const;
    
    // site compound and security costs
    double siteCompoundCost() const;
    double siteCompoundCost(int accessRoadEntrances, int constructionTime) const;

    // control O&M building costs
    double buildingCost() const;
    double buildingCost(double buildingSize) const;
    
};
