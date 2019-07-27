#! /usr/bin/python3

"""
Created by John Sell 07 26 2019

Here is a nice little function that accepts a str
and speaks the string. 

Note: You must have festival installed. See installationNotes
for more details.

Usage: 
from textToSpeech import SpeakText

SpeakText("Here is some text to speak")

"""

import os

CMD1 = 'echo '
CMD2 = "festival --tts"

def SpeakText(text):
    os.system(CMD1 + '"' + text + '" | ' + CMD2)

