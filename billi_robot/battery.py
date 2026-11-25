"""ADC battery estimate; voltage calibration must be measured on the real board."""


class BatteryMonitor:
    def __init__(self, adc_max=4095, adc_voltage=3.3, divider_ratio=2.0,
                 empty_voltage=3.3, full_voltage=4.2, low_percent=15):
        self.adc_max = int(adc_max)
        self.adc_voltage = float(adc_voltage)
        self.divider_ratio = float(divider_ratio)
        self.empty_voltage = float(empty_voltage)
        self.full_voltage = float(full_voltage)
        self.low_percent = int(low_percent)
        if self.adc_max <= 0 or self.adc_voltage <= 0 or self.divider_ratio <= 0:
            raise ValueError("ADC scale and divider ratio must be positive")
        if self.empty_voltage >= self.full_voltage:
            raise ValueError("empty_voltage must be below full_voltage")

    def update(self, raw_value):
        raw_value = int(raw_value)
        if raw_value < 0 or raw_value > self.adc_max:
            raise ValueError("ADC reading is outside its configured range")
        voltage = (raw_value / float(self.adc_max)) * self.adc_voltage * self.divider_ratio
        ratio = (voltage - self.empty_voltage) / (self.full_voltage - self.empty_voltage)
        percent = int(max(0.0, min(100.0, ratio * 100.0)))
        return {"voltage": voltage, "percent": percent, "low": percent <= self.low_percent}
