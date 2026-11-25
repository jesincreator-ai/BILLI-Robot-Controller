"""Small, hardware-neutral sensor snapshot exchanged with the Guardian."""


class SensorSnapshot:
    def __init__(self, battery_percent=None, tilt_deg=None, distance_cm=None,
                 sensors_ok=True, servo_fault=False, heartbeat_ms=None):
        self.battery_percent = battery_percent
        self.tilt_deg = tilt_deg
        self.distance_cm = distance_cm
        self.sensors_ok = bool(sensors_ok)
        self.servo_fault = bool(servo_fault)
        self.heartbeat_ms = heartbeat_ms

    def as_dict(self):
        return {
            "battery_percent": self.battery_percent,
            "tilt_deg": self.tilt_deg,
            "distance_cm": self.distance_cm,
            "sensors_ok": self.sensors_ok,
            "servo_fault": self.servo_fault,
            "heartbeat_ms": self.heartbeat_ms,
        }
