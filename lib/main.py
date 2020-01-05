from lib.app.app import App

import tkinter as tk


if __name__ == '__main__':
    # Color to be used by the bottom 'menu' bar
    menu_color = '#101030'

    root = tk.Tk()
    root.config(bg=menu_color)
    root.minsize(600, 650)
    root.title("SinCos Art")

    app = App(root, menu_color)

    root.mainloop()
