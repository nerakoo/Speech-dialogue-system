# author:nerako
# This program is used to synthesize speech
# -----------------------2024.2.16-------------------------

import pyttsx3

class TTS:
    def __init__(self):
        self.engine = pyttsx3.init()
        # base set
        rate = self.engine.getProperty('rate')
        self.engine.setProperty('rate', 150)

        volume = self.engine.getProperty('volume')
        self.engine.setProperty('volume', 1.0)

        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[1].id)
        print("TTS engine is ready!")

    def speak(self,text):
        a = self.engine.say(text)
        self.engine.runAndWait()
        self.engine.stop()

    def save(self):
        self.engine.save_to_file('words', filename='filename', name='name')
        self.engine.runAndWait()

# if __name__ == '__main__':
#     NEW_TTS = TTS()
#     NEW_TTS.speak("Conversational Agents and Spoken Language Processing")