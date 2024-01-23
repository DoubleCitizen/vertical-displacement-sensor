import cv2
import numpy as np

from classes.camera import Camera
from classes.trackbars import Trackbars
from utils.utils import get_resize_picture


class Level:
    def __init__(self, camera: Camera, trackbars: Trackbars, options: dict):
        self.gray = None
        self.camera = camera
        self.trackbars = trackbars
        success, img = camera.get_image()
        self.height, self.width = img.shape[:2]
        self.center_bubble = 0
        self.center_bubble_x = 0
        self.center_bubble_y = 0
        self.x1 = 0
        self.y1 = 0
        self.x2 = 0
        self.y2 = 0
        self.is_vert = 0
        self.getgrad = "NONE"
        self.x1_framing, self.y1_framing, self.x2_framing, self.y2_framing = 0, 0, 0, 0

    def get_second_method(self):
        """
        Функция определяет сколько в одном пикселе угловых секунд
        И выводит результат
        :param x1: координата пузырька
        :param y1: координата пузырька
        :param x2: координата пузырька
        :param y2: координата пузырька
        :param is_vert: булевское значение повернутости экрана
        :param count_sec: Количество секунд в одном пикселе
        :param width_win: ширина окна
        :param height_win: высота окна
        :return: Возрвращает угловые секунды
        """
        if self.trackbars.horizontal_count == 0:
            center = (self.y1 + self.y2) / 2
            reference_point = self.height / 2
        else:
            center = (self.x1 + self.x2) / 2
            reference_point = self.width / 2
        # result_second = (reference_point - center) * self.COUNT_ARC_SECOND
        self.center_bubble = center
        self.center_bubble_x = (self.x1 + self.x2) / 2
        self.center_bubble_y = (self.y1 + self.y2) / 2
        # print(f"reference_point = {reference_point}")

    def view_image(self, src, str, scale=100):
        try:
            src = cv2.resize(src, self.get_resize_picture(src, scale))
            cv2.imshow(str, src)
        except:
            pass

    def get_cont(self, img, from_=200, to_=5000):
        contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        x, y, w, h = 0, 0, 0, 0
        for id, cnt in enumerate(contours):
            area = cv2.contourArea(cnt)
            if area > from_ and area < to_:
                peri = cv2.arcLength(cnt, True)
                approx = cv2.approxPolyDP(cnt, 0.01 * peri, True)
                x, y, w, h = cv2.boundingRect(approx)

        # Переменные для того чтобы повторно не проводить обрезку
        area_framing = abs(self.x2_framing - self.x1_framing) * abs(self.y2_framing - self.y1_framing) - (w + h)

        # self.x1_framing, self.y1_framing, self.x2_framing, self.y2_framing = 0, 0, 0, 0
        if abs(self.x1_framing - x) + abs(self.x2_framing - (x + w)) + abs(self.y1_framing - y) + abs(
                self.y2_framing - (y + h)) > 10 * 4 or area_framing > 100000:
            return x, y, x + w, y + h
        else:
            return self.x1_framing, self.y1_framing, self.x2_framing, self.y2_framing

    def select_method(self, image, r=215, g=236, b=241, scale=100, hsv=[0, 255, 56, 255, 0, 255], med=0):
        # image = cv2.resize(image, get_resize_picture(image, scale))

        lower = np.array((hsv[0], hsv[2], hsv[4]), np.uint8)
        upper = np.array((hsv[1], hsv[3], hsv[5]), np.uint8)
        # self.view_image(image, "original", scale)
        # Применение Медианного фильтра
        MedianNeChet = med
        if med > 1:
            if med % 2 == 0:
                MedianNeChet += 1
            image = cv2.medianBlur(image, MedianNeChet)

        # Фильтрация
        ## Преобразование HSV-изображения к оттенкам серого для дальнейшего
        ## оконтуривания
        # todo
        try:
            self.gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        except Exception as e:
            print(e)

        # Обрезка
        # w, h = self.gray.shape[:2]
        hsv_img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        curr_mask = cv2.inRange(hsv_img, lower, upper)
        # hsv_img[curr_mask > 0] = ([208, 255, 200])
        hsv_img[curr_mask < 255] = ([255, 255, 255])
        hsv_img = cv2.GaussianBlur(hsv_img, (3, 3), 0)

        self.view_image(hsv_img, "hsv_img", scale)
        thresh = cv2.inRange(hsv_img, lower, upper)
        #todo
        # Copy the thresholded image.
        im_floodfill = thresh.copy()

        # Mask used to flood filling.
        # Notice the size needs to be 2 pixels than the image.
        h, w = thresh.shape[:2]
        mask = np.zeros((h + 2, w + 2), np.uint8)

        # Floodfill from point (0, 0)
        cv2.floodFill(im_floodfill, mask, (0, 0), 255);

        # Invert floodfilled image
        im_floodfill_inv = cv2.bitwise_not(im_floodfill)

        # Combine the two images to get the foreground.
        im_out = thresh | im_floodfill_inv
        self.view_image(im_out, "im_out", scale)
        #todo

        x1, y1, x2, y2 = self.get_cont(im_out, from_=200, to_=1000000)
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 10)
        self.view_image(image, "image", scale)

        return x1, y1, x2, y2

    @staticmethod
    def get_resize_picture(src, scale):
        width = int(src.shape[1] * scale / 100)
        height = int(src.shape[0] * scale / 100)

        dsize = (width, height)
        return dsize

    def main(self):
        # r = self.trackbars.r
        # g = self.trackbars.g
        # b = self.trackbars.b
        med = self.trackbars.med

        h_min = self.trackbars.h_min
        h_max = self.trackbars.h_max
        s_min = self.trackbars.s_min
        s_max = self.trackbars.s_max
        v_min = self.trackbars.v_min
        v_max = self.trackbars.v_max
        hsv_list = [h_min, h_max, s_min, s_max, v_min, v_max]

        success, img = self.camera.get_image()
        self.get_second_method()


        scale_percent = self.trackbars.scale_percent
        if scale_percent == 0:
            scale_percent = 1

        # Подсчёт значений по x, y
        self.x1, self.y2, self.x2, self.y1 = self.select_method(img, scale=scale_percent, hsv=hsv_list,
                                                                med=med)
        self.height, self.width = img.shape[:2]
