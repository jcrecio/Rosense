"""
@author: Juan Carlos Recio Abad
@name: Rosense
@description: Robot for Monitoring Traffic Sensors Road M-40 from DGT Spain Application
"""
import sys
import urllib.request
import re
import time

INFOCARDGT_URI = 'http://infocar.dgt.es/etraffic/'

class Monitor:
    def __init__(self, km):
        self.kilometer = km
        self.logsensors = dict()

    def getsensorsuri(self):
        return INFOCARDGT_URI

    def getsensorscontent(self, querystring):
        url = self.getsensorsuri() + 'Buscador?'

        data = urllib.parse.urlencode(querystring).encode("utf-8")
        content = urllib.request.urlopen(url + data.decode())

        return content.read()
    
    def getsensordetail(self, url):
        content = urllib.request.urlopen(url)
        page = content.read()

        return self.applysensorfilters(page)
    
    def applysensorfilters(self, content):
        sensorfilter = '<li(.*?)<span class=\'popEcab\'>Intensidad</span>(.*?)</li>'
        sensorfilter += '(.*?)<li(.*?)<span class=\'popEcab\'>Velocidad media</span>(.*?)</li>'
        sensorfilter += '(.*?)<li(.*?)<span class=\'popEcab\'>Ocupaci\xf3n</span>(.*?)</li>'
        sensorfilter += '(.*?)<li(.*?)<span class=\'popEcab\'>Ligeros</span>(.*?)</li>'

        return re.compile(sensorfilter, re.DOTALL).findall(content.decode())

    def printdetailsensor(self, sensorid, detailsensor):
        print('____________________________')
        print('Sensor: M-40 ' + sensorid)
        try:
            current_sensor = [detailsensor[0][1], detailsensor[0][4], detailsensor[0][7], detailsensor[0][10]]

            if self.logsensors == {}:
                is_changed = True
            else:
                if self.logsensors.has_key(sensorid):
                    is_changed = self.informationhaschanged(self.logsensors[sensorid], current_sensor)
                else:
                    is_changed = True

            if is_changed:
                self.logsensor(sensorid, current_sensor)
                self.logsensors[sensorid] = current_sensor[0] + current_sensor[1] + current_sensor[2] + current_sensor[3]

                print('Sensor info logged into file.')
                print(self.logsensors[sensorid])
            else:
                print('No changes. Checked at ' + time.asctime(time.localtime(time.time())))
        except:
            print("Error retrieving data: ", sys.exc_info()[0])

    def getavailablesensors(self, km):
        fields = {'accion_buscar': 'Buscar',
                  'Camaras': 'true',
                  'caracter': 'acontencimiento',
                  'SensoresMeteorologico': 'true',
                  'SensoresTrafico': 'true',
                  'Paneles': 'true',
                  'IncidenciasOTROS': 'true',
                  'IncidenciasEVENTOS': 'true',
                  'IncidenciasRETENCION': 'true',
                  'IncidenciasOBRAS': 'true',
                  'IncidenciasMETEOROLOGICA': 'true',
                  'IncidenciasPUERTOS': 'true',
                  'lateralDetalles': 'sensores',
                  'pagina': 'buscador',
                  'poblacion': '',
                  'provincia': '28',
                  'carretera': '55188',
                  'PK': km,
                  'version': 'texto'
                  }
        filter = 'tipo=SensorTrafico&amp;nombre=M-40(.*?)elemGenCod=(.*?)onclick="JavaScript:window.open\(\'(.*?)\',\'SensTraf'
        content = self.getsensorscontent(fields)

        return re.compile(filter, re.DOTALL).findall(content.decode())
    
    def connectsensors(self, sensors):
        for sensor in sensors:
            formattedsensor = self.formatsensor(sensor[2])
            urisensor = self.getsensorsuri() + formattedsensor
            detailsensor = self.getsensordetail(urisensor)

            self.printdetailsensor((sensor[0]).replace('%', ' ').replace('&amp;', ''), detailsensor)

    def formatsensor(self, sensor):
        return sensor.replace('amp;', '')

    def informationhaschanged(self, previousinfo, currentinfo):
        return not (previousinfo == (currentinfo[0] + currentinfo[1] + currentinfo[2] + currentinfo[3]))
    

    
    def logsensor(self, sensorid, sensor):
        try:
            f = open("log.txt", "a")
            f.write('-\n')
            f.write('Sensor ' + sensorid + ' got new info at km ' + kilometer + ' registered at ' + time.asctime(time.localtime(time.time())) + ' \n')
            f.write('Intensity ' + sensor[0]+'\n')
            f.write('Average speed ' + sensor[1]+'\n')
            f.write('Density ' + sensor[2]+'\n')
            f.write('Light vehicles ' + sensor[3]+'\n')
        except:
            print('Sensor info could not be logged into file.')


def isnumeric(s):
    return s.isdigit()


def logstartmonitoring():
    try:
        f = open("log.txt", "a")
        f.write('Robot started at '+time.asctime(time.localtime(time.time()))+'\n')
        f.close()
    except:
        print('Sensor info logged into file.')


def initmessage():
    print('Robot for Monitoring Traffic Radars Road M-40 from DGT Spain 2013 Application')
    print('--------------------------------------------------------------------')    


def getkilometer():
    km = input("What kilometer would you like to monitor?")
    return km


def beginconnection(monitors):
    while 1:
        for monitor in monitors:
            print('---------------- Connected to M-40 sensors at km ' + monitor.kilometer + ' ---------------')

            sensors = monitor.getavailablesensors(monitor.kilometer)
            if sensors:
                sensors.pop(0)

            monitor.connectsensors(sensors)

        print('---------------- Next monitoring within ' + timeloop + ' seconds  ---------------')

        time.sleep(float(timeloop))


def startmonitors(monitors, kilometer):
    kms = kilometer.split(" ")

    for km in kms:
        if isnumeric(km):
            monitors.append(Monitor(km))
        else:
            try:
                arraykm = km.split("-")
                maxkm = int(arraykm[1])

                i = int(arraykm[0])
                while i < maxkm:
                    if isnumeric(i):
                        monitors.append(Monitor(str(i)))
                    i += 1
            except:
                print(km + ' is not a valid kilometer or interval.')
    beginconnection(monitors)


def gettimeloop():
    return input("Interval of time (seconds) to request for information: ")

initmessage()
logstartmonitoring()
kilometer = getkilometer()
timeloop = gettimeloop()
monitors = list()
startmonitors(monitors, kilometer)
