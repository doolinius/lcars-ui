
class TestClass:

    def __init__(self):
        self.mqtt_topic = "intrepid/chiller"

    def on_message(self, client, userdata, message):
        print("TestClass Received Message: ", str(message.payload.decode("utf-8")))

class QuuxClass:

    def __init__(self):
        self.mqtt_topic = "intrepid/quux"

    def on_message(self, client, userdata, message):
        print("QuuxClass Received Message: ", str(message.payload.decode("utf-8")))
