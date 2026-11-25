# BILLI Robot Controller (M7)

Offline four-servo body controller for BILLI R-20. Motion planning is hardware-neutral Python; `hardware/esp32.py` is the MicroPython PWM adapter. No network, cloud API, paid service, or model runtime is required.

## Safety model

- Exactly four independently calibrated joint ranges are required.
- Target angles are clamped to the configured software limits and are approached gradually (`max_step_deg` per tick).
- Every new movement and every control tick asks the Guardian gate for permission. A veto latches the controller into stopped state.
- Command timeout stops an active movement when its command is no longer fresh.
- Servo pins default to `None` intentionally. Configure only after checking the exact ESP32-WROOM board, connected devices, power circuit and wiring.
- `emergency_stop()` holds the last planner pose; it is not a physical power disconnect. Use a hardware enable/power-cut circuit for a real emergency stop.

## Desktop tests and simulation

```bash
python -m unittest discover -s tests -v
python examples/simulate.py
```

## ESP32 setup

1. Calibrate the mechanical safe range of each joint with the arm unloaded and servos powered from an appropriate external supply.
2. Edit `config.py`: fill `SERVO_PINS`, verify `SERVO_LIMITS_DEG`, pulse range and frequency.
3. Implement or import the M8 Guardian adapter exposing `allow_motion()`; do not use the demo always-allow adapter in production.
4. Upload `billi_robot/`, `hardware/`, `config.py`, `main.py` to the board.
5. Initialize `robot.tick(time.ticks_ms())` from a cooperative loop (typically 20 ms) and route sensor telemetry to M8.

Do not power four servos from the ESP32 3.3 V rail. Use an appropriately rated regulated servo supply with a shared signal ground. Verify stall current and brownout behavior before testing.

## Battery reading

`BatteryMonitor` estimates pack voltage from ADC and a divider. Its linear percentage is only an approximation, not a calibrated state-of-charge measurement. Configure the divider ratio, ADC range and pack voltage limits from measured hardware values. Never connect a battery directly to an ESP32 ADC pin without a correctly rated divider/protection circuit.

## Inter-manager contract

M7 owns all servo outputs. M8 must provide a fail-closed `allow_motion()` gate. M6 may request expressive motion but cannot write servo PWM. Keep sensor freshness and Guardian evaluation in the supervisor loop.

## License

MIT. See `LICENSE`.
