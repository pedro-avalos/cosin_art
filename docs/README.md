# CoSin Art

This personal project aims to create generative art using simple parametric trigonometric equations.

## Getting Started

### Prerequisites

Python 3.x <https://www.python.org/downloads/>  
Pip (included with Python installation)  

Modules:
* os (included with Python installation)
* sys (included with Python installation)
* colorsys (included with Python installation)
* math (included with Python installation)
* random (included with Python installation)
* tkinter (included with Python installation)
* PIL: Use `py -m pip install Pillow` OR `python pip install Pillow` OR `pip install Pillow`, depending on your OS and PATH
    * Check <https://pypi.org/project/Pillow/> for more information
 
### Installation

Clone or download the .zip file of the project. Then unzip the file and run lib/main.py.  
To run it you use cmd and go to the directory using cd, then use `python main.py`.

### Usage

There are four buttons, two text boxes, and a dropdown menu.  

You can use the three main buttons to:
* Create a random art piece
* Go back to the last art piece
* Save the art piece in the 'data' folder

The dropdown menu can be used to switch between color modes for the graph.  

Additionally there are two entries / text boxes and a 'Set' button. Use these to use your own values for a (const1) and b (const2) on the text boxes. This can also be used to use the selected color mode.  
The text boxes will show the current a and b values; they update whenever the 'Random' button is pressed

#### Parametric Equations

x(t) = 100 * (cos(t * a) + sin(t * b))  
y(t) = 100 * (sin(t * a) + cos(t * b))  

You can watch an animated version here: <https://www.desmos.com/calculator/gsgupnzcfy>
