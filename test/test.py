#!/usr/bin/env python
# encoding: utf-8
"""
untitled.py

Created by Andrew Ning on 2014-03-11.
Copyright (c) NREL. All rights reserved.
"""

import unittest
import landbos


class TestDefaultCosts(unittest.TestCase):

    def setUp(self):

        self.rating = 2000.0
        self.diameter = 110.0
        self.hubHeight = 100.0
        self.nTurbines = 100
        self.voltage = 137.0
        self.distToInterconnect = 5.0
        self.TCC = 1000.0
        self.towerTopMass = 88.0
        self.terrain = 0   # FLAT_TO_ROLLING
        self.layout = 1  # COMPLEX
        self.soil = 0  # STANDARD

        self.farmSize = landbos.farmSize(self.rating, self.nTurbines)

        self.constructionTime = landbos.defaultConstructionTime(self.nTurbines)
        self.accessRoadEntrances = landbos.defaultAccessRoadEntrances(self.nTurbines)
        self.buildingSize = landbos.defaultBuildingSize(self.farmSize)
        self.tempMetTowers = landbos.defaultTempMetTowers(self.farmSize)
        self.permanentMetTowers = landbos.defaultPermanentMetTowers(self.farmSize)
        self.weatherDelayDays = landbos.defaultWeatherDelayDays(self.nTurbines)
        self.craneBreakdowns = landbos.defaultCraneBreakdowns(self.nTurbines)


    def test_transportation(self):
        cost = landbos.transportationCost(self.TCC, self.rating, self.nTurbines,
            self.hubHeight)
        self.assertEqual(200000000, cost)

    def test_transportation2(self):
        cost = landbos.transportationCost(self.TCC, self.rating, self.nTurbines,
            self.hubHeight, transportDist=10.0)
        self.assertAlmostEqual(200993446, cost, delta=0.5)


    def test_engineering(self):
        cost = landbos.engineeringCost(self.nTurbines, self.farmSize)
        self.assertAlmostEqual(1197400, cost, delta=0.5)


    def test_engineering2(self):

        farmSize = 190.0  # changed to trigger the if condition

        cost = landbos.engineeringCost(self.nTurbines, farmSize)
        self.assertAlmostEqual(1035725, cost, delta=0.5)


    def test_powerPerformance(self):
        cost = landbos.powerPerformanceCost(self.hubHeight, self.permanentMetTowers,
            self.tempMetTowers)
        self.assertAlmostEqual(1130400, cost, delta=0.5)


    def test_powerPerformance2(self):
        cost = landbos.powerPerformanceCost(self.hubHeight, permanent=5, temporary=4)
        self.assertAlmostEqual(2117200, cost, delta=0.5)


    def test_accessRoads(self):
        cost = landbos.accessRoadsCost(self.terrain, self.layout,
            self.nTurbines, self.diameter, self.constructionTime, self.accessRoadEntrances)
        self.assertAlmostEqual(7713048, cost, delta=0.5)


    def test_accessRoads2(self):
        accessRoadEntrances = 8
        constructionTime = 15
        cost = landbos.accessRoadsCost(self.terrain, self.layout,
            self.nTurbines, self.diameter, constructionTime, accessRoadEntrances)
        self.assertAlmostEqual(7841568, cost, delta=0.5)


    def test_siteCompound(self):

        cost = landbos.siteCompoundCost(self.accessRoadEntrances, self.constructionTime,
            self.farmSize)
        self.assertAlmostEqual(901575, cost, delta=0.5)


    def test_building(self):

        cost = landbos.buildingCost(self.buildingSize)
        self.assertAlmostEqual(801125, cost, delta=0.5)


    def test_building2(self):

        buildingSize = 8000.0
        cost = landbos.buildingCost(buildingSize)
        self.assertAlmostEqual(1176125, cost, delta=0.5)


    def test_foundation(self):

        cost = landbos.foundationCost(self.rating, self.diameter, self.towerTopMass,
            self.hubHeight, self.soil, self.nTurbines)
        self.assertAlmostEqual(11286437, cost, delta=0.5)


    def test_foundation2(self):

        soil = 1  # BOUYANT  # change soil type

        cost = landbos.foundationCost(self.rating, self.diameter, self.towerTopMass,
            self.hubHeight, soil, self.nTurbines)
        self.assertAlmostEqual(13286437, cost, delta=0.5)


    def test_erection(self):

        cost = landbos.erectionCost(self.rating, self.hubHeight, self.nTurbines,
            self.weatherDelayDays, self.craneBreakdowns, deliveryAssistRequired=False)
        self.assertAlmostEqual(9382605, cost, delta=0.5)

    def test_erection2(self):

        cost = landbos.erectionCost(self.rating, self.hubHeight, self.nTurbines,
            self.weatherDelayDays, self.craneBreakdowns, deliveryAssistRequired=True)
        self.assertAlmostEqual(15382605, cost, delta=0.5)


    def test_electricalMaterials(self):

        cost = landbos.electricalMaterialsCost(self.terrain, self.layout,
        self.farmSize, self.diameter, self.nTurbines)
        self.assertAlmostEqual(14675585, cost, delta=0.5)

    def test_electricalMaterials2(self):

        padMountTransformer = False
        thermalBackfill = 20.0
        cost = landbos.electricalMaterialsCost(self.terrain, self.layout,
        self.farmSize, self.diameter, self.nTurbines, padMountTransformer, thermalBackfill)
        self.assertAlmostEqual(10711185, cost, delta=0.5)


    def test_electricalInstallation(self):

        cost = landbos.electricalInstallationCost(self.terrain, self.layout,
        self.farmSize, self.diameter, self.nTurbines)
        self.assertAlmostEqual(7757730, cost, delta=0.5)


    def test_electricalInstallation2(self):

        rockTrenchingLength = 5.0
        overheadCollector = 5.0
        cost = landbos.electricalInstallationCost(self.terrain, self.layout,
        self.farmSize, self.diameter, self.nTurbines, rockTrenchingLength, overheadCollector)
        self.assertAlmostEqual(8512430, cost, delta=0.5)



    def test_substation(self):

        cost = landbos.substationCost(self.voltage, self.farmSize)
        self.assertAlmostEqual(5530851, cost, delta=0.5)


    def test_transmission(self):

        cost = landbos.transmissionCost(self.voltage, self.distToInterconnect)
        self.assertAlmostEqual(4246268, cost, delta=0.5)

    def test_transmission2(self):

        cost = landbos.transmissionCost(self.voltage, self.distToInterconnect,
            newSwitchyardRequired=False)
        self.assertAlmostEqual(1598569, cost, delta=0.5)


    def test_projectMgmt(self):

        cost = landbos.projectMgmtCost(self.constructionTime)
        self.assertAlmostEqual(2607139, cost, delta=0.5)


    def test_projectMgmt2(self):

        constructionTime = 40.0

        cost = landbos.projectMgmtCost(constructionTime)
        self.assertAlmostEqual(6510000, cost, delta=0.5)


    def test_development(self):

        cost = landbos.developmentCost()
        self.assertAlmostEqual(5e6, cost, delta=0.5)


    # def test_insurance(self):
    #     fcost = landbos.foundationCost(self.rating, self.diameter, self.towerTopMass,
    #         self.hubHeight, self.soil, self.nTurbines)

    #     values = landbos.insuranceMultiplierAndCost(self.TCC,
    #         self.farmSize, fcost, performanceBond=False)

    #     cost = values['cost'] + values['alpha']*landbos.totalCost()

    #     self.assertAlmostEqual(2265350, cost, delta=0.5)


#     def test_insurance2(self):
#         fcost = self.bos.foundationCost()

#         values = self.bos.insuranceMultiplierAndCost(fcost,
#                                    performanceBond=True)

#         cost = values['cost'] + values['alpha']*self.bos.totalCost(performanceBond=True)

#         self.assertAlmostEqual(7210510, cost, delta=0.5)


#     def test_markup(self):
#         tcost = self.bos.transportationCost()

#         values = self.bos.markupMultiplierAndCost(tcost)

#         cost = values['cost'] + values['alpha']*self.bos.totalCost()

#         self.assertAlmostEqual(11151202, cost, delta=0.5)


#     def test_totalCost(self):

#         cost = self.bos.totalCost()
#         self.assertAlmostEqual(285646716, cost, delta=0.5)



if __name__ == "__main__":
    unittest.main()
