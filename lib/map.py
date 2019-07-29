#! /usr/bin/python3

"""
map Object Class

Created by John Sell 
07 25 2019

"""

from constants import Constants
import random
import json
import copy
from sys import getsizeof

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

    # Eventually will procedurally generate a map. For now, it...does!
    def _GenerateMap(self):
        self._GenerateHeightMap()
        self._GenerateTreeMap()
        self._GenerateRiverMap()

    # Recursively traces a river down a slope starting at the cell
    # tempArr[x][y]
    def _TraceRiverPath(self, x, y, tempArr, length = 0):
        curCellHeight = tempArr[x][y]

        # We shall spawn a river!
        adjacentCells = [
            [x    , y + 1],
            [x    , y - 1],
            [x - 1, y    ],
            [x + 1, y    ],
        ]

        lowestAdjacentCellHeight = curCellHeight
        lowestAdjacentCell = None

        # Find the loweset adjacent cell
        for cellCoords in adjacentCells:
            try:
                if cellCoords[0] < 0 or cellCoords[1] < 0:
                    continue
                adjacentCellHeight = tempArr[cellCoords[0]][cellCoords[1]]
            except:
                # We've gone outside of the map...just skip this cell
                continue
            if adjacentCellHeight < lowestAdjacentCellHeight:
                lowestAdjacentCellHeight = adjacentCellHeight
                lowestAdjacentCell = cellCoords
        
        # If there are no adjacent cells that are lower, we give up!
        # No sense in building a river where this is no downward slope...it'd be a lake!
        if lowestAdjacentCell is None:
            self._riverMap[x][y] = 12 # A puddle
            return None

        # Now we need to figure out the direction of flow...yippee
        direction = None

        xChange = x - lowestAdjacentCell[0]
        yChange = y - lowestAdjacentCell[1]

        if xChange > 0:
            # West to East
            direction = 5
        elif xChange < 0:
            # East to West
            direction = 10

        if yChange > 0:
            # North to South
            direction = 1
        elif yChange < 0:
            # South to North
            direction = 6

        print("We have a flow: " + self._constants.RiverDescriptions[direction])
        print("x: " +str(lowestAdjacentCell[0]) + " y: " + str(lowestAdjacentCell[1]) + " d: " + str(direction))
      
        # Update the river map
        self._riverMap[x][y] = direction

        # Now trace the lowestCell down
        return self._TraceRiverPath(lowestAdjacentCell[0], lowestAdjacentCell[1], tempArr, length + 1)
                

    def _GenerateRiverMap(self):
        # Load elevation map into a temporary array so we can mess with it ;)
        tempArr = copy.deepcopy(self._heightMap)

        # Iterate through the entire map looking for high-points
        for x in range(0, self._size):
            for y in range(0, self._size):
                curCellHeight = tempArr[x][y]

                if curCellHeight > self._constants.MinRiverSpawnHeight:
                    if random.random() > self._constants.RiverSpawnChance:
                        self._TraceRiverPath(x, y, tempArr)


                        

                        

    def _GenerateTreeMap(self):
        sSize = self._constants.SpreadSize
        heightBound = float(len(self._constants.TreeDescriptions) - 1)
        maxHeight = heightBound

        for time in range(0,3):
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
                    curVal = self._treeMap[x][y]

                    self._treeMap[x][y] = curVal + tempArr[x][y]
                    if(self._treeMap[x][y] > heightBound):
                        self._treeMap[x][y] = heightBound
                    if(self._treeMap[x][y] < 0):
                        self._treeMap[x][y] = 0
                    if(self._heightMap[x][y] > 8):
                        self._treeMap[x][y] = 0
                    if(self._heightMap[x][y] < 1):
                        self._treeMap[x][y] = 0
            
            # Modify Parameters for the Next Pass
            maxHeight = maxHeight * .5
            sSize     = sSize     * .5

    def _GenerateHeightMap(self):
        sSize = self._constants.SpreadSize
        heightBound = float(len(self._constants.HeightDescriptions) - 1)
        maxHeight = heightBound

        for time in range(0,3):
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
    m =  Map(30)
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
    