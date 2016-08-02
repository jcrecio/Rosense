"""
@author: Juan Carlos Recio Abad
@name: Rosense
@description: Robot for Monitoring DGT Traffic Information from Road M-40 Spain
"""

import time
import json
import filemanager
import httpformatter
import monitor

INFO_CAR_DGT_URI = 'http://infocar.dgt.es/etraffic/'
LOG_FILE = "log.dat"


class Rosense(object):

    __instance = None

    def __new__(cls):
        if Rosense.__instance is None:
            Rosense.__instance = object.__new__(cls)
        return Rosense.__instance

    def __init__(self):
        self.file_manager = filemanager.FileManager(LOG_FILE)
        self.http_formatter = httpformatter.HttpFormatter(INFO_CAR_DGT_URI)

        self.monitors = list()

    def log_start(self):
        self.file_manager.log('Robot started at ' + time.asctime(time.localtime(time.time())))

    def connect(self, time_loop):
        while True:
            for mon in self.monitors:
                sensors = mon.sensors()

                if sensors:
                    sensors.pop(0)

                mon.connect(sensors)

            # Connects to the source every 'time_loop' seconds to get new information
            time.sleep(float(time_loop))

    def add_monitor(self, kilometer):
        mon = monitor.Monitor(kilometer)

        mon.file_manager = self.file_manager
        mon.http_formatter = self.http_formatter

        self.monitors.append(mon)

    def add_monitors(self, kilometers):
        for kilometer in kilometers:
            self.add_monitor(kilometer)

    def start(self, kms):
        self.log_start()
        self.add_monitors(kms)
        self.connect(30)

    # Gets the last logged information of the sensors on the given kilometers
    def sensors(self):
        sensors_print = dict()

        for mon in self.monitors:
            sensors_list = mon.get_sensors()
            if sensors_list:
                sensors_print[mon.kilometer] = sensors_list

        content = json.dumps(sensors_print)
        return content

