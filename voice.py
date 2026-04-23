import pyttsx3
import time

engine = pyttsx3.init()

# VOICE
voices = engine.getProperty('voices') 
engine.setProperty('voice', voices[2].id)   # changing index, changes voices. 1 for female

def say(text, sleep_time=2):
    engine.say(text)
    time.sleep(sleep_time)
    engine.runAndWait()
