"""ESP32 MicroPython PWM adapter.

GPIO numbers are supplied by the owner after checking the exact board and wiring.
No pins are silently assigned by this module.
"""


class ESP32ServoDriver:
    def __init__(self, pins, limits=None, min_pulse_us=1000, max_pulse_us=2000, frequency=50):
        if pins is None or len(pins) != 4 or any(pin is None for pin in pins):
            raise ValueError("configure four verified servo GPIO numbers first")
        try:
            from machine import Pin, PWM
        except ImportError:
            raise RuntimeError("ESP32ServoDriver requires MicroPython machine.Pin and machine.PWM")
        if limits is None:
            limits = [(0, 180)] * 4
        if len(limits) != 4:
            raise ValueError("four calibrated limit pairs are required")
        self._pwms = []
        self._limits = limits
        self.min_pulse_us = int(min_pulse_us)
        self.max_pulse_us = int(max_pulse_us)
        self.period_us = int(1000000 / int(frequency))
        if self.min_pulse_us <= 0 or self.max_pulse_us <= self.min_pulse_us:
            raise ValueError("invalid servo pulse range")
        for pin_number in pins:
            pwm = PWM(Pin(int(pin_number)), freq=int(frequency))
            self._pwms.append(pwm)

    def set_angle(self, index, angle):
        low, high = self._limits[index]
        angle = max(float(low), min(float(high), float(angle)))
        normalized = (angle - float(low)) / (float(high) - float(low))
        pulse = self.min_pulse_us + normalized * (self.max_pulse_us - self.min_pulse_us)
        pwm = self._pwms[index]
        if hasattr(pwm, "duty_ns"):
            pwm.duty_ns(int(pulse * 1000))
        elif hasattr(pwm, "duty_u16"):
            pwm.duty_u16(int((pulse / self.period_us) * 65535))
        else:
            pwm.duty(int((pulse / self.period_us) * 1023))

    def deinit(self):
        for pwm in self._pwms:
            if hasattr(pwm, "deinit"):
                pwm.deinit()


class ESP32BatteryADC:
    """Read an external resistor-divider output through an ESP32 ADC input."""
    def __init__(self, pin_number, attenuation=None):
        if pin_number is None:
            raise ValueError("configure a verified ADC1 pin first")
        try:
            from machine import Pin, ADC
        except ImportError:
            raise RuntimeError("ESP32BatteryADC requires MicroPython machine.Pin and machine.ADC")
        self._adc = ADC(Pin(int(pin_number)))
        if attenuation is not None and hasattr(self._adc, "atten"):
            self._adc.atten(attenuation)
        elif hasattr(ADC, "ATTN_11DB") and hasattr(self._adc, "atten"):
            self._adc.atten(ADC.ATTN_11DB)

    def read_raw(self):
        if hasattr(self._adc, "read_u16"):
            value = self._adc.read_u16()
            return int((value * 4095) / 65535)
        return int(self._adc.read())
