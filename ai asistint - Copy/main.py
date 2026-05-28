import cv2
from ultralytics import YOLO
import face_recognition
import numpy as np
import speech_recognition as sr
import subprocess
import webbrowser
import psutil
import threading
from pycaw.pycaw import AudioUtilities
from datetime import datetime

# Твои модули
from voice import say, say_en
from gpt import text_ai
from parsing import get_news     
from translator import translate_text
# --- ГЛОБАЛЬНЫЕ ПЕРЕМЕННЫЕ ---
current_user = "Хозяин"
is_running = True






def translate_listen():

    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    
    with mic as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = recognizer.listen(source, phrase_time_limit=4)
            text = recognizer.recognize_google(audio, language='ru-RU').lower()
            return text
        except:
            return False










# --- 1. ЗРЕНИЕ (VISION) ---
def vision_worker():
    global current_user, is_running
    try:
        yolo_model = YOLO('yolov8n-face-lindevs.pt')
        known_image = face_recognition.load_image_file("me.jpeg")
        known_encoding = face_recognition.face_encodings(known_image)[0]
    except Exception as e:
        print(f"Ошибка загрузки зрения: {e}")
        return

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    while is_running:
        ret, frame = cap.read()
        if not ret: break

        results = yolo_model(frame, verbose=False)
        found_me = False

        for box in results[0].boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            face_crop = frame[max(0, y1-20):min(frame.shape[0], y2+20), 
                              max(0, x1-20):min(frame.shape[1], x2+20)]
            
            if face_crop.size > 0:
                rgb_crop = cv2.cvtColor(face_crop, cv2.COLOR_BGR2RGB)
                locations = face_recognition.face_locations(rgb_crop)
                if locations:
                    encodings = face_recognition.face_encodings(rgb_crop, locations)
                    if encodings and face_recognition.compare_faces([known_encoding], encodings[0], 0.6)[0]:
                        found_me = True
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        cv2.putText(frame, "ACCESS GRANTED", (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        current_user = "Хозяин" if found_me else "Хозяин"
        cv2.imshow('Jarvis Vision', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            is_running = False
            break
    cap.release()
    cv2.destroyAllWindows()

# --- 2. ГОЛОС И ТВОИ КОМАНДЫ ---
def voice_worker():
    global current_user, is_running
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    while is_running:
        with mic as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            try:
                audio = recognizer.listen(source, phrase_time_limit=4)
                text = recognizer.recognize_google(audio, language='ru-RU').lower()
                print(f"Распознано: {text}")
            except:
                continue

        # ПРОВЕРКА ЛИЦА
        if current_user != "Хозяин":
            if "джарвис" in text:
                say("Я вас не узнаю. Доступ к терминалу заблокирован.")
            continue

        # ПАРАМЕТРЫ ГРОМКОСТИ
        device = AudioUtilities.GetSpeakers()
        volume = device.EndpointVolume
        current_vol = volume.GetMasterVolumeLevelScalar()

        # --- СПИСОК КОМАНД ---
        
        if 'привет' in text:
            say("Привет, я твой голосовой помощник!")

        elif 'тише' in text:
            say("делаю тише...")
            volume.SetMasterVolumeLevelScalar(max(0.0, current_vol - 0.1), None)

        elif 'громче' in text:
            say("делаю громче...")
            volume.SetMasterVolumeLevelScalar(min(1.0, current_vol + 0.1), None)

        # GOOGLE CHROME
        elif 'открой гугл' in text:
            say("Открываю гугл...")
            subprocess.Popen([r'C:\Program Files\Google\Chrome\Application\chrome.exe'])
        
        elif 'закрой гугл' in text:
            say("Закрываю гугл...")
            for p in psutil.process_iter():
                if p.name().lower() == "chrome.exe": p.kill()

        elif 'новости' in text:
            say("Открываю новости...")

            news = get_news()
            for i in range(len(news["news"])):
                print(news["news"][i])
            
        elif 'переводчик' in text:
            say("переводчик активирован!")
            text_to_lang = translate_listen()
            if text_to_lang:
                    print(f"выбраный язык:{text_to_lang}")
                    print("говорите")
                    text_to_translate = translate_listen()
                    if text_to_translate:
                        translated_text = translate_text(text_to_translate, target_lang=text_to_lang)
                        say_en(f"{translated_text}")


        # YOUTUBE
        elif 'открой youtube' in text:
            say("Открываю ютуб...")
            webbrowser.open_new('https://www.youtube.com')

        # DISCORD
        elif 'открой discord' in text:
            say("Открываю дискорд...")
            subprocess.Popen([r'C:\Users\owner\AppData\Local\Discord\app-1.0.9231\Discord.exe'])
        
        elif 'закрой дискорд' in text:
            say("Закрываю дискорд...")
            for p in psutil.process_iter():
                if p.name().lower() == "discord.exe": p.kill()

        # РЕЖИМЫ
        elif 'режим музыки' in text:
            say("Режим музыки активирован!")
            webbrowser.open_new('https://music.youtube.com/watch?v=hli11HZkttQ&list=LM')
        
        elif 'время' in text:
            say(f"Сейчас: {datetime.now().strftime('%d.%m.%Y %H:%M')}")

        # TEARDOWN
        elif 'режим разрушения' in text:
            if 'отключи' in text:
                say("Отключаю режим разрушения...")
                for p in psutil.process_iter():
                    if p.name().lower() == "teardown.exe": p.kill()
            else:
                say("Режим разрушения активирован!")
                subprocess.Popen([r'C:\Program Files (x86)\Steam\steamapps\common\Teardown\teardown.exe'])

        elif 'погода' in text:
            say("Открываю погоду...")
            webbrowser.open_new('https://weather.com/weather/today/...')

        # КАЛЬКУЛЯТОР
        elif 'открой калькулятор' in text:
            say("Открываю калькулятор...")
            subprocess.Popen(['calc.exe'])
        
        elif 'закрой калькулятор' in text:
            say("Закрываю калькулятор...")
            for p in psutil.process_iter():
                if p.name() == "CalculatorApp.exe" or p.name() == "calc.exe": p.kill()

        # MINECRAFT
        elif 'открой minecraft' in text:
            say("Открываю майнкрафт...")
            subprocess.Popen([r'C:\XboxGames\Minecraft Launcher\Content\Minecraft.exe'])
        
        elif 'закрой майнкрафт' in text:
            say("Закрываю майнкрафт...")
            for p in psutil.process_iter():
                if p.name().lower() == "minecraft.exe": p.kill()

        elif 'режим информации' in text:
            say("Режим информации активирован!")
            webbrowser.open_new('https://www.wikipedia.org/')

        # ИИ ОТВЕТ
        elif 'джарвис' in text:
            response = text_ai(text)
            say(response)

# --- ЗАПУСК ---
if __name__ == "__main__":
    threading.Thread(target=vision_worker, daemon=True).start()
    voice_worker()