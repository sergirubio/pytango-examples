# -*- coding: utf-8 -*-
#
# This file is part of the PowerSupply project
#
#
#
# Distributed under the terms of the GPL license.
# See LICENSE.txt for more info.

""" Power  Supply

Dummy Power Supply for testing
"""

# PyTango imports
import PyTango
from PyTango import DebugIt
from PyTango.server import run
from PyTango.server import Device, DeviceMeta
from PyTango.server import attribute, command
from PyTango.server import device_property
from PyTango import AttrQuality, DispLevel, DevState
from PyTango import AttrWriteType, PipeWriteType
# Additional import
# PROTECTED REGION ID(PowerSupply.additionnal_import) ENABLED START #
import time
# PROTECTED REGION END #    //  PowerSupply.additionnal_import

__all__ = ["PowerSupply", "main"]


class PowerSupply(Device):
    """
    Dummy Power Supply for testing
    """
    __metaclass__ = DeviceMeta
    # PROTECTED REGION ID(PowerSupply.class_variable) ENABLED START #

    # PROTECTED REGION END #    //  PowerSupply.class_variable

    # -----------------
    # Device Properties
    # -----------------

    LoadImpedance = device_property(
        dtype='double',
        mandatory=True
    )

    HWUpdatetime = device_property(
        dtype='double', default_value=1
    )

    # ----------
    # Attributes
    # ----------

    Voltage = attribute(
        dtype='double',
        access=AttrWriteType.READ_WRITE,
        label="PSV",
        unit="V",
        max_value=100,
        min_value=0,
        max_alarm=50,
        max_warning=30,
        memorized=True,
    )

    Current = attribute(
        dtype='double',
        unit="A",
    )

    # ---------------
    # General methods
    # ---------------

    def init_device(self):
        Device.init_device(self)
        # PROTECTED REGION ID(PowerSupply.init_device) ENABLED START #
        self.voltage = 0.
        self.current = 0.
        self.set_state(DevState.OFF)
        # PROTECTED REGION END #    //  PowerSupply.init_device

    def always_executed_hook(self):
        # PROTECTED REGION ID(PowerSupply.always_executed_hook) ENABLED START #
        t  = '%s state is %s\n' % (self.get_name(), self.get_state())
        t += 'Voltage = %s, Current = %s' % (self.voltage, self.current)
        self.set_status(t)
        print(t)
        # PROTECTED REGION END #    //  PowerSupply.always_executed_hook

    def delete_device(self):
        # PROTECTED REGION ID(PowerSupply.delete_device) ENABLED START #
        self.set_state(DevState.UNKNOWN)
        # PROTECTED REGION END #    //  PowerSupply.delete_device

    # ------------------
    # Attributes methods
    # ------------------

    def read_Voltage(self):
        # PROTECTED REGION ID(PowerSupply.Voltage_read) ENABLED START #
        return self.voltage
        # PROTECTED REGION END #    //  PowerSupply.Voltage_read

    def write_Voltage(self, value):
        # PROTECTED REGION ID(PowerSupply.Voltage_write) ENABLED START #
        self.voltage = value
        self.current = self.voltage / self.LoadImpedance
        # PROTECTED REGION END #    //  PowerSupply.Voltage_write

    def read_Current(self):
        # PROTECTED REGION ID(PowerSupply.Current_read) ENABLED START #
        return self.current
        # PROTECTED REGION END #    //  PowerSupply.Current_read


    # --------
    # Commands
    # --------

    @command(
    )
    @DebugIt()
    def On(self):
        # PROTECTED REGION ID(PowerSupply.On) ENABLED START #
        self.set_state(DevState.ON)
        # PROTECTED REGION END #    //  PowerSupply.On

    @command(
    )
    @DebugIt()
    def Off(self):
        # PROTECTED REGION ID(PowerSupply.Off) ENABLED START #
        self.set_state(DevState.OFF)
        # PROTECTED REGION END #    //  PowerSupply.Off

# ----------
# Run server
# ----------


def main(args=None, **kwargs):
    # PROTECTED REGION ID(PowerSupply.main) ENABLED START #
    return run((PowerSupply,), args=args, **kwargs)
    # PROTECTED REGION END #    //  PowerSupply.main

if __name__ == '__main__':
    main()
