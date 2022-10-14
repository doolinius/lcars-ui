from screens.authorize import ScreenAuthorize
from screens.main import ScreenMain
from ui.ui import UserInterface
import config
from mqtt_client import MQTT_Client


if __name__ == "__main__":
    mqtt_client = MQTT_Client()
    mqtt_client.start()# 
    firstScreen = ScreenAuthorize()
    #firstScreen = ScreenMain()
    ui = UserInterface(firstScreen, config.RESOLUTION, config.UI_PLACEMENT_MODE, config.FPS, config.DEV_MODE, config.SOUND)
    ui.add_mqtt_client(mqtt_client)

    while (True):
        ui.tick()
