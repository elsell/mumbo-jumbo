"""
map Object Class

Created by John Sell 
07 25 2019

"""

from constants import Constants

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

    # Eventually will procedurally generate a map. For now, it does NOTHING!
    def _GenerateMap(self):
        pass

    ## DESCRIPTION GETTERS ##
    def DescribeHeight(self, x, y):
        return self._constants.HeightDescriptions[self._heightMap[x][y]]
        
    def DescribeRiver(self, x, y):
        return self._constants.RiverDescriptions[self._riverMap[x][y]]

    def DescribeLocation(self, x, y):
        return self._constants.LocationDescriptions[self._locMap[x][y]]

    def DescribeTrees(self, x, y):
        return self._constants.TreeDescriptions[self._treeMap[x][y]]


if __name__ == "__main__":
    c =  Map(10)
    print(c.DescribeHeight(3,6))
