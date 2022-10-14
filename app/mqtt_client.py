import paho.mqtt.client as mqtt
import time

connflag = False

def on_connect(client, userdata, flags, rc):
    global connflag
    print("MQTT client connected!")
    connflag = True


class MQTT_Client:

    def __init__(self):
        self.client = mqtt.Client("Intrepid")
        self.broker = "localhost"
        self.topic = "intrepid/#"
        self.client.on_connect = on_connect
        
    def register(self, module): #, topic, func):
        print("Registered callback for", module.mqtt_topic)
        self.client.message_callback_add(module.mqtt_topic, module.on_message)

    def start(self):
        global connflag
        print("MQTT Client Starting...")
        self.client.connect(self.broker)
        #while not connflag:
        #    print("Connecting...")
        #    time.sleep(1)
        self.client.loop_start()
        self.client.subscribe(self.topic)

