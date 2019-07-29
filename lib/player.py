#! /usr/bin/python3

"""
Created by John Sell
07 28 2019

Who shall play this game? The player!
"""

from constants import Constants

class Equipment:
    def __init(self, hp, attack, noise, speed, sneak):
        self._hpBuff = hp
        self._attackBuff = attack
        self._noiseBuff = noise
        self._speedBuff = speed
        self._sneakBuff = sneak

    @property
    def BuffAmounts(self):
        return {
            "hp"    : self._hpBuff,
            "attack": self._attackBuff,
            "noise" : self._noiseBuff,
            "speed" : self._speedBuff,
            "sneak" : self._sneakBuff  
        }

class Player:
    def __init__(self):
        constants = Constants()

        self._stats = constants.PlayerDefaults
        self._equipment = {
            "body" : [],
            "legs" : [],
            "arms" : [],
            "hands": [],
            "feet" : []
        }

        self._activeEnemy = None