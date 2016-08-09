from bottle import Bottle, run, request
import rosense
import threading

app = Bottle()
ro = rosense.Rosense()


# GET /sensors
@app.route('/sensors')
def get_sensors():

    sensors = ro.sensors()
    return sensors


# POST /rosense/start, from body: kilometers
@app.post('/rosense/start')
def start_monitors():
    params = request.json['kilometers']
    t = threading.Thread(target=ro.start, args=([params]))
    t.start()

    return "Rosense started"


run(app, host='localhost', port=5050)
