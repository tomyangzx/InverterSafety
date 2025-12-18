"""
Unit tests for crash_handler.py
Tests the safety state machine and crash sequence execution.
"""

import unittest
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from crash_handler import CrashHandler, SafetyState


class TestCrashHandler(unittest.TestCase):
    """Test cases for CrashHandler class"""
    
    def test_initialization(self):
        """Test crash handler initialization"""
        handler = CrashHandler(
            dc_link_voltage=800.0,
            motor_speed_rpm=5000.0,
            discharge_time_ms=100,
            asc_time_ms=50
        )
        
        self.assertEqual(handler.dc_link_voltage, 800.0)
        self.assertEqual(handler.motor_speed_rpm, 5000.0)
        self.assertEqual(handler.discharge_time_ms, 100)
        self.assertEqual(handler.asc_time_ms, 50)
        self.assertEqual(handler.current_state, SafetyState.NORMAL_OPERATION)
    
    def test_high_speed_crash_sequence(self):
        """Test crash sequence with high motor speed (requires ASC)"""
        handler = CrashHandler(
            dc_link_voltage=800.0,
            motor_speed_rpm=5000.0,  # Above threshold
            discharge_time_ms=10,  # Short time for testing
            asc_time_ms=5
        )
        
        result = handler.execute_crash_sequence()
        
        # Verify sequence completed successfully
        self.assertTrue(result)
        
        # Verify final state is SAFE_STATE
        self.assertEqual(handler.get_current_state(), SafetyState.SAFE_STATE)
        
        # Verify voltage was reduced
        self.assertLess(handler.dc_link_voltage, 800.0)
        
        # Verify motor speed was reduced
        self.assertLess(handler.motor_speed_rpm, 5000.0)
    
    def test_low_speed_crash_sequence(self):
        """Test crash sequence with low motor speed (ASC not required)"""
        handler = CrashHandler(
            dc_link_voltage=800.0,
            motor_speed_rpm=1000.0,  # Below threshold
            discharge_time_ms=10,
            asc_time_ms=5
        )
        
        result = handler.execute_crash_sequence()
        
        # Verify sequence completed successfully
        self.assertTrue(result)
        
        # Verify final state is SAFE_STATE
        self.assertEqual(handler.get_current_state(), SafetyState.SAFE_STATE)
        
        # Verify voltage was reduced
        self.assertLess(handler.dc_link_voltage, 800.0)
    
    def test_stationary_crash_sequence(self):
        """Test crash sequence with motor stopped"""
        handler = CrashHandler(
            dc_link_voltage=800.0,
            motor_speed_rpm=0.0,
            discharge_time_ms=10,
            asc_time_ms=5
        )
        
        result = handler.execute_crash_sequence()
        
        # Verify sequence completed successfully
        self.assertTrue(result)
        
        # Verify final state is SAFE_STATE
        self.assertEqual(handler.get_current_state(), SafetyState.SAFE_STATE)
    
    def test_asc_threshold_logic(self):
        """Test ASC activation threshold logic"""
        # Test just above threshold
        handler_above = CrashHandler(
            dc_link_voltage=800.0,
            motor_speed_rpm=3001.0,  # Just above threshold (3000 RPM)
            discharge_time_ms=10,
            asc_time_ms=5
        )
        handler_above.execute_crash_sequence()
        
        # Motor should be decelerated when ASC is used
        self.assertLess(handler_above.motor_speed_rpm, 3001.0)
        
        # Test just below threshold
        handler_below = CrashHandler(
            dc_link_voltage=800.0,
            motor_speed_rpm=2999.0,  # Just below threshold
            discharge_time_ms=10,
            asc_time_ms=5
        )
        initial_speed = handler_below.motor_speed_rpm
        handler_below.execute_crash_sequence()
        
        # Motor speed should not change when ASC is skipped
        self.assertEqual(handler_below.motor_speed_rpm, initial_speed)
    
    def test_discharge_voltage_reduction(self):
        """Test that active discharge reduces voltage"""
        handler = CrashHandler(
            dc_link_voltage=800.0,
            motor_speed_rpm=0.0,
            discharge_time_ms=10,
            asc_time_ms=5
        )
        
        initial_voltage = handler.dc_link_voltage
        handler.execute_crash_sequence()
        final_voltage = handler.dc_link_voltage
        
        # Voltage should be reduced
        self.assertLess(final_voltage, initial_voltage)
        
        # Voltage should be reduced by approximately 30%
        expected_voltage = initial_voltage * 0.7
        self.assertAlmostEqual(final_voltage, expected_voltage, places=1)
    
    def test_state_transitions(self):
        """Test that states transition in correct order"""
        handler = CrashHandler(
            dc_link_voltage=800.0,
            motor_speed_rpm=0.0,
            discharge_time_ms=10,
            asc_time_ms=5
        )
        
        # Initial state
        self.assertEqual(handler.current_state, SafetyState.NORMAL_OPERATION)
        
        # Execute sequence
        handler.execute_crash_sequence()
        
        # Final state should be SAFE_STATE
        self.assertEqual(handler.current_state, SafetyState.SAFE_STATE)
    
    def test_different_voltage_levels(self):
        """Test crash handler with different DC-link voltage levels"""
        voltages = [400.0, 600.0, 800.0, 900.0]
        
        for voltage in voltages:
            with self.subTest(voltage=voltage):
                handler = CrashHandler(
                    dc_link_voltage=voltage,
                    motor_speed_rpm=1000.0,
                    discharge_time_ms=10,
                    asc_time_ms=5
                )
                
                result = handler.execute_crash_sequence()
                
                # Sequence should succeed for all voltages
                self.assertTrue(result)
                
                # Final state should be SAFE_STATE
                self.assertEqual(handler.current_state, SafetyState.SAFE_STATE)
                
                # Voltage should be reduced
                self.assertLess(handler.dc_link_voltage, voltage)
    
    def test_custom_thresholds(self):
        """Test crash handler with custom safety thresholds"""
        handler = CrashHandler(
            dc_link_voltage=800.0,
            motor_speed_rpm=4000.0,
            discharge_time_ms=10,
            asc_time_ms=5
        )
        
        # Modify threshold
        handler.high_speed_threshold_rpm = 5000.0
        
        # With higher threshold, ASC should be skipped
        initial_speed = handler.motor_speed_rpm
        handler.execute_crash_sequence()
        
        # Motor speed should not be reduced (ASC not activated)
        self.assertEqual(handler.motor_speed_rpm, initial_speed)


class TestSafetyGoals(unittest.TestCase):
    """Test compliance with safety goals"""
    
    def test_sg1_prevent_unintended_torque(self):
        """
        SG1: Prevent unintended torque during crash event (ASIL D)
        Verify that ASO state disables all torque generation
        """
        handler = CrashHandler(
            dc_link_voltage=800.0,
            motor_speed_rpm=2000.0,
            discharge_time_ms=10,
            asc_time_ms=5
        )
        
        handler.execute_crash_sequence()
        
        # Final state should prevent torque generation (ASO or SAFE_STATE)
        self.assertIn(handler.current_state, 
                     [SafetyState.ASO, SafetyState.SAFE_STATE])
    
    def test_sg2_safe_discharge(self):
        """
        SG2: Safely discharge 800V DC-link to prevent electrical hazard (ASIL D)
        Verify that active discharge reduces voltage
        """
        handler = CrashHandler(
            dc_link_voltage=800.0,
            motor_speed_rpm=0.0,
            discharge_time_ms=10,
            asc_time_ms=5
        )
        
        initial_voltage = handler.dc_link_voltage
        handler.execute_crash_sequence()
        
        # Voltage should be significantly reduced
        voltage_reduction = initial_voltage - handler.dc_link_voltage
        self.assertGreater(voltage_reduction, 100.0)  # At least 100V reduction
    
    def test_sg3_prevent_back_emf(self):
        """
        SG3: Prevent back-EMF overvoltage during high-speed shutdown (ASIL C)
        Verify that ASC is activated for high-speed conditions
        """
        handler = CrashHandler(
            dc_link_voltage=800.0,
            motor_speed_rpm=6000.0,  # High speed
            discharge_time_ms=10,
            asc_time_ms=5
        )
        
        initial_speed = handler.motor_speed_rpm
        handler.execute_crash_sequence()
        
        # Motor should be decelerated (ASC was activated)
        self.assertLess(handler.motor_speed_rpm, initial_speed)
        
        # Motor should be slowed down significantly
        speed_reduction = initial_speed - handler.motor_speed_rpm
        self.assertGreater(speed_reduction, 1000.0)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions"""
    
    def test_zero_voltage(self):
        """Test crash handler with zero DC-link voltage"""
        handler = CrashHandler(
            dc_link_voltage=0.0,
            motor_speed_rpm=0.0,
            discharge_time_ms=10,
            asc_time_ms=5
        )
        
        result = handler.execute_crash_sequence()
        
        # Should still complete successfully
        self.assertTrue(result)
    
    def test_very_high_speed(self):
        """Test crash handler with very high motor speed"""
        handler = CrashHandler(
            dc_link_voltage=800.0,
            motor_speed_rpm=15000.0,  # Very high speed
            discharge_time_ms=10,
            asc_time_ms=5
        )
        
        result = handler.execute_crash_sequence()
        
        # Should complete successfully
        self.assertTrue(result)
        
        # ASC should be activated (motor speed reduced)
        self.assertLess(handler.motor_speed_rpm, 15000.0)
    
    def test_exact_threshold_speed(self):
        """Test crash handler at exact threshold speed"""
        handler = CrashHandler(
            dc_link_voltage=800.0,
            motor_speed_rpm=3000.0,  # Exact threshold
            discharge_time_ms=10,
            asc_time_ms=5
        )
        
        result = handler.execute_crash_sequence()
        
        # Should complete successfully
        self.assertTrue(result)
        
        # At exact threshold, ASC should NOT be activated (> threshold required)
        self.assertEqual(handler.motor_speed_rpm, 3000.0)


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)
