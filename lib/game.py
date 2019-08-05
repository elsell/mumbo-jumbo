#! /usr/bin/python3

"""
Created by John Sell
07 28 2019

Main Game class to control 
the Game!
"""

import random
from map import Map
from constants import Constants, Clamp, VERBOSE
from player import Player
import enemy
from speechEngine import SpeechEngine, Question
from sys import argv

SE = None

class Game:
    def __init__(self, mapSize):
        self._isPaused = False
        self._isQuit   = False

        # 1 = 1 Hour, Every turn is an hour
        self._timeOfDay = 0

        self._map = Map(mapSize)
        self._C = Constants()

        self._description = ""

        self._playerTurn = False
        self._playerPosition = {
            "x": int(mapSize * .5),
            "y": int(mapSize * .5)
        }

        self._attack = False
        self._enemyMove = 0

        self._turnsSinceEngagement = 0

        self._player = Player()
        self._playerAttackTarget = None
        self._playerEngaged = False
        self._playerInCombat = False
        self._playerMovementDirection = self._C.NoMovement

    def Start(self):
        while not self._isQuit:
            # Handle Game Pause
            while self._isPaused:
                # TODO: Read external pause input to 'unpause' game
                self._isPaused = False
            
            # Perform 1 player and 1 enemy ply
            self._DoPly()

            # Update the time of day (1 hour / turn)
            self._timeOfDay = self._timeOfDay + 1


    def _ParseCommand(self, command):
        if VERBOSE:
            print("Parsing Command: " + command)
        if command == "go north":
            if self._playerPosition["y"] < self._map._size - 1 and \
             not self._playerEngaged:
                self._playerMovementDirection = self._C.North
            else:
                self._description = "you cannot go north"
                self._playerMovementDirection = self._C.NoMovement
        elif command == "go west":
            if self._playerPosition["x"] > 0 and not self._playerEngaged:
                self._playerMovementDirection = self._C.West
            else:                
                self._description = "you cannot go west"
                self._playerMovementDirection = self._C.NoMovement
        elif command == "go east":
            if self._playerPosition["x"] < self._map._size - 1 and \
             not self._playerEngaged:
                self._playerMovementDirection = self._C.East
            else:                
                self._description = "you cannot go east"
                self._playerMovementDirection = self._C.NoMovement
        elif command == "go south":
            if self._playerPosition["y"] > 0 and not self._playerEngaged:
                self._playerMovementDirection = self._C.South
            else:                
                self._description = "you cannot go south"   
                self._playerMovementDirection = self._C.NoMovement  
        elif command == "attack head":
            self._attack = True
            self._playerAttackTarget = self._C.Head
        elif command == "attack body":
            self._attack = True
            self._playerAttackTarget = self._C.Body
        elif command == "attack arms":
            self._attack = True
            self._playerAttackTarget = self._C.Arms
        elif command == "attack legs":
            self._attack = True
            self._playerAttackTarget = self._C.Legs             

    def _DoPly(self):
        if VERBOSE:
            print("Player Turn: " + str(self._playerTurn))

        if self._playerTurn:
            self._playerTurn = False
            self._UpdateMap()

            if VERBOSE:
                print("\n\n-= Accepting Command =-")
            command = SE.AskQuestion(Question("", [
                ["go", "attack"],
                ["north", "south", "east", "west",
                 "head",  "body",  "arms", "legs"]
            ]), True)

            if VERBOSE:
                print("Player Command: " + command)  

            self._ParseCommand(command)
        else:
            if self._playerMovementDirection is not self._C.NoMovement:
                self._CheckForEngagement()
                self._HandlePlayerMove()   

            if self._attack:

                if self._playerEngaged:
                    self._HandleEngagement()
                else:
                    self._HandleSurpriseEngagement()
            
            if self._playerEngaged:
                self.HandleEnemyAttack()

            SE.SpeakText(self._description)
            self._description = ""

            self._playerTurn = True
       
        


    # Spawn Enemies and Such
    def _UpdateMap(self):
        if VERBOSE:
            print("Updating Map...")
            self._map.SaveToFile("game_debug_map.data")
            print("TSE: " + str(self._turnsSinceEngagement))
        #Create 5x5 area around player in which to spawn enemies and such
        xLow  = self._playerPosition["x"] - 2
        xHigh = self._playerPosition["x"] + 2 
        yLow  = self._playerPosition["y"] - 2
        yHigh = self._playerPosition["y"] + 2

        # Clamp those values to the map size
        xLow  = int(Clamp(xLow,  0, self._map._size))
        xHigh = int(Clamp(xHigh, 0, self._map._size))
        yLow  = int(Clamp(yLow,  0, self._map._size))
        yHigh = int(Clamp(yHigh, 0, self._map._size))

        px = int(self._playerPosition["x"])
        py = int(self._playerPosition["y"])

        # Clear Enemy Map
        for x in range(0, self._map._size):
            for y in range(0, self._map._size):
                if not (px == x and py == y):
                    self._map._enemyMap[x][y] = None

        # Spawn new Enemies
        for x in range(xLow, xHigh):
            for y in range(yLow, yHigh):
                if not (px == x and py == y):
                    chance = ((20 - self._turnsSinceEngagement)/20 )*100
                    randomChoice = random.randrange(0, 100)
                    if randomChoice > chance:
                        validEnemies = []
                        # Find Valid Enemies
                        for en in enemy.ENEMIES:
                            if (
                                en.CanSpawnAt(
                                    self._map._heightMap[x][y],
                                     self._map._riverMap[x][y],
                                     self._map._treeMap[x][y],
                                     self._timeOfDay
                                )):
                                validEnemies.append(en)
                        # Randomly choose an enemy
                        if len(validEnemies) > 0:
                            randEnemy = 0
                            if len(validEnemies) > 1:
                                randEnemy = random.randrange(0, len(validEnemies) - 1)
                            self._map._enemyMap[x][y] = validEnemies[randEnemy]
                            if VERBOSE:
                                print("Spawning a " + validEnemies[randEnemy].Name)
                        


        # If the player is on an enemy, reset turnsSinceEngagement
        if self._map._enemyMap[px][py] != None:
            self._turnsSinceEngagement = 0
        else:
            self._turnsSinceEngagement = self._turnsSinceEngagement + 1

        # Ensure max chance of engagement is 50%
        self._turnsSinceEngagement = Clamp(self._turnsSinceEngagement, 0, 10)
   
        
    def _HandlePlayerMove(self):
        if VERBOSE:
            print("Handling Player Move...")

        if not self._playerEngaged:
            px = int(self._playerPosition["x"])
            py = int(self._playerPosition["y"])
            if self._playerMovementDirection is not self._C.NoMovement:
                if self._playerMovementDirection is self._C.North:
                    self._playerPosition["y"] = py + 1
                elif self._playerMovementDirection is self._C.West:
                    self._playerPosition["x"] = px - 1
                elif self._playerMovementDirection is self._C.South:
                    self._playerPosition["y"] = py - 1        
                elif self._playerMovementDirection is self._C.East:
                    self._playerPosition["x"] = px + 1
                self._description = "you come to "
            else:
                self._description = "you are in "

            # Height Description
            self._description = self._description + \
                self._map.DescribeHeight(px, py) + ". "
            
            # Tree Description
            if self._map._treeMap[px][py] is not 0:
                self._description = self._description + "you are surrounded by "\
                    + self._map.DescribeTrees(px,py) + ". "
            else:
                # North
                if self._map._treeMap[px][py + 1] is not 0:
                    self._description = self._description + " to your north are "\
                        + self._map.DescribeTrees(px,py + 1) + ". "
                # West
                elif self._map._treeMap[px - 1][py] is not 0:
                    self._description = self._description + " to your west are "\
                        + self._map.DescribeTrees(px - 1,py) + ". "
                # South 
                elif self._map._treeMap[px][py - 1] is not 0:
                    self._description = self._description + " to your south are "\
                        + self._map.DescribeTrees(px,py - 1) + ". "
                # East
                if self._map._treeMap[px + 1][py] is not 0:
                    self._description = self._description + " to your east are "\
                        + self._map.DescribeTrees(px + 1,py) + ". "  

            # River Description
            if self._map._riverMap[px][py] is not 0:
                self._description = self._description + " a stream, flowing "\
                    + self._map.DescribeRiver(px,py) + " burbles nearby. "
            else:
                # North
                if self._map._riverMap[px][py + 1] is not 0:
                    self._description = self._description + " a stream, flowing "\
                        + self._map.DescribeRiver(px,py + 1) + " burbles to your north. "
                # West
                elif self._map._riverMap[px - 1][py] is not 0:
                    self._description = self._description + " a stream, flowing "\
                        + self._map.DescribeRiver(px - 1,py) + "burbles to your west. "
                # South 
                elif self._map._riverMap[px][py - 1] is not 0:
                    self._description = self._description + " a stream, flowing "\
                        + self._map.DescribeRiver(px,py - 1) + "burbles to your south. "
                # East
                if self._map._riverMap[px + 1][py] is not 0:
                    self._description = self._description + " a stream, flowing "\
                        + self._map.DescribeRiver(px + 1,py) + "burbles to your east. "   

            # Location Description                     
            if self._map._locMap[px][py] is not 0:
                self._description = self._description + " there is "\
                    + self._map.DescribeLocation(px,py) + " here. "
            else:
                # North
                if self._map._locMap[px][py + 1] is not 0:
                    self._description = self._description + " there is "\
                        + self._map.DescribeLocation(px,py + 1) + " to your north. "
                # West
                elif self._map._locMap[px - 1][py] is not 0:
                    self._description = self._description + " there is "\
                        + self._map.DescribeLocation(px - 1,py) + " to your west. "
                # South 
                elif self._map._locMap[px][py - 1] is not 0:
                    self._description = self._description + " there is "\
                        + self._map.DescribeLocation(px,py - 1) + " to your south. "
                # East
                if self._map._locMap[px + 1][py] is not 0:
                    self._description = self._description + " there is "\
                        + self._map.DescribeLocation(px + 1,py) + " to your east. "   


    # Determine if player should be engaged with an enemy
    def _CheckForEngagement(self):
        px = int(self._playerPosition["x"])
        py = int(self._playerPosition["y"])

        if VERBOSE:
            print("Checking For Engagement...")
        
        if not self._playerEngaged:
            if self._map._enemyMap[px][py] != None:
                self._player._activeEnemy = self._map._enemyMap[px][py]

                noise = self._player._stats["noise"] * (
                    .5 * self._player._stats["sneak"]
                )
                hear = self._player._activeEnemy.Hear

                r = random.randrange(0, 100)
                if noise <= .5 * hear:
                    if r <= 25:
                        self._playerEngaged = True
                elif noise > .5 * hear and noise < hear:
                    if r < 50:
                        self._playerEngaged = True
                elif noise >= hear:
                    self._playerEngaged = True

                if self._playerEngaged:
                    self._description = "The " + self._player._activeEnemy.Name\
                        + " blocks your path"
                    

    # Handle player -> enemy combat
    def _HandleEngagement(self):
        if VERBOSE:
            print("Handling Engagement...")

    # Handle (sneaky) player -> enemy combat
    def _HandleSurpriseEngagement(self):
        # Note: this should set engaged to true
        # Also, this should check if enemy is actually there
        if VERBOSE:
            print("Handling Surprise Engagement...")

    # Enemies must fight back!
    def HandleEnemyAttack(self):
        if VERBOSE:
            print("Handling Enemy Attack...")

    
        

if __name__ == "__main__":
    useKeyboard = False
    if len(argv) > 1:
        if argv[1] == "--keyboard" or argv[1] == "-K":
            useKeyboard = True


    SE = SpeechEngine(useKeyboard)
    g = Game(25)
    g.Start()

