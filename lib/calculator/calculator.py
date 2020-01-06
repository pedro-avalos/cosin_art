import colorsys
import math
import random
from PIL import Image, ImageDraw


# Function to convert hsv (hue, saturation, value) values to an rgb (red, green, blue) tuple
def hsv2rgb(h, s, v):
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h, s, v))


# Calculator class that does all the mathematical operations and graphing
class Calculator:
    # Initializing the instance of the class
    def __init__(self):
        # Image to draw on, not defined until needed
        self.img = None
        # Drawing object used to paint dots on the image
        self.draw = None

        # How many times to iterate through the equations to plot points
        # 0 <= t <= iterations
        self.iterations = 1000

        # The coordinates of the points to be plotted
        self.points = []

        # Also referred to as 'a' on the documentation
        # This is the first integer that is used in the equations
        self.const_1 = 0
        # This is the value of const_1 that was last used
        self.last_const_1 = self.const_1
        # Also referred to as 'b' on the documentation
        # This is the second integer that is used in the equations
        self.const_2 = 0
        # This is the value of const_2 that was last used
        self.last_const_2 = self.const_2

    # Method to create new, random integers
    def random_consts(self):
        # Save the last value of const_1 and const_2
        self.last_const_1 = self.const_1
        self.last_const_2 = self.const_2

        # Set const_1 to a new, random integer ranging from const_1-100 to const_1+100
        self.const_1 = random.randint(self.const_1 - 100, self.const_1 + 100)
        # Continue randomizing it if const_2 is 0 to avoid making a circle
        while self.const_1 == 0 or self.const_1 == self.last_const_1:
            self.const_1 = random.randint(self.const_1 - 100, self.const_1 + 100)

        # Set const_2 to a new, random integer ranging from const_2-100 to const_2+100
        self.const_2 = random.randint(self.const_2 - 100, self.const_2 + 100)
        # Continue randomizing it if const_2 is 0 to avoid making a circle
        # Continue randomizing it if const_2 is the same as const_1 to avoid making a line
        while self.const_2 == 0 or self.const_2 == abs(self.const_1):
            self.const_2 = random.randint(self.const_2 - 100, self.const_2 + 100)

        # Randomize them again if both const_1 and const_2 are the same as last_const_1 and last_const_2
        while self.const_1 == self.last_const_1 and self.const_2 == self.last_const_2:
            self.const_1 = random.randint(self.const_1 - 100, self.const_1 + 100)
            self.const_2 = random.randint(self.const_2 - 100, self.const_2 + 100)

    # Method to reset the values of the integers to the last integers used
    def old_consts(self):
        self.const_1 = self.last_const_1
        self.const_2 = self.last_const_2

    # Parametric equation of x(t)
    def x(self, t):
        return int(150 * (math.cos(t * self.const_1) + math.sin(t * self.const_2)))

    # Parametric equation of y(t)
    def y(self, t):
        return int(150 * (math.sin(t * self.const_1) + math.cos(t * self.const_2)))

    # Method to find the size needed for the bitmap image
    # It also finds the necessary starting point for the drawing object
    # This also saves the coordinates of the points to avoid iterating through the equations twice
    def calc_bounds(self):
        # Minimum and maximum values of x and y
        # Used to find the width and height of the image
        # The minimums are also used to find the starting point
        min_x = 0
        max_x = 0
        min_y = 0
        max_y = 0

        # Reset the coordinates of the points
        self.points = []

        # Iterate through the parametric equations
        for t in range(self.iterations):
            # Save the coordinates of the current point
            self.points.append((self.x(t), self.y(t)))

            # If the x coordinate is the smallest it's ever been, save it as the minimum x
            if self.points[t][0] < min_x:
                min_x = self.points[t][0]
            # If the x coordinate is the largest it's ever been, save it as the maximum x
            if self.points[t][0] > max_x:
                max_x = self.points[t][0]
            # If the y coordinate is the smallest it's ever been, save it as the minimum y
            if self.points[t][1] < min_y:
                min_y = self.points[t][1]
            # If the y coordinate is the largest it's ever been, save it as the maximum y
            if self.points[t][1] > max_y:
                max_y = self.points[t][1]

        # The size of the bitmap is the maximum - minimum (which is negative) + 5 (to have a small border)
        size = (int(max_x - min_x) + 5, int(max_y - min_y) + 5)
        # Because of how bitmap coordinates work, the starting point is the negative minimum x, negative minimum y
        start = (-int(min_x), -int(min_y))

        # Return the size and start of the graph
        return size, start

    # Method to graph the equation
    def graph(self, color_mode='Rainbow'):
        # To avoid graphing a line, if the integers are 0's, then create a blank image
        if self.const_1 == 0 and self.const_2 == 0:
            # Size is the minimum allowed by the app
            size = (600, 650)

            # The image is just black
            self.img = Image.new('RGB', size, 'Black')
        else:
            # The size and start of the graph are found with the calc_bounds() method
            size, start = self.calc_bounds()

            # If the color mode is black, the background should be white
            if color_mode == 'Black':
                self.img = Image.new('RGB', size, 'White')
            # Otherwise, the background is black
            else:
                self.img = Image.new('RGB', size, 'Black')
            # The drawing object modifies the new image
            self.draw = ImageDraw.Draw(self.img)

            # Iterate through the points
            # Iterate with the index value (for the coloring)
            for i, p in enumerate(self.points):
                # This is the decimal value the current iteration divided by the total iterations to do
                # The decimal is used to determine the color value to use
                color_fraction = i / self.iterations

                # If statements to determine what color to use for the point
                # Generally, the value is larger the farther the iteration is
                if color_mode == 'Red':
                    color = hsv2rgb(0, 1, color_fraction)
                elif color_mode == 'Green':
                    color = hsv2rgb(0.33, 1, color_fraction)
                elif color_mode == 'Blue':
                    color = hsv2rgb(0.66, 1, color_fraction)
                elif color_mode == 'Yellow':
                    color = hsv2rgb(0.16, 1, color_fraction)
                elif color_mode == 'Orange':
                    color = hsv2rgb(0.083, 1, color_fraction)
                elif color_mode == 'Purple':
                    color = hsv2rgb(0.83, 1, color_fraction)
                elif color_mode == 'Cyan':
                    color = hsv2rgb(0.5, 1, color_fraction)
                elif color_mode == 'Pink':
                    color = hsv2rgb(0.972, .25, color_fraction)
                elif color_mode == 'White':
                    color = hsv2rgb(0, 0, color_fraction)
                elif color_mode == 'Black':
                    # In the case of the black mode, the value is always the same
                    color = (0, 0, 0)
                else:
                    # In the case of the rainbow mode, the hue, and not the value, changes
                    color = hsv2rgb(color_fraction, 1, 1)

                # Draw the point on the image
                self.draw.point((start[0] + p[0], start[1] + p[1]), fill=color)

        # Return the image and the size of it
        return self.img, size
