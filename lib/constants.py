#! /usr/bin/python3

"""
Class to hold constant values
(Mostly maps between numeric values and descriptions)

Created by John Sell
07 25 2019
"""

class Constants:
    def __init__(self):
        pass

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
        return .25

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
            0: "from north to west",
            1: "from north to south",
            2: "from north to east",
            3: "from west to north",
            4: "from west to south",
            5: "from west to east",
            6: "from south to north",
            7: "from south to west",
            8: "from south to east",
            9: "from east to north",
            10: "from east to west",
            11: "from east to south",
            12: "a puddle"
        }

    
