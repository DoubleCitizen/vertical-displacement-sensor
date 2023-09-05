import json
from json import JSONDecodeError

import cv2


def back(*args):
    pass


class Trackbars:
    def empty(self, a):
        pass

    def load_json(self, path):
        try:
            with open(path, "r") as file:
                self.data = file.read()
            self.data = json.loads(self.data)
        except JSONDecodeError:
            self.data = {}

    def __init__(self, path_data):
        self.data = {}
        self.load_json(path_data)
        self.h_minT = self.data.get('h_min', 0)
        self.h_maxT = self.data.get('h_max', 255)
        self.s_minT = self.data.get('s_min', 56)
        self.s_maxT = self.data.get('s_max', 255)
        self.v_minT = self.data.get('v_min', 0)
        self.v_maxT = self.data.get('v_max', 255)
        self.w_2_leftT = self.data.get('w_2_left')
        self.w_1_rightT = self.data.get('w_1_right')
        # self.rT = self.data.get('r', 215)
        # self.gT = self.data.get('g', 236)
        # self.bT = self.data.get('b', 241)
        self.medT = self.data.get('med', 4)
        self.horizontal_countT = self.data.get('horizontal_count', 1)
        self.height_1T = self.data.get('height_1')
        self.height_2T = self.data.get('height_2')
        self.width_1T = self.data.get('width_1')
        self.width_2T = self.data.get('width_2')
        self.scale_percentT = self.data.get('scale_percent', 100)

        cv2.namedWindow("Options Images")
        cv2.resizeWindow("Options Images", 600, 180)
        cv2.createTrackbar("Rotate Angle", "Options Images", 0, 360, self.empty)
        cv2.createTrackbar("Horizontal Counting", "Options Images", 0, 1, self.empty)
        cv2.createTrackbar("Scale Percent", "Options Images", 20, 100, self.empty)
        cv2.createTrackbar("Median", "Options Images", 0, 10, self.empty)

        cv2.namedWindow("HSV New Method")
        cv2.resizeWindow("HSV New Method", 640, 300)
        cv2.createTrackbar("H Min", "HSV New Method", 0, 255, self.empty)
        cv2.createTrackbar("H Max", "HSV New Method", 0, 255, self.empty)
        cv2.createTrackbar("S Min", "HSV New Method", 0, 255, self.empty)
        cv2.createTrackbar("S Max", "HSV New Method", 0, 255, self.empty)
        cv2.createTrackbar("V Min", "HSV New Method", 0, 255, self.empty)
        cv2.createTrackbar("V Max", "HSV New Method", 0, 255, self.empty)

        cv2.setTrackbarPos("H Min", "HSV New Method", self.h_minT)
        cv2.setTrackbarPos("H Max", "HSV New Method", self.h_maxT)
        cv2.setTrackbarPos("S Min", "HSV New Method", self.s_minT)
        cv2.setTrackbarPos("S Max", "HSV New Method", self.s_maxT)
        cv2.setTrackbarPos("V Min", "HSV New Method", self.v_minT)
        cv2.setTrackbarPos("V Max", "HSV New Method", self.v_maxT)

        cv2.setTrackbarPos("Median", "Options Images", self.medT)
        cv2.setTrackbarPos("Horizontal Counting", "Options Images", self.horizontal_countT)
        cv2.setTrackbarPos("Scale Percent", "Options Images", self.scale_percentT)

    def save(self):
        data = {
            # "r": self.r,
            # "g": self.g,
            # "b": self.b,
            "med": self.med,
            "h_min": self.h_min,
            "h_max": self.h_max,
            "s_min": self.s_min,
            "s_max": self.s_max,
            "v_min": self.v_min,
            "v_max": self.v_max,
            "horizontal_count": self.horizontal_count,
            "scale_percent": self.scale_percent,
        }
        with open("data/data.json", "w") as file:
            file.write(json.dumps(data))

    # @property
    # def r(self):
    #     r = cv2.getTrackbarPos("Red", "NewMethod")
    #     return r
    #
    # @property
    # def g(self):
    #     g = cv2.getTrackbarPos("Green", "NewMethod")
    #     return g
    #
    # @property
    # def b(self):
    #     b = cv2.getTrackbarPos("Blue", "NewMethod")
    #     return b

    @property
    def med(self):
        med = cv2.getTrackbarPos("Median", "Options Images")
        return med

    @property
    def h_min(self):
        h_min = cv2.getTrackbarPos("H Min", "HSV New Method")
        return h_min

    @property
    def h_max(self):
        h_max = cv2.getTrackbarPos("H Max", "HSV New Method")
        return h_max

    @property
    def s_min(self):
        s_min = cv2.getTrackbarPos("S Min", "HSV New Method")
        return s_min

    @property
    def s_max(self):
        s_max = cv2.getTrackbarPos("S Max", "HSV New Method")
        return s_max

    @property
    def v_min(self):
        v_min = cv2.getTrackbarPos("V Min", "HSV New Method")
        return v_min

    @property
    def v_max(self):
        v_max = cv2.getTrackbarPos("V Max", "HSV New Method")
        return v_max

    @property
    def ang(self):
        ang = cv2.getTrackbarPos("Rotate Angle", "Rotate Images")
        return ang

    @property
    def horizontal_count(self):
        horizontal_count = cv2.getTrackbarPos("Horizontal Counting", "Options Images")
        return horizontal_count

    @property
    def scale_percent(self):
        scale_percent = cv2.getTrackbarPos("Scale Percent", "Options Images")
        return scale_percent

    @h_min.setter
    def h_min(self, value):
        self._h_min = value

    @h_max.setter
    def h_max(self, value):
        self._h_max = value

    @s_min.setter
    def s_min(self, value):
        self._s_min = value

    @s_max.setter
    def s_max(self, value):
        self._s_max = value

    @v_min.setter
    def v_min(self, value):
        self._v_min = value

    @v_max.setter
    def v_max(self, value):
        self._v_max = value

    # @r.setter
    # def r(self, value):
    #     self._r = value
    #
    # @g.setter
    # def g(self, value):
    #     self._g = value
    #
    # @b.setter
    # def b(self, value):
    #     self._b = value

    @med.setter
    def med(self, value):
        self._med = value
