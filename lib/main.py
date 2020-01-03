import colorsys
import math
import random
import tkinter as tk
from PIL import Image, ImageDraw, ImageTk


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

    def new_consts(self):
        self.last_const1 = self.const1
        self.last_const2 = self.const2
        self.const1 = random.randint(self.const1 - 100, self.const1 + 100)
        self.const2 = random.randint(self.const2 - 100, self.const2 + 100)

    def old_consts(self):
        self.const1 = self.last_const1
        self.const2 = self.last_const2

    def x(self, t):
        return int(100 * (math.cos(t * self.const1) + math.sin(t * self.const2)))

    def y(self, t):
        return int(100 * (math.sin(t * self.const1) + math.cos(t * self.const2)))

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
        size = (int(max_x - min_x) + 1, int(max_y - min_y) + 1)
        start = (-int(min_x), -int(min_y))
        return size, start

    def graph(self):
        size, start = self.calc_bounds()
        self.img = Image.new('RGB', size, 'Black')
        self.draw = ImageDraw.Draw(self.img)

        for t in range(self.iterations):
            color = hsv2rgb(t / self.iterations, 1, 1)
            self.draw.point((start[0] + self.x(t), start[1] + self.y(t)), fill=color)

        self.img.save('../data/image.bmp')
        return self.img, size


class App:
    def __init__(self, master):
        self.master = master
        self.canvas = tk.Canvas(self.master)
        self.canvas.pack(fill=tk.BOTH, expand = True)
        self.image = None
        self.butt_frame = tk.Frame(self.master)
        self.butt_frame.pack()
        self.back_button = tk.Button(self.butt_frame, text='Back', command=lambda: self.display("back"))
        self.back_button.pack(side=tk.LEFT)
        self.new_button = tk.Button(self.butt_frame, text='New', command=lambda: self.display("new"))
        self.new_button.pack(side=tk.RIGHT)
        self.calculator = Calculator()

    def display(self, event="new"):
        self.calculator.new_consts() if event == "new" else self.calculator.old_consts()
        pil_image, size = self.calculator.graph()
        if self.image is not None:
            self.canvas.delete(self.image)
        self.image = ImageTk.PhotoImage(pil_image)
        self.canvas.create_image(size[0]/2, size[1]/2, image=self.image)
        
        root.geometry("%dx%d" % (size[0]+30, size[1]+30))


if __name__ == '__main__':
    root = tk.Tk()
    root.title("SinCos Art")
    app = App(root)
    root.mainloop()
