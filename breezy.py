#!/usr/bin/env python3

import os
import syslog
from time import sleep
import yaml
import RPi.GPIO as GPIO


class Breezy:
    pin = 2
    max_tmp = 65
    target_cool_tmp = 45
    GPIO = None

    def __init__(self):
        with open('config.yml', 'r') as stream:
            data_loaded = yaml.load(stream)
            self.pin = data_loaded['breezy']['pin']
            self.max_tmp = data_loaded['breezy']['max_tmp']
            self.target_cool_tmp = data_loaded['breezy']['target_cool_tmp']
        self.GPIO = __import__('RPi.GPIO')
        self.GPIO.setwarnings(False)
        self.GPIO.setmode(self.GPIO.BCM)
        self.GPIO.setup(self.pin, self.GPIO.OUT)

    def hotflow(self, current_temp):
        syslog.syslog(syslog.LOG_NOTICE, "Breezy: Hotflow stated. Temp: {}".format(current_temp))
        while current_temp > self.target_cool_tmp:
            self.GPIO.output(self.pin, True)
            sleep(600)
            current_temp = self.get_temp()
            syslog.syslog(syslog.LOG_NOTICE, "Breezy: Hotflow continuing. Temp: {}".format(current_temp))

    def coldflow(self):
        sleep(60)

    def get_temp(self):
        res = os.popen('vcgencmd measure_temp').readline()
        return float(res.replace("temp=", "").replace("'C\n", ""))


try:
    breezy = Breezy()
    syslog.syslog(syslog.LOG_INFO, "Breezy: Starting. Temp: {}".format(breezy.get_temp()))
    while True:
        CPU_temp = breezy.get_temp()
        if CPU_temp > breezy.max_tmp:
            breezy.hotflow(CPU_temp)
        else:
            breezy.coldflow()

except KeyboardInterrupt:
    GPIO.output(breezy.pin, False)
