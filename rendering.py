import pygame

class Label:
    def __init__(self, display, loc, text, textcolor, textsize):
      self.loc = loc
      self.textcolor = textcolor
      self.textsize = textsize
      self.text = text
      self.font = pygame.font.Font('assets/Minecraftia.ttf', 20)
      self.display = display
    def render(self):

      text = self.font.render(self.text,False, self.textcolor)
      # Center the text
      x = ((self.loc[2] - self.loc[0]) // 2) - (text.get_rect().width // 2)
      y = ((self.loc[3] - self.loc[1]) // 2) - (text.get_rect().height // 2)
      self.display.blit(text, (self.loc[0] + x, self.loc[1] + y))

class Button:
  def __init__(self, display, loc, color, hovercolor, bordersize, bordercolor, func, text, textcolor, textsize):
    self.loc = loc
    self.color = color
    self.hovercolor = hovercolor
    self.bordersize = bordersize
    self.bordercolor = bordercolor
    self.textcolor = textcolor
    self.textsize = textsize
    self.func = func
    self.text = text
    self.font = pygame.font.Font('assets/Minecraftia.ttf', 20)
    self.display = display
  
  def render(self):
    mousepos = pygame.mouse.get_pos()
    color = self.color
    
    if(self.isHovering(mousepos)):
      color = self.hovercolor
    
    # Draw border
    pygame.draw.rect(self.display, (255,255,255), pygame.Rect(self.loc[0] - self.bordersize, self.loc[1] - self.bordersize, abs(self.loc[2] - self.loc[0]) + self.bordersize*2, abs(self.loc[3] - self.loc[1]) + self.bordersize*2),border_radius=10)
    # Draw middle
    r = pygame.Rect(self.loc[0], self.loc[1], (self.loc[2] - self.loc[0]), (self.loc[3] - self.loc[1]))
    pygame.draw.rect(surface=self.display,color=color,rect = r,border_radius=10)
    text = self.font.render(self.text,False, self.textcolor)
    # Center the text
    x = ((self.loc[2] - self.loc[0]) // 2) - (text.get_rect().width // 2)
    y = ((self.loc[3] - self.loc[1]) // 2) - (text.get_rect().height // 2)
    self.display.blit(text, (self.loc[0] + x, self.loc[1] + y))
  
  def isHovering(self, mousepos):
    if(mousepos[0] > self.loc[0] and mousepos[0] < self.loc[2] and mousepos[1] > self.loc[1] and mousepos[1] < self.loc[3]):
      return True
    return False