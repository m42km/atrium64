import pygame
import pygame.freetype

pygame.freetype.init()

# atrium.py - classes and stuff for the operating system

path = 'assets/'

txt = pygame.image.load(path + 'txt.png')
txt_selected = pygame.image.load(path + 'txt_selected.png')
folder = pygame.image.load(path + 'folder.png')

txtwindow = pygame.image.load(path + 'txtwindow.png') # i didnt make the texture for the window yet. will do soon

sys_font = pygame.freetype.Font(path + 'font/PressStart2P.ttf', 9) # font is 11px tall.

class File:
    def __init__(self, position_x, position_y, name, xpos_fix, data): # max position_y = 9, max position_x = 10 (1024/100 ~= 10) (576/64 = 9)
        # precalculating position of the icon
        self.position_x = position_x * 100 + 10 
        self.position_y = position_y * 64 + 10
        self.position_x2 = position_x + 100
        self.position_y2 = position_y + 64
        self.xpos_fix = xpos_fix
        self.name = name
        self.currtexture = txt
        self.data = data
        self.currclicks = 0 # for double clicking functionality
        
    def checkClicked(self, mouse_pos):
        isClicked = False
        if mouse_pos[0] < self.position_x2 and mouse_pos[0] > self.position_x:
            if mouse_pos[1] < self.position_y2 and mouse_pos[1] > self.position_y:
                isClicked = True
        return isClicked
        
    def clicked(self):
        self.currclicks += 1
        if self.currclicks == 2:
            self.currclicks = 0
            self.currtexture = txt
            self.nextLoop = True
        else:
            self.currtexture = txt_selected
            self.nextLoop = False
            
    def blit(self, display_screen):
        display_screen.blit(self.currtexture, (self.position_x, self.position_y)) # + 10 for padding lol
        sys_font.render_to(display_screen, (self.position_x + self.xpos_fix - 2, self.position_y2 + 17), self.name, (0, 0, 0))
        sys_font.render_to(display_screen, (self.position_x + self.xpos_fix, self.position_y2 + 15), self.name, (255, 255, 255))

class npWindow:
    def __init__(self, currFile, data, position_x, position_y):
        self.windowTitle = currFile
        self.text = data
        self.positionX = position_x
        self.positionY = position_y
        self.dragBarX = position_x + 499
        self.dragBarY = position_y + 25 # Hitboxes for bar to drag window
        self.namePosition = [self.positionX + 8, self.positionY + 8]
        self.dataPosition = [self.positionX + 8, self.positionY + 29] # text positioning
        self.texture = txtwindow
        self.dragStartPos = []
        self.isMyAssGettingDragged = False
        self.closed = False
        self.closeBox = [[self.positionX + 501, self.positionY + 3], [self.positionX + 534, self.positionY + 22]]
        self.oldPosition = [self.positionX, self.positionY]
    
    def isDragging(self, mouse_x, mouse_y):
        mouseDragging = False
        if mouse_x < self.dragBarX and mouse_x > self.positionX:
            if mouse_y < self.dragBarY and mouse_y > self.positionY:
                mouseDragging = True
        
        return mouseDragging
        
    def whenMouseDrag(self, startingX, startingY):
        self.isMyAssGettingDragged = True
        self.dragStartPos = [startingX, startingY]
    
    def whenStopDrag(self):
        self.isMyAssGettingDragged = False
        self.oldPosition = [self.positionX, self.positionY]
    
    def whileMouseDragging(self, mouseX, mouseY):
        self.positionX = self.oldPosition[0] + ((mouseX - self.dragStartPos[0])) # lfg i finally fixed it LOL (kind of but it doesn't go too fast now)
        self.positionY = self.oldPosition[1] + ((mouseY - self.dragStartPos[1]))
        self.dragBarX = self.positionX + 499
        self.dragBarY = self.positionY + 25
        self.namePosition = [self.positionX + 8, self.positionY + 8]
        self.dataPosition = [self.positionX + 8, self.positionY + 29]
    
    def onClose(self):
        self.closed = True
        
    def onReopen(self):
        self.closed = False
        
    def blit(self, display_screen):
        if not self.closed:
            display_screen.blit(self.texture, (self.positionX, self.positionY))
            sys_font.render_to(display_screen, (self.namePosition[0], self.namePosition[1]), self.windowTitle, (0, 0, 0))
            sys_font.render_to(display_screen, (self.dataPosition[0], self.dataPosition[1]), self.text, (0, 0, 0))