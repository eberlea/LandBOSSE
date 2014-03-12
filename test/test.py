#!/usr/bin/env python
# encoding: utf-8
"""
untitled.py

Created by Andrew Ning on 2014-03-11.
Copyright (c) NREL. All rights reserved.
"""

import unittest
from pybos import LandBOS


class TestDefaultCosts(unittest.TestCase):

    def setUp(self):

        rating = 2000.0
        diameter = 110.0
        hubHeight = 100.0
        nTurbines = 100
        voltage = 137.0
        distToInterconnect = 5.0
        TCC = 1000.0
        towerTopMass = 88.0
        terrain = 0   # FLAT_TO_ROLLING
        layout = 1  # COMPLEX
        soil = 0  # STANDARD

        self.bos = LandBOS(rating, diameter, hubHeight, nTurbines,
            voltage, distToInterconnect, TCC,
            towerTopMass, terrain, layout, soil)


    def test_transportation(self):
        cost = self.bos.transportationCost()
        self.assertEqual(200000000, cost)


    def test_transportation2(self):
        cost = self.bos.transportationCost(transportationDistance=10.0)
        self.assertAlmostEqual(200993446, cost, delta=0.5)


    def test_engineering(self):
        cost = self.bos.engineeringCost()
        self.assertAlmostEqual(1197400, cost, delta=0.5)


    def test_engineering2(self):

        rating = 1900.0  # just changed the rating to trigger the if condition
        diameter = 110.0
        hubHeight = 100.0
        nTurbines = 100
        voltage = 137.0
        distToInterconnect = 5.0
        TCC = 1000.0
        towerTopMass = 88.0
        terrain = 0   # FLAT_TO_ROLLING
        layout = 1  # COMPLEX
        soil = 0  # STANDARD

        bos = LandBOS(rating, diameter, hubHeight, nTurbines,
            voltage, distToInterconnect, TCC,
            towerTopMass, terrain, layout, soil)

        cost = bos.engineeringCost()
        self.assertAlmostEqual(1035725, cost, delta=0.5)


    def test_powerPerformance(self):
        cost = self.bos.powerPerformanceCost()
        self.assertAlmostEqual(1130400, cost, delta=0.5)


    def test_powerPerformance2(self):
        self.bos.setTempTowers(4)
        self.bos.setPermanentTowers(5)
        cost = self.bos.powerPerformanceCost()
        self.assertAlmostEqual(2117200, cost, delta=0.5)


    def test_accessRoads(self):
        cost = self.bos.accessRoadsCost()
        self.assertAlmostEqual(7713048, cost, delta=0.5)


    def test_accessRoads2(self):
        self.bos.setAccessRoadEntrances(8)
        self.bos.setConstructionTime(15)
        cost = self.bos.accessRoadsCost()
        self.assertAlmostEqual(7841568, cost, delta=0.5)


    def test_siteCompound(self):

        cost = self.bos.siteCompoundCost()
        self.assertAlmostEqual(901575, cost, delta=0.5)


    def test_building(self):

        cost = self.bos.buildingCost()
        self.assertAlmostEqual(801125, cost, delta=0.5)


    def test_building2(self):

        self.bos.setBuildingSize(8000)
        cost = self.bos.buildingCost()
        self.assertAlmostEqual(1176125, cost, delta=0.5)


    def test_foundation(self):

        cost = self.bos.foundationCost()
        self.assertAlmostEqual(11286437, cost, delta=0.5)

    def test_foundation2(self):

        rating = 2000.0
        diameter = 110.0
        hubHeight = 100.0
        nTurbines = 100
        voltage = 137.0
        distToInterconnect = 5.0
        TCC = 1000.0
        towerTopMass = 88.0
        terrain = 0   # FLAT_TO_ROLLING
        layout = 1  # COMPLEX
        soil = 1  # BOUYANT  # change soil type

        bos = LandBOS(rating, diameter, hubHeight, nTurbines,
            voltage, distToInterconnect, TCC,
            towerTopMass, terrain, layout, soil)

        cost = bos.foundationCost()
        self.assertAlmostEqual(13286437, cost, delta=0.5)


    def test_erection(self):

        cost = self.bos.erectionCost()
        self.assertAlmostEqual(9382605, cost, delta=0.5)

    def test_erection2(self):

        cost = self.bos.erectionCost(deliveryAssistRequired=True)
        self.assertAlmostEqual(15382605, cost, delta=0.5)


    def test_electricalMaterials(self):

        cost = self.bos.electricalMaterialsCost()
        self.assertAlmostEqual(14675585, cost, delta=0.5)

    def test_electricalMaterials2(self):

        padMountTransformer = False
        thermalBackfill = 20.0
        cost = self.bos.electricalMaterialsCost(padMountTransformer, thermalBackfill)
        self.assertAlmostEqual(10711185, cost, delta=0.5)


    def test_electricalInstallation(self):

        cost = self.bos.electricalInstallationCost()
        self.assertAlmostEqual(7757730, cost, delta=0.5)


    def test_electricalInstallation2(self):

        rockTrenchingLength = 5.0
        overheadCollector = 5.0
        cost = self.bos.electricalInstallationCost(rockTrenchingLength, overheadCollector)
        self.assertAlmostEqual(8512430, cost, delta=0.5)



    def test_substation(self):

        cost = self.bos.substationCost()
        self.assertAlmostEqual(5530851, cost, delta=0.5)


    def test_transmission(self):

        cost = self.bos.transmissionCost()
        self.assertAlmostEqual(4246268, cost, delta=0.5)

    def test_transmission2(self):

        cost = self.bos.transmissionCost(newSwitchyardRequired=False)
        self.assertAlmostEqual(1598569, cost, delta=0.5)


    def test_projectMgmt(self):

        cost = self.bos.projectMgmtCost()
        self.assertAlmostEqual(2607139, cost, delta=0.5)


    def test_projectMgmt2(self):

        self.bos.setConstructionTime(40)

        cost = self.bos.projectMgmtCost()
        self.assertAlmostEqual(6510000, cost, delta=0.5)


    def test_development(self):

        cost = self.bos.developmentCost()
        self.assertAlmostEqual(5e6, cost, delta=0.5)


    def test_insurance(self):
        fcost = self.bos.foundationCost()

        values = self.bos.insuranceMultiplierAndCost(fcost,
                                   performanceBond=False)

        cost = values['cost'] + values['alpha']*self.bos.totalCost()

        self.assertAlmostEqual(2265350, cost, delta=0.5)


    def test_insurance2(self):
        fcost = self.bos.foundationCost()

        values = self.bos.insuranceMultiplierAndCost(fcost,
                                   performanceBond=True)

        cost = values['cost'] + values['alpha']*self.bos.totalCost(performanceBond=True)

        self.assertAlmostEqual(7210510, cost, delta=0.5)


    def test_markup(self):
        tcost = self.bos.transportationCost()

        values = self.bos.markupMultiplierAndCost(tcost)

        cost = values['cost'] + values['alpha']*self.bos.totalCost()

        self.assertAlmostEqual(11151202, cost, delta=0.5)


    def test_totalCost(self):

        cost = self.bos.totalCost()
        self.assertAlmostEqual(285646716, cost, delta=0.5)



if __name__ == "__main__":
    unittest.main()
