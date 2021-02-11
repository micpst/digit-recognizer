import os
import numpy as np
import tkinter as tk
import matplotlib.pyplot as plt

from PIL import Image, ImageTk
from mpl_toolkits.axes_grid1 import ImageGrid
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Prediction(tk.Frame):
    def __init__(self, parent=None, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        
        figure = plt.Figure(figsize=(1,1))
        ax = figure.add_subplot(111)

        self.chart = FigureCanvasTkAgg(figure, self)
        self.chart.get_tk_widget().pack(fill="both", expand=1)
        ax.set_title("Predictions")

class Input(tk.Frame):
    def __init__(self, parent=None, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        figure = plt.Figure(figsize=(1,1))
        ax = figure.add_subplot(111)

        self.chart = FigureCanvasTkAgg(figure, self)
        self.chart.get_tk_widget().pack(fill="both", expand=1)

        ax.imshow(np.arange(784).reshape((28, 28)))
        ax.set_title("Input image 28x28")
        ax.axis("off")

class Toolbar(tk.Frame):
    def __init__(self, parent=None, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.parent = parent
        self.load_assets()

        self.pen_button = tk.Button(self, image=self.img_brush, bg="white", activebackground="white", relief="flat", border=0)
        self.eraser_button = tk.Button(self, image=self.img_eraser, bg="white", activebackground="white", relief="flat", border=0)
        self.clear_button = tk.Button(self, image=self.img_delete, bg="white", activebackground="white", relief="flat", border=0)
        self.resize_button = tk.Button(self, image=self.img_resize, bg="white", activebackground="white", relief="flat", border=0)
        self.select_button = tk.Button(self, image=self.img_select, bg="white", activebackground="white", relief="flat", border=0)
        
        self.pen_button.grid(row=0, column=0, padx=10, pady=10)
        self.eraser_button.grid(row=0, column=1, padx=10, pady=10)
        self.clear_button.grid(row=0, column=3, padx=10, pady=10)
        self.resize_button.grid(row=0, column=4, padx=10, pady=10)
        self.select_button.grid(row=0, column=5, padx=10, pady=10)

    def load_assets(self):
        self.img_brush = ImageTk.PhotoImage(Image.open(os.path.join("assets", "brush.png")))
        self.img_eraser = ImageTk.PhotoImage(Image.open(os.path.join("assets", "eraser.png")))
        self.img_delete = ImageTk.PhotoImage(Image.open(os.path.join("assets", "delete.png")))
        self.img_resize = ImageTk.PhotoImage(Image.open(os.path.join("assets", "resize.png")))
        self.img_select = ImageTk.PhotoImage(Image.open(os.path.join("assets", "select.png")))

class Paint(tk.Canvas):
    def __init__(self, parent=None, *args, **kwargs):
        tk.Canvas.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.rowconfigure([0,1,2,3,4,5,6,7,8,9], weight=1)  
        self.columnconfigure([0,1,2], weight=1)

        self.toolbar_component = Toolbar(self, bg="white", bd=2, relief="raised")  
        self.toolbar_component.grid(row=9, column=1)

class Guesser(tk.Tk):
    def __init__(self, width, height, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.configure(bg="white")
        self.rowconfigure([0, 1], weight=1)  
        self.columnconfigure([0, 1, 2], weight=1)

        self.paint_component = Paint(self, bg="white", bd=2, relief="raised", highlightthickness=0)  
        self.input_component = Input(self, bg="white", bd=2, relief="raised") 
        self.prediction_component = Prediction(self, bg="white", bd=2, relief="raised") 

        self.paint_component.grid(rowspan=2, columnspan=2, sticky="nwse", padx=10, pady=10)
        self.input_component.grid(row=0, column=2, sticky="nwse", padx=(0,10), pady=(10,5))
        self.prediction_component.grid(row=1, column=2, sticky="nwse", padx=(0,10), pady=(5,10))

        self.geometry(f"{width}x{height}")
        self.minsize(width=width, height=height)
        self.iconphoto(False, tk.PhotoImage(file=os.path.join("assets", "icon.png")))
        self.title("Number quesser")
        self.mainloop()

if __name__ == '__main__': 
    Guesser(1000, 500)