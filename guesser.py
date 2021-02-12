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
        self.select_button = tk.Button(self, image=self.img_select, bg="white", activebackground="white", relief="flat", border=0)
        
        self.pen_button.grid(row=0, column=0, padx=10, pady=10)
        self.eraser_button.grid(row=0, column=1, padx=10, pady=10)
        self.clear_button.grid(row=0, column=3, padx=10, pady=10)
        self.select_button.grid(row=0, column=4, padx=10, pady=10)

        self.clear_button.bind("<Button-1>", self.parent.handle_on_clear)

    def load_assets(self):
        self.img_brush = ImageTk.PhotoImage(Image.open(os.path.join("assets", "brush.png")))
        self.img_eraser = ImageTk.PhotoImage(Image.open(os.path.join("assets", "eraser.png")))
        self.img_delete = ImageTk.PhotoImage(Image.open(os.path.join("assets", "delete.png")))
        self.img_select = ImageTk.PhotoImage(Image.open(os.path.join("assets", "select.png")))

class Paint(tk.Canvas):
    def __init__(self, parent=None, *args, **kwargs):
        tk.Canvas.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.width = self.winfo_reqwidth()
        self.height = self.winfo_reqheight()

        self.rowconfigure([0,1,2,3,4,5,6,7,8,9], weight=1)  
        self.columnconfigure([0,1,2], weight=1)

        self.toolbar_component = Toolbar(self, bg="white", bd=2, relief="raised")  
        self.toolbar_component.grid(row=9, column=1)

        self.x = None
        self.y = None
        self.color = "black"
        self.thickness = 5

        self.bind("<Configure>", self.handle_on_resize)
        self.bind("<Button-1>", self.handle_on_click)
        self.bind("<B1-Motion>", self.handle_on_motion)
        self.bind("<ButtonRelease-1>", self.handle_on_release)

    def handle_on_resize(self, e):
        wscale = float(e.width) / self.width
        hscale = float(e.height) / self.height

        self.width = e.width
        self.height = e.height
        
        self.scale("all", 0, 0, wscale, hscale)

    def handle_on_click(self, e):
        self.x = e.x
        self.y = e.y
        
        x1, y1 = (self.x - self.thickness/2), (self.y - self.thickness/2)
        x2, y2 = (self.x + self.thickness/2), (self.y + self.thickness/2)

        self.create_oval(x1, y1, x2, y2, fill=self.color)
        
    def handle_on_motion(self, e):
        if self.x and self.y:
            self.create_line(self.x, self.y, e.x, e.y, 
                             width=self.thickness, 
                             fill=self.color, 
                             capstyle="round", 
                             smooth=1, 
                             splinesteps=36)
        self.x = e.x
        self.y = e.y

    def handle_on_release(self, e):
        self.x = None
        self.y = None

    def handle_on_clear(self, e):
        self.delete("all")

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

if __name__ == "__main__": 
    Guesser(1000, 500)