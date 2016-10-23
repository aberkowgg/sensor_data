from flask import Flask
import requests
import simplejson as json
app = Flask(__name__)
from flask import render_template
from bitstring import BitArray
from flask import jsonify

@app.route("/")
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"

# from bitstring import BitArray

@app.route('/sensor_data/', methods=['GET'])
def sensor_data():
    return render_template('sensor_data.html')

@app.route('/refresh_sensor_data/', methods=['GET'])
def refresh_sensor_data():
    print "########"
    # import ipdb
    # ipdb.set_trace()

    response = requests.get('https://clientedge-conductor.link-labs.com/clientEdge/data/uplinkPayload/applicationToken/b2f41103d2ba369afb75/events/2016-10-20T15:51:26.213/2016-10-15T15:50:26.213?maxResults=5',
                     auth=('developer.test@link-labs.com', 'devTest123'))

    json_data = json.loads(response.text)


    # payloads = [parse_sensor_payload(result['value']['pld']) for result in json_data['results']]
    payloads = [result['value']['pld'] for result in json_data['results']]

    print payloads

    payloads.append("001DE8F6F15D7D5275FC")
    payloads.append("01005B430AB20189B450")

    sensors = []

    for pld in payloads:
        sensor = Sensor(pld)
        print sensor.to_dict()
        sensors.append(sensor.to_dict())

    # payloads = [result['value']['pld'] for result in json_data['results']]



    return jsonify({'response': sensors})

#easy_install bitstring
class Sensor(object):
    pld_string = ""
    sensor_data = {}
    binary_string = ""

    num_of_bits = 80
    scale = 16  ## equals to hexadecimal

    # The class "constructor" - It's actually an initializer
    def __init__(self, pld_string):
        # = {"msg_cnt": "", "msg_type": ""}
        self.pld_string = pld_string
        self.binary_string = bin(int(pld_string, self.scale))[2:].zfill(self.num_of_bits)

        msg_type = self.binary_string[6:8]
        print "******mes type "
        print msg_type
        # self.sensor_data['msg_cnt'] = self.binary_string[0:6]

        # import ipdb
        # ipdb.set_trace()

        if msg_type == "00":
            self.sensor_data = self.init_gps_msg()

        else:
            self.sensor_data = self.init_sensor_msg()

        #     msg_type == "01":

        # else:
        #     self.sensor_data['msg_type'] = "Other"


    def init_gps_msg(self):

        # self.sensor_data = dict.fromkeys(['msg_cnt', 'msg_type', 'latitude', 'longitude', 'altitude', 'gw_rssi',
        #                                  'reserved'])
        sensor_data = {}
        sensor_data['message_count'] = self.bin2dec(self.binary_string[0:6])
        sensor_data['message_type'] =  "GPS"
        sensor_data['latitude'] = self.calc_longitude(self.binary_string[8:33])
        sensor_data['longitude'] = self.calc_longitude(self.binary_string[33:59])
        sensor_data['altitude'] = self.calc_altitude(self.binary_string[59:72])
        sensor_data['gw_rssi'] = self.calc_gw_rssi(self.binary_string[72:79])
        sensor_data['reserved'] = 0
        return sensor_data



    def init_sensor_msg(self):
        # import ipdb
        # ipdb.set_trace()
        # sensor_data = dict.fromkeys(['msg_cnt', 'msg_type', 'motion', 'light_data', 'humidity', 'temperature',
        #                                  'pressure'])
        sensor_data = {}
        sensor_data['message_count'] = self.bin2dec(self.binary_string[0:6])
        sensor_data['message_type'] = "Sensor"
        sensor_data['motion'] = self.calc_motion(self.binary_string[8:9])
        sensor_data['light_data'] = self.calc_light_data(self.binary_string[9:24])
        sensor_data['humidity'] = self.calc_humidity(self.binary_string[24:32])
        sensor_data['temperature'] = self.calc_temp(self.binary_string[32:48])
        sensor_data['pressure'] = self.calc_pressure(self.binary_string[48:])
        return sensor_data


    def calc_motion(self, bin_string):
        # return "No Motion (0)" if bin_string == "0" else "Motion (1)"
        return self.bin2dec(bin_string)


    def calc_light_data(self, bin_string):
        unsinged_int = BitArray(bin=bin_string).uint
        return unsinged_int * 2

    def calc_humidity(self, bin_string):
        unsinged_int = BitArray(bin=bin_string).uint
        return unsinged_int / float(2)

    def calc_temp(self, bin_string):
        singed_int = BitArray(bin=bin_string).int
        return singed_int / float(100)

    def calc_pressure(self, bin_string):
        return self.bin2dec(bin_string)

    def calc_longitude(self, bin_string):
        return self.bin2dec(bin_string, True) / float(100000)

    def calc_altitude(self, bin_string):
        return 3500 + self.bin2dec(bin_string, True)

    def calc_gw_rssi(self, bin_string):
        unsinged_int = BitArray(bin=bin_string).uint
        return unsinged_int * -1

    @staticmethod
    def bin2dec(bin_string, signed=False):
        dec = BitArray(bin=bin_string)
        return dec.int if signed else dec.uint

    def get_sensor_data(self):
        return self.sensor_data


    def to_dict(self):
        return {"sensor_data" : self.sensor_data,"pld_string" : self.pld_string,"binary_string" : self.binary_string}

if __name__ == "__main__":
    app.run(host='0.0.0.0')
