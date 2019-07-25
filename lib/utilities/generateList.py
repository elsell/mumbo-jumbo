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
some trees
sparse trees
trees
thick trees
"""

listString = treeDescriptions

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