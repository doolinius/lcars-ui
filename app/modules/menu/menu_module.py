from ui.module import LcarsModule
from ui.widgets.lcars_widgets import *
from modules.menu.menu_widgets import *
from modules.menu.menu_db import MenuDB

class MenuModule(LcarsModule):

    def __init__(self):
        LcarsModule.__init__(self)
        self.menu_label = LcarsText(colours.ORANGE, (0, 0), "CURRENT MENU", 3, colours.BLACK)
        self.addSprite(self.menu_label)

        # add the dinner labels
        self.dinner_labels = []
        y = 78
        for i in range(7):
            #label = LcarsText(colours.ORANGE, (y, 48), '', 3, colours.BLACK, self.toggle_made)
            label = DinnerText(y, 48, self.toggle_made)
            # invisible by default
            #label.visible = False
            self.dinner_labels.append(label)
            self.addSprite(label)
            y += 58
        self.db = MenuDB()

    def setMenu(self, menu):
        if menu:
            self.menu_label.setText("CURRENT MENU      {}   through    {}".format(menu['start_date'], menu['end_date']))
            i = 0
            for dinner in menu['dinners']:
                self.dinner_labels[i].setDinner(dinner)
                i += 1
        else:
            self.menu_label.setText("NO CURRENT MENU")
            pass
        

    def enter(self):
        #self.db.connect()
        self.current = self.db.get_current()
        self.setMenu(self.current)

    def toggle_made(self, item, event, clock):
        print("toggling made...")
        dinner = item.dinner
        made = 0
        if dinner['made'] == 0:
            made = 1
            item.setColour(colours.DISABLED)
        else:
            item.setColour(colours.ORANGE)
        item.dinner['made'] = made
        self.db.set_made(dinner['menu_id'], dinner['dinner_id'], made)

    def exit(self):
        self.db.close()
