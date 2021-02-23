import os
import numpy as np
import tkinter as tk
import matplotlib.pyplot as plt

from PIL import ImageGrab
from tkinter.colorchooser import askcolor
from mpl_toolkits.axes_grid1 import ImageGrid
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Chart(tk.Frame):
    def __init__(self, master=None, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self.master = master
        
        figure = plt.Figure(figsize=(1,1))
        ax = figure.add_subplot(111)

        self.chart = FigureCanvasTkAgg(figure, self)
        self.chart.get_tk_widget().pack(fill="both", expand=1)
        ax.set_title("Predictions")

class Input(tk.Frame):
    def __init__(self, master=None, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self.master = master

        self.img = np.ones(784).reshape((28, 28, 1))

        figure = plt.Figure(figsize=(1,1))
        ax = figure.add_subplot(111)

        self.chart = FigureCanvasTkAgg(figure, self)
        self.chart.get_tk_widget().pack(fill="both", expand=1)
        
        ax.imshow(self.img, cmap="gray", vmin=0, vmax=1)
        ax.set_title("Input image 28x28")
        ax.axis("off")

    def update_image(self, src):
        self.img = src.resize((28, 28))
        self.img = self.img.convert("L")
        self.img = np.array(self.img)
        self.img = self.img.reshape(*self.img.shape, 1)
        self.img = self.img / 255

        ax = self.chart.figure.gca()
        ax.imshow(self.img, cmap="gray", vmin=0, vmax=1)
        self.chart.figure.canvas.draw()

class Toolbar(tk.Frame):
    def __init__(self, master=None, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self.master = master

        self.img_width  = tk.PhotoImage(file=os.path.join("assets", "width.png"))
        self.img_brush  = tk.PhotoImage(file=os.path.join("assets", "brush.png"))
        self.img_eraser = tk.PhotoImage(file=os.path.join("assets", "eraser.png"))
        self.img_delete = tk.PhotoImage(file=os.path.join("assets", "delete.png"))
        self.img_select = tk.PhotoImage(file=os.path.join("assets", "select.png"))

        self.fg_button = tk.Button(self, padx=8, pady=1, bg=self.master.foreground, relief="sunken")
        self.bg_button = tk.Button(self, padx=8, pady=1, bg=self.master.background, relief="sunken")
        self.width_button  = tk.Button(self, image=self.img_width,  bg="white", activebackground="white", border=0)
        self.brush_button  = tk.Button(self, image=self.img_brush,  bg="white", activebackground="white", border=0)
        self.eraser_button = tk.Button(self, image=self.img_eraser, bg="white", activebackground="white", border=0)
        self.clear_button  = tk.Button(self, image=self.img_delete, bg="white", activebackground="white", border=0)
        self.select_button = tk.Button(self, image=self.img_select, bg="white", activebackground="white", border=0)

        self.fg_button.pack(side="left",     padx=(10,5), pady=10)
        self.bg_button.pack(side="left",     padx=5, pady=10)
        self.width_button.pack(side="left",  padx=5, pady=10)
        self.brush_button.pack(side="left",  padx=5, pady=10)
        self.eraser_button.pack(side="left", padx=5, pady=10)
        self.clear_button.pack(side="left",  padx=5, pady=10)
        self.select_button.pack(side="left", padx=(5,10), pady=10)

        self.bind("<Enter>", self.master.handle_on_cursor_leave)
        self.fg_button.bind("<Button-1>",     self.master.change_foreground)
        self.bg_button.bind("<Button-1>",     self.master.change_background)
        self.width_button.bind("<Button-1>",  self.master.toggle_width_scale)
        self.brush_button.bind("<Button-1>",  self.master.switch_tool)
        self.eraser_button.bind("<Button-1>", self.master.switch_tool)
        self.select_button.bind("<Button-1>", self.master.switch_tool)
        self.clear_button.bind("<Button-1>",  self.master.clear_canvas)

class Scale(tk.Frame):
    def __init__(self, master=None, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self.master = master
        self.scale = tk.Scale(self, bg="white", bd=0, highlightthickness=0, from_=20, to=5)
        self.scale.pack(padx=(0,10), pady=10)
        self.scale.bind("<ButtonRelease-1>", self.master.update_width)

class Paint(tk.Canvas):
    BRUSH = 1
    ERASER = 2
    SELECTOR = 3

    def __init__(self, master=None, *args, **kwargs):
        tk.Canvas.__init__(self, master, *args, **kwargs)
        self.master = master

        self.width = self.winfo_reqwidth()
        self.height = self.winfo_reqheight()

        self.x = None
        self.y = None
        self.mode = 0
        self.line_width = 5
        self.foreground = "black"
        self.background = "white"

        self.toolbar = Toolbar(self, bg="white", bd=2, relief="raised")
        self.width_scale = Scale(self, bg="white", bd=2, relief="raised")

        self.rowconfigure(0, weight=15)
        self.rowconfigure(1, weight=1)  
        self.columnconfigure([0,8], weight=200)
        self.columnconfigure([1,2,3,4,5,6,7], weight=1)

        self.toolbar.grid(row=1, column=1, columnspan=7, sticky="n")
        self.width_scale.grid(row=0, column=3, sticky="s")
        self.width_scale.grid_remove()

        self.bind("<Configure>",       self.handle_on_resize)
        self.bind("<Motion>",          self.handle_on_cursor_motion)
        self.bind("<Leave>",           self.handle_on_cursor_leave)
        self.bind("<Button-1>",        self.handle_on_click)
        self.bind("<B1-Motion>",       self.handle_on_motion)
        self.bind("<ButtonRelease-1>", self.handle_on_release)

    def change_foreground(self, e):
        self.foreground = askcolor(color=self.foreground)[1]
        self.toolbar.fg_button.configure(bg=self.foreground, activebackground=self.foreground)

    def change_background(self, e):
        self.background = askcolor(color=self.background)[1]
        self.toolbar.bg_button.configure(bg=self.background, activebackground=self.background)
        self.configure(bg=self.background)
        self.itemconfig("eraser", fill=self.background)

    def toggle_width_scale(self, e):
        if self.width_scale.winfo_ismapped():
            self.width_scale.grid_remove()
        else:
            self.width_scale.grid()

    def update_width(self, e):
        self.line_width = self.width_scale.scale.get()

    def switch_tool(self, e):
        self.mode = {
            self.toolbar.brush_button:  self.BRUSH,
            self.toolbar.eraser_button: self.ERASER,
            self.toolbar.select_button: self.SELECTOR
        }[e.widget]

    def clear_canvas(self, e):
        self.delete("all")

    def handle_on_resize(self, e):
        wscale = float(e.width) / self.width
        hscale = float(e.height) / self.height

        self.width = e.width
        self.height = e.height
        
        self.scale("all", 0, 0, wscale, hscale)

    def handle_on_cursor_motion(self, e):
        if self.mode in (self.BRUSH, self.ERASER):
            x1, y1 = (e.x - self.line_width/2), (e.y - self.line_width/2)
            x2, y2 = (e.x + self.line_width/2), (e.y + self.line_width/2)
            
            self.delete("cursor")

            if self.mode == self.BRUSH:
                self.create_oval(x1, y1, x2, y2, fill=self.foreground, tag="cursor")
                
            elif self.mode == self.ERASER:
                self.create_rectangle(x1, y1, x2, y2, fill=self.background, outline="black", tag="cursor")

    def handle_on_cursor_leave(self, e):
        self.delete("cursor")

    def handle_on_click(self, e):
        self.x = e.x
        self.y = e.y

        x1, y1 = (self.x - self.line_width/2), (self.y - self.line_width/2)
        x2, y2 = (self.x + self.line_width/2), (self.y + self.line_width/2)

        if self.mode == self.BRUSH:
            self.create_oval(x1, y1, x2, y2, fill=self.foreground, outline=self.foreground, tag="brush")

        elif self.mode == self.ERASER:
            self.create_rectangle(x1, y1, x2, y2, fill=self.background, outline=self.background, tag="eraser")

        elif self.mode == self.SELECTOR:
            self.create_text(self.x, self.y, text="0x0", anchor="sw", tag="selector-size")
            self.create_rectangle(self.x, self.y, self.x, self.y, outline="black", width=1, tag="selector")

    def handle_on_motion(self, e):
        if self.x and self.y:
            if self.mode in (self.BRUSH, self.ERASER):
                if self.mode == self.BRUSH:
                    self.create_line(self.x, self.y, e.x, e.y, 
                                     width=self.line_width, 
                                     fill=self.foreground, 
                                     capstyle="round", 
                                     smooth=1, 
                                     splinesteps=36,
                                     tag="brush")

                elif self.mode == self.ERASER:
                    self.create_line(self.x, self.y, e.x, e.y, 
                                     width=self.line_width, 
                                     fill=self.background, 
                                     capstyle="projecting", 
                                     smooth=1, 
                                     splinesteps=40,
                                     tag="eraser")

                self.x = e.x
                self.y = e.y

            elif self.mode == self.SELECTOR:
                dx = e.x - self.x
                dy = e.y - self.y

                anchor  = "n" if dy < 0 else "s"
                anchor += "w" if dx < 0 else "e"

                self.itemconfigure("selector-size", text=f"{abs(dx)}x{abs(dy)}", anchor=anchor)
                self.coords("selector", self.x, self.y, e.x, e.y)

    def handle_on_release(self, e):
        self.x = None
        self.y = None

        if self.mode == self.SELECTOR:
            bbox = self.coords("selector")
            img = ImageGrab.grab(bbox=(bbox[0] + self.winfo_rootx() + 1, 
                                       bbox[1] + self.winfo_rooty() + 1, 
                                       bbox[2] + self.winfo_rootx(),
                                       bbox[3] + self.winfo_rooty()))
            self.master.input.update_image(img)
            self.delete("selector", "selector-size")

class Guesser(tk.Tk):
    def __init__(self, width, height, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.paint = Paint(self, bg="white", bd=2, relief="raised", highlightthickness=0)
        self.input = Input(self, bg="white", bd=2, relief="raised") 
        self.chart = Chart(self, bg="white", bd=2, relief="raised") 

        self.rowconfigure([0,1], weight=1)  
        self.columnconfigure([0,1,2], weight=1)

        self.paint.grid(rowspan=2, columnspan=2, sticky="nwse", padx=10, pady=10)
        self.input.grid(row=0, column=2, sticky="nwse", padx=(0,10), pady=(10,5))
        self.chart.grid(row=1, column=2, sticky="nwse", padx=(0,10), pady=(5,10))

        self.configure(bg="white")
        self.geometry(f"{width}x{height}")
        self.minsize(width=width, height=height)
        self.iconphoto(False, tk.PhotoImage(file=os.path.join("assets", "icon.png")))
        self.title("Number quesser")
        self.mainloop()

if __name__ == "__main__": 
    Guesser(1000, 500)