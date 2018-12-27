import pygame
from pygame.locals import QUIT, KEYDOWN, KEYUP, JOYAXISMOTION, JOYBUTTONDOWN, JOYBUTTONUP, K_ESCAPE, MOUSEBUTTONUP, MOUSEMOTION
import sys
import os

os.environ['SDL_VIDEO_CENTERED'] = '1'

#float range. Start=a, End=b, Step=c
def frange(a, b, c):
    t = a
    while t < b:
        yield t
        t += c

def drawGraph(screen, arr, step=5):
        maxy = screen.get_height()
        for i in range(len(arr)-1):
            #x = i*step
            p1 = (i*step, maxy-arr[i])
            p2 = ((i+1)*step, maxy-arr[i+1])
            pygame.draw.line(screen, (0,0,0), p1, p2)
        
class PygameHelper:
    def __init__(self, size=(640,480), fill=(255,255,255)):
        pygame.init()
        self.screen = pygame.display.set_mode(size)
        self.screen.fill(fill)
        pygame.display.flip()
        self.running = False
        self.readyToQuit = False
        self.clock = pygame.time.Clock() #to track FPS
        self.size = size
        self.fps= 0
        
        print "n de joysticks encontrados no sistema: %s" %pygame.joystick.get_count()
        if pygame.joystick.get_count() > 0:
            j = pygame.joystick.Joystick(0)
            try:
                print "iniciando joystick"
                j.init()
            except Exception, e:
                print "erro iniciando joystick: %s" % e
                sys.exit(1)
        
    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
            elif event.type == KEYDOWN:
                self.keyDown(event.key)
            elif event.type == KEYUP:
                if event.key == K_ESCAPE:
                    self.running = False
                self.keyUp(event.key)
            elif event.type == MOUSEBUTTONUP:
                self.mouseUp(event.button, event.pos)
            elif event.type == MOUSEMOTION:
                self.mouseMotion(event.buttons, event.pos, event.rel)
            elif event.type == JOYAXISMOTION:
                self.joyAxisMotion(event.joy, event.axis, event.value)
            elif event.type == JOYBUTTONUP:
                self.joyButtonUp(event.joy, event.button)
            elif event.type == JOYBUTTONDOWN:
                self.joyButtonDown(event.joy, event.button)

    #wait until a key is pressed, then return
    def waitForKey(self):
        press=False
        while not press:
            for event in pygame.event.get():
                if event.type == KEYUP:
                    press = True
             
    #enter the main loop, possibly setting max FPS
    def mainLoop(self, fps=0):
        self.running = True
        self.fps= fps
        
        while self.running:
            pygame.display.set_caption("FPS: %i" % self.clock.get_fps())
            self.handleEvents()
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(self.fps)
            self.running = not self.readyToQuit
        else:
            pygame.quit()
            
    def update(self):
        pass
        
    def draw(self):
        pass
        
    def keyDown(self, key):
        pass
        
    def keyUp(self, key):
        pass
    
    def mouseUp(self, button, pos):
        pass
        
    def mouseMotion(self, buttons, pos, rel):
        pass

    def joyAxisMotion(self, joy, axis, value):
        pass

    def joyButtonUp(self, joy, button):
        pass

    def joyButtonDown(self, joy, button):
        pass

    def quit(self):
        self.readyToQuit = True
        