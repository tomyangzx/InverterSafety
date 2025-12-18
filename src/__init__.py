"""
InverterSafety - Safety-critical components for 800V inverter systems
"""

from .crash_handler import CrashHandler, SafetyState

__all__ = ['CrashHandler', 'SafetyState']
