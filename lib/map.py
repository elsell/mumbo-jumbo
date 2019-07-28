#! /usr/bin/python3

"""
map Object Class

Created by John Sell 
07 25 2019

"""

from constants import Constants
import random
import json

class Map:
    def __init__(self, size):  
        if(size < 1):
            raise ValueError(
                "Map size must be greater than 0 (Provided " + str(size) + ")"
            )

        # Get us some constants!
        self._constants = Constants()

        # Create and initialize member variables
        self._size = size

        self._heightMap = [ [ 1 for y in range( size ) ] for x in range( size ) ]

        self._riverMap  = [ [ 0 for y in range( size ) ] for x in range( size ) ]

        self._locMap    = [ [ 0 for y in range( size ) ] for x in range( size ) ]

        self._treeMap   = [ [ 0 for y in range( size ) ] for x in range( size ) ]

        # Now we shall generate our map
        self._GenerateMap()

    # Eventually will procedurally generate a map. For now, it does RANDOMNESS!
    def _GenerateMap(self):
        # Fill map with random data
        for x in range(0, self._size):
            for y in range(0, self._size):
                self._heightMap[x][y] = random.randint(0, len(self._constants.HeightDescriptions) - 1)
                self._riverMap[x][y] = random.randint(0, len(self._constants.RiverDescriptions) - 1)
                self._locMap[x][y] = random.randint(0, len(self._constants.LocationDescriptions) - 1)
                self._treeMap[x][y] = random.randint(0, len(self._constants.TreeDescriptions) - 1)
                

    ## DESCRIPTION GETTERS ##
    def DescribeHeight(self, x, y):
        return self._constants.HeightDescriptions[self._heightMap[x][y]]
        
    def DescribeRiver(self, x, y):
        return self._constants.RiverDescriptions[self._riverMap[x][y]]

    def DescribeLocation(self, x, y):
        return self._constants.LocationDescriptions[self._locMap[x][y]]

    def DescribeTrees(self, x, y):
        return self._constants.TreeDescriptions[self._treeMap[x][y]]

    # Saves serialized representation of the map for visualization purposes
    def SaveToFile(self, filename = "map.data"):
        # Build Object to Convert to JSON
        obj = {
            "heightMap": self._heightMap,
            "riverMap": self._riverMap,
            "locationMap": self._locMap,
            "treeMap": self._treeMap
        }
        with open(filename, 'w') as file:
            file.write(json.dumps(obj))



if __name__ == "__main__":
    # Perform Self-Test
    
    # Create Map
    map =  Map(10)
    
    # Print Height Descriptions
    print("________HEIGHT DESCRIPTIONS_________")
    for x in range(0, map._size):
        for y in range(0, map._size):
            print("(" + str(x) + "," + str(y) + "): " + map.DescribeHeight(x,y))
    
    # Print River Descriptions
    print("________RIVER DESCRIPTIONS_________")
    for x in range(0, map._size):
        for y in range(0, map._size):
            print("(" + str(x) + "," + str(y) + "): " + map.DescribeRiver(x,y))

    # Print Location Descriptions
    print("________LOCATION DESCRIPTIONS_________")
    for x in range(0, map._size):
        for y in range(0, map._size):
            print("(" + str(x) + "," + str(y) + "): " + map.DescribeLocation(x,y))

    # Print Tree Descriptions
    print("________TREE DESCRIPTIONS_________")
    for x in range(0, map._size):
        for y in range(0, map._size):
            print("(" + str(x) + "," + str(y) + "): " + map.DescribeTrees(x,y))