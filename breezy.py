#!/usr/bin/env python3

import os
import syslog
from time import sleep
import yaml
import RPi.GPIO as GPIO

pin = 2
max_tmp = 65
target_cool_tmp = 45


def setup():
    with open('config.yml', 'r') as stream:
        data_loaded = yaml.load(stream)
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)
    return ()


def hotflow(current_temp):
    syslog.syslog(syslog.LOG_NOTICE, "Breezy: Hotflow stated. Temp: {}".format(current_temp))
    while current_temp > target_cool_tmp:
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
        if CPU_temp > max_tmp:
            hotflow(CPU_temp)
        else:
            coldflow()

except KeyboardInterrupt:
    GPIO.output(pin, False)
