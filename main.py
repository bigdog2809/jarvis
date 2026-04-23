import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr
import subprocess
import webbrowser
import psutil
from pycaw.pycaw import AudioUtilities
from datetime import datetime
from voice import say
from gpt import text_ai

duration = 4  # seconds
samplerate = 44100  # Hz
languge = 'ru-RU'  # Russian language

while True:
    print("Recording...")
    recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='int16')
    sd.wait()

    wav.write('output.wav', samplerate, recording)
    print ("Recording finished. Saved as output.wav")
    recognizer = sr.Recognizer()
    with sr.AudioFile('output.wav') as source:
        audio = recognizer.record(source)

    try:
            # Получаем колонки
        device = AudioUtilities.GetSpeakers()
        # Интерфейс громкости
        volume = device.EndpointVolume

        text = recognizer.recognize_google(audio, language=languge)
        if text.lower() in 'привет':
            say("Привет, я твой голосовой помощник!")

        elif text.lower() in 'джарвис тише':
            say("делаю тише...")
            # Текущая громкость
            current = volume.GetMasterVolumeLevelScalar()
            print("Сейчас:", current)

            # Сделать тише на 10%
            new_volume = max(0.0, current - 0.1)
            volume.SetMasterVolumeLevelScalar(new_volume, None)

        elif text.lower() in 'джарвис громче':
            say("делаю громче...")
            # Текущая громкость
            current = volume.GetMasterVolumeLevelScalar()
            print("Сейчас:", current)

            # Сделать громче на 10%
            new_volume = max(0.0, current + 0.1)
            volume.SetMasterVolumeLevelScalar(new_volume, None)

            print("Новая:", new_volume)

        elif text.lower() in 'джарвис закрой гугл':
            say("Закрываю гугл...")
            for process in (process for process in psutil.process_iter() if process.name()=="chrome.exe"):
                process.kill()
        elif text.lower() in 'джарвис открой гугл':
            say("Открываю гугл...")
            subprocess.call(r'C:\Program Files\Google\Chrome\Application\chrome.exe')

        elif text.lower() in 'джарвис открой youtube':
            say("Открываю ютуб...")
            webbrowser.open_new('https://www.youtube.com')

        elif text.lower() in 'джарвис закрой дискорд':
            say("Закрываю дискорд...")
            for process in (process for process in psutil.process_iter() if process.name()=="Discord.exe"):
                process.kill()
        elif text.lower() in 'джарвис открой discord':
            say("Открываю дискорд...")
            subprocess.call(r'C:\Users\owner\AppData\Local\Discord\app-1.0.9231\Discord.exe')
        
        elif text.lower() in 'джарвис режим музыки':
            say("Режим музыки активирован!")
            webbrowser.open_new('https://music.youtube.com/watch?v=hli11HZkttQ&list=LM')
        
        elif text.lower() in 'джарвис время':
            say(f"Сейчас: {datetime.now().strftime('%d.%m.%Y %H:%M')}")

        elif text.lower() in 'джарвис отключи режим разрушения':
            say("Отключаю режим разрушения...")
            for process in (process for process in psutil.process_iter() if process.name()=="teardown.exe"):
                process.kill()
        elif text.lower() in 'джарвис режим разрушения':
            say("Режим разрушения активирован!")
            subprocess.call(r'C:\Program Files (x86)\Steam\steamapps\common\Teardown\teardown.exe')

        elif text.lower() in 'джарвис погода':
            say("Открываю погоду...")
            webbrowser.open_new('https://weather.com/weather/today/l/4e14a8819e49c592da7345a9119b3b90f5dc9018cd5d09dae5424069651c0650')

        elif text.lower() in 'джарвис закрой калькулятор':
            say("Закрываю калькулятор...")
            for process in (process for process in psutil.process_iter() if process.name()=="CalculatorApp.exe"):
                process.kill() 

        elif text.lower() in 'джарвис открой калькулятор':
            say("Открываю калькулятор...")
            subprocess.call(r'C:\Windows\System32\calc.exe')

        elif text.lower() in 'джарвис режим информации':
            say("Режим информации активирован!")
            webbrowser.open_new('https://www.wikipedia.org/')
        
        elif text.lower() in 'джарвис закрой майнкрафт':
            say("Закрываю майнкрафт...")
            for process in (process for process in psutil.process_iter() if process.name()=="Minecraft.exe"):
                process.kill()
        elif text.lower() in 'джарвис открой minecraft':
            say("Открываю маинкрафт...")
            subprocess.call(r'C:\XboxGames\Minecraft Launcher\Content\Minecraft.exe')
        
        else:
            if 'джарвис' in text.lower():
                response = text_ai(text)
                say(response, sleep_time=5)

    except Exception as e:
        print("Error: ", e)