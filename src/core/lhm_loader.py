"""Load the bundled .NET Framework hardware-monitor library through pythonnet."""

import os
import sys
import clr

_LOADED = False
_Computer = None
_SensorType = None
_HardwareType = None


def ensure_loaded(base_dir=None, logger=None):
    """Return (Computer, SensorType, HardwareType) from the bundled net472 runtime."""
    global _LOADED, _Computer, _SensorType, _HardwareType
    if _LOADED:
        return _Computer, _SensorType, _HardwareType

    if base_dir is None:
        base_dir = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    library_dir = os.path.join(base_dir, "assets", "LHM_0.9.6_lib", "net472")
    dll_path = os.path.join(library_dir, "LibreHardwareMonitorLib.dll")
    if not os.path.isfile(dll_path):
        raise FileNotFoundError(f"Bundled hardware-monitor library is missing: {dll_path}")

    # pythonnet and the CLR need the adjacent assemblies from the same release.
    if library_dir not in sys.path:
        sys.path.append(library_dir)
    message = "Loading LibreHardwareMonitorLib 0.9.6 (.NET Framework 4.7.2)"
    if logger is not None and hasattr(logger, "add_log"):
        try:
            logger.add_log(message)
        except Exception:
            pass
    else:
        print(message)

    clr.AddReference(dll_path)
    from LibreHardwareMonitor.Hardware import Computer, SensorType, HardwareType
    _Computer, _SensorType, _HardwareType = Computer, SensorType, HardwareType
    _LOADED = True
    return _Computer, _SensorType, _HardwareType


def get_types(base_dir=None):
    return ensure_loaded(base_dir)
