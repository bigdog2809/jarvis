from matplotlib import text
import pyttsx3
import time

engine = pyttsx3.init()

# VOICE
voices = engine.getProperty('voices') 


def say(text, sleep_time=2):
    engine.setProperty('voice', voices[3].id)
    engine.say(text)
    time.sleep(sleep_time)
    engine.runAndWait()







def say_en(text, sleep_time=2):
    engine.setProperty('voice', voices[2].id)  
    engine.say(text)
    time.sleep(sleep_time)
    engine.runAndWait()