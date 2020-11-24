"""
Created on Mon Oct 5 13:25:06 2020

@author: Luca Damian and Larry Ditton

This is an object oriented tic-tac-toe game in which the tics are literal ticks
and the toes are literal toes. It has a game manager class (manager), a player
class that controls the tiles, and a board class. Ther is a splash screen (1pt
extra credit) and a game over screen (1 pt extra credit). 

Code modifications are annotated below. 
"""

import turtle, random, time
import numpy as np



# =============CLASSES============

#Game manager class that calls main function which runs game, shows splash 
#and end screens and determines winner.
class Manager:
    def __init__(self):
        
        #Define attributes:
        turtle.tracer(0)
        self.panel=turtle.Screen()
        self.panel.colormode(255)
        self.w=1000
        self.h=self.w       
        self.size = 3
        self.forest = (62, 86, 65)
        self.chestnut = (162, 73, 54)
        self.ticFirst=False
        self.running=True
        self.winner = 0
        
        #Turtles for splash and winner screen(extra credit)
        self.startTurt = turtle.Turtle()
        self.winTurt = turtle.Turtle()
        
        #List of lists to act as scoreboard to determine winner:
        self.scoreBoard = [['', '', ''],  
                           ['', '', ''],
                           ['', '', '']]
                 
        #Turtle setup for panel and start/end screens:
        turtle.setup(self.w,self.h)
        self.panel.setworldcoordinates(0, self.w, self.h, 0)
        self.panel.bgcolor(self.forest)
        self.panel.addshape("Toe3.gif")
        self.panel.addshape("Tick2.gif")
        self.panel.addshape("TicWins.gif")
        self.panel.addshape("ToeWins.gif")
        self.panel.addshape("DrawGame.gif")
        self.panel.addshape("Splash.gif")
        self.startTurt.up()
        self.startTurt.goto(500,500)
        self.winTurt.up()
        self.winTurt.goto(500,500)
        
        #Splash screen and start game once splash screen clicked:
        self.panel.clear()
        self.startTurt.shape("Splash.gif")
        self.startTurt.onclick(self.main)
             
    
            
    def main(self, x,y):
        '''Main game manager method that creates board and player object and
        determines winner'''
        
        self.startTurt.clear()
        self.startTurt.hideturtle()
        turtle.tracer(0)
        self.panel.colormode(255)
        self.panel.bgcolor(self.forest)
        
        #Instantiante board object and draw board:
        self.TicBoard = Board(self.w, self.size, self.chestnut)
        self.TicBoard.drawBoard()
        
        #Instantiate player object
        self.Tiles = Players(self.size, self.w, self.ticFirst, self.forest, self.scoreBoard)
       
                 
        #While game runs keep updating panel and checking for endgame condition:
        while self.running:
            
            self.endGame(self.scoreBoard, self.winner, self.winTurt)
            self.panel.update()     
                            
          
        self.panel.mainloop() # keep listeners on
        

        
    def endGame(self, scoreBoard, winner, winTurt):
        '''Check to see if there is a winner (from checkWin method) or if 
        there is a draw if all spaces filled. Show end screen if winner/draw 
        determined'''
        
        #Check and see which type of winner and stop running game if winner 
        #determined:
        if self.checkWin(scoreBoard)=='X':
            winner = 1
            print('Tic wins!')
            self.running = False
        elif self.checkWin(scoreBoard)=='O':
            winner = 2
            print('Toe Wins!')
            self.running = False
        elif self.checkWin(scoreBoard)=='':
            pass

        elif self.checkWin(scoreBoard)==0:
            for i in scoreBoard:
                if '' in i:
                    game = False
                    break
                else:
                    game = True
            if game:
                winner = 3
                print('Stalemate!')
                self.running=False
                
        #Show appropriate end game splash screen:           
        if winner == 1:
                self.panel.clear()
               
                winTurt.shape("TicWins.gif")
                
        elif winner == 2:
                self.panel.clear()
             
                winTurt.shape("ToeWins.gif")
                
        elif winner == 3:
                self.panel.clear()
          
                winTurt.shape("DrawGame.gif")
                                 
   
    #The following method modified from Dr. Z's "checkWin" starter code:
    def checkRows(self, scoreBoard):
        '''Looks along a row to see if everything in the row is the same value.
        If the entire row is the same, it returns the value found across the whole row.
        If the entire row is NOT the same, it returns 0.'''
        for row in scoreBoard:
            if len(set(row)) == 1:
                return row[0]
        return 0 # you may want to change this value! (this is the "no-3-in-a-row" "value)
    
    def checkDiagonals(self, scoreBoard):
        '''Looks along diagonals for the same values thorughout.
        If the entire diagonal is the same (length doesn't matter), this function
        returns the value found on the diagaonal.
        If the entire diagonal is NOT the same, this function returns 0.'''
        if len(set([scoreBoard[i][i] for i in range(len(scoreBoard))])) == 1:
            return scoreBoard[0][0]
        if len(set([scoreBoard[i][len(scoreBoard)-i-1] for i in range(len(scoreBoard))])) == 1:
            return scoreBoard[0][len(scoreBoard)-1]
        return 0 # you may want to change this value! (this is the "no-3-in-a-row" "value)
    
    def checkWin(self, scoreBoard):
        '''Checks the for the win conditions by looking through the rows and a 
        diagonal in one direction, then rotating the list and looking for rows 
        again (effectively columns and diagonal in the opposite direction).'''
        #transposition to check rows, then columns
        for newBoard in [scoreBoard, np.transpose(scoreBoard)]:
            result = self.checkRows(newBoard)
            if result:
                return result
        return self.checkDiagonals(scoreBoard)    
        

#Board class which draws the game board:
class Board:
    def __init__(self, width, size, lineColor):
        self.width = width
        self.size=size
        self.lines=size-1
        self.startLoc=width/size
        self.gridTurt = turtle.Turtle()
        self.gridTurt.color(lineColor)
        self.gridTurt.width(10)
        self.gridTurt.up()
        self.gridTurt.speed(0)
    
    
    def drawBoard(self):
        '''Draws the grid lines on the board depending on number of grids'''
        
        #Create Horizontal Lines
        for i in range(self.lines):
            
            self.gridTurt.up()
            self.gridTurt.goto((self.width/100),(self.startLoc))
            self.gridTurt.down()
            self.gridTurt.forward(self.width-(self.width/50))
            self.gridTurt.up()
            self.startLoc += self.width/self.size

        self.startLoc = self.width/self.size
        self.gridTurt.left(90)
        self.gridTurt.up()
       
        #Create Vertical Lines
        for i in range(self.lines):
            
            self.gridTurt.goto((self.startLoc),(self.width/100))
            self.gridTurt.down()
            self.gridTurt.forward(self.width-(self.width/50))
            self.gridTurt.up()
            self.startLoc += self.width/self.size



#Player class that creates tiles, determines which tile is selected,
#"flips" the selected tiles (alternates when selected), and adds appropriate 
#score to scoreBoard list:
    
class Players:
    def __init__(self, size, width, ticFirst, shapeColor, scoreBoard): 
        self.size = size
        self.grids = size**2        
        self.sqSize = width/size
        self.buff = self.sqSize/2 #for use in size of clickable area
        self.ticSize = self.sqSize/21 #for use with turtle "square" shape scaling
        self.xyPos = width/size/2
        self.ticFirst = ticFirst #determines which image is shown upon 1st click
        self.scoreBoard = scoreBoard
        print("Tick Turn!")
       
        #Lists for positions and player turtles:
        self.position = []
        self.ticToes = []
    
        #Create positions for player tiles to go to     
        for Ys in range(self.size):
            for Xs in range(self.size):
                self.position.append((self.xyPos+Xs*self.sqSize,self.xyPos+Ys*self.sqSize))
        
        #Create tiles 
        for times in range(self.grids):
            self.ticToes.append(turtle.Turtle())
        
        #Position tiles and add click functionality to tiles
        for times in range(self.grids):
            self.ticToes[times].speed(0)
            self.ticToes[times].up()
            self.ticToes[times].shape("square")
            self.ticToes[times].color(shapeColor)
            self.ticToes[times].shapesize(self.ticSize, self.ticSize)
            self.ticToes[times].goto(self.position[times])
            #Call flip method in init function (extra credit):
            self.ticToes[times].onclick(self.flip)   
            
        
    #The following function modified from Dr. Z's "selectTurtle" starter code
    #The function determines which tile was clicked and returns the ID of that tile
    def whereClicked(self,x,y):
        '''to see if click is within range of one of a list of turtles
        and identify that turtle'''
       
        for i in range(len(self.ticToes)):
            
            tileX = self.ticToes[i].xcor() # get x position of each tile
            tileY = self.ticToes[i].ycor() # get y position of each tile
            
           
            if tileX - self.buff < x < tileX + self.buff and tileY - self.buff < y < tileY + self.buff:
                # see if click is within a grid tile
                return i #return the index of the ticToe list
                
    
    def flip(self,x,y):
        '''Callback function for onclick to show a tick or toe and alternate on
        each subsequent click - 2 player game''' 
        
        selected = self.whereClicked(x,y)    #use whereClicked to determine clicked square
     
        self.ticFirst = not self.ticFirst    #allows for alternating images (2 player game)
        
       
        #Show correct picture at tile selected and add to scoreBoard list for 
        #use in checkwin:
            
        if self.ticFirst == True:   
            print("Toe Turn")
            self.ticToes[selected].shape("Tick2.gif")
            
            if selected <= 2:
                self.scoreBoard[0][selected] = 'X'
            
            elif 3 <= selected <= 5:
                numSel = selected%3
                self.scoreBoard[1][numSel] = 'X'
                
            elif 6 <= selected <= 8:
                numSel = selected%3
                self.scoreBoard[2][numSel] = 'X'
                
        
        else:
            print("Tick Turn")
            self.ticToes[selected].shape("Toe3.gif")
           
            if selected <= 2:
                self.scoreBoard[0][selected] = 'O'
            
            elif 3 <= selected <= 5:
                numSel = selected%3
                self.scoreBoard[1][numSel] = 'O'
                
            elif 6 <= selected <= 8:
                numSel = selected%3
                self.scoreBoard[2][numSel] = 'O'


#=================Instantiate game manager and run game!============
game = Manager()
    
turtle.done()
