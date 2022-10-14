# Drawing:
# lcars.py => ui.tick()
# ui/ui.py => tick() => self.update()
#   update() => screen.all_sprites.update(surface)
#       updates and draws all sprites to the surface

# Event Handling
# lcars.py => ui.tick()
# ui/ui.py => tick() => self.handleEvents()
#   handleEvents() => for each sprite in all_sprites:
#                           sprite.handleEvent()
#                     screen.handleEvents() 

import pygame

class LcarsModule:

    def __init__(self):
        #self.sprites = pygame.sprite.LayeredDirty()
        #self.surface = pygame.Surface((1020, 510))
        self.views = {}
        self.views['main'] = LcarsModuleView('main')
        self.switchView('main')
        self.mqtt_topic = None

    def addView(self, viewName):
        self.views[viewName] = LcarsModuleView(viewName)
        
    def switchView(self, viewName):
        # get view by name
        v = self.views.get(viewName)
        # set sprites and surface to new view
        self.sprites = v.sprites
        self.surface = v.surface

    def removeView(self, viewName):
        self.views.pop(viewName)

    def addSprite(self, sprite, viewName="main"):
        #self.sprites.add(sprite)#, layer=1)
        self.views[viewName].sprites.add(sprite)

    def enter(self):
        pass

    def exit(self):
        pass

    def update(self):
        self.sprites.update(self.surface)

    def handleEvents(self, event, fpsClock):
        if hasattr(event, "pos"):
            x, y = event.pos
            x -= 212
            y -= 194
            event.pos = (x, y)
            for sprite in self.sprites.sprites():
                focussed = sprite.rect.collidepoint((x,y))
                if (focussed or sprite.focussed) and sprite.handleEvent(event, fpsClock):
                    break

class LcarsModuleView:

    def __init__(self, viewName):
        self.name = viewName
        self.sprites = pygame.sprite.LayeredDirty()
        self.surface = pygame.Surface((1020, 510))

