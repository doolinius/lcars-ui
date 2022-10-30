from ui.module import LcarsModule
from ui.widgets.lcars_widgets import *
from modules.sousvide.anova import AnovaController

class SousVideModule(LcarsModule):
    
    def __init__(self):
        LcarsModule.__init__(self)
        self.anova = AnovaController('01:02:03:04:AB:19')
        self.anova = None #AnovaController('01:02:03:04:AB:19')
        self.target_temp = -1 #self.anova.read_set_temp()
        self.temp = -1 #self.anova.read_temp()
        self.status = "offline"

        self.main_label = LcarsText(colours.BLUE, (0,0), "SOUS VIDE", 3, colours.BLACK)
        self.addSprite(self.main_label)


        self.minus_button = LcarsButton(colours.BEIGE, (62, 0), "-", (70, 54), "tab-left", self.decrementTemp)
        self.addSprite(self.minus_button)
        self.target_temp_label = LcarsText(colours.ORANGE, (62 ,90), str(self.target_temp), 3, colours.BLACK)
        self.addSprite(self.target_temp_label)
        self.plus_button = LcarsButton(colours.BEIGE, (62, 140), "+", (70, 54), "tab-right", self.incrementTemp)
        self.addSprite(self.plus_button)

        self.current_temp_label = LcarsText(colours.ORANGE, (124,90), str(round(self.temp)), 3, colours.BLACK)
        self.addSprite(self.current_temp_label)


    def enter(self):
        self.target_temp = self.anova.read_set_temp()
        self.temp = self.anova.read_temp()
        self.status = self.anova.anova_status()

    def exit(self):
        pass


    def incrementTemp(self):
        pass

    def decrementTemp(self):
        pass

    def set_target_temp(self):
        pass
