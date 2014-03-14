#!/usr/bin/env python
# encoding: utf-8
"""
test_openmdao.py

Created by Andrew Ning on 2014-03-11.
Copyright (c) NREL. All rights reserved.
"""

import unittest
from landbos import LandBOS


class TestDefaultCosts(unittest.TestCase):

    def test_totalCost(self):
        bos = LandBOS()
        bos.rating = 2000
        bos.diameter = 110
        bos.hubHeight = 100
        bos.nTurbines = 100
        bos.voltage = 137
        bos.distInter = 5
        bos.terrain = 'FLAT_TO_ROLLING'
        bos.layout = 'COMPLEX'
        bos.soil = 'STANDARD'
        bos.TCC = 1000.0
        bos.topMass = 88.0

        bos.run()

        self.assertAlmostEqual(285646716, bos.cost, delta=0.5)


if __name__ == '__main__':
    unittest.main()
