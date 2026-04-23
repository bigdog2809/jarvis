from pycaw.pycaw import AudioUtilities

# Получаем колонки
device = AudioUtilities.GetSpeakers()

# Интерфейс громкости
volume = device.EndpointVolume

# Текущая громкость
current = volume.GetMasterVolumeLevelScalar()
print("Сейчас:", current)

# Сделать тише на 20%
new_volume = max(0.0, current - 0.2)
volume.SetMasterVolumeLevelScalar(new_volume, None)

print("Новая:", new_volume)
