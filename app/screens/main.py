from datetime import datetime

from ui.widgets.background import LcarsBackgroundImage, LcarsImage
from ui.widgets.gifimage import LcarsGifImage
from ui.widgets.lcars_widgets import *
from ui.widgets.screen import LcarsScreen
from modules.menu import MenuModule
from modules.chiller import ChillerModule

from datasources.network import get_ip_address_string
import vlc
import time

BUTTON_SIZE = (183, 66)

class ScreenMain(LcarsScreen):
    def setup(self, all_sprites):

        # the next vertical position available for a button on the left
        self.buttonLeft = 24
        self.nextButton = 247
        self.bottom = 404
        self.playingWOMP = False

        self.modules = {}
        self.currentModule = None

        # Pass reference to MQTT client??
        self.addModule("chiller", ChillerModule())
        self.addModule("menu", MenuModule())

        all_sprites.add(LcarsBackgroundImage("assets/lcars_screen_1.png"),
                        layer=0)

        # panel text
        all_sprites.add(LcarsText(colours.BLACK, (30, 70), "LCARS 105", 2),
                        layer=1)
                        
        all_sprites.add(LcarsText(colours.ORANGE, (19, 216), "HOME AUTOMATION", 3),
                        layer=1)

        # Menu, Environmental, Security, 
        self.addBlockButton(all_sprites, colours.RED_BROWN, "MESS HALL")
        self.addBlockButton(all_sprites, colours.ORANGE, "SECURITY")
        self.addBlockButton(all_sprites, colours.BEIGE, "ENVIRONMENTAL")
        self.addBlockButton(all_sprites, colours.BLUE, "TEN FORWARD")
        #all_sprites.add(LcarsBlockMedium(colours.RED_BROWN, (328, 24), "LIGHTS"),
        #                layer=1)
        #all_sprites.add(LcarsBlockSmall(colours.ORANGE, (395, 24), "CAMERAS"),
        #                layer=1)
        #all_sprites.add(LcarsBlockLarge(colours.BEIGE, (434, 24), "ENERGY"),
        #                layer=1)

        self.ip_address = LcarsText(colours.BLACK, (444, 520),
                                    get_ip_address_string())
        all_sprites.add(self.ip_address, layer=1)

        # info text
        '''
        all_sprites.add(LcarsText(colours.WHITE, (192, 174), "EVENT LOG:", 1.5),
                        layer=3)
        all_sprites.add(LcarsText(colours.BLUE, (244, 174), "2 ALARM ZONES TRIGGERED", 1.5),
                        layer=3)
        all_sprites.add(LcarsText(colours.BLUE, (286, 174), "14.3 kWh USED YESTERDAY", 1.5),
                        layer=3)
        all_sprites.add(LcarsText(colours.BLUE, (330, 174), "1.3 Tb DATA USED THIS MONTH", 1.5),
                        layer=3)

        self.info_text = all_sprites.get_sprites_from_layer(3)
        '''

        # date display
        self.stardate = LcarsText(colours.BLUE, (19, 608), "STAR DATE 2311.05 17:54:32", 3)
        self.lastClockUpdate = 0
        all_sprites.add(self.stardate, layer=1)

        # buttons
        all_sprites.add(LcarsButton(colours.RED_BROWN, (14, 1059), "LOGOUT", BUTTON_SIZE, "button", self.logoutHandler),
                        layer=4)
        #all_sprites.add(LcarsToggleButton(colours.PURPLE, (207, 227), "WOMP FM"),
        #                layer=4)
        all_sprites.add(LcarsToggleButton(colours.ORANGE, (141, 856), "100.5", (86, 29), "rect", self.playWOMP),
                        layer=4)
        '''
        all_sprites.add(LcarsButton(colours.BEIGE, (107, 127), "SENSORS", self.sensorsHandler),
                        layer=4)
        all_sprites.add(LcarsButton(colours.PURPLE, (107, 262), "GAUGES", self.gaugesHandler),
                        layer=4)
        all_sprites.add(LcarsButton(colours.PEACH, (107, 398), "WEATHER", self.weatherHandler),
                        layer=4)
        all_sprites.add(LcarsButton(colours.PEACH, (108, 536), "HOME", self.homeHandler),
                        layer=4)
                        '''

        # gadgets
        '''
        all_sprites.add(LcarsGifImage("assets/gadgets/fwscan.gif", (277, 556), 100), layer=1)

        self.sensor_gadget = LcarsGifImage("assets/gadgets/lcars_anim2.gif", (235, 150), 100)
        self.sensor_gadget.visible = False
        all_sprites.add(self.sensor_gadget, layer=2)

        self.dashboard = LcarsImage("assets/gadgets/dashboard.png", (187, 232))
        self.dashboard.visible = False
        all_sprites.add(self.dashboard, layer=2)

        self.weather = LcarsImage("assets/weather.jpg", (188, 122))
        self.weather.visible = False
        all_sprites.add(self.weather, layer=2)

        #all_sprites.add(LcarsMoveToMouse(colours.WHITE), layer=1)
        '''
        self.beep1 = Sound("assets/audio/panel/201.wav")
        Sound("assets/audio/panel/220.wav").play()

    def addModule(self, name, module):
        self.modules[name] = module

        # Register Module with MQTT client
        if module.mqtt_topic:
            print("Registering", name, "module with MQTT")
            self.mqtt_client.register(module)

        # set the current module to the first one added
        if not self.currentModule:
            self.currentModule = module
            self.currentModule.enter()

    def changeModule(self, newModule):
        self.currentModule.exit()
        self.currentModule = self.modules[newModule]
        self.currentModule.enter()

    def addBlockButton(self, all_sprites, colour, text, handler=None):
        # get starting coordinate
        pos = (self.nextButton, self.buttonLeft)
        # get size
        size = (162, 62)
        if (self.nextButton + 62) > 652:
            size = (162, 652 - self.nextButton)
        self.nextButton += size[1] + 5
        all_sprites.add(LcarsBlock(colour, (pos), text, size, handler), layer=1)

    def update(self, screenSurface, fpsClock):
        if pygame.time.get_ticks() - self.lastClockUpdate > 1000:
            self.stardate.setText("STAR DATE {}".format(datetime.now().strftime("%d%m.%y %H:%M:%S")))
            self.lastClockUpdate = pygame.time.get_ticks()
        LcarsScreen.update(self, screenSurface, fpsClock)
        if self.currentModule:
            self.currentModule.update()
            #self.surface.blit(self.currentModule.surface, (212, 194))
            screenSurface.blit(self.currentModule.surface, (212, 194))

    def handleEvents(self, event, fpsClock):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.beep1.play()
            self.currentModule.handleEvents(event, fpsClock)

        if event.type == pygame.MOUSEBUTTONUP:
            self.currentModule.handleEvents(event, fpsClock)
            return False


    def hideInfoText(self):
        if self.info_text[0].visible:
            for sprite in self.info_text:
                sprite.visible = False

    def showInfoText(self):
        for sprite in self.info_text:
            sprite.visible = True

    def gaugesHandler(self, item, event, clock):
        self.hideInfoText()
        self.sensor_gadget.visible = False
        self.dashboard.visible = True
        self.weather.visible = False

    def sensorsHandler(self, item, event, clock):
        self.hideInfoText()
        self.sensor_gadget.visible = True
        self.dashboard.visible = False
        self.weather.visible = False

    def weatherHandler(self, item, event, clock):
        self.hideInfoText()
        self.sensor_gadget.visible = False
        self.dashboard.visible = False
        self.weather.visible = True

    def homeHandler(self, item, event, clock):
        self.showInfoText()
        self.sensor_gadget.visible = False
        self.dashboard.visible = False
        self.weather.visible = False
        
    def logoutHandler(self, item, event, clock):
        from screens.authorize import ScreenAuthorize
        self.loadScreen(ScreenAuthorize())

    def playWOMP(self, item, event, clock):
        if not self.playingWOMP:
            url = 'https://us2.maindigitalstream.com/ssl/WUKL'
            instance = vlc.Instance()
            self.player = instance.media_player_new()
            media=instance.media_new(url)
            self.player.set_media(media)
            self.player.play()
            self.playingWOMP = True
        else:
            self.player.stop()
            self.playingWOMP = False


