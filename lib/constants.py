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


    @property
    def HeightDescriptions(self):
        return{
            0: "a sea",
            1: "a beach",
            2: "a damp grotto",
            3: "a prairie",
            4: "a grassy meadow",
            5: "a hilly region",
            6: "a rocky outcropping",
            7: "a mountainside",
            8: "a mountain",
            9: "Most Certainly In Space",
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
            0: "some trees",
            1: "sparse trees",
            2: "trees",
            3: "thick trees",
        }

   
    @property
    def RiverDescriptions(self):
        return{
            0: "from north to north-west",
            1: "from north to west",
            2: "from north to south-west",
            3: "from north to south",
            4: "from north to south-east",
            5: "from north to east",
            6: "from north to north-east",
            7: "from north-west to north",
            8: "from north-west to west",
            9: "from north-west to south-west",
            10: "from north-west to south",
            11: "from north-west to south-east",
            12: "from north-west to east",
            13: "from north-west to north-east",
            14: "from west to north",
            15: "from west to north-west",
            16: "from west to south-west",
            17: "from west to south",
            18: "from west to south-east",
            19: "from west to east",
            20: "from west to north-east",
            21: "from south-west to north",
            22: "from south-west to north-west",
            23: "from south-west to west",
            24: "from south-west to south",
            25: "from south-west to south-east",
            26: "from south-west to east",
            27: "from south-west to north-east",
            28: "from south to north",
            29: "from south to north-west",
            30: "from south to west",
            31: "from south to south-west",
            32: "from south to south-east",
            33: "from south to east",
            34: "from south to north-east",
            35: "from south-east to north",
            36: "from south-east to north-west",
            37: "from south-east to west",
            38: "from south-east to south-west",
            39: "from south-east to south",
            40: "from south-east to east",
            41: "from south-east to north-east",
            42: "from east to north",
            43: "from east to north-west",
            44: "from east to west",
            45: "from east to south-west",
            46: "from east to south",
            47: "from east to south-east",
            48: "from east to north-east",
            49: "from north-east to north",
            50: "from north-east to north-west",
            51: "from north-east to west",
            52: "from north-east to south-west",
            53: "from north-east to south",
            54: "from north-east to south-east",
            55: "from north-east to east",
        }

    
