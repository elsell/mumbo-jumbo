#! /usr/bin/python3

""" 
Created by John Sell 
07 28 2019

* And then there were enemies *
"""

class Enemy:
    def __init__(self, name, hp, attack, hear, speed, minHeight, maxHeight,
                    river, tree, minTime, maxTime):
        self._name      = name
        self._hp        = hp
        self._attack    = attack
        self._hear      = hear
        self._speed     = speed
        self._minHeight = minHeight
        self._maxHeight = maxHeight
        # If needs to be by a river to spawn (1 = Yes)
        self._river     = river
        # Same as River
        self._tree      = tree
        self._minTime   = minTime
        self._maxTime   = maxTime

    # Determines if the given parameters are within its spawnable range
    def CanSpawnAt(self, height, river, tree, time):
        # Height Constraint
        canSpawnHeight = (height <= self.MaxHeight and height >= self.MinHeight)
        
        # River Constraint
        canSpawnRiver = True
        if self.River != 0:
            if river == 0:
                canSpawnRiver = False

        # Tree Constraint
        canSpawnTree = True
        if self.Tree != 0:
            if tree == 0:
                canSpawnTree = False  

        # Time Constraint
        canSpawnTime = (time <= self.MaxTime and time >= self.MinTime)

        return (
            canSpawnHeight and canSpawnRiver and canSpawnTree and canSpawnTime 
        )   

    

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

# Global list of all enemies in the game
# Ex:
# Enemy(name, hp, attack, hear, speed, minHeight, maxHeight, 
#           river, tree, minTime, maxTime)
ENEMIES = [
    Enemy("wolf",20,20,10,2,1,10,0,0,0,24),
]