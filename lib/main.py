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

    def reset(self):
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
        while self.const2 == 0 or self.const2 == self.last_const2:
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

        size = (int(max_x - min_x) + 5, int(max_y - min_y) + 5)
        start = (-int(min_x), -int(min_y))

        return size, start

    def graph(self):
        if self.const1 == 0 and self.const2 == 0:
            size = (400, 400)

            self.img = Image.new('RGB', size, 'Black')

            return self.img, size
        else:
            size, start = self.calc_bounds()

            self.img = Image.new('RGB', size, 'Black')
            self.draw = ImageDraw.Draw(self.img)

            for t in range(self.iterations):
                color = hsv2rgb(t / self.iterations, 1, 1)
                self.draw.point((start[0] + self.x(t), start[1] + self.y(t)), fill=color)

            return self.img, size


class App:
    def __init__(self, master):
        self.master = master

        self.calculator = Calculator()

        self.pil_image = None
        self.image = None

        self.canvas = tk.Canvas(self.master, background='Black')
        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.butt_frame = tk.Frame(self.master)
        self.butt_frame.pack(side=tk.LEFT, fill=tk.BOTH)
        self.const_frame = tk.Frame(self.master)
        self.const_frame.pack(side=tk.RIGHT, fill=tk.BOTH)

        self.back_button = tk.Button(self.butt_frame, text='Back', command=lambda: self.display('back'))
        self.back_button.pack(side=tk.LEFT, fill=tk.BOTH)
        self.new_button = tk.Button(self.butt_frame, text='Random', command=lambda: self.display('random'))
        self.new_button.pack(side=tk.RIGHT, fill=tk.BOTH)
        self.save_button = tk.Button(self.butt_frame, text='Save', command=self.save)
        self.save_button.pack(side=tk.LEFT, fill=tk.BOTH)
        self.reset_button = tk.Button(self.butt_frame, text='Reset', command=self.reset)
        self.reset_button.pack(side=tk.RIGHT, fill=tk.BOTH)

        self.entry_text1 = tk.StringVar()
        self.entry_text2 = tk.StringVar()

        self.entry_text1.set('0')
        self.entry_text2.set('0')

        self.set_button = tk.Button(self.const_frame, text='Set', command=lambda: self.display('set'))
        self.set_button.pack(side=tk.BOTTOM, fill=tk.BOTH)

        self.const1_label = tk.Label(self.const_frame, text='a = ')
        self.const1_label.pack(side=tk.LEFT)

        self.const1_entry = tk.Entry(self.const_frame, textvariable=self.entry_text1)
        self.const1_entry.pack(side=tk.RIGHT, fill=tk.BOTH)

        self.const2_label = tk.Label(self.const_frame, text='b = ')
        self.const2_label.pack(side=tk.RIGHT)

        self.const2_entry = tk.Entry(self.const_frame, textvariable=self.entry_text2)
        self.const2_entry.pack(side=tk.LEFT, fill=tk.BOTH)

    def display(self, event='random'):
        if event == 'random':
            self.calculator.random_consts()
        elif event == 'back':
            self.calculator.old_consts()
        else:
            self.calculator.const1 = int(self.entry_text1.get())
            self.calculator.const2 = int(self.entry_text2.get())

        self.pil_image, size = self.calculator.graph()
        if self.image is not None:
            self.canvas.delete(self.image)
        self.image = ImageTk.PhotoImage(self.pil_image)
        self.canvas.create_image(size[0]/2, size[1]/2, image=self.image)

        self.entry_text1.set(self.calculator.const1)
        self.entry_text2.set(self.calculator.const2)

        root.geometry("%dx%d" % (size[0], size[1]+50))

    def save(self):
        const1 = self.calculator.const1
        const2 = self.calculator.const2
        self.pil_image.save(f'../data/image_a{const1}_b{const2}.bmp')

    def reset(self):
        self.calculator.reset()
        self.pil_image, size = self.calculator.graph()
        if self.image is not None:
            self.canvas.delete(self.image)
        self.image = ImageTk.PhotoImage(self.pil_image)
        self.canvas.create_image(size[0] / 2, size[1] / 2, image=self.image)

        self.entry_text1.set(self.calculator.const1)
        self.entry_text2.set(self.calculator.const2)

        root.geometry("%dx%d" % (size[0], size[1]+50))


if __name__ == '__main__':
    root = tk.Tk()
    root.title("SinCos Art")
    app = App(root)
    root.mainloop()
