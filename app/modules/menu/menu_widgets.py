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

class DinnerRow:

    ROW_HEIGHT = 50
    PADDING = 10
    NAME_WIDTH = 350

    def __init__(self, menu_module, x, y, dinner=None):
        self.menu_module = menu_module
        self.dinner = dinner
        self.x = x
        self.y = y

        cur_x = self.x

        self.enableButton = LcarsButton(colours.PEACH, (y, cur_x), "", (self.ROW_HEIGHT, self.ROW_HEIGHT), "tab-left") # NEEDS HANDLER

        cur_x += self.ROW_HEIGHT + self.PADDING

        self.dinnerName = LcarsText(colours.ORANGE, (y-10, cur_x), "Foo Bar Baz", 3.5, colours.BLACK) # NEEDS HANDLER

        cur_x += self.NAME_WIDTH + self.PADDING

        self.vegButton = LcarsToggleButton(colours.PURPLE, (y, cur_x), "V", (self.ROW_HEIGHT, self.ROW_HEIGHT), "rect") # NEEDS HANDLER
        cur_x += self.ROW_HEIGHT + self.PADDING
        self.comfortButton = LcarsToggleButton(colours.RED_BROWN, (y, cur_x), "C", (self.ROW_HEIGHT, self.ROW_HEIGHT), "rect") # NEEDS HANDLER
        cur_x += self.ROW_HEIGHT + self.PADDING
        self.seasonButton = LcarsToggleButton(colours.PINK, (y, cur_x), "S", (self.ROW_HEIGHT, self.ROW_HEIGHT), "rect") # NEEDS HANDLER
        cur_x += self.ROW_HEIGHT + self.PADDING
        self.litmanButton = LcarsToggleButton(colours.BEIGE, (y, cur_x), "L", (self.ROW_HEIGHT, self.ROW_HEIGHT), "rect") # NEEDS HANDLER
        cur_x += self.ROW_HEIGHT + self.PADDING

        self.refreshButton = LcarsButton(colours.BLUE, (y, cur_x), "", (self.ROW_HEIGHT, self.ROW_HEIGHT), "tab-right") # NEEDS HANDLER

        menu_module.addSprite(self.enableButton, 'new_menu')
        menu_module.addSprite(self.dinnerName, 'new_menu')
        menu_module.addSprite(self.vegButton, 'new_menu')
        menu_module.addSprite(self.seasonButton, 'new_menu')
        menu_module.addSprite(self.comfortButton, 'new_menu')
        menu_module.addSprite(self.litmanButton, 'new_menu')
        menu_module.addSprite(self.refreshButton, 'new_menu')

    def refresh(self):
        # build query
        # execute query
        # update widgets
        pass
