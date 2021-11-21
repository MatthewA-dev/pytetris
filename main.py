import pygame
import copy
import enum
from game import Board, AI, Score
from rendering import Button, Label

pygame.init()
pygame.font.init()



class State(enum.Enum):
  MAIN = 0
  GAME = 1
  LOSE = 2
  PAUSED = 3
  LEADERBOARD = 4

class Game():
  def __init__(self, display):
    self.state = State.MAIN
    self.display = display
    self.hasAI = False
    self.reset()
    self.font = pygame.font.Font('assets/Minecraftia.ttf', 20)

    btemplate = Button(display = self.display, loc = (200 ,350, 400, 400),color = (0,0,0), hovercolor=(50,50,50), bordersize=3, bordercolor=(255,255,255), func=self.setState, text = "START", textcolor=(255,255,255), textsize=20)
    # Main menu assets

    self.logo = pygame.image.load("assets/logo.png")
    self.logo = pygame.transform.scale(self.logo, (400, 250))

    self.startButton = copy.copy(btemplate)
    self.startButton.text = "START"
    self.startButton.loc = (200 ,350, 400, 400)

    self.startAIButton = copy.copy(btemplate)
    self.startAIButton.text = "START WITH AI"
    self.startAIButton.loc = (200 ,450, 400, 500)

    self.leaderButton = copy.copy(btemplate)
    self.leaderButton.text = "LEADERBOARD"
    self.leaderButton.loc = (200 ,550, 400, 600)

    # Pause screen assets

    self.unpausebtn = copy.copy(btemplate)
    self.unpausebtn.loc = (200 ,450, 400, 500)
    self.unpausebtn.text = "UNPAUSE"

    self.backbtn = copy.copy(btemplate)
    self.backbtn.text = "BACK TO MENU"

    self.pauseLabel = Label(loc=(200 ,250, 400, 300), display = display, text = "PAUSED", textcolor=(255,255,255), textsize=20)

  def mainmenu(self):
    for event in pygame.event.get():  
      if event.type == pygame.QUIT:
        pygame.quit()
      elif event.type == pygame.MOUSEBUTTONDOWN:
        # Deal with clicks on buttons
        if(self.state == State.MAIN):
          if self.startButton.isHovering(pygame.mouse.get_pos()):
            self.startButton.func(False, State.GAME)
          elif self.startAIButton.isHovering(pygame.mouse.get_pos()):
            self.startAIButton.func(True, State.GAME)
          elif self.leaderButton.isHovering(pygame.mouse.get_pos()):
            self.startAIButton.func(False, State.LEADERBOARD)
        elif(self.state== State.LEADERBOARD):
          pass
    
    # Render stuff
    if(self.state == State.MAIN):
      self.startButton.render()
      self.startAIButton.render()
      self.leaderButton.render()
      self.display.blit(self.logo,(100,50))
    elif(self.state == State.LEADERBOARD):
      pass

  def game(self):
    # game loop
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
      # Deal with menu clicks
      elif event.type == pygame.MOUSEBUTTONDOWN:
        # Deal with clicks on buttons
        if(self.state == State.PAUSED):
          if self.backbtn.isHovering(pygame.mouse.get_pos()):
            self.backbtn.func(False, State.MAIN)
            self.reset()
          elif self.unpausebtn.isHovering(pygame.mouse.get_pos()):
            self.unpausebtn.func(self.hasAI, State.GAME)
      # Manage key inputs
      elif event.type == pygame.KEYDOWN:
        if(self.state != State.LOSE):
          if(not self.hasAI):
            if pygame.key.get_pressed()[pygame.K_LEFT]:
              self.board.shiftPiece(-1)
            if pygame.key.get_pressed()[pygame.K_RIGHT]:
              self.board.shiftPiece(1)
            if pygame.key.get_pressed()[pygame.K_z]:
              self.board.rotatePiece("LEFT", self.board.piece, False)
            if pygame.key.get_pressed()[pygame.K_x]:
              self.board.rotatePiece("RIGHT", self.board.piece, False)
            if pygame.key.get_pressed()[pygame.K_DOWN]:
              #HARDDROP
              while not self.board.checkOverlapping(self.board.piece,self.board.piececoords, self.board.grid) and not self.board.checkInGround(self.board.piece, self.board.piececoords):
                self.board.piececoords = (self.board.piececoords[0], self.board.piececoords[1] + 1)
              self.board.piececoords = (self.board.piececoords[0], self.board.piececoords[1] - 1)
              self.board.placePiece(False, self.board.piece, self.board.piececoords)
          if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            if(self.state == State.PAUSED):
              self.setState(self.hasAI, State.GAME)
            else:
              if(self.state != State.LOSE):
                self.setState(self.hasAI, State.PAUSED)
    # Game logic
    if(self.state not in [State.LOSE, State.PAUSED]):
      if(self.hasAI):
        self.ai.tick()
      self.board.tick()

    # Render menus
    if(self.state == State.GAME):
      self.board.render()
    elif(self.state == State.LOSE):
      # Render lose
      pass
    elif(self.state == State.PAUSED):
      self.board.score.render()
      self.unpausebtn.render()
      self.backbtn.render()
      self.pauseLabel.render()

  def triggerlose(self):
    self.state = State.LOSE

  def setState(self, aiVal, state):
    self.hasAI = aiVal
    self.state = state
  
  def reset(self):
    self.board = Board(150, 100, 450, 700, 10, 20, self.display, Score(50,20,25,self.display), self.hasAI, self.triggerlose)
    self.ai = AI(self.board)
    self.setState(False, State.MAIN)

  def gameloop(self):
    while True:
      self.display.fill((0,0,0))
      # Gameplay
      if(self.state in [State.LOSE, State.GAME, State.PAUSED]):
        self.game()
      # MAIN MENU
      elif(self.state == State.MAIN) or self.state == State.LEADERBOARD:
        self.mainmenu()
      pygame.display.flip()

def main():
  display = pygame.display.set_mode([600,800])
  game = Game(display=display)
  game.gameloop()
  

if( __name__ == "__main__"):
  main()