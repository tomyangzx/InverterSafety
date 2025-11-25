# Research Guide: Inverter Software & ISO 26262 Safety

To build an expert-level RAG system, you need to populate the `data/` directory with high-quality technical documents. Since this is a private RAG, you can download PDFs and text files and place them there.

## Key Topics to Collect

### 1. 800V Inverter Specifics
*   **Silicon Carbide (SiC) MOSFETs**: Look for documents on switching frequencies (10kHz-100kHz), `dV/dt` challenges (EMI, insulation stress), and gate driver design.
*   **DC-Link Capacitor**: Sizing, safety discharge circuits (Active Discharge), and lifetime estimation.
*   **Thermal Management**: Cooling strategies for high power density inverters.

### 2. ISO 26262 Functional Safety (ASIL C/D)
*   **Part 6**: Product development at the software level. This is your bible.
*   **HARA (Hazard Analysis and Risk Assessment)**: Examples of HARA for inverters (e.g., "Unintended Torque", "Loss of Braking Torque").
*   **ASIL Decomposition**: How to break down ASIL D goals into redundant ASIL B(D) components.
*   **Safety Manuals**: Look for "Safety Manuals" from microcontroller vendors (Infineon AURIX, NXP S32K) or PMIC vendors.

### 3. Field Oriented Control (FOC) & Safety
*   **Flux Weakening**: Control strategies for high-speed operation and the safety risks associated with it (Back-EMF).
*   **MTPA (Maximum Torque Per Ampere)**: Efficiency algorithms.
*   **Sensor Plausibility**: Resolver/Encoder offset calibration and runtime checks.

### 4. Safety Mechanisms (The "E-Gas" Concept)
*   **Level 1**: Functional control (The main FOC loop).
*   **Level 2**: Function monitoring (The "Safety" path - checks if torque request matches actual torque).
*   **Level 3**: Controller monitoring (RAM/ROM checks, Program Flow Control, Watchdogs).
*   **Safe Torque Off (STO)**: Hardware safety paths.

## Recommended Search Terms & Documents

Search for these titles on Google Scholar, IEEE Xplore, or manufacturer websites:

1.  *"Standardized E-Gas Monitoring Concept for Gasoline/Diesel/Electric Engine Control Units"* (Essential for Level 2 monitoring).
2.  *"ISO 26262 Part 6: Product development at the software level"*.
3.  *"Infineon AURIX Safety Manual"* (or similar for your target MCU).
4.  *"SiC MOSFET Gate Driver Design for 800V Applications"*.
5.  *"Field Oriented Control of PMSM with Safety Plausibility Checks"*.
6.  *"Application Note: Safe Torque Off (STO) in Inverters"*.

## Where to find them?
*   **Manufacturer Application Notes**: Texas Instruments, Infineon, STMicroelectronics, Analog Devices often have detailed "Application Notes" for EV Inverters.
*   **Research Papers**: IEEE Xplore (if you have access) or arXiv.org.
*   **Standards**: ISO standards are paid, but you may have access through your organization.
