# Field Oriented Control (FOC) Safety Risks

## 1. Flux Weakening Risks
*   **Concept**: To spin the motor faster than its base speed, negative d-axis current ($I_d$) is injected to oppose the magnet flux.
*   **Hazard**: If the inverter shuts down (PWM off) while spinning at high speed in flux weakening mode, the Back-EMF voltage can rise significantly above the DC-link voltage.
*   **Consequence**: Uncontrolled braking torque (regenerative braking) or destruction of the DC-link capacitor and battery contactors.
*   **Mitigation**:
    *   **Active Short Circuit (ASC)**: Instead of opening all switches (Open Phase), turn on all bottom switches (or all top switches) to short the motor windings. This circulates the current and prevents over-voltage.

## 2. Sensor Faults
*   **Resolver/Encoder Offset**:
    *   **Risk**: If the angle offset is wrong, the torque command will be applied at the wrong angle.
    *   **Result**: Can cause reverse rotation or unintended acceleration.
    *   **Mitigation**: Runtime offset detection algorithms.
*   **Current Sensor Drift**:
    *   **Risk**: If the current sensor has an offset, the controller will try to compensate, creating real torque when none is requested.
    *   **Mitigation**: Sum of currents check ($I_u + I_v + I_w \approx 0$).

## 3. Overcurrent
*   **Risk**: Short circuit in the motor windings or IGBT/SiC shoot-through.
*   **Mitigation**: Hardware Desaturation (Desat) detection in the Gate Driver (fastest protection, < 2µs).
