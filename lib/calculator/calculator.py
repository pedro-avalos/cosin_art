import colorsys
import math
import random
from PIL import Image, ImageDraw


def hsv2rgb(h, s, v):
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h, s, v))


class Calculator:
    def __init__(self):
        self.img = None
        self.draw = None

        self.iterations = 1000

        self.const1 = 0
        self.last_const1 = self.const1
        self.const2 = 0
        self.last_const2 = self.const2

    def random_consts(self):
        self.last_const1 = self.const1
        self.last_const2 = self.const2

        self.const1 = random.randint(self.const1 - 100, self.const1 + 100)
        while self.const1 == 0 or self.const1 == self.last_const1:
            self.const1 = random.randint(self.const1 - 100, self.const1 + 100)

        self.const2 = random.randint(self.const2 - 100, self.const2 + 100)
        while self.const2 == 0 or self.const2 == self.last_const2 or self.const2 == abs(self.const1):
            self.const2 = random.randint(self.const2 - 100, self.const2 + 100)

    def old_consts(self):
        self.const1 = self.last_const1
        self.const2 = self.last_const2

    def x(self, t):
        return int(150 * (math.cos(t * self.const1) + math.sin(t * self.const2)))

    def y(self, t):
        return int(150 * (math.sin(t * self.const1) + math.cos(t * self.const2)))

    def calc_bounds(self):
        min_x = 0
        max_x = 0
        min_y = 0
        max_y = 0

        for i in range(self.iterations):
            if self.x(i) < min_x:
                min_x = self.x(i)
            if self.x(i) > max_x:
                max_x = self.x(i)
            if self.y(i) < min_y:
                min_y = self.y(i)
            if self.y(i) > max_y:
                max_y = self.y(i)

        size = (int(max_x - min_x) + 5, int(max_y - min_y) + 5)
        start = (-int(min_x), -int(min_y))

        return size, start

    def graph(self, color_mode='Rainbow'):
        if self.const1 == 0 and self.const2 == 0:
            size = (600, 650)

            self.img = Image.new('RGB', size, 'Black')

            return self.img, size
        else:
            size, start = self.calc_bounds()

            if color_mode == 'Black':
                self.img = Image.new('RGB', size, 'White')
            else:
                self.img = Image.new('RGB', size, 'Black')
            self.draw = ImageDraw.Draw(self.img)

            for t in range(self.iterations):
                color_fraction = t / self.iterations
                if color_mode == 'Red':
                    color = (int(color_fraction * 255), 0, 0)
                elif color_mode == 'Green':
                    color = (0, int(color_fraction * 255), 0)
                elif color_mode == 'Blue':
                    color = (0, 0, int(color_fraction * 255))
                elif color_mode == 'White':
                    color = (int(color_fraction * 255), int(color_fraction * 255), int(color_fraction * 255))
                elif color_mode == 'Black':
                    color = (0, 0, 0)
                else:
                    color = hsv2rgb(color_fraction, 1, 1)

                self.draw.point((start[0] + self.x(t), start[1] + self.y(t)), fill=color)

            return self.img, size
