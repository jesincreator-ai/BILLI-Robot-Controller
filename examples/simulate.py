"""Desktop simulation; no GPIO or servos are touched."""
from billi_robot.planner import MotionPlanner
from billi_robot.controller import RobotController


class DryRunServos:
    def set_angle(self, index, angle):
        print("servo{} -> {:.1f} deg".format(index + 1, angle))


class DemoGuardian:
    def allow_motion(self):
        return True


planner = MotionPlanner([(10, 170)] * 4, max_step_deg=5)
robot = RobotController(planner, DryRunServos(), DemoGuardian())
robot.move_to([120, 70, 100, 90], 0)
for tick in range(20):
    robot.tick(tick * 20)
