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

        self._heightMap = [ [ 0 for y in range( size ) ] for x in range( size ) ]

        self._riverMap  = [ [ 0 for y in range( size ) ] for x in range( size ) ]

        self._locMap    = [ [ 0 for y in range( size ) ] for x in range( size ) ]

        self._treeMap   = [ [ 0 for y in range( size ) ] for x in range( size ) ]

        # Now we shall generate our map
        self._GenerateMap()

    # Eventually will procedurally generate a map. For now, it...does?
    def _GenerateMap(self):
        sSize = self._constants.SpreadSize
        heightBound = float(len(self._constants.HeightDescriptions) - 1)
        maxHeight = heightBound
        minHeight = -heightBound

        for time in range(0,4):
            # Ensure sSize is indeed an integer
            sSize = int(sSize)

            # Fill temp array with random data
            tempArr = [ [ 0 for y in range( self._size + sSize + 1) ] for x in range( self._size + sSize + 1) ]
            
            for x in range(0, self._size + sSize + 1):
                for y in range(0, self._size + 1):
                    tempArr[x][y] = random.uniform(-heightBound + 4.5, heightBound - 3) 

            # Horizontal Interpolation
            for x in range(0, self._size):
                for y in range(0, self._size):
                    yCoord = y - y % sSize
                    multiplier = float(y % sSize) / sSize
                    val1 = float(tempArr[x][yCoord + sSize])
                    val2 = float(tempArr[x][yCoord])
                    tempArr[x][y] = val1 * multiplier + val2 * (1 - multiplier)

            # Vertical Interpolation
            for x in range(0, self._size):
                for y in range(0, self._size):
                    xCoord = x - x % sSize
                    multiplier = float(x % sSize) / sSize
                    val1 = float(tempArr[xCoord + sSize][y])
                    val2 = float(tempArr[xCoord][y])
                    tempArr[x][y] = val1 * multiplier + val2 * (1 - multiplier)     
  

            # Add to Map
            for x in range(0, self._size):
                for y in range(0, self._size):
                    curVal = self._heightMap[x][y]

                    self._heightMap[x][y] = curVal + tempArr[x][y]
                    if(self._heightMap[x][y] > heightBound):
                        self._heightMap[x][y] = heightBound
                    if(self._heightMap[x][y] < 0):
                        self._heightMap[x][y] = 0
            
            # Modify Parameters for the Next Pass
            maxHeight = maxHeight * .5
            minHeight = minHeight * .5
            sSize     = sSize     * .5
                       

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
    m =  Map(50)
    m.SaveToFile()
    """

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
    """
    