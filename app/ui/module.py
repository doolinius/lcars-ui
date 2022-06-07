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
        self.sprites = pygame.sprite.LayeredDirty()
        self.surface = pygame.Surface((1020, 510))

    def addSprite(self, sprite):
        self.sprites.add(sprite)#, layer=1)

    def enter(self):
        pass

    def exit(self):
        pass

    def update(self):
        self.sprites.update(self.surface)

    def handleEvents(self, event, fpsClock):
        for sprite in self.sprites.sprites():
            if hasattr(event, "pos"):
                #print("Sprite top:{} left:{}".format(sprite.rect.top, sprite.rect.left))
                #print("Event position: ", event.pos)
                x, y = event.pos
                x -= 212
                y -= 194
                focussed = sprite.rect.collidepoint((x,y))
                if (focussed or sprite.focussed) and sprite.handleEvent(event, fpsClock):
                    break
