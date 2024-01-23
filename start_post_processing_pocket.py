from datetime import datetime, timedelta
import os, fnmatch
import numpy as np

from classes.data_inklinometers import DataInklinometers
from classes.json_module import JSONModule
from classes.trackbars import Trackbars
from classes.camera import Camera
from classes.level import Level
from utils.config import options_dict
from classes.read_file import ReaderTxt
from classes.convert_file_txt_to_dict2 import ConverterTxtToDict
from classes.save_inklinometer_data import SaveInlinometerData
from classes.timer import Timer
import cv2

from utils.get_creation_date_file import creation_date


def find(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result


trackbars = Trackbars("data/data.json")


def processing(file_name, text_info):
    reader_txt = ReaderTxt("data/data_port_spy_2.txt")
    json_module = JSONModule('data/variables.json')
    center_bubble = 0
    camera = Camera(f"data/{file_name}")
    level = Level(camera=camera, trackbars=trackbars, options=options_dict)

    # Начальное время (когда было записано видео)
    start_time = creation_date(f"data/{file_name}")
    # start_time = start_time.replace(microsecond=0)
    start_time = start_time.replace(microsecond=0, hour=16, minute=36, second=10, month=9, day=1, year=2023)

    # Создание таймера
    t = Timer()
    # Запуск таймера
    t.start()
    # Обьявление переменных прошедших секунд (реальных)
    seconds_passed_real = 0
    seconds_left_real = 0

    # Обьявление переменных прошедших секунд (кадровых)
    old_seconds_passed = 0
    seconds_passed = 0
    i = 0

    while True:
        if camera.get_frames() >= camera.get_all_frames():
            break

        seconds_passed = int(camera.get_frames() / camera.get_fps())
        if seconds_passed == old_seconds_passed:
            i += 1
        else:
            i = 1
        old_seconds_passed = seconds_passed

        seconds_left = int(abs(camera.get_all_frames() // camera.get_fps()) - int(seconds_passed))
        if int(seconds_passed) != 0:
            seconds_left_real = int((t.get_time() / int(seconds_passed)) * seconds_left)
            seconds_passed_real = int((t.get_time() / int(seconds_passed)) * int(seconds_passed))

        seconds_passed_str = str(seconds_passed)

        # Запуск модуля обработки лазерного инклинометра
        try:
            level.main()
        except:
            break
        # Сохранение значение ползунков
        trackbars.save()

        datetime_now_inklinometer = str(f"{start_time + timedelta(seconds=int(seconds_passed) + i / camera.get_fps())}")

        # Запись данных в txt файл
        with open(f'data/{file_name}.txt', 'a+') as f:
            f.write(f'{datetime_now_inklinometer}\t{level.center_bubble_x}\t{level.center_bubble_y}\n')

        # Выводить значения положения лазерного пятна, когда они не равны нулю
        if level.center_bubble != 0:
            center_bubble = level.center_bubble

        # Создание информационного окна
        winfo2 = np.zeros((512, 512, 3), np.uint8)
        cv2.putText(winfo2, f"Лазерное пятно = {center_bubble}px", (0, 150 - 100), cv2.FONT_HERSHEY_COMPLEX, 0.8,
                    (0, 150, 0),
                    2)
        if trackbars.horizontal_count == 0:
            cv2.putText(winfo2, f"Отсчет по оси y", (0, 180 - 100), cv2.FONT_HERSHEY_COMPLEX, 0.8,
                        (0, 150, 0),
                        2)
            cv2.putText(winfo2, "/|\\", (250 + 0, 200 - 100), cv2.FONT_HERSHEY_COMPLEX, 0.8,
                        (0, 150, 0),
                        2)
            cv2.putText(winfo2, " |", (250 + 5, 220 - 100), cv2.FONT_HERSHEY_COMPLEX, 0.8,
                        (0, 150, 0),
                        2)
            cv2.putText(winfo2, "\\|/", (250 + 0, 240 - 100), cv2.FONT_HERSHEY_COMPLEX, 0.8,
                        (0, 150, 0),
                        2)
        else:
            cv2.putText(winfo2, f"Отсчет по оси x <--->", (0, 180 - 100), cv2.FONT_HERSHEY_COMPLEX, 0.8,
                        (0, 150, 0),
                        2)
        cv2.putText(winfo2,
                    f"Прошло времени = {seconds_passed_real // 60 // 60}:{(seconds_passed_real // 60) % 60}:{seconds_passed_real % 60}",
                    (0, 180), cv2.FONT_HERSHEY_COMPLEX, 0.8,
                    (0, 150, 0),
                    2)
        cv2.putText(winfo2,
                    f"(кадровые) = {int(seconds_passed) // 60 // 60}:{(int(seconds_passed) // 60) % 60}:{int(seconds_passed) % 60}",
                    (0, 210), cv2.FONT_HERSHEY_COMPLEX, 0.8,
                    (0, 150, 0),
                    2)
        cv2.putText(winfo2,
                    f"Осталось времени = {seconds_left_real // 60 // 60}:{(seconds_left_real // 60) % 60}:{seconds_left_real % 60}",
                    (0, 240), cv2.FONT_HERSHEY_COMPLEX, 0.8,
                    (0, 150, 0),
                    2)
        cv2.putText(winfo2,
                    f"(кадровые) = {seconds_left // 60 // 60}:{(seconds_left // 60) % 60}:{seconds_left % 60}",
                    (0, 270), cv2.FONT_HERSHEY_COMPLEX, 0.8,
                    (0, 150, 0),
                    2)
        cv2.putText(winfo2,
                    text_info,
                    (0, 300), cv2.FONT_HERSHEY_COMPLEX, 0.8,
                    (0, 150, 0),
                    2)
        cv2.putText(winfo2,
                    f'Обрабатывается файл:',
                    (0, 330), cv2.FONT_HERSHEY_COMPLEX, 0.8,
                    (0, 150, 0),
                    2)
        cv2.putText(winfo2,
                    file_name,
                    (0, 360), cv2.FONT_HERSHEY_COMPLEX, 0.8,
                    (0, 150, 0),
                    2)
        cv2.imshow("Window", winfo2)

        cv2.waitKey(1)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


list_processing = find('*.mp4', 'data')
list_json = find('*.txt', 'data')
new_list_json = []
for json in list_json:
    new_json = json.split('\\')[1]
    new_json = new_json[:new_json.find('_i')]
    new_list_json.append(new_json)

for id, file_name in enumerate(list_processing):
    file_name = file_name.split('\\')[1]
    print(file_name)
    if file_name.find('mp4') != -1 and not (file_name in new_list_json):
        processing(file_name, f'{id + 1} / {len(list_processing)} файлов')

print('Обработка прошла успешно!')
