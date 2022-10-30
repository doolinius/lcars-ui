from ui.module import LcarsModule
from ui.widgets.lcars_widgets import *
import json
import paho.mqtt.client as mqtt

class ThermostatModule(LcarsModule):

    def __init__(self):
        LcarsModule.__init__(self)
        self.data = {
                "temperature": 0,
                "humidity": 0,
        }
        self.mqtt_client = mqtt.Client('ThermostatModule')
        self.mqtt_client.connect('localhost')

        #self.addView('main')
        self.main_label = LcarsText(colours.ORANGE, (0, 0), "Thermostat-IT-697", 3, colours.BLACK)
        self.addSprite(self.main_label)

       
        self.current_temp_label = LcarsText(colours.ORANGE, (124,90), str(round(self.data['temperature'])), 3, colours.BLACK)
        self.addSprite(self.current_temp_label)

        self.humidity_label = LcarsText(colours.ORANGE, (186,90), str(self.data['humidity']), 3, colours.BLACK)
        self.addSprite(self.humidity_label)
        self.mqtt_topic = "intrepid/thermostat"

        # Current Temperature and humidity display
        # Temperature threshold/thermostat temp
        # Temperature will have a +/- adjustment for the threshold

    def on_message(self, client, userdata, message):
        json_data = message.payload.decode("utf-8")
        print("ThermostatModule received message: " ,str(json_data))
        self.set_data(json_data)

    def enter(self):
        # send signal to get current temp/humidity
        pass

    def set_data(self, json_data):
        self.data = json.loads(json_data)
        self.set_labels()

    def set_labels(self):
        curtemp = "{:.2f}".format(self.data['temperature'])
        humidity = "{}%".format(round(self.data['humidity']))
        self.current_temp_label.setText(curtemp)
        self.humidity_label.setText(humidity)

    def decrementTemp(self, item, event, clock):
        self.data['target_temp'] -= 1
        self.set_target_temp()
        target_temp = "{}".format(round(self.data['target_temp']))
        self.target_temp_label.setText(target_temp)

    def incrementTemp(self, item, event, clock):
        self.data['target_temp'] += 1
        self.set_target_temp()
        target_temp = "{}".format(round(self.data['target_temp']))
        self.target_temp_label.setText(target_temp)

    def set_target_temp(self):
        # get temp from  adjustment field
        # send signal to MQTT broker ("/chiller/set")
        self.mqtt_client.connect('localhost')
        self.mqtt_client.publish("chiller/set", self.data['target_temp'])
