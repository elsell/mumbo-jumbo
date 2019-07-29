#! /usr/bin/python3

"""
Created by John Sell
07 28 2019

Who shall play this game? The player!
"""

from constants import Constants


class Player:
    def __init__(self):
        constants = Constants()

        self._stats = constants.PlayerDefaults
        self._equipment = {
            "body" : 0,
            "legs" : 0,
            "arms" : 0,
            "hands": 0,
            "feet" : 0
        }

        self._activeEnemy = None