import collections
import os
from datetime import datetime, timedelta

import numpy as np

from classes.data_inklinometers import DataInklinometers
from classes.trackbars import Trackbars
from classes.camera import Camera
from classes.level import Level
from utils.config import options_dict
from classes.read_file import ReaderTxt
from classes.convert_file_txt_to_dict2 import ConverterTxtToDict
from classes.json_module import JSONModule
from classes.save_inklinometer_data import SaveInlinometerData
import cv2


# print(os.path.abspath(__file__))
trackbars = Trackbars("data/data.json")
# camera = Camera("output_video2.avi")
camera = Camera("data/1/TRIAL____________GH010022.mp4")
# camera = Camera(1)
level = Level(camera=camera, trackbars=trackbars, options=options_dict)


def merge_twoDict(a, b):  # define the merge_twoDict() function
    return (a.update(b))


now_dict_data = {}
new_dict = {}
reader_txt = ReaderTxt("data/data_port_spy_2.txt")
json_module = JSONModule('data/variables.json')
converter_txt_to_dict = ConverterTxtToDict()
center_bubble = 0

while True:

    data = converter_txt_to_dict.convert(data=reader_txt.read())
    level.main()
    trackbars.save()

    winfo = np.zeros((512, 512, 3), np.uint8)
    if level.center_bubble != 0:
        center_bubble = level.center_bubble


    winfo2 = np.zeros((512, 512, 3), np.uint8)
    cv2.putText(winfo2, f"Лазерное пятно = {center_bubble}px", (0, 150), cv2.FONT_HERSHEY_COMPLEX, 0.8,
                (0, 150, 0),
                2)
    if trackbars.horizontal_count == 0:
        cv2.putText(winfo2, f"Отсчет по оси y", (0, 180), cv2.FONT_HERSHEY_COMPLEX, 0.8,
                    (0, 150, 0),
                    2)
        cv2.putText(winfo2, "/|\\", (250+0, 200), cv2.FONT_HERSHEY_COMPLEX, 0.8,
                    (0, 150, 0),
                    2)
        cv2.putText(winfo2, " |", (250+5, 220), cv2.FONT_HERSHEY_COMPLEX, 0.8,
                    (0, 150, 0),
                    2)
        cv2.putText(winfo2, "\\|/", (250+0, 240), cv2.FONT_HERSHEY_COMPLEX, 0.8,
                    (0, 150, 0),
                    2)
    else:
        cv2.putText(winfo2, f"Отсчет по оси x <--->", (0, 180), cv2.FONT_HERSHEY_COMPLEX, 0.8,
                    (0, 150, 0),
                    2)
    cv2.imshow("Window", winfo2)

    cv2.waitKey(1)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
