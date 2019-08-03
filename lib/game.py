#! /usr/bin/python3

"""
Created by John Sell
07 28 2019

Main Game class to control 
the Game!
"""

import random
from map import Map
from constants import Constants, Clamp
from player import Player
from speechEngine import SpeechEngine, Question

SE = SpeechEngine()

class Game:
    def __init__(self, mapSize):
        self._isPaused = False
        self._isQuit   = False

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


        


    def _DoPly(self):
        command = SE.AskQuestion(Question("", []), True)

        if self._playerTurn and self._playerMovementDirection is self._C.NoMovement:
            self._UpdateMap()

        # Player Movement
        if self._playerTurn:
            self._HandlePlayerMove(command)
        else:
            # See if the player should become engaged with an enemy 
            if not self._attack:
                self._CheckForEngagement()
            else:
                if self._playerEngaged:
                    self._HandleEngagement()
                else:
                    self._HandleSurpriseEngagement()
                if self._playerEngaged:
                    self.HandleEnemyAttack()
        
        


    # Spawn Enemies and Such
    def _UpdateMap(self):
        #Create 5x5 area around player in which to spawn enemies and such
        xLow  = self._playerPosition["x"] - 2
        xHigh = self._playerPosition["x"] + 2 
        yLow  = self._playerPosition["y"] - 2
        yHigh = self._playerPosition["y"] + 2

        # Clamp those values to the map size
        xLow  = Clamp(xLow,  0, self._map._size)
        xHigh = Clamp(xHigh, 0, self._map._size)
        yLow  = Clamp(yLow,  0, self._map._size)
        yHigh = Clamp(yHigh, 0, self._map._size)

        # Clear Enemy Map
        for x in range(0, self._map._size):
            for y in range(0, self._map._size):
                if not (self._playerPosition["x"] == x and self._playerPosition["y"] == y):
                    self._map._enemyMap[x][y] = 0

        # Spawn new Enemies
        for x in range(xLow, xHigh):
            for y in range(yLow, yHigh):
                if not (self._playerPosition["x"] == x and self._playerPosition["y"] == y):
                    randomChance = 20 - self._turnsSinceEngagement
                    if randomChance == random.randrange(0, randomChance, 1):
                        # TODO: Search for valid enemies and add them to the map
                        pass

        # If the player is on an enemy, reset turnsSinceEngagement
        if self._map._enemyMap[self._playerPosition["x"]][self._playerPosition["y"]] != 0:
            self._turnsSinceEngagement = 0
        else:
            self._turnsSinceEngagement = self._turnsSinceEngagement + 1

        # Ensure max chance of engagement is 50%
        self._turnsSinceEngagement = Clamp(self._turnsSinceEngagement, 0, 10)
        
        # TODO: Figure out why this is here
        self._enemyMove = self._enemyMove - 1

        
        

    # Given a command, move the player
    def _HandlePlayerMove(self, command):
        pass

    # Determine if player should be engaged with an enemy
    def _CheckForEngagement(self):
        pass

    # Handle player -> enemy combat
    def _HandleEngagement(self):
        pass

    # Handle (sneaky) player -> enemy combat
    def _HandleSurpriseEngagement(self):
        pass

    # Enemies must fight back!
    def HandleEnemyAttack(self):
        pass

    
        

if __name__ == "__main__":
    g = Game(10)
