import unittest
from billi_robot.planner import MotionPlanner
from billi_robot.controller import RobotController
from billi_robot.battery import BatteryMonitor


class FakeServoDriver:
    def __init__(self):
        self.positions = [90.0, 90.0, 90.0, 90.0]

    def set_angle(self, index, angle):
        self.positions[index] = angle


class FakeGuardian:
    def __init__(self, allowed=True):
        self.allowed = allowed

    def allow_motion(self):
        return self.allowed


class PlannerTests(unittest.TestCase):
    def test_targets_are_bounded_to_calibrated_ranges(self):
        planner = MotionPlanner([(10, 170)] * 4, max_step_deg=5)
        self.assertTrue(planner.move_to([200, 90, 90, 90]))
        self.assertEqual(planner.target[0], 170)

    def test_tick_moves_gradually_not_in_one_jump(self):
        planner = MotionPlanner([(0, 180)] * 4, max_step_deg=3)
        planner.move_to([120, 90, 90, 90])
        current = planner.tick()
        self.assertEqual(current[0], 93.0)
        self.assertFalse(planner.is_idle())


class ControllerTests(unittest.TestCase):
    def test_guardian_can_veto_motion(self):
        driver = FakeServoDriver()
        planner = MotionPlanner([(0, 180)] * 4)
        controller = RobotController(planner, driver, FakeGuardian(False))
        self.assertFalse(controller.move_to([100, 90, 90, 90], 0))
        self.assertEqual(driver.positions[0], 90.0)

    def test_emergency_stop_freezes_servo_targets(self):
        driver = FakeServoDriver()
        planner = MotionPlanner([(0, 180)] * 4)
        controller = RobotController(planner, driver, FakeGuardian(True))
        self.assertTrue(controller.move_to([140, 90, 90, 90], 0))
        controller.emergency_stop("test")
        controller.tick(10)
        self.assertTrue(controller.is_stopped())
        self.assertEqual(driver.positions[0], 90.0)

    def test_command_timeout_stops_active_motion(self):
        driver = FakeServoDriver()
        planner = MotionPlanner([(0, 180)] * 4)
        controller = RobotController(planner, driver, FakeGuardian(True), command_timeout_ms=50)
        controller.move_to([140, 90, 90, 90], 0)
        controller.tick(60)
        self.assertTrue(controller.is_stopped())


class BatteryTests(unittest.TestCase):
    def test_adc_voltage_is_converted_with_divider_and_percent(self):
        battery = BatteryMonitor(adc_max=4095, adc_voltage=3.3, divider_ratio=2.0,
                                 empty_voltage=3.3, full_voltage=4.2, low_percent=15)
        reading = battery.update(4095)
        self.assertAlmostEqual(reading["voltage"], 6.6, places=2)
        self.assertEqual(reading["percent"], 100)
        self.assertFalse(reading["low"])

    def test_invalid_adc_value_is_rejected(self):
        battery = BatteryMonitor()
        with self.assertRaises(ValueError):
            battery.update(-1)


if __name__ == "__main__":
    unittest.main()
