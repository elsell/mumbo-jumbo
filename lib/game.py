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

SE = SpeechEngine()

class Game:
    def __init__(self, mapSize):
        self._isPaused = False
        self._isQuit   = False

        # 1 = 1 Hour, Every turn is an hour
        self._timeOfDay = 0

        self._map = Map(mapSize)
        self._C = Constants()

        self._playerTurn = False
        self._playerPosition = {
            "x": mapSize * .5,
            "y": mapSize * .5
        }

        self._attack = False
        self._enemyMove = 0

        self._turnsSinceEngagement = 0

        self._player = Player()
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


        


    def _DoPly(self):

        command = ""
        if self._playerTurn:
            self._UpdateMap()

            if VERBOSE:
                print("\n\n-= Accepting Command =-")
            command = SE.AskQuestion(Question("", [
                ["go"],
                ["north", "south", "east", "west"]
            ]), True)

            if VERBOSE:
                print("Player Command: " + command)  
        else:
            if self._playerMovementDirection is not self._C.NoMovement:
                self._CheckForEngagement()
                self._HandlePlayerMove(command)   

            if self._attack:

                if self._playerEngaged:
                    self._HandleEngagement()
                else:
                    self._HandleSurpriseEngagement()
            
            if self._playerEngaged:
                self.HandleEnemyAttack()

            # TODO: Read Description
            self._playerTurn = True
       
        


    # Spawn Enemies and Such
    def _UpdateMap(self):
        if VERBOSE:
            print("Updating Map...")
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

        # Clear Enemy Map
        for x in range(0, self._map._size):
            for y in range(0, self._map._size):
                if not (self._playerPosition["x"] == x and self._playerPosition["y"] == y):
                    self._map._enemyMap[x][y] = 0

        # Spawn new Enemies
        for x in range(xLow, xHigh):
            for y in range(yLow, yHigh):
                if not (self._playerPosition["x"] == x and self._playerPosition["y"] == y):
                    chance = ((20 - self._turnsSinceEngagement)/20 )*100
                    randomChoice = random.randrange(0, 100)
                    if randomChoice <= chance:
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
                                if VERBOSE:
                                    print("Spawning a " + en.Name)
                                validEnemies.append(en)
                        # Randomly choose an enemy
                        if len(validEnemies) > 0:
                            randEnemy = 0
                            if len(validEnemies) > 1:
                                randEnemy = random.randrange(0, len(validEnemies) - 1)
                            self._map._enemyMap[x][y] = validEnemies[randEnemy]
                        


        # If the player is on an enemy, reset turnsSinceEngagement
        if self._map._enemyMap[int(self._playerPosition["x"])][int(self._playerPosition["y"])] != 0:
            self._turnsSinceEngagement = 0
        else:
            self._turnsSinceEngagement = self._turnsSinceEngagement + 1

        # Ensure max chance of engagement is 50%
        self._turnsSinceEngagement = Clamp(self._turnsSinceEngagement, 0, 10)


        
        

    # Given a command, move the player
    def _HandlePlayerMove(self, command):
        if VERBOSE:
            print("Handling Player Move...")
        

    # Determine if player should be engaged with an enemy
    def _CheckForEngagement(self):
        if VERBOSE:
            print("Checking For Engagement...")

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
    g = Game(100)
    g._map.SaveToFile("curGame.data")
    g.Start()

