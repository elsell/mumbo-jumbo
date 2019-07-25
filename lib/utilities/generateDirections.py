"""
Simple, crude, and effective direction combination list generator

Written by John Sell 
07 25 2019

"""

directions = ["north", "north-west", "west", "south-west", "south", "south-east", "east", "north-east"]

output = ""

i = 0
for d in directions:
    for otherD in directions:
        if d == otherD:
            continue
        output += str(i) + ': "from ' + d + ' to ' + otherD + '",\n'
        i = i + 1

print(output)