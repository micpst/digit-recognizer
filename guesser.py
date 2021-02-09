import numpy as np
import tkinter as tk
import matplotlib.pyplot as plt

from mpl_toolkits.axes_grid1 import ImageGrid
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Prediction(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.parent = parent
        self.label = tk.LabelFrame(self, text="Prediction")
        self.label.pack(fill="both", expand=1)

        figure = plt.Figure(figsize=(1,1))
        ax = figure.add_subplot(111)

        chart = FigureCanvasTkAgg(figure, self.label)
        chart.get_tk_widget().pack(fill="both", expand=1)

class Input(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.parent = parent
        self.label = tk.LabelFrame(self, text="Input")
        self.label.pack(fill="both", expand=1)

        figure = plt.Figure(figsize=(1,1))
        
        chart = FigureCanvasTkAgg(figure, self.label)
        chart.get_tk_widget().pack(fill="both", expand=1)

        ax = figure.add_subplot(111)
        ax.imshow(np.arange(784).reshape((28, 28)))      
        ax.axis("off")

class Toolbar(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.pen_button = tk.Button(self, text="pen")
        self.eraser_button = tk.Button(self, text="eraser")
        self.predict_button = tk.Button(self, text="predict")
        self.clear_button = tk.Button(self, text="clear")
        self.resolution_button = tk.Button(self, text="res")
        
        self.pen_button.grid(row=0, column=0)
        self.eraser_button.grid(row=0, column=1)
        self.predict_button.grid(row=0, column=2)
        self.clear_button.grid(row=0, column=3)
        self.resolution_button.grid(row=0, column=4)

class Paint(tk.Canvas):
     def __init__(self, parent, *args, **kwargs):
        tk.Canvas.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.rowconfigure([0,1,2,3,4,5,6,7,8,9], weight=1)  
        self.columnconfigure(1, weight=1)

        self.toolbar_component = Toolbar(self)  
        self.toolbar_component.grid(row=9, column=1)

class Guesser(tk.Tk):
    def __init__(self, width, height, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.rowconfigure([0, 1], weight=1)  
        self.columnconfigure([0, 1, 2], weight=1)

        self.paint_component = Paint(self, bg="white")  
        self.input_component = Input(self) 
        self.prediction_component = Prediction(self) 

        self.paint_component.grid(rowspan=2, columnspan=2, sticky="nwse")
        self.input_component.grid(row=0, column=2, sticky="nwse")
        self.prediction_component.grid(row=1, column=2, sticky="nwse")

        self.geometry(f"{width}x{height}")
        self.minsize(width=width, height=height)
        self.title("Number quesser")
        self.mainloop()

if __name__ == '__main__': 
    Guesser(1200, 700)