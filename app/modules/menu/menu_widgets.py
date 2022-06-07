from ui.widgets.lcars_widgets import *
from modules.menu.menu_db import MenuDB

class DinnerText(LcarsText):

    def __init__(self, x, y, handler=None):
        LcarsText.__init__(self, colours.ORANGE, (x, y), "", 3, colours.BLACK, handler)
        self.visible = False
        self.colour = colours.ORANGE
        self.dinner = None

    def setDinner(self, dinner):
        if dinner['made']:# == 1:
            self.colour = colours.DISABLED
        self.setText(dinner['name'])
        self.setColour(self.colour)
        self.visible = True

    def toggle_made(self, event, clock):
        print("toggling MADE...")
        self.dinner['made'] = 0 if self.dinner['made'] == 1 else 1

