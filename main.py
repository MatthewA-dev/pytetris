import time
from random import choice, randint
import pygame
import copy
import os
import math

pygame.init()
pygame.font.init()
os.chdir(os.path.dirname(os.path.abspath(__file__)))
# load pieces
pieceFile = open("pieces.txt","r")
pieces = pieceFile.read().split("\n;\n")
pieceFile.close()
p = []
for piece in pieces:
  piece = piece.split("\n")
  tempiece = [[int(y) for y in x] for x in piece]
  p.append(tempiece)

class AI():
  def __init__(self, board):
    self.board = board
  
  def getmove(self,piece):
    def key(element):
      return element[0]
    bestmove = (math.inf, [0,0], piece) 
    #moves = []
    for _ in range(4):
      pc = self.board.getPieceCoords(piece)
      #pc = [0,0]
    # get the furthest to the left coord that's valid for every piece rotation
      while(not (self.board.checkOut(piece, pc) or self.board.checkOverlapping(piece,pc,self.board.grid))):
        pc = [pc[0] - 1, pc[1]]
      pc = [pc[0] + 1, pc[1]]
      # Try every possible place for piece
      while not (self.board.checkOut(piece, pc) or self.board.checkOverlapping(piece,pc,self.board.grid)):
        # Hard drop the piece
        piececoords = copy.deepcopy(pc)
        while not self.board.checkOverlapping(piece,piececoords, self.board.grid) and not self.board.checkInGround(piece, piececoords):
          piececoords = (piececoords[0], piececoords[1] + 1)
        piececoords = (piececoords[0], piececoords[1] - 1)

        score = self.evaluate(self.board.placePiece(True, piece, piececoords), False)
        #moves.append((score,(pc,piece)))
        if(score < bestmove[0]):
          bestmove = (score, pc, piece)

        pc = [pc[0] + 1, pc[1]]
      piece = self.board.rotatePiece("RIGHT", piece, True)
    
    #moves.sort(key = key)

    #return (0,moves[0][1][0],moves[0][1][1])
    return bestmove
      
  # only get the evaluation of the board, ignoring next piece
  def evaluate(self, grid, onlyGrade):
    def getBoardDif(grid):
      heights = []
      for x in range(len(grid[0])):
        col = []
        for row in grid:
          col.append(row[x])
        height = 0
        for y in col:
            if(y == 0):
                height += 1
            else:
                break
        heights.append(len(col) - height)
      d = 0
      for i, h in enumerate(heights):
        try:
          if(i == 0):
            continue
          d += abs(h - heights[i - 1])
        except:
          continue
      return d

    def getHeight(grid):
      height = 0 
      for row in grid:
        if(len(set(row)) != 1):
          break
        else:
          height += 1
      height = len(grid) - height
      return height

    def getHoleCount(grid):
      holecount = 0

      for x in range(len(grid[0])):
        col = []
        for row in grid:
          col.append(row[x])
        changes = 0
        first = False
        for c in col:
          if(first):
            if c == 0:
              changes += 1
          elif(c != 0):
            first = True
        holecount += changes
      return holecount
      
    # Get difference between max height and other lines to avoid the spiky surface
    def getMaxDiff(grid):
      hs = [] # heights
      for x in range(len(grid[0])):
        col = []
        for row in grid:
          col.append(row[x])
        h = 0 
        for r in col:
          if(r != 0):
            break
          else:
            h += 1
        h = len(row) - h
        hs.append(h)

      dif = 0
      m = max(hs)
      for h in hs:
        dif += m - h
      return dif
    
    #return (holecount, height, dif)
    # Check that the next piece wont murder it
    if(not onlyGrade):
      if(self.board.checkDead(grid)):
        return 100*(getHoleCount(grid)*3 + getHeight(grid)*(1/10) + getBoardDif(grid)/2)
    #return (getHoleCount(grid)*2 + getBoardDif(grid)/5) / (getHeight(grid) / 20 + 1) + 2*(getHeight(grid))
    return getHoleCount(grid)*3 + getHeight(grid)*(1/10) + getBoardDif(grid)/2

  def tick(self):
    if(time.time() - self.board.lastTime > self.board.fallspeed):
      move = self.getmove(self.board.piece)
      piece = move[2]
      piececoords = move[1]
      while not self.board.checkOverlapping(piece,piececoords,self.board.grid) and not self.board.checkInGround(piece, piececoords):
        piececoords = (piececoords[0], piececoords[1] + 1)
      piececoords = (piececoords[0], piececoords[1] - 1)
      self.board.placePiece(False, piece, piececoords)


class Score():
  def __init__(self,x1, y1, size, screen):
    self.loc = (x1,y1)
    self.font = pygame.font.Font('Minecraftia.ttf', size)
    self.score = 0
    self.screen = screen
    self.level = 1
  def addScore(self, score):
    self.score += score
  def render(self):
    score = self.font.render("Score: " + str(self.score), True, (255,255,255))
    level = self.font.render("Level: " + str(self.level), True, (255,255,255))
    self.screen.blit(score, self.loc)
    self.screen.blit(level, (50,60))


class Board():
  def __init__(self, x1, y1, x2, y2, blockx, blocky, surface, score, hasAI):
    # non rendered part of board
    #blocky += 2
    # seconds for piece to fall 
    self.fallspeed = 0.00000001
    self.size = (x1,y1,x2,y2)
    self.gridsize = (blockx,blocky)
    self.surface = surface
    self.grid = [[0 for _ in range(blockx)] for _ in range(blocky)]
    self.lastTime = time.time()
    self.stack = copy.deepcopy(p)
    self.piece = self.choiceRemove()
    #self.piecestack = copy.deepcopy(p)
    #self.piece = p[1]
    self.piececoords = self.getPieceCoords(self.piece)
    self.score = score
    self.level = 1
    self.linescleared = 0
    # required lines to pass level
    self.requiredlines = 10
    self.hasAI = hasAI
  
  # Get piece coords for initial pos of piece
  def getPieceCoords(self,piece):
    return [(self.gridsize[0] // 2) - (len(piece) // 2), 0]

  # Get piece and remove it from stack
  def choiceRemove(self):
    piece = self.stack.pop(randint(0,len(self.stack) - 1))
    if(len(self.stack) == 0):
      self.stack = copy.deepcopy(p)
    return piece

  def shiftPiece(self, xshift):
    self.piececoords = (self.piececoords[0] + xshift, self.piececoords[1])
    # Check if it's out of bounds
    for piecerow in self.piece:
        for xindex, pi in enumerate(piecerow):
          if(pi == 1):
            if(self.piececoords[0] + xindex > self.gridsize[0] - 1 or self.piececoords[0] + xindex < 0):
              self.piececoords = (self.piececoords[0] - xshift, self.piececoords[1])
    # Check if its overlapping
    if(self.checkOverlapping(self.piece, self.piececoords, self.grid)):
      self.piececoords = (self.piececoords[0] - xshift, self.piececoords[1])
  
  def rotatePiece(self, rotdir, piece, returnPiece):
    rotpiece = [[0 for _ in range(len(piece[0]))] for _ in range(len(piece))]
    if(rotdir == "LEFT"):
     for yindex, row in enumerate(piece):
      for xindex, p in enumerate(row):
        rotpiece[len(piece) - 1 - xindex][yindex] = p
    elif(rotdir == "RIGHT"):
      for yindex, row in enumerate(piece):
        for xindex, p in enumerate(row):
          rotpiece[xindex][len(piece) - 1 - yindex] = p
    if(not returnPiece):
      if(self.checkOverlapping(rotpiece, self.piececoords, self.grid) or self.checkOut(rotpiece, self.piececoords)):
        self.fitPiece(rotpiece)
        return
      else:
        self.piece = rotpiece
    else:
      return rotpiece

  def fitPiece(self, piece):
    MAXCHANGE = 4
    lowestChange = MAXCHANGE ** 2
    lowestcoord = []
    for xchange in range(MAXCHANGE*2 + 1):
      xchange -= MAXCHANGE
      for ychange in range(MAXCHANGE*2 + 1):
        ychange -= MAXCHANGE
        tempcoords = [self.piececoords[0] + xchange, self.piececoords[1] + ychange]
        if(self.checkOverlapping(piece,tempcoords, self.grid) or self.checkOut(piece, tempcoords)):
          continue
        else:
          if(lowestChange > ((self.piececoords[0] - tempcoords[0])**2 + (self.piececoords[1] - tempcoords[1])**2)**0.5):
            lowestChange = ((self.piececoords[0] - tempcoords[0])**2 + (self.piececoords[1] - tempcoords[1])**2)**0.5
            lowestcoord = copy.deepcopy(tempcoords)
    if(lowestcoord == []):
      return False
    self.piececoords = lowestcoord
    self.piece = piece
    return True

  # To place the piece on the grid for rendering
  def overlapPiece(self):
    tempGrid = copy.deepcopy(self.grid)
    for index, piecerow in enumerate(self.piece):
      try:
        r = tempGrid[self.piececoords[1] + index]
      except IndexError:
        continue
      for x in range(self.piececoords[0], self.piececoords[0] + 4):
        try:
          if(x < 0):
            raise IndexError
          if(r[x] == 0):
            r[x] = piecerow[x - self.piececoords[0]]
        except IndexError:
          pass
      tempGrid[self.piececoords[1] + index] = r
    return tempGrid
  
  # Checking if placing the next piece will kill us
  def checkDead(self, grid):
    for piece in p:
      for _ in range(4):
        if(self.checkOverlapping(piece,self.getPieceCoords(piece),grid)):
          return True
        piece = self.rotatePiece("RIGHT",piece ,True)
    return False

  def checkOut(self, piece, piececoords):
    for yindex, piecerow in enumerate(piece):
        for xindex, pi in enumerate(piecerow):
          if(pi == 1):
            if(piececoords[0] + xindex > self.gridsize[0] - 1 or piececoords[0] + xindex < 0 or self.checkInGround(piece, piececoords) or piececoords[1] + yindex < 0):
              return True
    return False
  
  def checkInGround(self, piece, piececoords):
    inground = False
    for index, piecerow in enumerate(piece):
      if(inground):
        break
      for pi in piecerow:
        if(pi == 1):
          if(piececoords[1] + index > self.gridsize[1] - 1):
            inground = True
    return inground
  
  # Check if current piece is overlapping with grid
  def checkOverlapping(self, piece, piececoords, grid):
    for yindex, piecerow in enumerate(piece):
      for xindex, p in enumerate(piecerow):
        try:
          if(grid[piececoords[1] + yindex][piececoords[0] + xindex] != 0 and p != 0):
            return True
        except IndexError:
          pass
    return False
      
  def placePiece(self, returnBoard, piece, piececoords):
    g = copy.deepcopy(self.grid)
    for index, piecerow in enumerate(piece):
      try:
        r = g[piececoords[1] + index]
      except IndexError:
        continue
      for x in range(piececoords[0], piececoords[0] + 4):
        try:
          if(x < 0):
            raise IndexError
          if(r[x] == 0):
            r[x] = piecerow[x - piececoords[0]]
        except IndexError:
          continue
      g[piececoords[1] + index] = r
    if(not returnBoard):
      self.piece = self.choiceRemove()
      self.piececoords = self.getPieceCoords(self.piece)
      # Check for fail
      if(self.checkOverlapping(piece=self.piece,piececoords=self.piececoords, grid=self.grid)):
        print(f"Fallspeed: {self.fallspeed} seconds per tick")
        print(f"Level: {self.level}")
        #get score object
        print(f"Score: {self.score.score}")
        print(f"Lines Cleared: {self.linescleared} lines cleared")
        print(f"Has AI: {self.hasAI}")
        print("Grid: ")
        print("\n".join([str(x) for x in self.grid]))
        exit()

    # Check for a tetris
    tindexs = []
    for index, row in enumerate(g):
      if(0 not in row):
        tindexs.append(index)
    tindexs.reverse()
    # Calculate points. level and new fallspeeds
    sc = {0 : 0, 1 : 100, 2: 300, 3: 500, 4: 800}
    if(not returnBoard):
      self.linescleared += len(tindexs)
      self.score.addScore(sc[len(tindexs)] * self.level)
      self.score.level = self.level
      last = self.level
      self.level = (self.linescleared + self.requiredlines) // self.requiredlines
      if(last != self.level):
        self.fallspeed = self.fallspeed / 1.25
    for i in tindexs:
      g.pop(i)
    for _ in range(len(tindexs)):
      g.insert(0, [0 for _ in range(self.gridsize[0])])
    
    # Reset last time
    if(not returnBoard):
      self.lastTime = time.time()
      self.grid = g
    else:
      return g

  def render(self):
    self.surface.fill((0,0,0))
    score = pygame.font.Font('Minecraftia.ttf', 30).render("Grade: " + str(round(AI.evaluate(AI, self.grid, True),2)), True, (255,255,255))
    self.surface.blit(score, (50,750))
    self.score.render()
    tempGrid = self.overlapPiece()
    # Overlap piece coords with grid
    BORDER = 2
    pygame.draw.rect(self.surface, (0,0,0), pygame.Rect(self.size[0], self.size[1], self.size[2] - self.size[0] + BORDER, self.size[3] - self.size[1] + BORDER))
    for yindex, row in enumerate(tempGrid): # TODO remove top two: self.grid[2:]
      for xindex, block in enumerate(row):
        blocksx, blocksy = (self.size[2] - self.size[0]) // self.gridsize[0], (self.size[3] - self.size[1]) // (self.gridsize[1]) # TODO: subract two from gridsize[1] : gridsize[1] - 2
        # Adding one to add a border around the blocks
        if(block == 1):
          #color = (255,25,0)
          color = (110,110,110)
        else:
          color = (255,255,255)
        pygame.draw.rect(self.surface, color, pygame.Rect(blocksx * xindex + BORDER + self.size[0], blocksy * yindex + BORDER + self.size[1], blocksx - BORDER, blocksy - BORDER))

  def tick(self):
    if(time.time() - self.lastTime > self.fallspeed):
      self.lastTime = time.time()
      self.piececoords = (self.piececoords[0], self.piececoords[1] + 1)
      # if too low, place piece
      inground = self.checkInGround(self.piece, self.piececoords)
      if(inground):
        self.piececoords = (self.piececoords[0], self.piececoords[1] - 1)
        self.placePiece(False, self.piece, self.piececoords)
      if(not inground):
        # if in piece, place piece
        if(self.checkOverlapping(self.piece,self.piececoords, self.grid)):
          self.piececoords = (self.piececoords[0], self.piececoords[1] - 1)
          self.placePiece(False, self.piece, self.piececoords)


def main():
  display = pygame.display.set_mode([600,800])
  hasAI = True
  board = Board(150, 100, 450, 700, 10, 20, display, Score(50,30,25,display), hasAI)
  ai = AI(board)
  run = True
  # game loop
  while run:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False
      elif event.type == pygame.KEYDOWN:
        if(not hasAI):
          if pygame.key.get_pressed()[pygame.K_LEFT]:
            board.shiftPiece(-1)
          if pygame.key.get_pressed()[pygame.K_RIGHT]:
            board.shiftPiece(1)
          if pygame.key.get_pressed()[pygame.K_z]:
            board.rotatePiece("LEFT", board.piece, False)
          if pygame.key.get_pressed()[pygame.K_x]:
            board.rotatePiece("RIGHT", board.piece, False)
          if pygame.key.get_pressed()[pygame.K_DOWN]:
            #HARDDROP
            while not board.checkOverlapping(board.piece,board.piececoords, board.grid) and not board.checkInGround(board.piece, board.piececoords):
              board.piececoords = (board.piececoords[0], board.piececoords[1] + 1)
            board.piececoords = (board.piececoords[0], board.piececoords[1] - 1)
            board.placePiece(False, board.piece, board.piececoords)
    if(hasAI):
      ai.tick()
    board.tick()
    board.render()
    pygame.display.flip()
  pygame.quit()

if( __name__ == "__main__"):
  main()