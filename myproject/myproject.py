from bitstring import BitArray
import datetime
from flask import Flask
from flask import jsonify
from flask import render_template
import requests
import simplejson as json

app = Flask(__name__)


@app.route("/", methods=['GET'])
def sensor_data():
    return render_template('sensor_data_table.html')

@app.route("/card_view", methods=['GET'])
def sensor_data_cards():
    return render_template('sensor_data.html')


@app.route('/refresh_sensor_data/', methods=['GET'])
def refresh_sensor_data():

    json_data = fetch_sensor_results()

    #  Validate payload for results
    if 'results' in json_data:

        sensors = {}

        for result in json_data['results']:
            sensor = Sensor(result['value'])
            if sensor.get_type() == "Sensor":
                module = sensor.get_module()
                if module not in sensors:
                    sensors[module] = []
                sensors[module].append(sensor.to_dict())

        # payloads = [result['value']['pld'] for result in json_data['results']]
        return jsonify({'response': [ [k,v] for k, v in sensors.items() ]})

    else:
        return jsonify({'response': "Bad Request"}), 400


def fetch_sensor_results():
    # datetime.isoformat
    before_time = '2016-10-20T15:51:26.213'
    # before_time = (datetime.datetime.now() - datetime.timedelta(seconds=30)).isoformat()

    after_time = '2016-10-15T15:50:26.213'
    # after_time = datetime.datetime.now().isoformat()
    max_results = '50'
    ll_user_name = 'developer.test@link-labs.com'
    ll_password = 'devTest123'

    try:
        response = requests.get(
            'https://clientedge-conductor.link-labs.com/clientEdge/data/uplinkPayload/applicationToken/b2f41103d2ba369afb75/events/%s/%s?maxResults=%s' % (before_time, after_time, max_results),
            auth=(ll_user_name, ll_password))

        return json.loads(response.text)

    except Exception as e:
        return {'error' : str(e)}


class Sensor(object):
    pld_string = ""
    sensor_data = {}
    binary_string = ""
    value = {}

    num_of_bits = 80
    scale = 16  ## equals to hexadecimal

    # The class "constructor" - It's actually an initializer
    def __init__(self, value):

        self.value = value
        self.pld_string = value['pld']
        self.binary_string = bin(int(value['pld'], self.scale))[2:].zfill(self.num_of_bits)

        msg_type = self.binary_string[6:8]

        if msg_type == "01":
            self.sensor_data = self.init_sensor_msg()

        else:
            self.sensor_data['message_type'] = "Other"

    def init_sensor_msg(self):
        sensor_data = {}
        sensor_data['message_count'] = self.bin2dec(self.binary_string[0:6])
        sensor_data['message_type'] = "Sensor"
        sensor_data['motion'] = self.bin2dec(self.binary_string[8:9])
        sensor_data['light_data'] = self.calc_light_data(self.binary_string[9:24])
        sensor_data['humidity'] = self.calc_humidity(self.binary_string[24:32])
        sensor_data['temperature'] = self.calc_temp(self.binary_string[32:48])
        sensor_data['pressure'] = self.calc_pressure(self.binary_string[48:])
        return sensor_data

    def calc_light_data(self, bin_string):
        return self.bin2dec(bin_string) * 2

    def calc_humidity(self, bin_string):
        return self.bin2dec(bin_string) / float(2)

    def calc_temp(self, bin_string):
        return self.bin2dec(bin_string, True) / float(100)

    def calc_pressure(self, bin_string):
        return self.bin2dec(bin_string) * float(0.00390625)

    @staticmethod
    def bin2dec(bin_string, signed=False):
        dec = BitArray(bin=bin_string)
        return dec.int if signed else dec.uint

    def get_type(self):
        return self.sensor_data['message_type']

    def get_module(self):
        return self.value['module']

    def get_sensor_data(self):
        return self.sensor_data

    def to_dict(self):
        return {"sensor_data": self.sensor_data,
                "value": self.value,
                "pld_string": self.pld_string,
                "binary_string": self.binary_string
                }

if __name__ == "__main__":
    app.run(host='0.0.0.0')
