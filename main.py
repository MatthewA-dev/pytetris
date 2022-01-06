import pygame
import copy
import enum
import csv
import os
import traceback #TODO remove
from game import Board, AI, Score
from rendering import Button, Label, InputBox, Table

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
    self.display = display
    self.hasAI = False
    self.reset()
    self.state = State.MAIN
    self.font = pygame.font.Font('assets/Minecraftia.ttf', 20)
    self.scores = []

    # load scores
    if(not os.path.exists("scores.csv")):
      open("scores.csv","w")
    else:
      with open('scores.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, quotechar='|')
        for row in spamreader:
          self.scores.append(row)
    btemplate = Button(display = self.display, loc = (200 ,350, 200, 50),color = (0,0,0), hovercolor=(50,50,50), bordersize=3, bordercolor=(255,255,255), func=self.setState, text = "START", textcolor=(255,255,255), textsize=20)
    # Main menu assets

    self.logo = pygame.image.load("assets/logo.png")
    self.logo = pygame.transform.scale(self.logo, (400, 250))

    self.startButton = copy.copy(btemplate)
    self.startButton.text = "START"
    self.startButton.loc = (200 ,350, 200, 50)

    self.startAIButton = copy.copy(btemplate)
    self.startAIButton.text = "START WITH AI"
    self.startAIButton.loc = (200 ,450, 200, 50)

    self.leaderButton = copy.copy(btemplate)
    self.leaderButton.text = "LEADERBOARD"
    self.leaderButton.loc = (200 ,550, 200, 50)
    
    self.quitButton = copy.copy(btemplate)
    self.quitButton.text = "QUIT"
    self.quitButton.loc = (200, 650, 200, 50)

    # Pause screen assets

    self.unpausebtn = copy.copy(btemplate)
    self.unpausebtn.loc = (200 ,450, 200, 50)
    self.unpausebtn.text = "UNPAUSE"

    self.backbtn = copy.copy(btemplate)
    self.backbtn.text = "BACK TO MENU"

    self.pauseLabel = Label(loc=(200 ,250, 400, 300), display = display, text = "PAUSED", textcolor=(255,255,255), textsize=20)
  
    # Lose screen assets

    self.loseLabel = Label(display = self.display, loc = (0, 100, self.display.get_width(), 100), text = "GAME OVER", textcolor=(255,255,255), textsize=50)
    self.namelabel = Label(display = self.display, loc = (0, 200, self.display.get_width(), 200), text = "Enter your name", textcolor=(255,255,255), textsize=25)
    self.nameinput = InputBox(display = self.display, x = 125,y=300,w=350,h=50, textcolor = (255,255,255), color=(0,0,0),bordercolor=(255,255,255), bordersize=5, activecolor=(10,10,10), maxlen=13, fontsize=35)
    self.submitScore = copy.copy(btemplate)
    self.submitScore.text = "Submit Score"
    self.submitScore.loc = (200 ,400, 200, 50)

    # Leaderboard
    
    self.leaderLabel = Label(display = self.display, loc = (0, 50, self.display.get_width(), 50), text = "LEADERBOARD", textcolor=(255,255,255), textsize=20)
    self.leaderbackbtn = copy.copy(btemplate)
    self.leaderbackbtn.text = "BACK"
    self.leaderbackbtn.loc = (200, 650, 200, 50)
    self.leaderscore = Table(cellborder = 2,bordercolor=(255,255,255),display = self.display, loc = (100,100,400,500), color = (0,0,0), bordersize=5, textcolor = (255,255,255), titles=["Name","Level", "Points"], sizes=[[150,100,150],50], textsize=15 ,gridsize=[3,10])
    self.leaderscore.data = self.scores

    # Game Things
    
    self.leftcontrolLabels = []
    self.leftcontrolLabels.append(Label(display = self.display, loc = (20, 310, 100, 300), text = "Z = Rotate Left", textcolor=(255,255,255), textsize=12))
    self.leftcontrolLabels.append(Label(display = self.display, loc = (20, 330, 100, 320), text = "X = Rotate Right", textcolor=(255,255,255), textsize=12))
    self.rightcontrolLabels = []
    self.rightcontrolLabels.append(Label(display = self.display, loc = (460, 300, 600, 300), text = "Left = Move Left", textcolor=(255,255,255), textsize=12))
    self.rightcontrolLabels.append(Label(display = self.display, loc = (460, 320, 600, 320), text = "Right = Move Right", textcolor=(255,255,255), textsize=12))
    self.rightcontrolLabels.append(Label(display = self.display, loc = (460, 340, 600, 340), text = "Down = HardDrop", textcolor=(255,255,255), textsize=12))
    


  def mainmenu(self):
    for event in pygame.event.get():  
      if event.type == pygame.QUIT:
        self.quit()
      elif event.type == pygame.MOUSEBUTTONDOWN:
        # Deal with clicks on buttons
        if(self.state == State.MAIN):
          if self.startButton.isHovering(pygame.mouse.get_pos()):
            self.startButton.func(False, State.GAME)
          elif self.startAIButton.isHovering(pygame.mouse.get_pos()):
            self.startAIButton.func(True, State.GAME)
          elif self.leaderButton.isHovering(pygame.mouse.get_pos()):
            self.startAIButton.func(False, State.LEADERBOARD)
          elif self.quitButton.isHovering(pygame.mouse.get_pos()):
            self.quit()
        elif(self.state== State.LEADERBOARD):
          pass
    
    # Render stuff
    if(self.state == State.MAIN):
      self.startButton.render()
      self.startAIButton.render()
      self.leaderButton.render()
      self.display.blit(self.logo,(100,50))
      self.quitButton.render()
    elif(self.state == State.LEADERBOARD):
      pass

  def game(self):
    # game loop
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        self.quit()
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

    for x in self.leftcontrolLabels:
      x.render()
    for x in self.rightcontrolLabels:
      x.render()
    
    # Render menus
    if(self.state == State.GAME):
      self.board.render()
    elif(self.state == State.PAUSED):
      self.board.score.render()
      self.unpausebtn.render()
      self.backbtn.render()
      self.pauseLabel.render()

  def lose(self):
    for event in pygame.event.get():  
      if event.type == pygame.QUIT:
        self.quit()
      elif event.type == pygame.MOUSEBUTTONDOWN:

        if(self.submitScore.isHovering(pygame.mouse.get_pos())):
          self.scores.append([self.nameinput.text, self.board.level, self.board.score.score])
          self.submitScore.func(False,State.MAIN)
          self.reset()
        
        self.nameinput.handleClick(pygame.mouse.get_pos())
      
      elif event.type == pygame.KEYDOWN:
        if(self.nameinput.active):
          if(event.key == pygame.K_RETURN):
            self.scores.append([self.nameinput.text, self.board.level, self.board.score.score])
            self.submitScore.func(False,State.MAIN)
            self.reset()
          elif(event.key == pygame.K_BACKSPACE):
            self.nameinput.text = self.nameinput.text[:len(self.nameinput.text) - 1]
          else:
            self.nameinput.handleType(event.unicode)

    # Render
    self.loseLabel.render()
    self.namelabel.render()
    self.nameinput.render()
    self.submitScore.render()

  def triggerlose(self):
    self.state = State.LOSE

  def quit(self):
    with open('scores.csv', 'w', newline='') as csvfile:
      w = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
      for score in self.scores:
        w.writerow(score)
    pygame.quit()

  def key(self,element):
    return int(element[3])

  def leaderboard(self):
    for event in pygame.event.get():  
      if event.type == pygame.QUIT:
        self.quit()
      elif event.type == pygame.MOUSEBUTTONDOWN:

        if(self.leaderbackbtn.isHovering(pygame.mouse.get_pos())):
          self.leaderbackbtn.func(False, State.MAIN)
    
    # Render
    self.leaderbackbtn.render()
    self.leaderscore.render()
    self.leaderLabel.render()

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
      if(self.state in [State.GAME, State.PAUSED]):
        self.game()
      
      # MAIN MENU
      elif(self.state == State.MAIN):
        self.mainmenu()
      
      elif(self.state == State.LOSE):
        self.lose()
      
      elif(self.state == State.LEADERBOARD):
        self.leaderboard()
      
      

      pygame.display.flip()

def main():
  display = pygame.display.set_mode([600,800], pygame.SCALED | pygame.FULLSCREEN)
  game = Game(display=display)
  try:
    game.gameloop()
  except BaseException:
    #print(traceback.format_exc())
    game.quit()
  

if( __name__ == "__main__"):
  main()