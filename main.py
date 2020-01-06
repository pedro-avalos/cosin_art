from lib.app.app import App

import tkinter as tk

# Main entry point of the program
if __name__ == '__main__':
    # Color to be used by the bottom 'menu' bar
    menu_color = '#101030'

    # The root is the tkinter interface used to make the app
    root = tk.Tk()
    # The background color of the entire app should be the menu color
    root.config(bg=menu_color)
    # In order to avoid breaking the layout/appearance of the buttons
    # the app is not allowed to be smaller than 600 by 650 pixels
    root.minsize(600, 650)
    # This is the text shown in the title bar
    root.title("CoSin Art")

    # Create the app using the tkinter interface and the menu color
    app = App(root, menu_color)

    # Keep the app running
    root.mainloop()
