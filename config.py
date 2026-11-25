"""Hardware-specific configuration. Verify all values with the actual circuit."""
SERVO_PINS = (None, None, None, None)  # Fill with four verified GPIO numbers; do not guess.
SERVO_LIMITS_DEG = ((10, 170), (10, 170), (10, 170), (10, 170))
SERVO_MAX_STEP_DEG = 2.0
SERVO_MIN_PULSE_US = 1000
SERVO_MAX_PULSE_US = 2000
SERVO_FREQUENCY_HZ = 50
MOTION_COMMAND_TIMEOUT_MS = 5000
BATTERY_ADC_PIN = None  # Configure the verified ADC1 input and external divider.
BATTERY_ADC_MAX = 4095
BATTERY_ADC_VOLTAGE = 3.3
BATTERY_DIVIDER_RATIO = 2.0
BATTERY_EMPTY_V = 3.3
BATTERY_FULL_V = 4.2
