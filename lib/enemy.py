#! /usr/bin/python3

""" 
Created by John Sell 
07 28 2019

* And then there were enemies *
"""

class Enemy:
    def __init__(self, name, hp, attack, hear, speed, minHeight, maxHeight, river, tree, minTime, maxTime):
        self._name      = name
        self._hp        = hp
        self._attack    = attack
        self._hear      = hear
        self._speed     = speed
        self._minHeight = minHeight
        self._maxHeight = maxHeight
        self._river     = river
        self._tree      = tree
        self._minTime   = minTime
        self._maxTime   = maxTime

    

    # Property Getters
    @property
    def Name(self):
        return self._name
    
    @property
    def HP(self):
        return self._hp
    
    @property
    def Attack(self):
        return self._attack

    @property
    def Hear(self):
        return self._hear
    
    @property
    def Speed(self):
        return self._speed

    @property
    def MinHeight(self):
        return self._minHeight

    @property
    def MaxHeight(self):
        return self._maxHeight
    
    @property
    def River(self):
        return self._river

    @property
    def Tree(self):
        return self._tree

    @property
    def MinTime(self):
        return self._minTime

    @property
    def MaxTime(self):
        return self._maxTime

