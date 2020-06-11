#! /usr/bin/python3

"""
map Object Class

Created by John Sell 
07 25 2019

"""

from constants import Constants, VERBOSE
import random
import json
import time
import copy
from sys import getsizeof, argv

class Map:
    def __init__(self, size, seed = None):  
        if(size < 1):
            raise ValueError(
                "Map size must be greater than 0 (Provided " + str(size) + ")"
            )

        if seed != None:
            random.seed(seed)

        # Get us some constants!
        self._constants = Constants()

        # Create and initialize member variables
        self._size = size

        if(VERBOSE):
            print("Initializing Blank Map (this may take a while)...")

        self._heightMap = [ [ 0 for y in range( size ) ] for x in range( size ) ]

        self._riverMap  = [ [ 0 for y in range( size ) ] for x in range( size ) ]

        self._locMap    = [ [ 0 for y in range( size ) ] for x in range( size ) ]

        self._treeMap   = [ [ 0 for y in range( size ) ] for x in range( size ) ]

        self._enemyMap  = [ [ None for y in range( size ) ] for x in range( size ) ]

        if(VERBOSE):
            print("Done.")

        # Now we shall generate our map
        self._GenerateMap()

    # Eventually will procedurally generate a map. For now, it...does!
    def _GenerateMap(self):
        self._GenerateHeightMap()
        self._GenerateTreeMap()
        self._GenerateRiverMap()

    def _GetFlowDirection(self, cell1, cell2):
        """
        Returns a pair of cardinal directions denoting the flow
        direction from cell1 -> cell2.
        """
        xChange = cell1[0] - cell2[0]
        yChange = cell1[1] - cell2[1]

        # If the cells are the same, it's a lake and is not flowing
        if xChange == 0 and yChange == 0:
            return 9

        if xChange > 0:
            # East to West
            return 4
        elif xChange < 0:
            # West to East
            return 2
        if yChange > 0:
            # North to South
            return 1
        elif yChange < 0:
            # South to North
            return 3

    def _GetLowestAdjacentCell(self, heightMap, x, y, realisticRiverFlow):
        """
        Returns (lowestAdjacentCell, isSwamp) to the cell
        at position (x, y). If realisticRiverFlow is False,
        will return the adjacent cell that has the least elevation 
        change (but is still lower).
        """
        curCellHeight = heightMap[x][y]

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
                adjacentCellHeight = heightMap[cellCoords[0]][cellCoords[1]]
            except:
                # We've gone outside of the map...just skip this cell
                continue
            if adjacentCellHeight < lowestAdjacentCellHeight:
                lowestAdjacentCellHeight = adjacentCellHeight
                lowestAdjacentCell = cellCoords

        # Find highest of lowest adjacent cells  
        if not realisticRiverFlow:
            for cellCoords in adjacentCells:
                try:
                    if cellCoords[0] < 0 or cellCoords[1] < 0:
                        continue
                    adjacentCellHeight = heightMap[cellCoords[0]][cellCoords[1]]
                except:
                    # We've gone outside of the map...just skip this cell
                    continue
                if adjacentCellHeight > lowestAdjacentCellHeight and adjacentCellHeight < curCellHeight:
                    lowestAdjacentCellHeight = adjacentCellHeight
                    lowestAdjacentCell = cellCoords


        # Check to see if we're merging with another river
        if lowestAdjacentCell != None:
            if self._riverMap[lowestAdjacentCell[0]][lowestAdjacentCell[1]] != 0:
                return (lowestAdjacentCell, True)

        return (lowestAdjacentCell, False)

    
    def _MakeHistoryAwareDirection(self, flowDirectionNoHistory, previousFlowDirection):
        """
        Given the flow direction of a previous cell, and the no-history flow
        direction of the current cell, return the history-aware flow direction
        of the current cell.
        """
        direction = flowDirectionNoHistory

        # Flowing in a straight line
        if previousFlowDirection == flowDirectionNoHistory:
            pass
        
        # Flowing north -> South
        elif previousFlowDirection == 1:
            # West -> East
            if flowDirectionNoHistory == 2: 
                # South-East
                direction = 8
            # East -> West
            elif flowDirectionNoHistory == 4:
                # South-West
                direction = 7

        # Flowing South -> North
        elif previousFlowDirection == 3:
            # West -> East
            if flowDirectionNoHistory == 2:
                # East-North
                direction = 16
            # East -> West
            elif flowDirectionNoHistory == 4:
                # West-North
                direction = 15

        # Flowing West -> East
        elif previousFlowDirection == 2:
            # South -> North
            if flowDirectionNoHistory == 3:
                # North-East
                direction = 6
            # North -> South
            elif flowDirectionNoHistory == 1:
                # East-South
                direction = 18

        # Flowing East -> West
        elif previousFlowDirection == 4:
            # South -> North
            if flowDirectionNoHistory == 3:
                # North-West
                direction = 5
            # North -> South
            elif flowDirectionNoHistory == 1:
                # West-South
                direction = 17

        # Flowing North-West
        elif previousFlowDirection == 5:
            # West -> East
            if flowDirectionNoHistory == 2:
                # East-North
                direction = 16
            # East -> West
            elif flowDirectionNoHistory ==  4:
                # West-North
                direction = 15

        # Flowing North-East
        elif previousFlowDirection == 6:
            # West -> East
            if flowDirectionNoHistory == 2:
                # East-North
                direction = 16
            # East -> West
            elif flowDirectionNoHistory ==  4:
                # West-North
                direction = 15
            
        # Flowing South-West
        elif previousFlowDirection == 7:
            # North -> South
            if flowDirectionNoHistory == 1:
                # West-South
                direction = 17
            # South -> North
            elif flowDirectionNoHistory == 3:
                # North-West
                direction = 5

        # Flowing South-East
        elif previousFlowDirection == 8:
            # North -> South
            if flowDirectionNoHistory == 1:
                # East-South
                direction = 18
            # South -> North
            elif flowDirectionNoHistory == 3:
                # North-East
                direction = 6

        # Flowing West-North
        elif previousFlowDirection == 15:
            # North -> South
            if flowDirectionNoHistory == 1:
                # West-South
                direction = 17
            # South -> North
            elif flowDirectionNoHistory == 3:
                # North-West
                direction = 5

        # Flowing East-North
        elif previousFlowDirection == 16:
            # North -> South
            if flowDirectionNoHistory == 1:
                # East-South
                direction = 18
            # South -> North
            elif flowDirectionNoHistory == 3:
                # North-East
                direction = 6
                
        # Flowing West-South
        elif previousFlowDirection == 17:
            # West -> East
            if flowDirectionNoHistory == 2:
                # South-East
                direction = 8
            # East -> West
            elif flowDirectionNoHistory == 4:
                # South-West
                direction = 7

        # Flowing East-South
        elif previousFlowDirection == 18:
            # West -> East
            if flowDirectionNoHistory == 2:
                # South-East
                direction = 8
            # East -> West
            elif flowDirectionNoHistory == 4:
                # South-West
                direction = 7

        return direction


    # Recursively traces a river down a slope starting at the cell
    # tempArr[x][y]
    def _TraceRiverPath(self, x, y, tempArr, previousCell, path=[], length = 0):
        """
        Recursively trace a river path. If trace is successfull, returns
        (length, True), else if the path is less than 3 long and intersects with
        another river, returns (length, False)
        """

        lowestAdjacentCell, isSwamp = self._GetLowestAdjacentCell(tempArr, x, y, self._constants.RealisticRiverFlow)


        # If there are no adjacent cells that are lower, we give up!
        # No sense in building a river where this is no downward slope...it'd be a lake!
        if lowestAdjacentCell == None:
            self._riverMap[x][y] = 9 # A lake
            path.append([x,y])
            return length

        # Now we need to figure out the direction of flow...yippee    

        # Start with the flow direction without knowing where we came from
        flowDirectionNoHistory = self._GetFlowDirection((x,y), lowestAdjacentCell)

        # Find out the previous flow direction
        previousFlowDirection = self._riverMap[previousCell[0]][previousCell[1]]

        # If the previous cell is a head, we have to get the flow direction again
        if previousFlowDirection == 10:
            previousFlowDirection = self._GetFlowDirection(previousCell,(x,y))

        if previousFlowDirection is None:
            previousFlowDirection = flowDirectionNoHistory

        # Get a history-aware flow direction for the current cell
        direction = self._MakeHistoryAwareDirection(flowDirectionNoHistory, previousFlowDirection)
        
     
        # Update the river map
        self._riverMap[x][y] = direction
        path.append([x,y])

        # If the lowestAdjacentCell is the current cell, it butts up
        # against another river. Stop tracing, and make this a swamp
        if isSwamp:
            # If the length of the river is less than 3, roll back our changes
            if length < 4:
                for cell in path[:-1]:
                    self._riverMap[cell[0]][cell[1]] = 0
                    return 0
            # If we're at rocky highlands or above, it's a lake, otherwise a swamp
            if self._heightMap[lowestAdjacentCell[0]][lowestAdjacentCell[1]] >= 6:
                self._riverMap[lowestAdjacentCell[0]][lowestAdjacentCell[1]] = 9
            else:
                self._riverMap[lowestAdjacentCell[0]][lowestAdjacentCell[1]] = 11

            return length

        # Add the river head
        if length == 0:
            self._riverMap[x][y] = 10
            path.append([x,y])


        # Now trace the lowestCell down
        return self._TraceRiverPath(lowestAdjacentCell[0], lowestAdjacentCell[1], tempArr, (x,y), path, length + 1)
                

    def _GenerateRiverMap(self):
        if(VERBOSE):
            print("Generating River Map...")

        totalCells = self._size * self._size
        completedCells = 0

        # Load elevation map into a temporary array so we can mess with it ;)
        tempArr = copy.deepcopy(self._heightMap)

        # Iterate through the entire map looking for high-points
        for x in range(0, self._size):
            for y in range(0, self._size):
                curCellHeight = tempArr[x][y]

                if curCellHeight > self._constants.MinRiverSpawnHeight:
                    if random.random() < self._constants.RiverSpawnChance:
                        length = self._TraceRiverPath(x, y, tempArr, (x,y))

                        
            if(VERBOSE):
                completedCells = completedCells + self._size
                print("Progress: " + str(int(completedCells / totalCells * 100)) + "%", end="\r")
        if(VERBOSE):
            print("\nGeneration Complete.\n")                        


                        

                        

    def _GenerateTreeMap(self):
        if(VERBOSE):
            print("Generating Tree Map...")

        sSize = self._constants.SpreadSize
        heightBound = float(len(self._constants.TreeDescriptions) - 1)
        maxHeight = heightBound
        totalCells = 3 * (3 * pow(self._size, 2))
        completedCells = 0

        for time in range(0,3):
            # Ensure sSize is indeed an integer
            sSize = int(sSize)

            # Fill temp array with random data
            tempArr = [ [ 0 for y in range( self._size + sSize + 1) ] for x in range( self._size + sSize + 1) ]
            
            for x in range(0, self._size + sSize + 1):
                for y in range(0, self._size + sSize + 1):
                    tempArr[x][y] = random.uniform(-heightBound + 4.5, heightBound - 3) 


            # Horizontal Interpolation
            for x in range(0, self._size):
                for y in range(0, self._size):
                    yCoord = y - y % sSize
                    multiplier = float(y % sSize) / sSize
                    val1 = float(tempArr[x][yCoord + sSize])
                    val2 = float(tempArr[x][yCoord])
                    tempArr[x][y] = val1 * multiplier + val2 * (1 - multiplier)
                if(VERBOSE):
                    completedCells = completedCells + self._size
                    print("Progress: " + str(int(completedCells / totalCells * 100)) + "%", end="\r")

            # Vertical Interpolation
            for x in range(0, self._size):
                for y in range(0, self._size):
                    xCoord = x - x % sSize
                    multiplier = float(x % sSize) / sSize
                    val1 = float(tempArr[xCoord + sSize][y])
                    val2 = float(tempArr[xCoord][y])
                    tempArr[x][y] = val1 * multiplier + val2 * (1 - multiplier)   
                if(VERBOSE):
                    completedCells = completedCells + self._size
                    print("Progress: " + str(int(completedCells / totalCells * 100)) + "%", end="\r")
  

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
                if(VERBOSE):
                    completedCells = completedCells + self._size
                    print("Progress: " + str(int(completedCells / totalCells * 100)) + "%", end="\r")
            
            # Modify Parameters for the Next Pass
            maxHeight = maxHeight * .5
            sSize     = sSize     * .5
        if(VERBOSE):
            print("\nGeneration Complete.\n")            

    def _GenerateHeightMap(self):
        if(VERBOSE):
            print("Generating Height Map...")

        sSize = self._constants.SpreadSize
        heightBound = float(len(self._constants.HeightDescriptions) - 1)
        maxHeight = heightBound

        totalCells = 3 * 3 * pow(self._size, 2)
        completedCells = 0


        for time in range(0,3):
            # Ensure sSize is indeed an integer
            sSize = int(sSize)

            # Fill temp array with random data
            tempArr = [ [ 0 for y in range( self._size + sSize + 1) ] for x in range( self._size + sSize + 1) ]
            
            for x in range(0, self._size + sSize + 1):
                for y in range(0, self._size + sSize + 1):
                    tempArr[x][y] = random.uniform(self._constants.SeaFrequency * (-heightBound + 4.5), self._constants.MountainFrequency * (heightBound - 3)) 

            # Horizontal Interpolation
            for x in range(0, self._size):
                for y in range(0, self._size):
                    yCoord = y - y % sSize
                    multiplier = float(y % sSize) / sSize
                    val1 = float(tempArr[x][yCoord + sSize])
                    val2 = float(tempArr[x][yCoord])
                    tempArr[x][y] = val1 * multiplier + val2 * (1 - multiplier)
                if(VERBOSE):
                    completedCells = completedCells + self._size
                    print("Progress: " + str(int(completedCells / totalCells * 100)) + "%", end="\r")

            # Vertical Interpolation
            for x in range(0, self._size):
                for y in range(0, self._size):
                    xCoord = x - x % sSize
                    multiplier = float(x % sSize) / sSize
                    val1 = float(tempArr[xCoord + sSize][y])
                    val2 = float(tempArr[xCoord][y])
                    tempArr[x][y] = val1 * multiplier + val2 * (1 - multiplier)     
                if(VERBOSE):
                    completedCells = completedCells + self._size
                    print("Progress: " + str(int(completedCells / totalCells * 100)) + "%", end="\r")
  

            # Add to Map
            for x in range(0, self._size):
                for y in range(0, self._size):
                    curVal = self._heightMap[x][y]

                    self._heightMap[x][y] = curVal + tempArr[x][y]
                    if(self._heightMap[x][y] > heightBound):
                        self._heightMap[x][y] = heightBound
                    if(self._heightMap[x][y] < 0):
                        self._heightMap[x][y] = 0
                if(VERBOSE):
                    completedCells = completedCells + self._size
                    print("Progress: " + str(int(completedCells / totalCells * 100)) + "%", end="\r")
            
            # Modify Parameters for the Next Pass
            maxHeight = maxHeight * .5
            sSize     = sSize     * .5

        if(VERBOSE):
            print("\nGeneration Complete.\n")            
                       

    ## DESCRIPTION GETTERS ##
    def DescribeHeight(self, x, y):
        x = int(x)
        y = int(y)
        return self._constants.HeightDescriptions[int(self._heightMap[x][y])]
        
    def DescribeRiver(self, x, y):
        x = int(x)
        y = int(y)        
        return self._constants.RiverDescriptions[int(self._riverMap[x][y])]

    def DescribeLocation(self, x, y):
        x = int(x)
        y = int(y)        
        return self._constants.LocationDescriptions[int(self._locMap[x][y])]

    def DescribeTrees(self, x, y):
        x = int(x)
        y = int(y)        
        return self._constants.TreeDescriptions[int(self._treeMap[x][y])]

    # Saves serialized representation of the map for visualization purposes
    def SaveToFile(self, filename = "map.data", playerPos = []):
        # Build Object to Convert to JSON
        obj = {
            "heightMap": self._heightMap,
            "riverMap": self._riverMap,
            "locationMap": self._locMap,
            "treeMap": self._treeMap,
            "enemyMap": self._enemyMap
        }

        if len(playerPos) > 0:
            obj["playerPosition"] = playerPos
        
        with open(filename, 'w') as file:
            file.write(json.dumps(obj))



if __name__ == "__main__":
    # Perform Self-Test
    # Create Map
    mapSize = 30
    mapSeed = int(time.time() * 10000000 * random.random())

    if len(argv) < 2:
        print("Usage: {} <map_size> [map_seed]".format(argv[0]))
        raise SystemExit

    try:
        mapSize = int(argv[1])
        if len(argv) > 2:
            mapSeed = int(argv[2])
    except:
        print("Usage: {} <map_size> [map_seed]".format(argv[0]))
        raise SystemExit

    print("Generating map...")
    print("Size: " + str(mapSize) + "x" + str(mapSize))
    print("Seed: " + str(mapSeed))

    m =  Map(mapSize, mapSeed)
    m.SaveToFile()
    print("Map generation complete.")
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
    