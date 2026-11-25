# M7 integration contract

M7 is the only manager permitted to write the four servo outputs.

- Construct `MotionPlanner` with four mechanically measured angle ranges.
- Construct `RobotController(planner, servo_driver, guardian, command_timeout_ms)`.
- Pass the M8 `GuardianManager` itself as `guardian`; it implements `allow_motion()`.
- M8 starts latched. Supply a fresh safe `Telemetry` snapshot and require an explicit operator acknowledgment through `guardian.clear_faults(..., operator_ack=True)` before M7 is allowed to move.
- Call `robot.tick(now_ms)` at a consistent interval; 20 ms is a reasonable starting point, not a guaranteed requirement for every servo.
- All timestamps must use the same monotonic clock domain. Do not mix RTC wall-clock time with MicroPython `ticks_ms()`.
- Use `robot.emergency_stop(reason)` for local stop requests. It freezes the planner at its last position; a separate physical servo-power interlock is required for a true emergency stop.

M7 must never treat a missing Guardian object or a missing `allow_motion()` implementation as permission to move.
