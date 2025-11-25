# ISO 26262 Part 6: Product Development at the Software Level

## 1. General Overview
Part 6 of ISO 26262 specifies the requirements for product development at the software level for automotive applications. It covers the entire software lifecycle, from requirements specification to verification and validation.

## 2. Software Safety Requirements (SSR)
The SSRs are derived from the Technical Safety Requirements (TSRs).
*   **ASIL Decomposition**: If a requirement is ASIL D, it can be decomposed into two independent ASIL B(D) requirements.
*   **Freedom from Interference (FFI)**: Software components with different ASIL ratings (e.g., QM and ASIL D) must not interfere with each other. This is often achieved via memory protection (MPU) and temporal monitoring (Watchdogs).

## 3. Software Architectural Design
*   **High Complexity**: Avoid high complexity in software components.
*   **Strong Cohesion**: Components should have a single, well-defined purpose.
*   **Loose Coupling**: Minimize dependencies between components.
*   **Error Detection**: The architecture must include mechanisms to detect errors (e.g., Range Checks, Plausibility Checks, Control Flow Monitoring).

## 4. Software Unit Design and Implementation
*   **Coding Guidelines**: Use MISRA C/C++ to prevent common coding errors.
*   **No Dynamic Memory**: Avoid `malloc`/`free` in runtime code to prevent fragmentation and leaks.
*   **Stack Usage**: Stack depth must be calculated and monitored.

## 5. Software Verification
*   **Static Analysis**: Automated checks for code quality and MISRA compliance.
*   **Unit Testing**: Testing individual functions with coverage metrics (Statement, Branch, MC/DC).
    *   **ASIL D Requirement**: MC/DC (Modified Condition/Decision Coverage) is highly recommended for ASIL D.
