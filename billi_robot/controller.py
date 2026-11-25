"""Safety-gated motion executor. Only this manager writes servo commands."""


class RobotController:
    def __init__(self, planner, servo_driver, guardian, command_timeout_ms=5000):
        if planner is None or servo_driver is None or guardian is None:
            raise ValueError("planner, servo_driver and guardian are required")
        self.planner = planner
        self.servo_driver = servo_driver
        self.guardian = guardian
        self.command_timeout_ms = max(1, int(command_timeout_ms))
        self._stopped = False
        self._stop_reason = ""
        self._last_command_ms = 0

    def move_to(self, angles, now_ms):
        if self._stopped or not self.guardian.allow_motion():
            self.emergency_stop("guardian_veto")
            return False
        if not self.planner.move_to(angles):
            return False
        self._last_command_ms = int(now_ms)
        return True

    def tick(self, now_ms):
        if self._stopped:
            return self.planner.get_pose()
        if not self.guardian.allow_motion():
            self.emergency_stop("guardian_veto")
            return self.planner.get_pose()
        if not self.planner.is_idle() and int(now_ms) - self._last_command_ms > self.command_timeout_ms:
            self.emergency_stop("motion_command_timeout")
            return self.planner.get_pose()
        pose = self.planner.tick()
        for index in range(4):
            self.servo_driver.set_angle(index, pose[index])
        return pose

    def emergency_stop(self, reason="emergency_stop"):
        self._stopped = True
        self._stop_reason = str(reason)
        self.planner.hold()
        return True

    def clear_stop(self):
        if not self.guardian.allow_motion():
            return False
        self._stopped = False
        self._stop_reason = ""
        self._last_command_ms = 0
        return True

    def is_stopped(self):
        return self._stopped

    def stop_reason(self):
        return self._stop_reason

    def is_idle(self):
        return self.planner.is_idle()
