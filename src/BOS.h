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

    // --- values that can be overridden ---
    // Note: some values that are really integer values are defined here as doubles so
    //       that they can be overriden with continuous values for the "smooth"
    //       version of this code.

    int constructionTime;  // Construction Time (months)
    double buildingSize;  // O&M Building Size (ft2)
    double temporary;  // Quantity of Temporary Meteorological Towers for Testing
    double permanent;  // Quantity of Permanent Meteorological Towers for Testing
    int weatherDelayDays;  // Wind/Weather delay days
    int craneBreakdowns;  // Crane breakdowns
    int accessRoadEntrances;  // Access road entrances


    // ---------------------------------


public:

    // constructor
    BOS(double machineRating, double rotorDiameter, double hubHeight, int nTurbines,
        double interconnectVoltage, double distToInterconnect,
        double turbineCapitalCosts, double towerTopMass,
        SiteTerrain terrain, TurbineLayout layout, SoilCondition soil);

    // override any of these parameters
    void setConstructionTime(int months);
    void setAccessRoadEntrances(int number);
    void setBuildingSize(double sqft);
    void setTempTowers(double towers);
    void setPermanentTowers(double towers);
    void setWeatherDelays(int days);
    void setCraneBreakdowns(int number);

    // transportation costs
    double transportationCost(double transportationDistance = 0.0) const;

    // engineering costs
    double engineeringCost() const;

    // met masts and power performance costs
    double powerPerformanceCost() const;

    // access roads and site improvement costs
    double roadsCost() const;

    // site compound and security costs
    double siteCompoundCost() const;

    // control O&M building costs
    double buildingCost() const;

    // foundation costs
    double foundationCost() const;

    // erection costs
    double erectionCosts(bool deliveryAssistRequired = false) const;

    // electrical materials costs
    double electricalMaterialsCost() const;

    // electrical installation costs
    double electricalInstallationCost() const;

    // collector substation costs
    double substationCost() const;

    // transmission line and interconnect costs
    double transmissionCost(bool newSwitchyardRequired = true) const;

    // construction management costs
    double constructionMgmtCost() const;

    // project management costs
    double projectMgmtCost(int constructionTime) const;

    // development costs
    double developmentCost(double developmentFee = 5.0) const;

    // insurance costs
    double insuranceMultiplier(bool performanceBond = false) const;
    double insuranceFixedCosts(double foundationCost, bool performanceBond = false) const;
};
