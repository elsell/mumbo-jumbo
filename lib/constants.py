#! /usr/bin/python3

"""
Class to hold constant values, basically a settings class
(Mostly maps between numeric values and descriptions)

Created by John Sell
07 25 2019
"""

VERBOSE = True

class Constants:
    def __init__(self):
        pass

    @property
    def KeyboardPrompt(self):
        return "~> "

    @property
    def TimeUnitsInDay(self):
        """
        How many time units make up a day? If 24, then one day 
        is equivalent to 24 time units (which is what we're 
        used to with 24 hours in a day)

        Every turn advances the time by one time unit. A default
        of 48 is chosen here to make one day go by in 48 turns,
        or every turn is equivalent to 1/2 'hour'.
        """
        return 48

    # Mountain Frequency Modifier (1 = Most, 0 = Least)
    @property
    def MountainFrequency(self):
        return 0.8

    # Sea Frequency Modifier (1 = Most, 0 = Least)
    @property
    def SeaFrequency(self):
        return 0.4

    # True: Rivers flow to lowest adjacent cell
    # False: Rivers flow to highest-lowest adjacent cell
    @property
    def RealisticRiverFlow(self):
        return False

    # Prevents rivers of length less than this value from
    # forming.
    @property
    def MinimumRiverLength(self):
        return 2

    # This property relates to the 'smoothness' of the generated map
    @property
    def SpreadSize(self):
        return 16

    # Lowest elevation at which a river will spawn
    @property
    def MinRiverSpawnHeight(self):
        return 9

    # Chance that a river spawns on a > MinRiverSpawnHeight height cell
    @property
    def RiverSpawnChance(self):
        return .2

    @property
    def HeightDescriptions(self):
        return{
            0: "a sea",
            1: "a lowland area",
            2: "a meadow",
            3: "a plain",
            4: "a prairie",
            5: "a hilly area",
            6: "a highland area",
            7: "a rocky highland",
            8: "a mountainside",
            9: "a mountain",
            10: "a snowy mountaintop",
        }


    @property
    def NoMovement(self):
        return 0
    @property
    def North(self):
        return 1
    @property
    def South(self):
        return 2
    @property
    def East(self):
        return 3
    @property
    def West(self):
        return 4

    @property
    def Head(self):
        return 1
    @property
    def Body(self):
        return 2
    @property
    def Arms(self):
        return 3
    @property
    def Legs(self):
        return 4

    @property
    def PlayerDefaults(self):
        return{
            "hp"    : 0,
            "maxHp" : 1,
            "attack": 2,
            "noise" : 3,
            "speed" : 4,
            "sneak" : 5
        }

    @property
    def LocationDescriptions(self):
        return{
            0: "Observation tower",
            1: "Farmhouse",
            2: "Shop",
            3: "High-rise building",
            4: "Chicken coop",
            5: "Barracks",
            6: "Church / Chapel / Cathedral",
            7: "Monastery",
            8: "Town hall",
            9: "Skyscraper",
            10: "Stadium",
            11: "Pyramid",
            12: "Prison",
            13: "Ice station",
            14: "Eiffel tower",
            15: "Forester's house",
            16: "Lawyer's chambers",
            17: "Hardware store",
            18: "Brothel",
            19: "Office",
            20: "Factory",
            21: "Hairdresser",
            22: "open-plan office",
            23: "Harbor",
            24: "Internet cafe",
            25: "Cantine",
            26: "Orthodontist",
            27: "Kindergarten",
            28: "Market",
            29: "open air market",
            30: "Massage pactice",
            31: "trade fair stand",
            32: "Gym",
            33: "Nail salon",
            34: "Butcher's shop",
            35: "School",
            36: "Tanning salon",
            37: "Tax advisor",
            38: "Supermarket",
            39: "Laundromat",
            40: "Ad agency",
            41: "Sausage stand",
            42: "Dentist",
            43: "wig store",
            44: "Library",
            45: "School",
            46: "Cinema",
            47: "Theatre",
            48: "Museum",
            49: "Children's room",
        }
    
    @property
    def TreeDescriptions(self):
        return{
            0: "no foliage",
            1: "a tree",
            2: "a few trees",
            3: "a scattering of trees and shrubs",
            4: "a grove",
            5: "a thin wood",
            6: "a moderate wood",
            7: "a thicket",
            8: "a forest",
            9: "a dense forest",
        }

   
    @property
    def RiverDescriptions(self):
        return{
            0: "no river",
            # Pure Cardinal
            1: "from north to south",
            2: "from west to east",
            3: "from south to north",
            4: "from east to west",
            # Diagonal
            5: "north-west",
            6: "north-east",
            7: "south-west",
            8: "south-east",

            15: "west-north",
            16: "east-north",
            17: "west-south",
            18: "east-south",

            9: "a lake",
            10: "a river's head",
            11: "a swamp",
        }

    
def Clamp(n, lowBound, highBound):
    return max(0, min(n, highBound))