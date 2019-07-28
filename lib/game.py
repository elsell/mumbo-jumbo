#! /usr/bin/python3

"""
Created by John Sell
07 28 2019

Main Game class to control 
the Game!
"""

from map import Map
from constants import Constants

class Game:
    def __init__(self, mapSize):
        self._map = Map(mapSize)
        self._C = Constants()

        self._playerTurn = False
        self._playerPosition = {
            "x": mapSize * .5,
            "y": mapSize * .5
        }

        self._playerInCombat = False
        self._playerIsMoving = False
        


