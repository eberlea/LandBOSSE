# distutils: language = c++
# distutils: sources = src/BOS.cpp

from libcpp cimport bool


cdef extern from "BOS.h":

    cdef enum SiteTerrain:
        FLAT_TO_ROLLING
        RIDGE_TOP
        MOUNTAINOUS

    cdef enum TurbineLayout:
        SIMPLE
        COMPLEX

    cdef enum SoilCondition:
        STANDARD
        BOUYANT

    cdef struct MultCost:
        double alpha
        double cost


    cdef cppclass BOS:
        BOS(double, double, double, int,
        double, double, double, double,
        SiteTerrain, TurbineLayout, SoilCondition) except +

        void setConstructionTime(int)
        void setAccessRoadEntrances(int)
        void setBuildingSize(double)
        void setTempTowers(double)
        void setPermanentTowers(double)
        void setWeatherDelays(int)
        void setCraneBreakdowns(int)

        double transportationCost(double)
        double engineeringCost()
        double powerPerformanceCost()
        double accessRoadsCost()
        double siteCompoundCost()
        double buildingCost()
        double foundationCost()
        double erectionCost(bool)
        double electricalMaterialsCost(bool, double)
        double electricalInstallationCost(double, double)
        double substationCost()
        double transmissionCost(bool)
        double projectMgmtCost()
        double developmentCost(double)
        MultCost insuranceMultiplierAndCost(double, bool)
        MultCost markupMultiplierAndCost(double, double,
            double, double, double, double)
        double totalCost(bool, bool, bool, double, double,
            double, bool, double, double, double, double,
            double, double, double)




cdef class LandBOS:

    cdef BOS *thisptr

    def __cinit__(self, double machineRating, double rotorDiameter, double hubHeight,
                  int nTurbines, double interconnectVoltage, double distToInterconnect,
                  double turbineCapitalCosts, double towerTopMass,
                  SiteTerrain terrain, TurbineLayout layout, SoilCondition soil):
        self.thisptr = new BOS(machineRating, rotorDiameter, hubHeight, nTurbines,
            interconnectVoltage, distToInterconnect, turbineCapitalCosts,
            towerTopMass, terrain, layout, soil)

    def __dealloc__(self):
        del self.thisptr


    def setConstructionTime(self, months):
        self.thisptr.setConstructionTime(months)

    def setAccessRoadEntrances(self, number):
        self.thisptr.setAccessRoadEntrances(number)

    def setBuildingSize(self, sqft):
        self.thisptr.setBuildingSize(sqft)

    def setTempTowers(self, towers):
        self.thisptr.setTempTowers(towers)

    def setPermanentTowers(self, towers):
        self.thisptr.setPermanentTowers(towers)

    def setWeatherDelays(self, days):
        self.thisptr.setWeatherDelays(days)

    def setCraneBreakdowns(self, number):
        self.thisptr.setCraneBreakdowns(number)



    def transportationCost(self, transportationDistance=0.0):
        return self.thisptr.transportationCost(transportationDistance)

    def engineeringCost(self):
        return self.thisptr.engineeringCost()

    def powerPerformanceCost(self):
        return self.thisptr.powerPerformanceCost()

    def accessRoadsCost(self):
        return self.thisptr.accessRoadsCost()

    def siteCompoundCost(self):
        return self.thisptr.siteCompoundCost()

    def buildingCost(self):
        return self.thisptr.buildingCost()

    def foundationCost(self):
        return self.thisptr.foundationCost()

    def erectionCost(self, deliveryAssistRequired=False):
        return self.thisptr.erectionCost(deliveryAssistRequired)

    def electricalMaterialsCost(self, padMountTransformer=True,
                                thermalBackfill=0.0):
        return self.thisptr.electricalMaterialsCost(padMountTransformer,
            thermalBackfill)

    def electricalInstallationCost(self, rockTrenchingLength=10.0,
                                   overheadCollector=0.0):
        return self.thisptr.electricalInstallationCost(rockTrenchingLength,
            overheadCollector)

    def substationCost(self):
        return self.thisptr.substationCost()

    def transmissionCost(self, newSwitchyardRequired=True):
        return self.thisptr.transmissionCost(newSwitchyardRequired)

    def projectMgmtCost(self):
        return self.thisptr.projectMgmtCost()

    def developmentCost(self, developmentFee=5.0):
        return self.thisptr.developmentCost(developmentFee)

    def insuranceMultiplierAndCost(self, foundationCost,
                                   performanceBond=False):
        return self.thisptr.insuranceMultiplierAndCost(foundationCost,
            performanceBond)

    def markupMultiplierAndCost(self, transportationCost,
            contingency=3.0, warranty=0.02, useTax=0.0,
            overhead=5.0, profitMargin=5.0):
        return self.thisptr.markupMultiplierAndCost(transportationCost,
            contingency, warranty, useTax, overhead, profitMargin)

    def totalCost(self, deliveryAssistRequired=False, padMountTransformer=True,
            newSwitchyardRequired=True, rockTrenchingLength=10.0,
            thermalBackfill=0.0, overheadCollector=0.0,
            performanceBond=False, contingency=3.0, warranty=0.02,
            useTax=0.0, overhead=5.0, profitMargin=5.0,
            developmentFee=5.0, transportationDistance=0.0):

        return self.thisptr.totalCost(deliveryAssistRequired, padMountTransformer,
            newSwitchyardRequired, rockTrenchingLength, thermalBackfill,
            overheadCollector, performanceBond, contingency, warranty,
            useTax, overhead, profitMargin, developmentFee,
            transportationDistance)
