import pygame
from pygame.font import Font
from pygame.locals import *

from ui.utils.sound import Sound
from ui.widgets.sprite import LcarsWidget
from ui import colours

class LcarsElbow(LcarsWidget):
    """The LCARS corner elbow - not currently used"""
    
    STYLE_BOTTOM_LEFT = 0
    STYLE_TOP_LEFT = 1
    STYLE_BOTTOM_RIGHT = 2
    STYLE_TOP_RIGHT = 3
    
    def __init__(self, colour, style, pos, handler=None):
        image = pygame.image.load("assets/elbow.png").convert_alpha()
        # alpha=255
        # image.fill((255, 255, 255, alpha), None, pygame.BLEND_RGBA_MULT)
        if (style == LcarsElbow.STYLE_BOTTOM_LEFT):
            image = pygame.transform.flip(image, False, True)
        elif (style == LcarsElbow.STYLE_BOTTOM_RIGHT):
            image = pygame.transform.rotate(image, 180)
        elif (style == LcarsElbow.STYLE_TOP_RIGHT):
            image = pygame.transform.flip(image, True, False)
        
        self.image = image
        size = (image.get_rect().width, image.get_rect().height)
        LcarsWidget.__init__(self, colour, pos, size, handler)
        self.applyColour(colour)

class LcarsTab(LcarsWidget):
    """Tab widget (like radio button) - not currently used nor implemented"""

    STYLE_LEFT = 1
    STYLE_RIGHT = 2
    
    def __init__(self, colour, style, pos, handler=None):
        image = pygame.image.load("assets/tab.png").convert()
        if (style == LcarsTab.STYLE_RIGHT):
            image = pygame.transform.flip(image, False, True)
        
        size = (image.get_rect().width, image.get_rect().height)
        LcarsWidget.__init__(self, colour, pos, size, handler)
        self.image = image
        self.applyColour(colour)

class LcarsButton(LcarsWidget):
    """Button - either rounded or rectangular if rectSize is spcified"""
    """OR - specify a shape and size."""
    # round, button, rect, semi-left, semi-right, 
    # w/h for all? 

    def __init__(self, colour, pos, text, handler=None, rectSize=None):
        if rectSize == None:
            image = pygame.image.load("assets/button.png").convert_alpha()
            size = (image.get_rect().width, image.get_rect().height)
        else:
            size = rectSize
            image = pygame.Surface(rectSize, 0, 32).convert_alpha()
            image.fill(colour)

        self.backImage = image

        self.colour = colour
        self.image = self.backImage
        font = Font("assets/HelveticaUltraCompressed.ttf", 36)
        self.highlightTextImage = font.render(text, True, colours.BLACK)
        self.textImage = font.render(text, True, colours.BLACK, colour)
        LcarsWidget.__init__(self, colour, pos, size, handler)
        self.applyColour(colour)
        self.renderText(self.textImage)

        self.highlighted = False
        self.beep = Sound("assets/audio/panel/202.wav")

    def renderText(self, textImage):
        self.image.blit(textImage, 
                ((self.image.get_rect().width//2) - (textImage.get_rect().width)//2,
                    self.image.get_rect().height//2 - textImage.get_rect().height//2))

    def handleEvent(self, event, clock):

        if (event.type == MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos) and self.visible == True):
            self.image = self.backImage
            self.applyColour(colours.WHITE)
            self.renderText(self.highlightTextImage)
            self.highlighted = True
            self.beep.play()

        if (event.type == MOUSEBUTTONUP and self.highlighted and self.visible == True):
            self.image = self.backImage
            self.applyColour(self.colour)
            self.renderText(self.textImage)
            self.highlighted = False
           
        return LcarsWidget.handleEvent(self, event, clock)

class LcarsToggleButton(LcarsButton):
    """A toggle button similar to a checkbox"""

    def __init__(self, colour, pos, text, handler=None, rectSize=None):
        LcarsButton.__init__(self, colour, pos, text, handler, rectSize)
        self.selected = False
        self.unselect = Sound("assets/audio/panel/201.wav")

    def handleEvent(self, event, clock):

        if (event.type == MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)):
            if self.selected == False:
                # select it (turn it white)
                self.image = self.backImage
                self.applyColour(colours.WHITE)
                self.renderText(self.highlightTextImage)
                self.selected = True
                self.beep.play()
            else:
                # unselect it
                self.image = self.backImage
                self.applyColour(self.colour)
                self.renderText(self.textImage)
                self.selected = False
                self.unselect.play()

        return LcarsWidget.handleEvent(self, event, clock)
            

class LcarsText(LcarsWidget):
    """Text that can be placed anywhere"""

    def __init__(self, colour, pos, message, size=1.0, background=None, handler=None):
        self.colour = colour
        self.background = background
        self.text = message
        self.font = Font("assets/HelveticaUltraCompressed.ttf", int(18.0 * size))
        
        self.renderText(message)
        # center the text if needed 
        if (pos[1] < 0):
            pos = (pos[0], 640 - self.image.get_rect().width / 2)
            
        LcarsWidget.__init__(self, colour, pos, None, handler)

    def renderText(self, message):        
        self.text = message
        if (self.background == None):
            self.image = self.font.render(message, True, self.colour)
        else:
            self.image = self.font.render(message, True, self.colour, self.background)
        
    def setText(self, newText):
        self.text = newText
        self.renderText(newText)

    def setColour(self, newColour):
        self.colour = newColour
        self.renderText(self.text)

class LcarsBlockLarge(LcarsButton):
    """Left navigation block - large version"""

    def __init__(self, colour, pos, text, handler=None):
        size = (162, 147)
        LcarsButton.__init__(self, colour, pos, text, handler, size)

class LcarsBlockMedium(LcarsButton):
   """Left navigation block - medium version"""

   def __init__(self, colour, pos, text, handler=None):
        size = (162, 62)
        LcarsButton.__init__(self, colour, pos, text, handler, size)

class LcarsBlockSmall(LcarsButton):
   """Left navigation block - small version"""

   def __init__(self, colour, pos, text, handler=None):
        size = (162, 34)
        LcarsButton.__init__(self, colour, pos, text, handler, size)

    
class LcarsBlock(LcarsButton):
   """Left navigation block - arbitrary size version"""

   def __init__(self, colour, pos, text, size, handler=None):
        LcarsButton.__init__(self, colour, pos, text, handler, size)

