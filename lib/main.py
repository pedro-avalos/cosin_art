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
                else:
                    color = hsv2rgb(color_fraction, 1, 1)

                self.draw.point((start[0] + self.x(t), start[1] + self.y(t)), fill=color)

            return self.img, size


class App:
    def __init__(self, master, menu_color='Black'):
        self.master = master

        self.calculator = Calculator()

        self.pil_image = None
        self.image = None

        self.canvas = tk.Canvas(self.master, background='Black', highlightthickness=1)
        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.menu_color = menu_color

        self.butt_frame_1 = tk.Frame(self.master, background=self.menu_color)
        self.butt_frame_1.pack(side=tk.LEFT, fill=tk.BOTH)
        self.spacer_1 = tk.Frame(self.master, bg=self.menu_color)
        self.spacer_1.config(width=20, highlightbackground=self.menu_color, highlightcolor=self.menu_color)
        self.spacer_1.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5)
        self.graph_options_frame = tk.Frame(self.master, background=self.menu_color)
        self.graph_options_frame.pack(side=tk.LEFT, fill=tk.BOTH)
        self.spacer_2 = tk.Frame(self.master, bg=self.menu_color)
        self.spacer_2.config(width=25, bg=self.menu_color, highlightbackground=self.menu_color, highlightcolor=self.menu_color)
        self.spacer_2.pack(side=tk.LEFT, fill=tk.BOTH)
        self.butt_frame_2 = tk.Frame(self.master, background=self.menu_color)
        self.butt_frame_2.pack(side=tk.LEFT, fill=tk.BOTH)

        self.save_button = tk.Button(self.butt_frame_1, text='Save', command=self.save)
        self.save_button.config(bg=self.menu_color, bd=2, fg='White')
        self.save_button.pack(side=tk.LEFT, fill=tk.BOTH)

        self.back_button = tk.Button(self.butt_frame_1, text='Back', command=lambda: self.display('back'))
        self.back_button.config(bg=self.menu_color, bd=2, fg='White')
        self.back_button.pack(side=tk.LEFT, fill=tk.BOTH)

        self.entry_text1 = tk.StringVar()
        self.entry_text2 = tk.StringVar()

        self.entry_text1.set('0')
        self.entry_text2.set('0')

        self.const1_label = tk.Label(self.graph_options_frame, text='a = ')
        self.const1_label.config(bg=self.menu_color, bd=2, fg='White')
        self.const1_label.pack(side=tk.LEFT)

        self.const1_entry = tk.Entry(self.graph_options_frame, textvariable=self.entry_text1)
        self.const1_entry.config(bg='Black', bd=2, fg='White')
        self.const1_entry.pack(side=tk.LEFT, fill=tk.BOTH)

        self.const2_label = tk.Label(self.graph_options_frame, text='b = ')
        self.const2_label.config(bg=self.menu_color, bd=2, fg='White')
        self.const2_label.pack(side=tk.LEFT)

        self.const2_entry = tk.Entry(self.graph_options_frame, textvariable=self.entry_text2)
        self.const2_entry.config(bg='Black', bd=2, fg='White')
        self.const2_entry.pack(side=tk.LEFT, fill=tk.BOTH)

        self.color_options = ['Rainbow', 'Red', 'Green', 'Blue', 'White']

        self.color_variable = tk.StringVar()
        self.color_variable.set(self.color_options[0])

        self.color_menu = tk.OptionMenu(self.graph_options_frame, self.color_variable, *self.color_options)
        self.color_menu.config(bg=self.menu_color, bd=2, fg='White', highlightthickness=0)
        self.color_menu['menu'].config(bg=self.menu_color, fg='White')
        self.color_menu.pack(side=tk.LEFT, fill=tk.BOTH)

        self.set_button = tk.Button(self.butt_frame_2, text='Set', command=lambda: self.display('set'))
        self.set_button.config(bg=self.menu_color, bd=2, fg='White')
        self.set_button.pack(side=tk.LEFT, fill=tk.BOTH)

        self.new_button = tk.Button(self.butt_frame_2, text='Random', command=lambda: self.display('random'))
        self.new_button.config(bg=self.menu_color, bd=2, fg='White')
        self.new_button.pack(side=tk.LEFT, fill=tk.BOTH)

    def display(self, event='random'):
        if event == 'random':
            self.calculator.random_consts()
        elif event == 'back':
            self.calculator.old_consts()
        else:
            self.calculator.const1 = int(self.entry_text1.get())
            self.calculator.const2 = int(self.entry_text2.get())

        self.pil_image, size = self.calculator.graph(self.color_variable.get())
        if self.image is not None:
            self.canvas.delete(self.image)
        self.image = ImageTk.PhotoImage(self.pil_image)
        self.canvas.create_image(size[0]/2, size[1]/2, image=self.image)

        self.entry_text1.set(self.calculator.const1)
        self.entry_text2.set(self.calculator.const2)

        root.geometry("%dx%d" % (size[0], size[1]+65))

    def save(self):
        if self.calculator.const1 != 0 and self.calculator.const2 != 0:
            const1 = self.calculator.const1
            const2 = self.calculator.const2

            self.pil_image.save(f'../data/image_a{const1}_b{const2}.bmp')
        else:
            pass


if __name__ == '__main__':
    option_color = '#101030'
    root = tk.Tk()
    root.config(bg=option_color)
    root.minsize(600, 650)
    root.title("SinCos Art")
    app = App(root, option_color)
    root.mainloop()
