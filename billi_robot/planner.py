"""Four-axis rate-limited motion planner with calibrated software limits."""


class MotionPlanner:
    JOINT_COUNT = 4

    def __init__(self, limits, max_step_deg=2.0, initial=None):
        if len(limits) != self.JOINT_COUNT:
            raise ValueError("exactly four joint limit pairs are required")
        self.limits = []
        for pair in limits:
            low, high = float(pair[0]), float(pair[1])
            if low < 0 or high > 180 or low >= high:
                raise ValueError("joint limits must satisfy 0 <= min < max <= 180")
            self.limits.append((low, high))
        self.max_step_deg = float(max_step_deg)
        if self.max_step_deg <= 0:
            raise ValueError("max_step_deg must be positive")
        if initial is None:
            initial = [90.0] * self.JOINT_COUNT
        if len(initial) != self.JOINT_COUNT:
            raise ValueError("initial pose must contain four angles")
        self.current = []
        for index, angle in enumerate(initial):
            low, high = self.limits[index]
            self.current.append(self._clamp(float(angle), low, high))
        self.target = list(self.current)

    @staticmethod
    def _clamp(value, low, high):
        return max(low, min(high, value))

    def move_to(self, angles):
        if len(angles) != self.JOINT_COUNT:
            return False
        proposed = []
        for index, angle in enumerate(angles):
            if not isinstance(angle, (int, float)) or angle != angle:
                return False
            low, high = self.limits[index]
            proposed.append(self._clamp(float(angle), low, high))
        self.target = proposed
        return True

    def tick(self):
        for index in range(self.JOINT_COUNT):
            current = self.current[index]
            target = self.target[index]
            delta = target - current
            if delta > self.max_step_deg:
                delta = self.max_step_deg
            elif delta < -self.max_step_deg:
                delta = -self.max_step_deg
            self.current[index] = current + delta
        return list(self.current)

    def hold(self):
        self.target = list(self.current)

    def is_idle(self):
        for index in range(self.JOINT_COUNT):
            if abs(self.target[index] - self.current[index]) > 0.001:
                return False
        return True

    def get_pose(self):
        return list(self.current)
