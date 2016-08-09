"""
@author: Juan Carlos Recio Abad
@name: Rosense
@description: Robot for Monitoring DGT Traffic Information from Road M-40 Spain
"""

import time
import json
import filemanager
import httpservice
import monitor
import settings
from filter import Filter

INFO_CAR_DGT_URI = 'http://infocar.dgt.es/etraffic/'
LOG_FILE = "log.dat"


class Rosense(object):
    FILTERS = {settings.FILTER_SENSOR_DETAIL:
                   Filter('<li(.*?)<span class=\'popEcab\'>Intensidad</span>(.*?)</li>(.*?)<li(.*?)' \
                          '<span class=\'popEcab\'>Velocidad media</span>(.*?)</li>(.*?)<li(.*?)<span ' \
                          'class=\'popEcab\'>Ocupaci\xf3n</span>(.*?)</li>(.*?)<li(.*?)<span class=\'pop' \
                          'Ecab\'>Ligeros</span>(.*?)</li>'),
               settings.FILTER_SENSOR_OPTION:
                   Filter('tipo=SensorTrafico&amp;nombre=M-40(.*?)elemGenCod=(.*?)onclick="JavaScript:' \
                          'window.open\(\'(.*?)\',\'SensTraf')}

    __instance = None

    def __new__(cls):
        if Rosense.__instance is None:
            Rosense.__instance = object.__new__(cls)
        return Rosense.__instance

    def __init__(self):
        self.file_manager = filemanager.FileManager(LOG_FILE)
        self.http_formatter = httpservice.HttpService(INFO_CAR_DGT_URI)

        self.monitors = list()

    def log_start(self):
        self.file_manager.log('Robot started at ' + time.asctime(time.localtime(time.time())))

    def connect(self, time_loop):
        while True:
            self.connect_monitors()

            # Connects to the source every 'time_loop' seconds to get new information
            time.sleep(float(time_loop))

    def connect_monitors(self):
        for mon in self.monitors:
            sensors = mon.sensors()

        if sensors:
            sensors.pop(0)

        mon.connect(sensors)  # TODO: Code smell, monitor extracts sensors and pass them in itself!?

    def add_monitor(self, kilometer):
        mon = monitor.Monitor(kilometer, Rosense.FILTERS)

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
