import random
from constants import Constants, VERBOSE
from threading import Thread
import math

class Building:
    def __init__(self, building_type):
        self.type = building_type

class Structure_Maps:
    def __init__(self, size, seed):
        if(size < 1):
            raise ValueError(
                "Map size must be greater than 0 (Provided " + str(size) + ")"
        )

        if seed != None:
            random.seed(seed)
        else:
            seed = random.randint(0,100000000000000000)
        self._seed = seed


        # Get us some constants!
        self._constants = Constants()

        # Create and initialize member variables
        self._size = size

        self._townMap = []

        if(VERBOSE):
            print("Initializing Blank Map...")

        self._InitMaps(size)

        if(VERBOSE):
            print("Done.")

        # Now we shall generate our map
        self._GenerateMaps()

    def _InitMaps(self, size):
        """
        Dispatches threads to init the blank maps. Also waits 
        for threads to join.
        """
        threads = []

        threads.append(Thread(target=self._InitTownMap,args=(size,)))

        for t in threads:
            t.start()

        for t in threads:
            t.join()

    def _InitTownMap(self, size):
        if(VERBOSE):
            print("Initializing Town Map...")        
        self._townMap         = [ [ 0 for y in range( size ) ] for x in range( size ) ]
        if(VERBOSE):
            print("Initializing Town Map - Done")        

    
    def _GenerateMaps(self):
        """
        Generates maps, one per thread. 
        Waits for threads to join.
        """
        self._GenerateTownMap()

    def _GenerateTownMap(self):
        numberOfTypesBuilt = []
        for buildingType in range(0, len(self._constants.BuildingTypes)):
            numberOfTypesBuilt.append(self._constants.BuildingWeights[buildingType])

        townCenters = []


        distanceThresh = self._size* self._constants.BuildingDistanceThreshold[0]
        # Clamp distance threshold to the provided range
        distanceThresh = max(
            min(
                distanceThresh,
                self._constants.BuildingDistanceThreshold[2]
            ),
            self._constants.BuildingDistanceThreshold[1]
        )


        failedBuilds = 0
        while failedBuilds < self._constants.BuildingThreshold:
            failed = False
            selectedX = random.randint(0, self._size - 1)
            selectedY = random.randint(0, self._size - 1)

            # Check to see if this location is within the distance threshold
    
            if len(townCenters) > 0:
                for center in townCenters:
                    d = math.sqrt(
                        pow(selectedX - center[0], 2) +
                        pow(selectedY - center[1], 2)
                    )

                    # Skip this place if we're too close
                    if d < distanceThresh:
                        failedBuilds += 1
                        failed = True
                        break
            # Again, skip on if we've got a failed build location
            if failed:
                continue

            # Now we have a location at which we can build a town

            buildLocs = [
                (selectedX - 1, selectedY + 1),
                (selectedX    , selectedY + 1),
                (selectedX + 1, selectedY + 1),
                (selectedX + 1, selectedY    ),
                (selectedX + 1, selectedY - 1),
                (selectedX    , selectedY - 1),
                (selectedX - 1, selectedY - 1),
                (selectedX - 1, selectedY    ),
            ]

            # Check to make sure we're not going to place buildings outside
            # of the map first.
            outsideMap = False
            for loc in buildLocs:
                if not (0 < loc[0] < self._size and 0 < loc[1] < self._size):
                    outsideMap = True
            if outsideMap:
                continue

            # We're now safe to build, add the town center!
            townCenters.append((selectedX, selectedY))

            # Place a town center
            self._townMap[selectedX][selectedY] = 1 # Town Hall

            for loc in buildLocs:
                minBuildType = min(numberOfTypesBuilt)
                buildingType = [i for i,j in enumerate(numberOfTypesBuilt) if j == minBuildType][0]
                
                if buildingType == 0:
                    # TODO: Make this configurable. Used to increase 
                    # variance of town sizes by introducing more entropy to
                    # how blank spaces are generated. 
                    numberOfTypesBuilt[buildingType] += random.uniform(.1,.6)
                else:
                    numberOfTypesBuilt[buildingType] += self._constants.BuildingWeights[buildingType]

                self._townMap[loc[0]][loc[1]] = buildingType


                



if __name__ == "__main__":
    sm = Structure_Maps(25, 100)
    for row in sm._townMap:
        for col in row:
            if col == 0:
                col = "."
            print("{} ".format(col),end="")
        print()
