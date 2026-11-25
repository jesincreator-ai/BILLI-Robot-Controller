"""Hardware startup template. Connect M8 Guardian before enabling any motion."""
from config import SERVO_PINS, SERVO_LIMITS_DEG, SERVO_MAX_STEP_DEG
from config import SERVO_MIN_PULSE_US, SERVO_MAX_PULSE_US, SERVO_FREQUENCY_HZ
from config import MOTION_COMMAND_TIMEOUT_MS
from billi_robot.planner import MotionPlanner
from billi_robot.controller import RobotController
from hardware.esp32 import ESP32ServoDriver


def create_controller(guardian_gate):
    if SERVO_PINS[0] is None:
        raise RuntimeError("edit config.py and verify all four servo pins before startup")
    driver = ESP32ServoDriver(SERVO_PINS, SERVO_LIMITS_DEG,
                              SERVO_MIN_PULSE_US, SERVO_MAX_PULSE_US, SERVO_FREQUENCY_HZ)
    planner = MotionPlanner(SERVO_LIMITS_DEG, SERVO_MAX_STEP_DEG)
    return RobotController(planner, driver, guardian_gate, MOTION_COMMAND_TIMEOUT_MS)
