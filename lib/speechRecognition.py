#! /usr/bin/python3

"""
Created by John Sell 07 26 2019
Basic code that will serve as the building blocks
for future tts work
"""

import os

text = "Oh come on Jerry! I exclaimed. We need to continue on!"

frontCmd = 'echo '
baseCmd = "../bin/tts/festival/bin/festival --tts"

os.system(frontCmd + '"' + text + '" | ' + baseCmd)