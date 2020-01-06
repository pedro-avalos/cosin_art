from lib.calculator.calculator import Calculator

import os
import sys
import tkinter as tk
from PIL import ImageTk

# Tuple of the available color modes
COLOR_OPTIONS = (
    'Rainbow',
    'Red',
    'Green',
    'Blue',
    'Yellow',
    'Orange',
    'Purple',
    'Cyan',
    'Pink',
    'White',
    'Black'
)

# Directory to save the images at (data folder)
SAVE_DIR = f'{os.path.dirname(sys.argv[0])}/data/'


# App class that handles the GUI
class App:
    # Initializing the instance of the class
    def __init__(self, master, menu_color='Black'):
        # Save the master tkinter interface given
        self.master = master

        # Initialize a calculator instance
        self.calculator = Calculator()

        # Pillow image given by the calculator (a bitmap, not usable by the canvas)
        self.pil_image = None
        # Image displayed on the app's canvas (usable by tkinter's canvas)
        self.image = None

        # Canvas that displays the graph
        self.canvas = tk.Canvas(self.master)
        # The background color is black by default
        # There is a small outline around it to distinguish it from the rest of the GUI
        self.canvas.config(background='Black', highlightthickness=1)
        # Place this at the top of the app, and it expands and fills the app as it is resized
        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Save the color of the menu bar at the bottom
        self.menu_color = menu_color

        # Frame to hold the left-most buttons (Save and Back)
        self.butt_frame_1 = tk.Frame(self.master)
        # The background color is the menu color
        self.butt_frame_1.config(background=self.menu_color)
        # This is at the left-most side of the screen (and below the canvas as the canvas is at the top)
        # This also expands and fills up the app as it is resized
        self.butt_frame_1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Frame to add a space between the butt_frame1 and graph_options_frame
        self.spacer_1 = tk.Frame(self.master)
        # The background and highlight colors are the menu color
        self.spacer_1.config(bg=self.menu_color, highlightbackground=self.menu_color, highlightcolor=self.menu_color)
        # This is packed leftward (right of the butt_frame_1) with padding to be a spacer
        # This also expands and fills up the app as it is resized
        self.spacer_1.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5, expand=True)
        
        # Frame to hold the a and b text boxes and the color mode
        self.graph_options_frame = tk.Frame(self.master)
        # The background color is the menu color
        self.graph_options_frame.config(background=self.menu_color)
        # This is packed leftward (right of the spacer_1)
        # This also expands and fills up the app as it is resized
        self.graph_options_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Frame to add a space between the graph_options_frame and butt_frame_2
        self.spacer_2 = tk.Frame(self.master)
        # The background and highlight colors are the menu color
        self.spacer_2.config(bg=self.menu_color, highlightbackground=self.menu_color, highlightcolor=self.menu_color)
        # This is packed leftward (right of the graph_options_frame) with padding to be a spacer
        # This also expands and fills up the app as it is resized
        self.spacer_2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Frame to hold the right-most buttons (Set and Random)
        self.butt_frame_2 = tk.Frame(self.master)
        # The background color is the menu color
        self.butt_frame_2.config(background=self.menu_color)
        # This is packed leftward (right of the spacer_2)
        # This also expands and fills up the app as it is resized
        self.butt_frame_2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Button to save the image
        self.save_button = tk.Button(self.butt_frame_1, text='Save', command=self.save)
        # The background color is the menu color, and the foreground is white
        # It also has a small border (2 pixels)
        self.save_button.config(bg=self.menu_color, fg='White', bd=2)
        # Pack this leftward
        # This also fills up the x and y space available
        self.save_button.pack(side=tk.LEFT, fill=tk.BOTH)

        # Button to go back to the last used const_1 and const_2
        self.back_button = tk.Button(self.butt_frame_1, text='Back', command=lambda: self.display('back'))
        # The background color is the menu color and the foreground is white
        # It also has a small border (2 pixels)
        self.back_button.config(bg=self.menu_color, fg='White', bd=2)
        # Pack this leftward
        # This also fills up the x and y space available
        self.back_button.pack(side=tk.LEFT, fill=tk.BOTH)

        # Variable to display and save const_1
        self.entry_text_1 = tk.StringVar()
        # Variable to display and save const_2
        self.entry_text_2 = tk.StringVar()

        # By default set them as 0
        self.entry_text_1.set('0')
        self.entry_text_2.set('0')

        # Label to display "a = " before the text box
        self.const_1_label = tk.Label(self.graph_options_frame, text='a = ')
        # The background color is the menu color and the foreground is white
        # It also has a small border (2 pixels)
        self.const_1_label.config(bg=self.menu_color, fg='White', bd=2)
        # Pack this leftward
        # This also fills up the x and y space available
        self.const_1_label.pack(side=tk.LEFT, fill=tk.BOTH)

        # Text box (called entry in tkinter) for the value of const_1
        self.const_1_entry = tk.Entry(self.graph_options_frame, textvariable=self.entry_text_1)
        # The background is black and the foreground color is white
        # It also has a small border (2 pixels)
        self.const_1_entry.config(bg='Black', fg='White', bd=2)
        # Pack this leftward
        # This also fills up the x and y space available
        self.const_1_entry.pack(side=tk.LEFT, fill=tk.BOTH)

        # Label to display "b = " before the text box
        self.const_2_label = tk.Label(self.graph_options_frame, text='b = ')
        # The background color is the menu color and the foreground is white
        # It also has a small border (2 pixels)
        self.const_2_label.config(bg=self.menu_color, fg='White', bd=2)
        # Pack this leftward
        # This also fills up the x and y space available
        self.const_2_label.pack(side=tk.LEFT, fill=tk.BOTH)

        # Text box (called entry in tkinter) for the value of const_2
        self.const_2_entry = tk.Entry(self.graph_options_frame, textvariable=self.entry_text_2)
        # The background is black and the foreground color is white
        # It also has a small border (2 pixels)
        self.const_2_entry.config(bg='Black', fg='White', bd=2)
        # Pack this leftward
        # This also fills up the x and y space available
        self.const_2_entry.pack(side=tk.LEFT, fill=tk.BOTH)

        # Selected color mode
        self.color_mode = tk.StringVar()
        # By default it is the first in the tuple (rainbow)
        self.color_mode.set(COLOR_OPTIONS[0])

        # Dropdown menu (called option menu in tkinter) for the color mode
        self.color_menu = tk.OptionMenu(self.graph_options_frame, self.color_mode, *COLOR_OPTIONS)
        # The background is the menu color and the foreground is white
        # It also has a small border (2 pixels)
        # The option menu has a highlight by default, but this is set to 0 to make it look more like a button
        self.color_menu.config(bg=self.menu_color, fg='White', bd=2, highlightthickness=0)
        # The background color of the menu that drops down is the menu color and the foreground is white
        self.color_menu['menu'].config(bg=self.menu_color, fg='White')
        # Pack this leftward
        # This also fills up the x and y space available
        self.color_menu.pack(side=tk.LEFT, fill=tk.BOTH)

        # Button to randomize the values of const_1 and const_2
        self.rand_button = tk.Button(self.butt_frame_2, text='Random', command=lambda: self.display('random'))
        # The background color is the menu color and the foreground is white
        # It also has a small border (2 pixels)
        self.rand_button.config(bg=self.menu_color, fg='White', bd=2)
        # Pack this rightward (Right-most button)
        # This also fills up the x and y space available
        self.rand_button.pack(side=tk.RIGHT, fill=tk.BOTH)

        # Button to set the values to the ones in the text boxes
        self.set_button = tk.Button(self.butt_frame_2, text='Set', command=lambda: self.display('set'))
        # The background color is the menu color and the foreground is white
        # It also has a small border (2 pixels)
        self.set_button.config(bg=self.menu_color, fg='White', bd=2)
        # Pack this rightward (Left of rand_button)
        # This also fills up the x and y space available
        self.set_button.pack(side=tk.RIGHT, fill=tk.BOTH)

    # Method to display the image with a given 'event' (random integers or set ones from the text boxes)
    def display(self, event='random'):
        # If the event is random, then randomize new integers
        if event == 'random':
            self.calculator.random_consts()
        # If the event is back, then revert to the old integers
        elif event == 'back':
            self.calculator.old_consts()
        # Otherwise, it is set
        # Get the values from the text boxes and use those for the const_1 and const_2 in the calculator instance
        else:
            self.calculator.const_1 = int(self.entry_text_1.get())
            self.calculator.const_2 = int(self.entry_text_2.get())

        # The Pillow image and size are retrieved from the calculator graph (which is given the selected color mode)
        self.pil_image, size = self.calculator.graph(self.color_mode.get())
        # If there was a previous image, then delete it
        if self.image is not None:
            self.canvas.delete(self.image)
        # Create the new image using the Pillow image
        self.image = ImageTk.PhotoImage(self.pil_image)
        # Put the image on the canvas
        self.canvas.create_image(size[0]/2, size[1]/2, image=self.image)
        # Change the background color of the canvas to white if the selected color mode is black
        if self.color_mode.get() == 'Black':
            self.canvas.config(background='White')
        # Otherwise, set it to black
        else:
            self.canvas.config(background='Black')

        # Set the const_1 and const_2 text variables to the new integers
        self.entry_text_1.set(self.calculator.const_1)
        self.entry_text_2.set(self.calculator.const_2)

        # Resize the tkinter interface to fit the entire image
        self.master.geometry("%dx%d" % (size[0], size[1]+65))

    # Method to save the image
    def save(self):
        # Check if the Pillow image exists to avoid saving a non-existent image
        if self.pil_image is not None:
            # Retrieve the values for const_1 and const_2
            const_1 = self.calculator.const_1
            const_2 = self.calculator.const_2

            # Check if directory where images are saved doesn't exist
            if not os.path.exists(SAVE_DIR):
                # If it doesn't exist, then create it
                os.makedirs(SAVE_DIR)

            # Save the Pillow image
            self.pil_image.save(f'{SAVE_DIR}{self.color_mode.get()}_a{const_1}_b{const_2}.bmp')
