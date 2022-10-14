from test_class import TestClass, QuuxClass
from mqtt_client import MQTT_Client
import time

def on_chiller_message(client, userdata, message):
    print("Chiller: ", message.payload)

tester = TestClass()
quuxTester = QuuxClass()
mqtt_client = MQTT_Client()
mqtt_client.start()
time.sleep(3)
mqtt_client.register(tester)
mqtt_client.register(quuxTester)
mqtt_client.client.message_callback_add("intrepid/chiller", on_chiller_message)
time.sleep(20)
