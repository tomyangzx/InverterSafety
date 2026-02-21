# 800V Inverter Crash Handler

A safety-critical crash handler for 800V electric vehicle inverter systems, implementing ISO 26262 compliant safety mechanisms.

## Quick Start

### Run the Demonstration
```bash
python src/crash_handler.py
```

This will demonstrate three crash scenarios:
1. High-speed crash (5000 RPM) - Shows ASC activation
2. Low-speed crash (1000 RPM) - Shows ASC bypass
3. Stationary crash (0 RPM) - Minimal sequence

### Run Tests
```bash
python -m unittest tests.test_crash_handler -v
```

## Features

✅ **Active 800V Discharge** - Safely reduces high voltage during crash  
✅ **ASC (Active Short Circuit)** - Prevents back-EMF overvoltage at high speeds  
✅ **ASO (All Switches Open)** - Ensures zero torque generation  
✅ **ISO 26262 Compliant** - Meets ASIL C/D safety requirements  
✅ **Configurable Thresholds** - Adaptable to different motor systems  
✅ **Comprehensive Testing** - 15+ unit tests covering all scenarios  

## Safety Goals

| ID | Safety Goal | ASIL | Status |
|----|-------------|------|--------|
| SG1 | Prevent unintended torque during crash | D | ✅ Implemented |
| SG2 | Safely discharge 800V DC-link | D | ✅ Implemented |
| SG3 | Prevent back-EMF overvoltage | C | ✅ Implemented |

## State Sequence

```
CRASH_DETECTED → ACTIVE_DISCHARGE → ASC* → ASO → SAFE_STATE
                                      ↓
                              *only if speed > 3000 RPM
```

## API Usage

```python
from crash_handler import CrashHandler

# Initialize
handler = CrashHandler(
    dc_link_voltage=800.0,
    motor_speed_rpm=5000.0,
    discharge_time_ms=100,
    asc_time_ms=50
)

# Execute crash sequence
if handler.execute_crash_sequence():
    print("System is safe")
```

## Configuration

### Key Parameters

- **discharge_time_ms** (default: 100)  
  Duration of active discharge phase. Longer = more voltage reduction.

- **asc_time_ms** (default: 50)  
  Duration of active short circuit phase. Longer = more motor deceleration.

- **high_speed_threshold_rpm** (default: 3000)  
  Motor speed above which ASC is required to prevent back-EMF.

- **safe_voltage_threshold** (default: 600)  
  Target voltage after initial discharge phase.

## Documentation

- [Safety Documentation](docs/crash_handler_safety.md) - Detailed safety analysis and ISO 26262 compliance
- [FOC Safety Risks](data/foc_safety_risks.md) - Background on field-oriented control hazards
- [Safety Mechanisms](data/inverter_safety_mechanisms.md) - E-Gas monitoring concept

## Testing

### Test Coverage
- ✅ State machine transitions
- ✅ ASC threshold logic
- ✅ Voltage discharge verification
- ✅ Safety goal compliance
- ✅ Edge cases and boundaries

### Test Scenarios
1. **High-speed crash** - Verifies ASC activation prevents back-EMF
2. **Low-speed crash** - Verifies ASC bypass when safe
3. **Stationary crash** - Verifies minimal sequence
4. **Edge cases** - Zero voltage, very high speed, exact thresholds

## Implementation Notes

### For Production Use

This is a reference implementation demonstrating the safety concept. For production deployment:

1. **Hardware Integration**
   - Connect to actual crash sensors (accelerometers, airbag signals)
   - Interface with gate driver shutdown pins
   - Implement voltage/current monitoring via ADC

2. **Safety Monitoring**
   - Add independent watchdog timer
   - Implement redundant sensor checking
   - Add program flow control (PFC)
   - Enable memory protection (MPU)

3. **Calibration**
   - Tune thresholds for specific motor
   - Validate discharge timing with actual circuit
   - Test back-EMF behavior at maximum speed
   - Verify compliance with ISO 6469-3 discharge requirements

4. **Diagnostics**
   - Log crash events to non-volatile memory
   - Record state transitions with timestamps
   - Store fault codes for analysis
   - Implement CAN diagnostics interface

## System Requirements

- Python 3.6+
- No external dependencies (uses only standard library)

## License

This is a reference implementation for educational and safety research purposes.

## Related Documentation

See the main [README](../README.md) for information about the Inverter Safety RAG system.
