# -*- coding: utf-8 -*-
#
# This file is part of the SKAPowerSupplyGroup project
#
#
#
# Distributed under the terms of the GPL license.
# See LICENSE.txt for more info.

""" SKA Power Supply Group

Description
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
# PROTECTED REGION ID(SKAPowerSupplyGroup.additionnal_import) ENABLED START #
from skabase.SKABaseDevice import SKABaseDevice
import tango
import tango.client
import time
import math
import traceback
# PROTECTED REGION END #    //  SKAPowerSupplyGroup.additionnal_import

__all__ = ["SKAPowerSupplyGroup", "main"]


class SKAPowerSupplyGroup(SKABaseDevice):
    """
    Description
    """
    __metaclass__ = DeviceMeta
    # PROTECTED REGION ID(SKAPowerSupplyGroup.class_variable) ENABLED START #
    # PROTECTED REGION END #    //  SKAPowerSupplyGroup.class_variable

    # -----------------
    # Device Properties
    # -----------------





    PowerSupplyGroup = device_property(
        dtype='str',
        mandatory=True
    )

    # ----------
    # Attributes
    # ----------










    PowerSupplyList = attribute(
        dtype=('str',),
        max_dim_x=2048,
    )

    Current = attribute(
        dtype=('double',),
        max_dim_x=128,
    )

    Voltage = attribute(
        dtype=('double',),
        access=AttrWriteType.READ_WRITE,
        max_dim_x=128,
    )

    # ---------------
    # General methods
    # ---------------

    def init_device(self):
        SKABaseDevice.init_device(self)
        # PROTECTED REGION ID(SKAPowerSupplyGroup.init_device) ENABLED START #
        self.tg = tango.Group('power supplies')
        self.setpoints = [0.0]
        # name of the group for the Power Supplies
        self.tg.add(self.PowerSupplyGroup)
        # PROTECTED REGION END #    //  SKAPowerSupplyGroup.init_device

    def always_executed_hook(self):
        # PROTECTED REGION ID(SKAPowerSupplyGroup.always_executed_hook) ENABLED START #
        print(self.PowerSupplyGroup)
        print(self.tg.get_device_list())
        r = self.tg.read_attribute('State')
        states = {}
        try:
            for b in r:
                name = b.dev_name()
                value = b.get_data().value if not b.has_failed() else DevState.FAULT
                states[name] = value
            self.set_status('\n'.join('%s: %s' % t for t in states.items()))
            stateset = list(set(states.values()))
            if not stateset:
                self.set_state(DevState.INIT)
            elif DevState.FAULT in stateset:
                self.set_state(DevState.FAULT)
            elif DevState.ALARM in stateset:
                self.set_state(DevState.ALARM)
            elif len(stateset) != 1:
                self.set_state(DevState.UNKNOWN)
            else:
                self.set_state(stateset[0])
        except:
            self.logger.error(traceback.format_exc())
        # PROTECTED REGION END #    //  SKAPowerSupplyGroup.always_executed_hook

    def delete_device(self):
        # PROTECTED REGION ID(SKAPowerSupplyGroup.delete_device) ENABLED START #
        pass
        # PROTECTED REGION END #    //  SKAPowerSupplyGroup.delete_device

    # ------------------
    # Attributes methods
    # ------------------

    def read_PowerSupplyList(self):
        # PROTECTED REGION ID(SKAPowerSupplyGroup.PowerSupplyList_read) ENABLED START #
        devs = list(self.tg.get_device_list())
        if not len(devs):
            self.set_state(DevState.FAULT)
            raise Exception('No Power Supplies running?')
        return list(sorted(devs))
        # PROTECTED REGION END #    //  SKAPowerSupplyGroup.PowerSupplyList_read

    def read_Current(self):
        # PROTECTED REGION ID(SKAPowerSupplyGroup.Current_read) ENABLED START #
        r = self.tg.read_attribute('Current')
        currents = {}
        try:
            for b in r:
                name = b.dev_name()
                value = b.get_data().value if not b.has_failed() else math.nan
                currents[name] = value
        except:
            self.logger.error(traceback.format_exc())
        return list(v for k,v in sorted(currents.items()))
        # PROTECTED REGION END #    //  SKAPowerSupplyGroup.Current_read

    def read_Voltage(self):
        # PROTECTED REGION ID(SKAPowerSupplyGroup.Voltage_read) ENABLED START #
        r = self.tg.read_attribute('Voltage')
        voltages = {}
        try:
            for b in r:
                name = b.dev_name()
                value = b.get_data().value if not b.has_failed() else math.nan
                if value != self.setpoints[0]:
                    self.set_state(DevState.FAULT)
                voltages[name] = value
        except:
            self.logger.error(traceback.format_exc())
        return list(v for k,v in sorted(voltages.items()))
            
        
        # PROTECTED REGION END #    //  SKAPowerSupplyGroup.Voltage_read

    def write_Voltage(self, value):
        # PROTECTED REGION ID(SKAPowerSupplyGroup.Voltage_write) ENABLED START #
        r = self.tg.write_attribute('Voltage', value)
        self.setpoints = value
        # PROTECTED REGION END #    //  SKAPowerSupplyGroup.Voltage_write


    # --------
    # Commands
    # --------

    @command(
    )
    @DebugIt()
    def On(self):
        # PROTECTED REGION ID(SKAPowerSupplyGroup.On) ENABLED START #
        self.tg.command_inout('On')
        # PROTECTED REGION END #    //  SKAPowerSupplyGroup.On

    @command(
    )
    @DebugIt()
    def Off(self):
        # PROTECTED REGION ID(SKAPowerSupplyGroup.Off) ENABLED START #
        self.tg.command_inout('Off')
        # PROTECTED REGION END #    //  SKAPowerSupplyGroup.Off

# ----------
# Run server
# ----------


def main(args=None, **kwargs):
    # PROTECTED REGION ID(SKAPowerSupplyGroup.main) ENABLED START #
    return run((SKAPowerSupplyGroup,), args=args, **kwargs)
    # PROTECTED REGION END #    //  SKAPowerSupplyGroup.main

if __name__ == '__main__':
    main()
