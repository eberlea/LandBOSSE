//
//  BOS.h
//  LandBOS
//
//  Created by Andrew Ning on 3/10/14.
//  Copyright (c) 2014 NREL. All rights reserved.
//

#ifndef __LandBOS__BOS__
#define __LandBOS__BOS__

#include <math.h>

#endif /* defined(__LandBOS__BOS__) */


enum SiteTerrain {FLAT_TO_ROLLING, RIDGE_TOP, MOUNTAINOUS};
enum TurbineLayout {SIMPLE, COMPLEX};
enum SoilCondition {STANDARD, BOUYANT};

struct MultCost {
    double alpha;
    double cost;
};

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

    // transportation
    double transportationCost(double transportationDistance=0.0) const;

    // engineering
    double engineeringCost() const;

    // met masts and power performance
    double powerPerformanceCost() const;

    // access roads and site improvement
    double roadsCost() const;

    // site compound and security
    double siteCompoundCost() const;

    // control O&M building
    double buildingCost() const;

    // foundation
    double foundationCost() const;

    // erection
    double erectionCost(bool deliveryAssistRequired=false) const;

    // electrical materials
    double electricalMaterialsCost() const;

    // electrical installation
    double electricalInstallationCost() const;

    // collector substation
    double substationCost() const;

    // transmission line and interconnect
    double transmissionCost(bool newSwitchyardRequired=true) const;

    // construction management
    double constructionMgmtCost() const;

    // project management
    double projectMgmtCost() const;

    // development
    double developmentCost(double developmentFee=5.0) const;

    // insurance
    MultCost insuranceMultiplierAndCost(double foundationCost,
        bool performanceBond) const;

    // markup and contingency
    MultCost markupMultiplierAndCost(double transportationCost,
        double contingency=3.0, double warranty=0.02, double useTax=0.0,
        double overhead=5.0, double profitMargin=5.0) const;


    // total
    double totalCost(bool deliveryAssistRequired, bool newSwitchyardRequired, bool performanceBond,
                     double contingency, double warranty, double useTax, double overhead,
                     double profitMargin, double developmentFee, double transportationDistance);

};
