#!/usr/bin/env python3

import syslog

import Breezy

try:
    breezy = Breezy.FanControl.FanControl()
    syslog.syslog(syslog.LOG_INFO, "[breezy] > Starting. Temp: {}".format(breezy.get_temp()))
    while True:
        CPU_temp = breezy.get_temp()
        if CPU_temp > breezy.max_tmp:
            breezy.hotflow(CPU_temp)
        else:
            breezy.coldflow()

except KeyboardInterrupt:
    breezy = Breezy.FanControl.FanControl()
    breezy.clean_up()