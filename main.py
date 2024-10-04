import sys
import pygame
from pygame import mouse
from pygame.locals import *
import math
import random
import time
#-------------- Initialize Variables -------------- 
width = 600 # Should always divide cleanly by number used to div board
height = 550 # Should always divide cleanly by number used to div board
divNumber = 25 # Number of divisions on the board
boardW = width // divNumber # Number of cells in x axis
boardH = height // divNumber # Number of cells in y axis
totalCells = boardW * boardH # Total number of cells
numberOfMines = math.ceil((0.215*totalCells - 7.59) - (0.0001*(totalCells**2))) # Number of mines based on total cells
#----- Seed -----
seed = random.randint(0,1000) 
print(f"seed: {seed}") #Using the same seed will generate the same board allowing for replaying games
random.seed(seed) 
#-------------- Initialize Pygame Stuff -------------- 
pygame.init()
DISPLAYSURF = pygame.display.set_mode((width, height))
font = pygame.font.Font("freesansbold.ttf", divNumber)
gameOverFont = pygame.font.Font("freesansbold.ttf", width)
#-------------- Classes -------------- 
class cell:
  def __init__(self, x, y, isMine, numberOfSuroundingMines = 0, revealed = False, flagged = False):
    self.x = x
    self.y = y
    self.isMine = isMine
    self.numberOfSuroundingMines = numberOfSuroundingMines
    self.revealed = revealed
    self.flagged = flagged 
#-------------------------------
  def display(self):
    if self.revealed == True:
      if self.isMine == False and self.flagged == False:
        pygame.draw.rect(DISPLAYSURF, (0, 255, 255), (self.x*divNumber, self.y*divNumber,divNumber,divNumber))
        if self.numberOfSuroundingMines > 0:
          DISPLAYSURF.blit(font.render(str(self.numberOfSuroundingMines), True, (0, 0, 0), (0, 255, 255)), (self.x*divNumber, self.y*divNumber))
      elif self.isMine and self.flagged == False:
        pygame.draw.rect(DISPLAYSURF, (255, 0, 0), (self.x*divNumber, self.y*divNumber,divNumber,divNumber))
    elif self.flagged:
      pygame.draw.rect(DISPLAYSURF, (0, 255, 0), (self.x*divNumber, self.y*divNumber,divNumber,divNumber))
    else: 
      pygame.draw.rect(DISPLAYSURF, (0, 0, 0), (self.x*divNumber, self.y*divNumber,divNumber,divNumber),divNumber//10)
        
#-------------- Functions  -------------- 
def createBoard():
  #----- Variables -----
  global numberOfMines
  #---- Create Board ----
  board = []
  for r in range(boardW):
    row = []
    for c in range(boardH):
      newCell = cell(r, c, False)
      row.append(newCell)
    board.append(row)
  return board
#----------
def calcMines():
  for row in range(boardW):
    for col in range(boardH):
      neighbours = 0
      for i in range(-1,2):
        for j in range(-1,2):
          if 0 <= row+i < boardW and 0 <= col+j < boardH:
            if board[row+i][col+j].isMine: neighbours += 1

      board[row][col].numberOfSuroundingMines = neighbours
#----------
def populateMines():
  global numberOfMines
  minesRemaining = numberOfMines
  while minesRemaining > 0:
    row = random.randint(0,boardW-1)
    col = random.randint(0,boardH-1)
    if board[row][col].isMine == False:
      board[row][col].isMine = True
      minesRemaining -= 1
#----------
def revNeighbours(row, col):
  for i in range(-1,2):
    for j in range(-1,2):
      if 0 <= row+i < boardW and 0 <= col+j < boardH and not board[row+i][col+j].flagged:
        board[row+i][col+j].revealed = True
#----------
def clearZeros(row, col):
  for i in range(-1,2):
    for j in range(-1,2):
      if 0 <= row+i < boardW and 0 <= col+j < boardH:
        currentCell = board[row+i][col+j]
        if currentCell.numberOfSuroundingMines == 0 and currentCell.revealed == False and currentCell.isMine == False:
          board[row+i][col+j].revealed = True
          revNeighbours(row+i, col+j)
#----------
def gameOver():
  global board
  replay = False
  for row in range(boardW):
    for col in range(boardH):
      if board[row][col].isMine: 
        board[row][col].flagged = False
        board[row][col].revealed = True
        time.sleep(0.1)
      board[row][col].display()
      pygame.display.update()
      
  
  time.sleep(3)
  pygame.draw.rect(DISPLAYSURF, (255, 0, 0), (0, 0, width, height))
  DISPLAYSURF.blit(font.render("Game Over", True, (0, 0, 0), (255, 0, 0)), (width//5, height//4))
  #pygame.draw.rect(DISPLAYSURF, (0, 0, 0),)
  DISPLAYSURF.blit(font.render("Play Again?", True, (0, 0, 0), (0, 255, 0)), (width//5, height//2))
  while not replay:
    pygame.display.update()
    for event in pygame.event.get():
      #----Quit----
      if event.type == QUIT:
        pygame.quit()
        sys.exit()
      #----Left Click----:
      if event.type == MOUSEBUTTONDOWN:
        mouse_pos_x, mouse_pos_y  = pygame.mouse.get_pos()
        if mouse_pos_x > width//5 and mouse_pos_x < width//5 + width//2 and mouse_pos_y > height//2 and mouse_pos_y < height//2 + height//4:
          replay = True
  reset()
  main()
#----------
def gameWon():
  global board
  replay = False
  for row in range(boardW):
    for col in range(boardH):
      if board[row][col].isMine: 
        board[row][col].revealed = True
        time.sleep(0.1)
      board[row][col].display()
      pygame.display.update()


  pygame.draw.rect(DISPLAYSURF, (0, 255, 0), (0, 0, width, height))
  DISPLAYSURF.blit(font.render("Game Over", True, (0, 0, 0), (0, 255, 0)), (width//5, height//4))
  #pygame.draw.rect(DISPLAYSURF, (0, 0, 0),)
  DISPLAYSURF.blit(font.render("Play Again?", True, (0, 0, 0), (255, 0, 0)), (width//5, height//2))
  while not replay:
    pygame.display.update()
    for event in pygame.event.get():
      #----Quit----
      if event.type == QUIT:
        pygame.quit()
        sys.exit()
      #----Left Click----:
      if event.type == MOUSEBUTTONDOWN:
        mouse_pos_x, mouse_pos_y  = pygame.mouse.get_pos()
        if mouse_pos_x > width//5 and mouse_pos_x < width//5 + width//2 and mouse_pos_y > height//2 and mouse_pos_y < height//2 + height//4:
          replay = True
  reset()
  main()
#----------
def reset():
  global board
  global totalCells
  for row in board:
    for cell in row:
      del cell
#----------
def main():
  #-------------- Start Variables --------------
  global board 
  board = createBoard()
  populateMines()
  calcMines()
  firstAction = 0
  x,y = None, None
  #-------- Main Game Loop --------
  while True:
    DISPLAYSURF.fill((255,255,255))
    #Clicking check
    for event in pygame.event.get():
      #----Quit----
      if event.type == QUIT:
        pygame.quit()
        sys.exit()
      #----Left Click----:
      if event.type == MOUSEBUTTONDOWN:
        firstAction += 1
        mouse_pos_x, mouse_pos_y  = pygame.mouse.get_pos()
        try: 
          x,y = mouse_pos_x//divNumber, mouse_pos_y//divNumber
        except: pass
        #Flag part
        mods = pygame.key.get_mods()  # Get the state of the modifier keys
        if mods & KMOD_CTRL and not board[x][y].revealed :  # Check if Alt key is pressed
            # Alt is held down and mouse button is clicked, toggle the flagged state
            board[x][y].flagged = not board[x][y].flagged
            x, y = None , None
    try:
      if board[x][y].isMine == False and board[x][y].flagged == False:
        clearZeros(x,y)
    except: pass
    #----- Loop Through all Cells -----
    flaggedMines = 0
    correctFlaggedMines = 0
    for r in range(boardW):
      for c in range(boardH):
        board[r][c].display()
        if r == x and c == y:
          if firstAction == 1 and board[r][c].isMine: 
            board[r][c].isMine = False
            calcMines()
          board[r][c].revealed = True
          if board[r][c].isMine == True and board[r][c].flagged == False:
            gameOver()
            return
          #new stuff, not gonna include in assignment
        if board[r][c].flagged: 
          flaggedMines += 1
          if board[r][c].isMine:
            correctFlaggedMines +=1
        if board[r][c].revealed == True and board[r][c].numberOfSuroundingMines == 0 and not board[r][c].flagged:
          revNeighbours(r,c)
          
    pygame.display.update()
    #new stuff, not gonna include in assignment
    if flaggedMines == numberOfMines and flaggedMines == correctFlaggedMines:
      gameWon()
    time.sleep(0.01)
#-------------- Main Program --------------
main()



