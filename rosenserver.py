from bottle import Bottle, run, request
import rosense
import threading

app = Bottle()
ro = rosense.Rosense()


@app.route('/sensors')
def get_sensors():
    sensors = ro.sensors()
    return sensors


@app.post('/start')
def start_monitors():
    t = threading.Thread(target=ro.start, args=([request.json['kilometers']]))
    t.start()

    return "Rosense started"


run(app, host='localhost', port=5050)
