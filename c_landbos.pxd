cdef extern from "src/LandBOS.h":

    ctypedef enum SiteTerrain:
        FLAT_TO_ROLLING
        RIDGE_TOP
        MOUNTAINOUS

    ctypedef enum TurbineLayout:
        SIMPLE
        COMPLEX

    ctypedef enum SoilCondition:
        STANDARD
        BOUYANT

    ctypedef struct MultCost:
        double alpha
        double cost

    double farmSize(double rating, int nTurb)

    int defaultConstructionTime(int nTurb)

    int defaultAccessRoadEntrances(int nTurb)

    double defaultBuildingSize(double farmSize)

    int defaultTempMetTowers(double farmSize)

    int defaultPermanentMetTowers(double farmSize)

    int defaultWeatherDelayDays(int nTurb)

    int defaultCraneBreakdowns(int nTurb)


    double transportationCost(double tcc, double rating, int nTurb,
            double hubHt, double transportDist)

    double engineeringCost(int nTurb, double farmSize)

    double powerPerformanceCost(double hubHt, double permanent,
            double temporary)

    double accessRoadsCost(SiteTerrain terrain, TurbineLayout layout,
            int nTurb, double diameter, int constructionTime,
            int accessRoadEntrances)

    double siteCompoundCost(int accessRoadEntrances, int constructionTime,
            double farmSize)

    double buildingCost(double buildingSize)

    double foundationCost(double rating, double diameter, double topMass,
            double hubHt, SoilCondition soil, int nTurb)

    double erectionCost(double rating, double hubHt, int nTurb, int weatherDelayDays,
            int craneBreakdowns, bint deliveryAssistRequired)

    double electricalMaterialsCost(SiteTerrain terrain, TurbineLayout layout,
            double farmSize, double diameter, int nTurb, bint padMountTransformer,
            double thermalBackfill)

    double electricalInstallationCost(SiteTerrain terrain, TurbineLayout layout,
            double farmSize, double diameter, int nTurb,
            double rockTrenchingLength, double overheadCollector)

    double substationCost(double voltage, double farmSize)

    double transmissionCost(double voltage, double distInter,
            bint newSwitchyardRequired)

    double projectMgmtCost(int constructionTime)

    double developmentCost(double developmentFee)

    MultCost insuranceMultiplierAndCost(double tcc, double farmSize,
            double foundationCost, bint performanceBond)

    MultCost markupMultiplierAndCost(double transportationCost, double contingency,
            double warranty, double useTax, double overhead, double profitMargin)



