import tkinter as tk

from lib.app.app import App

if __name__ == '__main__':
    menu_color = '#101030'
    root = tk.Tk()
    root.config(bg=menu_color)
    root.minsize(600, 650)
    root.title("SinCos Art")
    app = App(root, menu_color)
    root.mainloop()
