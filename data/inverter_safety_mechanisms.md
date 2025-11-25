# Inverter Safety Mechanisms (E-Gas Concept)

## 1. The 3-Level Monitoring Concept (E-Gas)
This is the standard architecture for controlling torque in EVs to prevent "Unintended Acceleration" or "Unintended Deceleration".

### Level 1: Functional Level (QM)
*   **Role**: Performs the main motor control (Field Oriented Control).
*   **Inputs**: Pedal position, Battery voltage, Motor speed.
*   **Output**: PWM signals to the Gate Drivers.
*   **Safety**: This level is NOT trusted for safety. It focuses on performance.

### Level 2: Function Monitoring (ASIL C/D)
*   **Role**: Monitors the Level 1 output to ensure it is plausible.
*   **Mechanism**:
    *   Calculates a "Permissible Torque" based on pedal position and limits.
    *   Compares "Actual Torque" (estimated from currents) vs. "Permissible Torque".
    *   **Fault Reaction**: If the difference exceeds a threshold for a specific time (e.g., > 50Nm for > 200ms), it triggers a Safe State (e.g., Open Phase / STO).
*   **Independence**: Must run on a separate core or be logically separated from Level 1.

### Level 3: Controller Monitoring (ASIL D)
*   **Role**: Ensures the microcontroller hardware is working correctly.
*   **Checks**:
    *   **RAM/ROM Tests**: Check for bit flips (ECC errors).
    *   **Program Flow Control (PFC)**: Ensures code executes in the correct order (using checkpoints).
    *   **ADC Diagnostics**: Checks if ADC pins are stuck or drifting.
    *   **Watchdog**: External watchdog (Window Watchdog) to reset the MCU if it hangs.

## 2. Safe Torque Off (STO)
*   **Definition**: A hardware-only safety function that prevents the inverter from generating torque.
*   **Mechanism**: It cuts the power to the Gate Drivers directly, bypassing the microcontroller.
*   **Usage**: Triggered by the Level 2/3 monitoring or external crash signals.
