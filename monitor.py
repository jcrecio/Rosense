import sys
import time
import settings


class Monitor:

    def __init__(self, km, filters):
        self.kilometer = km
        self.filters = filters
        self.file_manager = None
        self.http_formatter = None

        self.log_sensors = dict()

    def get_sensor(self, url):
        page = self.http_formatter.get(url)
        return self.apply_filters(page)

    def apply_filters(self, content):
        return self.filters[settings.FILTER_SENSOR_DETAIL].apply(content)

    def log_detail_sensor(self, sid, detail):
        try:
            sensor = [detail[0][1], detail[0][4], detail[0][7], detail[0][10]]

            if self.changed(sid, sensor):
                self.log(sid, sensor)
                self.log_sensors[sid] = sensor[0] + sensor[1] + sensor[2] + sensor[3]
            else:
                self.file_manager.log('No changes. Checked at ' + time.asctime(time.localtime(time.time())))

        except Exception:
            self.file_manager.log("Error retrieving data: " + str(sys.exc_info()[0]))

    def sensors(self):
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
                  'PK': self.kilometer,
                  'version': 'texto'
                  }

        content = self.http_formatter.request(fields)

        return self.filters[settings.FILTER_SENSOR_OPTION].apply(content)

    def connect(self, sensors):
        for sensor in sensors:
            formatted_sensor = self.input_sensor(sensor[2])
            sid = sensor[0]
            sensor = self.get_sensor(formatted_sensor)

            self.log_detail_sensor(self.output_sensor(sid), sensor)

    def input_sensor(self, sensor):
        return sensor.replace('amp;', '')

    def output_sensor(self, sid):
        if not sid:
            return 'No available sensor information'
        return str(sid).replace('%', ' ').replace('&amp;', '')

    def changed(self, previous_info, current_info):
        return self.log_sensors != {} \
               or not (previous_info == (current_info[0] + current_info[1] + current_info[2] + current_info[3]))

    def log(self, sensor_id, sensor):

        intensity = sensor[0] if sensor[0] else None
        avgspeed = sensor[1] if sensor[1] else None
        density = sensor[2] if sensor[2] else None
        light = sensor[3] if sensor[3] else None

        traces = ['-\n',
                  'Sensor ' + sensor_id + ' got new info at km ' + str(self.kilometer)+ '\n',
                  'Intensity ' + intensity + '\n',
                  'Average speed ' + avgspeed + '\n',
                  'Density ' + density + '\n',
                  'Light vehicles ' + light + '\n']

        self.file_manager.log(traces)

    def get_sensors(self):
        return self.log_sensors
