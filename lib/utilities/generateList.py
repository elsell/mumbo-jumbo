"""
Simple, crude, and effective list generator

Written by John Sell 
07 25 2019
"""

locations = """
Observation tower
Farmhouse
Shop
High-rise building
Chicken coop
Barracks
Church / Chapel / Cathedral
Monastery
Town hall
Skyscraper
Stadium
Pyramid
Prison
Ice station
Eiffel tower
Forester's house
Lawyer's chambers
Hardware store
Brothel
Office
Factory (assembly line)
Hairdresser
open-plan office
Harbor
Internet cafe
Cantine
Orthodontist
Kindergarten
Market
open air market
Massage pactice
trade fair stand
Gym
Nail salon
Butcher's shop
School
Tanning salon
Tax advisor
Supermarket
Laundromat
Ad agency
Sausage stand
Dentist
wig store
Library
School
Cinema
Theatre
Museum
Children's room
"""

treeDescriptions = """
no foliage
a tree
a few trees
a scattering of trees and shrubs
a grove
a thin wood
a moderate wood
a thicket
a forest
a dense forest
"""

elevations = """
a sea
a lowland area
a meadow
a plain
a prairie
a hilly area
a highland area
a rocky highland
a mountainside
a mountain
a snowy mountaintop
"""

listString = elevations

# Convert string list to list list
listItems = listString.split("\n")

output = ""

i = 0
for d in listItems:
    if(d == ""):
        continue
    output += str(i) + ': "' + d + '",\n'
    i = i + 1

print(output)