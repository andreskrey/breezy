#!/usr/bin/env python3

import os
import syslog
from time import sleep
import RPi.GPIO as GPIO

pin = 2
maxTMP = 65
targetTMPWhenCooling = 45


def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)
    return ()


def hotflow(current_temp):
    syslog.syslog(syslog.LOG_NOTICE, "Breezy: Hotflow stated. Temp: {}".format(current_temp))
    while current_temp > targetTMPWhenCooling:
        GPIO.output(pin, True)
        sleep(600)
        current_temp = gettemp()
        syslog.syslog(syslog.LOG_NOTICE, "Breezy: Hotflow continuing. Temp: {}".format(current_temp))


def coldflow():
    sleep(60)


def gettemp():
    res = os.popen('vcgencmd measure_temp').readline()
    return float(res.replace("temp=", "").replace("'C\n", ""))


try:
    syslog.syslog(syslog.LOG_INFO, "Breezy: Starting. Temp: {}".format(gettemp()))
    setup()
    while True:
        CPU_temp = gettemp()
        if CPU_temp > maxTMP:
            hotflow(CPU_temp)
        else:
            coldflow()

except KeyboardInterrupt:
    GPIO.output(pin, False)
