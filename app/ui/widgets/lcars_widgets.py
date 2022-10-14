import pygame
from pygame.font import Font
from pygame.locals import *

from ui.utils.sound import Sound
from ui.widgets.sprite import LcarsWidget
from ui import colours

from pygame import gfxdraw

def draw_circle(surface, color, pos, radius):
    x, y = pos
    gfxdraw.aacircle(surface, x, y, radius, color)
    gfxdraw.filled_circle(surface, x, y, radius, color)

def make_rect(width, height, colour):
    image = pygame.Surface((width, height), 0, 32)#.convert_alpha()
    image.fill(colour)
    return(image)

def make_circle(height, colour):
    radius = height//2
    image = pygame.Surface((height+2, height+2), 0, 32)#.convert_alpha()
    draw_circle(image, colour, (radius,radius), radius)
    return(image)

def make_semicircle(height, colour, direction):
    radius = height//2
    image = pygame.Surface((radius+2, height+2), 0, 32)#.convert_alpha()
    center = (radius, radius)
    if direction == "right":
        center = (0, radius)
    draw_circle(image, colour, center, radius)
    return(image)

def make_button(width, height, colour):
    radius = height//2
    image = pygame.Surface((width+2, height), 0, 32)#.convert_alpha()
    draw_circle(image, colour, (radius,radius), radius)
    draw_circle(image, colour, (width-radius,radius), radius)
    pygame.draw.rect(image, colour, Rect(radius, 0, width-height, height))
    return(image)

def make_tab(width, height, colour, direction):
    radius = height//2
    image = pygame.Surface((width+2, height+1), 0, 32)#.convert_alpha()
    if direction == "left":
        draw_circle(image, colour, (radius,radius), radius)
        pygame.draw.rect(image, colour, Rect(radius, 0, width-radius+1, height+1))
    else:
        draw_circle(image, colour, (width-radius,radius), radius)
        pygame.draw.rect(image, colour, Rect(0, 0, width-radius, height+1))
    return(image)

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
        #self.applyColour(colour)

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
        #self.applyColour(colour)

class LcarsButton(LcarsWidget):
    """Button - either rounded or rectangular if rectSize is spcified"""
    """OR - specify a shape and size."""
    # round, button, rect, semi-left, semi-right, 
    # w/h for all? 

    #def __init__(self, colour, pos, text, handler=None, rectSize=None):
    def __init__(self, colour, pos, text, size, shape="button", handler=None):

        self.text = text
        self.colour = colour

        width, height = size
        if shape == "button":
            self.image = make_button(width, height, colour)
            self.highlightImage = make_button(width, height, colours.WHITE)
            self.disabledImage = make_button(width, height, colours.DISABLED)
        elif shape == "rect":
            self.image = make_rect(width, height, colour)
            self.highlightImage = make_rect(width, height, colours.WHITE)
            self.disabledImage = make_rect(width, height, colours.DISABLED)
        elif shape == "circle":
            self.image = make_circle(height, colour)
            self.highlightImage = make_circle(height, colours.WHITE)
            self.disabledImage = make_circle(height, colours.DISABLED)
        elif shape == "semi-left":
            self.image = make_semicircle(height, colour, "left")
            self.highlightImage = make_semicircle(height, colours.WHITE, "left")
            self.disabledImage = make_semicircle(height, colours.DISABLED, "left")
        elif shape == "semi-right":
            self.image = make_semicircle(height, colour, "right")
            self.highlightImage = make_semicircle(height, colours.WHITE, "right")
            self.disabledImage = make_semicircle(height, colours.DISABLED, "right")
        elif shape == "tab-left":
            self.image = make_tab(width, height, colour, "left")
            self.highlightImage = make_tab(width, height, colours.WHITE, "left")
            self.disabledImage = make_tab(width, height, colours.DISABLED, "left")
        elif shape == "tab-right":
            self.image = make_tab(width, height, colour, "right")
            self.highlightImage = make_tab(width, height, colours.WHITE, "right")
            self.disabledImage = make_tab(width, height, colours.DISABLED, "right")

        self.normalImage = self.image
        self.renderText()
        
        '''
        if rectSize == None:
            #image = pygame.image.load("assets/button.png").convert_alpha()
            image = make_button(100, 64, colours.WHITE)
            size = (image.get_rect().width, image.get_rect().height)
        else:
            size = rectSize
            image = pygame.Surface(rectSize, 0, 32).convert_alpha()
            image.fill(colour)

        self.backImage = image

        self.image = self.backImage
        self.highlightTextImage = font.render(text, True, colours.BLACK)
        self.textImage = font.render(text, True, colours.BLACK, colour)
        self.applyColour(colour)
        self.renderText(self.textImage)
        '''
        LcarsWidget.__init__(self, colour, pos, size, handler)

        self.highlighted = False
        self.beep = Sound("assets/audio/panel/202.wav")

    def renderText(self):
        font = Font("assets/HelveticaUltraCompressed.ttf", 36)
        textImage = font.render(self.text, True, colours.BLACK, self.colour)
        self.image.blit(textImage, 
                ((self.image.get_rect().width//2) - (textImage.get_rect().width)//2,
                    self.image.get_rect().height//2 - textImage.get_rect().height//2))

        highlightTextImage = font.render(self.text, True, colours.BLACK, colours.WHITE)
        self.highlightImage.blit(highlightTextImage, 
                ((self.highlightImage.get_rect().width//2) - (highlightTextImage.get_rect().width)//2,
                    self.highlightImage.get_rect().height//2 - highlightTextImage.get_rect().height//2))

        disabledTextImage = font.render(self.text, True, colours.BLACK, colours.DISABLED)
        self.disabledImage.blit(disabledTextImage, 
                ((self.disabledImage.get_rect().width//2) - (disabledTextImage.get_rect().width)//2,
                    self.disabledImage.get_rect().height//2 - disabledTextImage.get_rect().height//2))

    def handleEvent(self, event, clock):
        #if (event.type == MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos) and self.visible == True):
        if (event.type == MOUSEBUTTONDOWN and self.visible == True):
            self.image = self.highlightImage
            self.highlighted = True
            self.beep.play()

        if (event.type == MOUSEBUTTONUP and self.highlighted and self.visible == True):
            self.image = self.normalImage
            self.highlighted = False
           
        return LcarsWidget.handleEvent(self, event, clock)

class LcarsToggleButton(LcarsButton):
    """A toggle button similar to a checkbox"""

    def __init__(self, colour, pos, text, size, shape, handler=None):

        LcarsButton.__init__(self, colour, pos, text, size, shape, handler)
        self.setSelected(False)
        self.unselect = Sound("assets/audio/panel/201.wav")

    def setSelected(self, selected=True):
        if selected:
            # select it (enable/color it)
            self.image = self.normalImage
            self.selected = True
        else:
            # unselect it
            self.image = self.disabledImage
            self.selected = False


    def handleEvent(self, event, clock):

        if (event.type == MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)):
            if self.selected == False:
                self.setSelected(True)
                self.beep.play()
            else:
                # unselect it
                self.setSelected(False)
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
        LcarsButton.__init__(self, colour, pos, text, size, "rect", handler)

class LcarsBlockMedium(LcarsButton):
   """Left navigation block - medium version"""

   def __init__(self, colour, pos, text, handler=None):
        size = (162, 62)
        LcarsButton.__init__(self, colour, pos, text, size, "rect", handler)

class LcarsBlockSmall(LcarsButton):
   """Left navigation block - small version"""

   def __init__(self, colour, pos, text, handler=None):
        size = (162, 34)
        LcarsButton.__init__(self, colour, pos, text, size, "rect", handler)

    
class LcarsBlock(LcarsButton):
   """Left navigation block - arbitrary size version"""

   def __init__(self, colour, pos, text, size, handler=None):
        LcarsButton.__init__(self, colour, pos, text, size, "rect", handler)

