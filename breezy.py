#!/usr/bin/env python3

import os
import syslog
from time import sleep
import yaml
import RPi.GPIO as GPIO

class Breezy:
    # Default values
    pin = 2
    max_tmp = 65
    target_cool_tmp = 45

    def __init__(self):
        with open('config.yml', 'r') as stream:
            data_loaded = yaml.load(stream)
            self.pin = data_loaded['breezy']['pin']
            self.max_tmp = data_loaded['breezy']['max_tmp']
            self.target_cool_tmp = data_loaded['breezy']['target_cool_tmp']
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)

    def hotflow(self, current_temp):
        GPIO.output(self.pin, True)
        syslog.syslog(syslog.LOG_NOTICE, "[breezy] > Hotflow started. Temp: {}".format(current_temp))
        while current_temp > self.target_cool_tmp:
            sleep(600)
            current_temp = self.get_temp()

            # Stop process if we reach target temp
            if current_temp < self.target_cool_tmp:
                break

            syslog.syslog(syslog.LOG_NOTICE, "[breezy] > Hotflow continuing. Temp: {}".format(current_temp))
        syslog.syslog(syslog.LOG_NOTICE, "[breezy] > Hotflow stopped. Temp: {}".format(current_temp))

    def coldflow(self):
        GPIO.output(self.pin, False)
        sleep(60)

    def get_temp(self):
        res = os.popen('vcgencmd measure_temp').readline()
        return float(res.replace("temp=", "").replace("'C\n", ""))

    def clean_up(self):
        GPIO.output(self.pin, False)


try:
    breezy = Breezy()
    syslog.syslog(syslog.LOG_INFO, "[breezy] > Starting. Temp: {}".format(breezy.get_temp()))
    while True:
        CPU_temp = breezy.get_temp()
        if CPU_temp > breezy.max_tmp:
            breezy.hotflow(CPU_temp)
        else:
            breezy.coldflow()

except KeyboardInterrupt:
    breezy = Breezy()
    breezy.clean_up()
