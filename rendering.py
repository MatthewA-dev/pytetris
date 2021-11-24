import pygame
import copy

class Label:
    def __init__(self, display, loc, text, textcolor, textsize):
      self.loc = loc
      self.textcolor = textcolor
      self.text = text
      self.font = pygame.font.Font('assets/Minecraftia.ttf', textsize)
      self.display = display
    def render(self):

      text = self.font.render(self.text,False, self.textcolor)
      # Center the text
      x = ((self.loc[2] - self.loc[0]) // 2) - (text.get_rect().width // 2)
      y = ((self.loc[3] - self.loc[1]) // 2) - (text.get_rect().height // 2)
      self.display.blit(text, (self.loc[0] + x, self.loc[1] + y))

class Button:
  # loc in (x,y,w,h)
  def __init__(self, display, loc, color, hovercolor, bordersize, bordercolor, func, text, textcolor, textsize):
    self.loc = loc
    self.color = color
    self.hovercolor = hovercolor
    self.bordersize = bordersize
    self.bordercolor = bordercolor
    self.textcolor = textcolor
    self.func = func
    self.text = text
    self.font = pygame.font.Font('assets/Minecraftia.ttf', textsize)
    self.display = display
  
  def render(self):
    mousepos = pygame.mouse.get_pos()
    color = self.color
    
    if(self.isHovering(mousepos)):
      color = self.hovercolor
    
    # Draw border
    pygame.draw.rect(self.display, (255,255,255), pygame.Rect(self.loc[0] - self.bordersize, self.loc[1] - self.bordersize, self.loc[2] + self.bordersize*2, self.loc[3] + self.bordersize*2),border_radius=10)
    # Draw middle
    r = pygame.Rect(self.loc[0], self.loc[1], self.loc[2], self.loc[3])
    pygame.draw.rect(surface=self.display,color=color,rect = r,border_radius=10)
    text = self.font.render(self.text,False, self.textcolor)
    # Center the text
    x = (self.loc[2] // 2) - (text.get_rect().width // 2)
    y = (self.loc[3] // 2) - (text.get_rect().height // 2)
    self.display.blit(text, (self.loc[0] + x, self.loc[1] + y))
  
  def isHovering(self, mousepos):
    #mousepos[0] > self.rect.x and mousepos[0] < self.rect.x + self.rect.width and mousepos[1] > self.rect.y and mousepos[1] < self.rect.y + self.rect.height
    if(mousepos[0] > self.loc[0] and mousepos[0] < self.loc[0] + self.loc[2] and mousepos[1] > self.loc[1] and mousepos[1] < self.loc[1] + self.loc[3]):
      return True
    return False


class InputBox:
  def __init__(self,display, x, y, w, h, color, bordercolor, bordersize, activecolor, textcolor, maxlen, text='', fontsize = 20):
    self.display = display
    self.rect = pygame.Rect(x, y, w, h)
    self.color = color
    self.maxlen = maxlen
    self.textcolor = textcolor
    self.bordercolor = bordercolor
    self.bordersize = bordersize
    self.activecolor = activecolor
    self.text = text
    self.txt_surface = pygame.font.Font('assets/Minecraftia.ttf', fontsize)
    self.active = False

  def isHovering(self, mousepos):
    if(mousepos[0] > self.rect.x and mousepos[0] < self.rect.x + self.rect.width and mousepos[1] > self.rect.y and mousepos[1] < self.rect.y + self.rect.height):
      return True
    return False
  
  def handleClick(self, mousepos):
    self.active = self.isHovering(mousepos)

  def handleType(self, char):
    if(len(self.text) == self.maxlen):
      return
    self.text += char

  def render(self):
    # Draw border
    borderRect = copy.copy(self.rect)
    borderRect.left -= self.bordersize
    borderRect.top -= self.bordersize
    borderRect.width += self.bordersize*2
    borderRect.height += self.bordersize*2
    pygame.draw.rect(self.display, self.bordercolor, borderRect, border_radius=10)
    
    # Draw middle
    color = self.color
    if(self.active):
      color = self.activecolor
    pygame.draw.rect(surface=self.display, color=color, rect = self.rect, border_radius=10)
    # Draw text
    text = self.txt_surface.render(self.text, False, self.textcolor)
    y = (self.rect.height // 2) - (text.get_rect().height // 2)
    self.display.blit(text, (self.rect.x + 5, self.rect.y + y))


class Table():
  def __init__(self, display, loc, color, bordersize, bordercolor, cellborder,textcolor, textsize, gridsize, titles, sizes):
    self.x = loc[0]
    self.y = loc[1]
    self.w = loc[2]
    self.h = loc[3]
    self.color = color
    self.bordersize = bordersize
    self.bordercolor = bordercolor
    self.cellborder = cellborder
    self.textcolor = textcolor
    self.font = pygame.font.Font('assets/Minecraftia.ttf', textsize)
    self.textsize = textsize
    self.display = display
    self.cellx = gridsize[0]
    self.celly = gridsize[1]
    self.titles = titles
    self.data = []
    # index 0 is widths for every cell, index 1 is height
    self.cellheight = sizes[1]
    self.cellwidths = sizes[0]
  def sortkey(self, element):
    return int(element[2])
  def render(self):
    # Draw border
    pygame.draw.rect(self.display, self.bordercolor, pygame.Rect(self.x - self.bordersize, self.y - self.bordersize, self.w + self.bordersize*2, self.h + self.bordersize*2),border_radius=10)
    # Draw middle
    r = pygame.Rect(self.x, self.y, self.w, self.h)
    pygame.draw.rect(surface=self.display,color=self.color,rect = r,border_radius=10)
    for y, row in enumerate([self.titles] + sorted(self.data, key = self.sortkey, reverse = True)):
      for x, element in enumerate(row):
        if(y > self.celly):
          return
        
        # Draw border
        cell = pygame.Rect(self.x + sum(self.cellwidths[:x]), self.y + (self.cellheight * y), self.cellwidths[x], self.cellheight)
        pygame.draw.rect(self.display, self.bordercolor, cell)
        
        # Draw cells
        cell.x += self.cellborder
        cell.y += self.cellborder
        cell.width -= self.cellborder*2
        cell.height -= self.cellborder*2
        
        pygame.draw.rect(self.display, self.color, cell)
        words = Label(display=self.display, loc = (cell.x, cell.y,cell.x + cell.width, + cell.y + cell.height), text = str(element), textcolor = (255,255,255), textsize = self.textsize)
        words.render()