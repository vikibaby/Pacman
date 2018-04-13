# mdpAgents.py
# parsons/20-nov-2017
#
# Version 1
#
# The starting point for CW2.
#
# Intended to work with the PacMan AI projects from:
#
# http://ai.berkeley.edu/
#
# These use a simple API that allow us to control Pacman's interaction with
# the environment adding a layer on top of the AI Berkeley code.
#
# As required by the licensing agreement for the PacMan AI we have:
#
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).

# The agent here is was written by Simon Parsons, based on the code in
# pacmanAgents.py

from pacman import Directions
from game import Agent
import api
import random
import game
import util
import sys
#set a number as reward
reward = 0.01
#set a number as discount
discount = 0.8
# set a distance that packman feeling danger
danger = 3
#set a glable value to save the number of food
numoffood = 0

#build map
class Grid:
    # grid:   an array that has one position for each element in the grid.
    # width:  the width of the grid
    # height: the height of the grid
    def __init__(self, width, height):
        self.width = width
        self.height = height
        subgrid = []
        for i in range(self.height):
            row=[]
            for j in range(self.width):
                row.append(0)
            subgrid.append(row)

        self.grid = subgrid

    # print map at terminal.
    def prettyDisplay(self):
        for i in range(self.height):
            for j in range(self.width):
                # print grid elements with no newline
                print self.grid[self.height - (i + 1)][j],
            # A new line after each line of the grid
            print
        # A line after the grid
        print

    # Set and get the values of specific elements in the grid.
    def setValue(self, x, y, value):
        self.grid[y][x] = value

    def getValue(self, x, y):
        return self.grid[y][x]

    # Return width and height to support functions that manipulate the
    # values stored in the grid.
    def getHeight(self):
        return self.height

    def getWidth(self):
        return self.width



class MDPAgent(Agent):

    # Constructor: this gets run when we first invoke pacman.py
    def __init__(self):
        print "Starting up MDPAgent!"
        #mark = 1
        name = "Pacman"

    # Gets run after an MDPAgent object is created and once there is
    # game state to access.

    def registerInitialState(self, state):
        #print "Running registerInitialState for MDPAgent!"
        #print "I'm at:"
        #print api.whereAmI(state)
        global numoffood
        numoffood = len(api.food(state))

        self.makeMap(state)
        self.addWallsFoodToMap(state)
        #self.updateMap(state)
        #self.map1.prettyDisplay()
        #print"registerInitialState"



    # This is what gets run in between multiple games
    def final(self, state):
        print "Looks like the game just ended!"

    # Make a map by creating a grid of the right size
    def makeMap(self,state):
        corners = api.corners(state)
        #print corners
        height = self.getLayoutHeight(corners)
        width  = self.getLayoutWidth(corners)
        self.map1 = Grid(width, height)
        self.map2 = Grid(width, height)
    # Functions to get the height and the width of the grid.
    #
    # We add one to the value returned by corners to switch from the
    # index (returned by corners) to the size of the grid (that damn
    # "start counting at zero" thing again).
    def getLayoutHeight(self, corners):
        height = -1
        for i in range(len(corners)):
            if corners[i][1] > height:
                height = corners[i][1]
        return height + 1

    def getLayoutWidth(self, corners):
        width = -1
        for i in range(len(corners)):
            if corners[i][0] > width:
                width = corners[i][0]
        return width + 1

    # Functions to manipulate two same new map.
    # Put every element in the list of wall  and the list of food into the two maps
    def addWallsFoodToMap(self, state):
        walls = api.walls(state)
        for i in range(len(walls)):
            self.map1.setValue(walls[i][0], walls[i][1], '%')
            self.map2.setValue(walls[i][0], walls[i][1], '%')
        food = api.food(state)
        #print food
        for i in range(len(food)):
            self.map1.setValue(food[i][0], food[i][1],1)
            self.map2.setValue(food[i][0], food[i][1],1)




    # using current utilities in map1 to calculate the new utility of each grid without wall and food
    # save the new utilities we just calculated to the map2
    def updateMap(self, state):
        #print "map1 before update"
        #self.map1.prettyDisplay()

        for i in range(self.map1.getWidth()):
            for j in range(self.map1.getHeight()):
                #only compute untility for the positions which are not wall and food.
                if self.map1.getValue(i, j) != '%'and self.map1.getValue(i, j) != 1 :

                    thevalue = self.map1.getValue(i, j)

                    #the utilitiy of unlegal-move-direction still is the utilitiy of current(this) position
                    if (self.map1.getValue(i+1, j) != '%'):
                        theeast = self.map1.getValue(i+1, j)
                    else: theeast = thevalue

                    if (self.map1.getValue(i-1, j) != '%'):
                        thewest = self.map1.getValue(i-1, j)
                    else: thewest = thevalue

                    if(self.map1.getValue(i, j+1) != '%'):
                        thenorth = self.map1.getValue(i, j+1)
                    else: thenorth = thevalue

                    if(self.map1.getValue(i, j-1) != '%'):
                        thesouth = self.map1.getValue(i, j-1)
                    else: thesouth = thevalue

                    #get the payoff for four direction
                    up = 0.8 * thenorth + 0.1 * theeast + 0.1 * thewest
                    left = 0.8 * theeast + 0.1 * thenorth + 0.1 * thesouth
                    right = 0.8 * thewest + 0.1 * thenorth + 0.1 * thesouth
                    down = 0.8 * thesouth + 0.1 * theeast + 0.1 * thewest

                    #set the best payoff as the utility of this position
                    thevalue = discount * max(up,left,right,down)-reward
                    self.map2.setValue(i,j, thevalue)
        #print "map1 after update"
        #self.map1.prettyDisplay()
        #print "map2 after update"
        #self.map2.prettyDisplay()




    def getAction(self, state):

        #compare previous number of food and current number of food
        global numoffood
        if numoffood != len(api.food(state)):
           numoffood = len(api.food(state))
          # print "RRRRRRemakemap,just eat a food!"
          #Remake maps
           self.makeMap(state)
           self.addWallsFoodToMap(state)
           #self.updateMap(state)
           
        #
        #the new utilitis saved in the map2 in the FUNCTION self.updateMap(state)
        self.updateMap(state)
        #calculate the utility for map1, until the utilitis does not change anymore
        while (self.map1 != self.map2):
            #print "while map1"
            #self.map1.prettyDisplay()
            #print "while map2"
            #self.map2.prettyDisplay()
        # so updated utilitis in map1
            self.map1 = self.map2
            self.updateMap(state)
            #print "while new map2"
            #self.map2.prettyDisplay()
            #print "while map11"
            #self.map1.prettyDisplay()


        # get current pacman state and value
        mystate = api.whereAmI(state)
        #get my value
        myvalue = self.map1.getValue(mystate[0], mystate[1])
        #Get the actions we can try
        legal = api.legalActions(state)
        #get all state of ghosts
        ghosts = api.ghosts(state)
        #check if any ghost in my danger area(within 3 step to me)
        ghostlist = api.distanceLimited(ghosts, state, danger)

        # if there are ghosts in my danger area       
        if ghostlist:
            #print "Ghost ARound!!",ghostlist
            #Check directions of these ghost in the danger area
            #Remove all direction of these ghost in legal-move-directions of pacman

            for i in range(len(ghostlist)):
                    if ghostlist[i][1] > mystate[1] :
                       if Directions.NORTH in legal:
                               legal.remove(Directions.NORTH)
                               #print "hear the ghost n"
                    if ghostlist[i][1] < mystate[1] :
                            if Directions.SOUTH in legal:
                               legal.remove(Directions.SOUTH)
                              #print "hear the ghost s"
                    if ghostlist[i][0] < mystate[0] :
                            if Directions.WEST in legal:
                                legal.remove(Directions.WEST)
                                #print "hear the ghost w"
                    if ghostlist[i][0] > mystate[0]:
                            if Directions.EAST in legal:
                                legal.remove(Directions.EAST)
                                #print "hear the ghost e"

        #check if  pacman only have one direction can go
        # If it is, just go this direction.
        if len(legal) == 2 and Directions.STOP in legal:
            legal.remove(Directions.STOP)
            goto = random.choice(legal)

        # If pacman have more than one direction can go
        # let pacman make correct choice where pacman should go
        else:
            # if the direction of east is a wall and pacman go east,
            # but pacman will not move.
            # therefor the new utilitiy is same with the utilitiy of current(this) position
            if (self.map1.getValue(mystate[0]+1, mystate[1]) != '%'):
                myeast = self.map1.getValue(mystate[0]+1, mystate[1])
            else: myeast = myvalue

            if (self.map1.getValue(mystate[0]-1, mystate[1]) != '%'):
                mywest = self.map1.getValue(mystate[0]-1, mystate[1])
            else: mywest = myvalue

            if(self.map1.getValue(mystate[0], mystate[1]+1) != '%'):
                mynorth = self.map1.getValue(mystate[0], mystate[1]+1)
            else: mynorth = myvalue

            if(self.map1.getValue(mystate[0], mystate[1]-1) != '%'):
                mysouth = self.map1.getValue(mystate[0], mystate[1]-1)
            else: mysouth = myvalue
            #print"Second legal",legal
            #print "myeast",myeast,"mywest",mywest,"mynorth",mynorth,"mysouth",mysouth

            #make a list to save all the payoff of legal directions
            mylist = []
            if Directions.EAST in legal:
                mylist.append(myeast)
            if Directions.SOUTH in legal:
                mylist.append(mysouth)
            if Directions.NORTH in legal:
                mylist.append(mynorth)
            if Directions.WEST in legal:
                mylist.append(mywest)
            #print "mylist",mylist

            #if no legal directions, ask pacman stay the same position
            if 	len(mylist) == 0:
                goto = Directions.STOP
            #find the max payoff is from which legal directions
            #ask pacman going the direction with biggest payoff
            elif max(mylist) == myeast and Directions.EAST in legal:
                goto = Directions.EAST
                #print"max E"
            elif max(mylist) == mysouth and Directions.SOUTH in legal:
                goto = Directions.SOUTH
                #print"max S"
            elif max(mylist) == mywest and Directions.WEST in legal:
                goto = Directions.WEST
                #print"max W"
            elif max(mylist) == mynorth and Directions.NORTH in legal:
                goto = Directions.NORTH
                #print"max N"
            # if pacman cannot make decision, just make a random choice
            else: goto = random.choice(api.legalActions(state))

        #print "GGGGGoto",goto
        return api.makeMove(goto, api.legalActions(state))
