import cv2
from ultralytics import YOLO
import face_recognition
import numpy as np

# Загрузить YOLO для детекции лиц
yolo_model = YOLO('yolov8n-face-lindevs.pt')  # Обычная YOLOv8

# Эталонное лицо
known_image = face_recognition.load_image_file("me.jpeg")
known_encoding = face_recognition.face_encodings(known_image)[0]

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

print("Камера запущена. Нажмите 'q' для выхода")

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # YOLO детектирует объекты (ищем класс 0 - person, или используем все)
    results = yolo_model(frame, verbose=False, classes=[0])  # 0 = person
    
    for box in results[0].boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        
        # Проверка размера crop
        w = x2 - x1
        h = y2 - y1
        
        if w < 50 or h < 50:  # Слишком маленькое лицо
            continue
        
        # Добавить отступы для лучшего распознавания
        padding = 20
        x1 = max(0, x1 - padding)
        y1 = max(0, y1 - padding)
        x2 = min(frame.shape[1], x2 + padding)
        y2 = min(frame.shape[0], y2 + padding)
        
        # Вырезать область
        face_crop = frame[y1:y2, x1:x2]
        
        # Конвертировать в RGB
        rgb_crop = cv2.cvtColor(face_crop, cv2.COLOR_BGR2RGB)
        
        try:
            # Найти лица в crop
            face_locations = face_recognition.face_locations(rgb_crop)
            
            if len(face_locations) > 0:
                # Получить encoding
                face_encodings = face_recognition.face_encodings(rgb_crop, face_locations)
                
                if len(face_encodings) > 0:
                    face_encoding = face_encodings[0]
                    
                    # Сравнить
                    match = face_recognition.compare_faces([known_encoding], face_encoding, tolerance=0.6)[0]
                    distance = face_recognition.face_distance([known_encoding], face_encoding)[0]
                    
                    if match:
                        color = (0, 255, 0)
                        label = f"ВЫ ({1-distance:.2f})"
                    else:
                        color = (0, 0, 255)
                        label = "Неизвестный"
                else:
                    color = (255, 0, 0)
                    label = "?"
            else:
                color = (255, 0, 0)
                label = "No face"
                
        except Exception as e:
            color = (128, 128, 128)
            label = "Error"
            print(f"Error: {e}")
        
        # Нарисовать результат
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        cv2.putText(frame, label, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
    
    cv2.imshow('Face Recognition', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()