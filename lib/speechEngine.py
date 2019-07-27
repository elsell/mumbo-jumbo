#! /usr/bin/python3

""" 
Created by John Sell 
07 27 2019

SpeechRecognition and TTS Facilitator
"""
import os
from pocketsphinx import LiveSpeech, get_model_path



# Ex: Question("Where will you move?", [['go'], ['south','north']])
class Question:
    def __init__(self, message, responses):
        self._message = message
        self._responses = responses

        # Number of words in anticipated response
        self._responseLen = len(responses)

    @property
    def Message(self):
        return self._message
    
    @property
    def Responses(self):
        return self._responses

    @property
    def WordsInResponse(self):
        return self._responseLen

class SpeechEngine:
    def __init__(self):
        pass
    
    def SpeakText(self, text):
        CMD1 = 'echo '
        CMD2 = "festival --tts"

        os.system(CMD1 + '"' + text + '" | ' + CMD2)

    def AskQuestion(self, question):
        if not isinstance(question, Question):
            raise TypeError("AskQuestion takes a Question object")
        
        self.SpeakText(question.Message)

        model_path = get_model_path()

        speech = LiveSpeech(
            verbose=False,
            sampling_rate=16000,
            buffer_size=2048,
            no_search=False,
            full_utt=False,
            hmm=os.path.join(model_path, 'en-us'),
            lm=os.path.join(model_path, 'en-us.lm.bin'),
            dic=os.path.join(model_path, 'johnsell-en-us.dict')
        )
        quit = False
        tries = 1
        response = ""
        for phrase in speech:
            response = ""
            if quit:
                speech.end_utt()
                speech.stop()
                break

            words = str(phrase).split(" ")
            print(words)

            numWords = 0
            for wordPosition in question.Responses:
                isAMatch = False

                for word in wordPosition:
                    if words[numWords] == word:
                        isAMatch = True
                        response += words[numWords] + " "

                if(numWords >= question.WordsInResponse - 1) and isAMatch:
                    quit = True
                    break

                if not isAMatch:
                    break
                numWords = numWords + 1

            tries = tries + 1
            if quit:
                break
            else:
                # If not quit here, the spoken phrase does not match the 
                # response anticipated. Tell the user!
                self.SpeakText("What was that again?")
        print("QUIT: " + str(quit))

        return response




    
if __name__ == "__main__":
    e = SpeechEngine()
    q = Question("Where will you go Joe?", [['go'], ['south','north']])

    f = e.AskQuestion(q)
    print("RESPONSE: " + f)