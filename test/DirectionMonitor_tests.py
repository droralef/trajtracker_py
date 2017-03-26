import unittest

import numpy as np
from trajtracker.movement import DirectionMonitor


class DirectionMonitorTests(unittest.TestCase):

    #===================================================================================
    #   Configure
    #===================================================================================

    #----------------------------------------------------
    def test_set_units_per_mm(self):
        DirectionMonitor(3)

        try:
            DirectionMonitor("")
            self.fail()
        except:
            pass

        try:
            DirectionMonitor(None)
            self.fail()
        except:
            pass

        try:
            DirectionMonitor(0)
            self.fail()
        except:
            pass

        try:
            DirectionMonitor(-1)
            self.fail()
        except:
            pass

    #----------------------------------------------------
    def test_set_min_distance(self):
        dm = DirectionMonitor(3)
        dm.min_distance = 1

        try:
            dm.min_distance = ""
            self.fail()
        except:
            pass

        try:
            dm.min_distance = None
            self.fail()
        except:
            pass

        try:
            dm.min_distance = 0
            self.fail()
        except:
            pass

        try:
            dm.min_distance = -1
            self.fail()
        except:
            pass

    #----------------------------------------------------
    def test_set_angle_units(self):
        dm = DirectionMonitor(3)
        dm.angle_units = DirectionMonitor.Units.Degrees
        dm.angle_units = DirectionMonitor.Units.Radians

        try:
            dm.angle_units = ""
            self.fail()
        except:
            pass

        try:
            dm.angle_units = None
            self.fail()
        except:
            pass

        try:
            dm.angle_units = 0
            self.fail()
        except:
            pass


    #----------------------------------------------------
    def test_set_zero_angle(self):
        dm = DirectionMonitor(3)
        dm.zero_angle = 1
        dm.zero_angle = -1

        try:
            dm.zero_angle = ""
            self.fail()
        except:
            pass

        try:
            dm.zero_angle = None
            self.fail()
        except:
            pass

    #===================================================================================
    #   Invalid calls
    #===================================================================================


    #----------------------------------------------------
    def test_update_xyt_arg_types(self):
        dm = DirectionMonitor(1)

        dm.update_xyt(0, 0, 0)

        self.assertRaises(ValueError, lambda: dm.update_xyt("", 0, 0))
        self.assertRaises(ValueError, lambda: dm.update_xyt(None, 0, 0))

        self.assertRaises(ValueError, lambda: dm.update_xyt(0, "", 0))
        self.assertRaises(ValueError, lambda: dm.update_xyt(0, None, 0))

        self.assertRaises(ValueError, lambda: dm.update_xyt(0, 0, ""))
        self.assertRaises(ValueError, lambda: dm.update_xyt(0, 0, None))



    #===================================================================================
    #   Get angle
    #===================================================================================

    #----------------------------------------------------
    def test_get_angle_degrees(self):
        dm = DirectionMonitor(1)

        dm.update_xyt(0, 0, 0)
        self.assertIsNone(dm.curr_angle)

        dm.update_xyt(0, 1, 1)
        self.assertEqual(0, dm.curr_angle)

        dm.update_xyt(1, 1, 1)
        self.assertEqual(90, dm.curr_angle)

        dm.update_xyt(0, 1, 1)
        self.assertEqual(-90, dm.curr_angle)

        dm.update_xyt(0, 0, 1)
        self.assertEqual(180, dm.curr_angle)


    #----------------------------------------------------
    def test_get_angle_radians(self):
        dm = DirectionMonitor(1, angle_units=DirectionMonitor.Units.Radians)

        dm.update_xyt(0, 0, 0)
        dm.update_xyt(0, 1, 1)
        self.assertEqual(0, dm.curr_angle)

        dm.update_xyt(1, 1, 1)
        self.assertEqual(np.pi/2, dm.curr_angle)

        dm.update_xyt(0, 1, 1)
        self.assertEqual(-np.pi/2, dm.curr_angle)

        dm.update_xyt(0, 0, 1)
        self.assertEqual(np.pi, dm.curr_angle)


    #----------------------------------------------------
    def test_min_distance(self):
        dm = DirectionMonitor(1, min_distance=2)

        dm.update_xyt(0, 0, 0)
        dm.update_xyt(0, 1, 1)
        self.assertIsNone(dm.curr_angle)

        dm.update_xyt(0, 2, 1)
        self.assertEqual(0, dm.curr_angle)


    #----------------------------------------------------
    def test_units_per_mm(self):
        dm = DirectionMonitor(2, min_distance=1)

        dm.update_xyt(0, 0, 0)
        dm.update_xyt(0, 1, 1)
        self.assertIsNone(dm.curr_angle)

        dm.update_xyt(0, 2, 1)
        self.assertEqual(0, dm.curr_angle)


    #----------------------------------------------------
    def test_zero_angle(self):
        dm = DirectionMonitor(1, zero_angle=90)

        dm.update_xyt(0, 0, 0)
        self.assertIsNone(dm.curr_angle)

        dm.update_xyt(0, 1, 1)
        self.assertEqual(-90, dm.curr_angle)

        dm.update_xyt(1, 1, 1)
        self.assertEqual(0, dm.curr_angle)

        dm.update_xyt(0, 1, 1)
        self.assertEqual(180, dm.curr_angle)

        dm.update_xyt(0, 0, 1)
        self.assertEqual(90, dm.curr_angle)


    #===================================================================================
    #   Track curves
    #===================================================================================

    #----------------------------------------------------
    def test_track_1_curve(self):

        dm = DirectionMonitor(1)

        dm.update_xyt(0, 0, 0)
        dm.update_xyt(0.1, 1, 1)
        dm.update_xyt(0.21, 2, 2)
        start_angle = dm.curr_angle
        self.assertEqual(1, dm.n_curves)
        self.assertEqual(1, dm.curr_curve_direction)
        self.assertEqual((.21, 2, 2), dm.curr_curve_start_xyt)

        dm.update_xyt(0.321, 3, 3)
        dm.update_xyt(0.4321, 4, 4)
        dm.update_xyt(0.54321, 5, 5)
        self.assertEqual(1, dm.n_curves)
        self.assertEqual(start_angle, dm.curr_curve_start_angle)
        self.assertEqual((.21, 2, 2), dm.curr_curve_start_xyt)


    #----------------------------------------------------
    def test_track_n_curves(self):

        dm = DirectionMonitor(1)

        x = 0
        dm.update_xyt(x, 0, 0)
        x += 0.1
        dm.update_xyt(x, 1, 1)
        x += 0.11
        dm.update_xyt(x, 2, 2)
        self.assertEqual(1, dm.n_curves)

        x += 0.1
        dm.update_xyt(x, 3, 3)
        self.assertEqual(2, dm.n_curves)

        x += 0.09
        dm.update_xyt(x, 4, 4)
        self.assertEqual(2, dm.n_curves)

        x += 0.1
        dm.update_xyt(x, 5, 5)
        self.assertEqual(3, dm.n_curves)

        x += 0.1
        dm.update_xyt(x, 6, 6)
        self.assertEqual(3, dm.n_curves)


    #----------------------------------------------------
    def test_curve_min_distance(self):

        dm = DirectionMonitor(1, min_distance=1.5)

        x = 0
        dm.update_xyt(x, 0, 0)
        x += 0.1
        dm.update_xyt(x, 1, 1)
        x += 0.11
        dm.update_xyt(x, 2, 2)
        self.assertEqual(0, dm.n_curves)

        x += 0.111
        dm.update_xyt(x, 3, 3)
        self.assertEqual(1, dm.n_curves)



if __name__ == '__main__':
    unittest.main()
