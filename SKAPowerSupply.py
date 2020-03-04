# -*- coding: utf-8 -*-
#
# This file is part of the SKAPowerSupply project
#
#
#
# Distributed under the terms of the GPL license.
# See LICENSE.txt for more info.

""" Power Supply for SKA

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
#from SKABaseDevice import SKABaseDevice
# Additional import
# PROTECTED REGION ID(SKAPowerSupply.additionnal_import) ENABLED START #
import time
from skabase.SKABaseDevice import SKABaseDevice #<<<
# PROTECTED REGION END #    //  SKAPowerSupply.additionnal_import

__all__ = ["SKAPowerSupply", "main"]


class SKAPowerSupply(SKABaseDevice):
    """
    """
    __metaclass__ = DeviceMeta
    # PROTECTED REGION ID(SKAPowerSupply.class_variable) ENABLED START #
    
    @command()
    def Reset(self):
        """ Reset command overloading SKABaseDevice.Reset """
        self.set_state(DevState.OFF)
        
    def is_Reset_allowed(self):
        return self.get_state() in [DevState.FAULT,DevState.RUNNING,DevState.ON]
        
    def read_attr_hardware(self,*args):
        self.logger.info('Adding delay of %s seconds' % self.HWUpdateTime)
        time.sleep(self.HWUpdateTime)
        
    def set_output_current(self):
        try:
            self.current = self.voltage / self.LoadImpedance
            return True
        except:
            self.set_state(DevState.FAULT)
            self.current = 0
            self.voltage = 0
            return False
    
    
    # PROTECTED REGION END #    //  SKAPowerSupply.class_variable

    # -----------------
    # Device Properties
    # -----------------





    LoadImpedance = device_property(
        dtype='double',
    )

    HWUpdateTime = device_property(
        dtype='double', default_value=1
    )

    # ----------
    # Attributes
    # ----------









    Voltage = attribute(
        dtype='double',
        access=AttrWriteType.READ_WRITE,
        label="V",
        unit="V",
        max_value=100,
        min_value=0,
        max_alarm=70,
        min_alarm=0,
        max_warning=60,
        min_warning=0,
    )

    Current = attribute(
        dtype='double',
        label="I",
        unit="A",
    )


    # ---------------
    # General methods
    # ---------------

    def init_device(self):
        SKABaseDevice.init_device(self)
        # PROTECTED REGION ID(SKAPowerSupply.init_device) ENABLED START #
        self.voltage = 0.0
        self.current = 0.0
        self.set_state(DevState.OFF)
        # PROTECTED REGION END #    //  SKAPowerSupply.init_device

    def always_executed_hook(self):
        # PROTECTED REGION ID(SKAPowerSupply.always_executed_hook) ENABLED START #
        st   = '%s is %s' % (self.get_name(), self.get_state())
        st += '\nVoltage = %s, Current = %s' % (self.voltage, self.current)
        self.set_status(st)
        self.logger.info(self.get_status())
        # PROTECTED REGION END #    //  SKAPowerSupply.always_executed_hook

    def delete_device(self):
        # PROTECTED REGION ID(SKAPowerSupply.delete_device) ENABLED START #
        self.set_state(DevState.UNKNOWN)
        # PROTECTED REGION END #    //  SKAPowerSupply.delete_device

    # ------------------
    # Attributes methods
    # ------------------

    def read_Voltage(self):
        # PROTECTED REGION ID(SKAPowerSupply.Voltage_read) ENABLED START #
        self.logger.info('read_Voltage')
        return self.voltage
        # PROTECTED REGION END #    //  SKAPowerSupply.Voltage_read

    def write_Voltage(self, value):
        # PROTECTED REGION ID(SKAPowerSupply.Voltage_write) ENABLED START #
        self.voltage = value
        if self.get_state() == DevState.ON:
            self.set_output_current()
        # PROTECTED REGION END #    //  SKAPowerSupply.Voltage_write

    def is_Voltage_allowed(self, attr):
        # PROTECTED REGION ID(SKAPowerSupply.is_Voltage_allowed) ENABLED START #
        if attr==attr.READ_REQ:
            return True
        else:
            return self.get_state() not in [DevState.FAULT]
        # PROTECTED REGION END #    //  SKAPowerSupply.is_Voltage_allowed

    def read_Current(self):
        # PROTECTED REGION ID(SKAPowerSupply.Current_read) ENABLED START #
        self.logger.info('read_Current')
        return self.current
        # PROTECTED REGION END #    //  SKAPowerSupply.Current_read


    # --------
    # Commands
    # --------

    @command(
    )
    @DebugIt()
    def On(self):
        # PROTECTED REGION ID(SKAPowerSupply.On) ENABLED START #
        if self.set_output_current():
            self.set_state(DevState.ON)
        # PROTECTED REGION END #    //  SKAPowerSupply.On

    def is_On_allowed(self):
        # PROTECTED REGION ID(SKAPowerSupply.is_On_allowed) ENABLED START #
        return self.get_state() not in [DevState.ON,DevState.FAULT,DevState.RUNNING]
        # PROTECTED REGION END #    //  SKAPowerSupply.is_On_allowed

    @command(
    )
    @DebugIt()
    def Off(self):
        # PROTECTED REGION ID(SKAPowerSupply.Off) ENABLED START #
        self.set_state(DevState.OFF)
        # PROTECTED REGION END #    //  SKAPowerSupply.Off     

    def is_Off_allowed(self):
        # PROTECTED REGION ID(SKAPowerSupply.is_Off_allowed) ENABLED START #
        return self.get_state() not in [DevState.OFF,DevState.FAULT]
        # PROTECTED REGION END #    //  SKAPowerSupply.is_Off_allowed

# ----------
# Run server
# ----------


def main(args=None, **kwargs):
    # PROTECTED REGION ID(SKAPowerSupply.main) ENABLED START #
    return run((SKAPowerSupply,), args=args, **kwargs)
    # PROTECTED REGION END #    //  SKAPowerSupply.main

if __name__ == '__main__':
    main()
