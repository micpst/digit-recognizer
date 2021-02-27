import os
import numpy as np
import tkinter as tk
import tensorflow as tf
import matplotlib.pyplot as plt

from tkinter import ttk
from PIL import ImageGrab
from tkinter.colorchooser import askcolor
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class BarChart(tk.Frame):
    def __init__(self, master=None, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self.master = master

        figure = plt.Figure(figsize=(1,1))
        ax = figure.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(figure, self)
        self.canvas.get_tk_widget().pack(fill="both", expand=1)
        self.bars = ax.bar(range(10), np.zeros(10), color="#777777")

        ax.set_title("Predictions")
        ax.set_xticks(range(10))
        ax.set_yticks([0, .5, 1])
        ax.set_ylim([0, 1])

    def plot(self, predictions):
        ax = self.canvas.figure.gca()
        self.bars.remove()
        self.bars = ax.bar(range(10), predictions, color="#777777")
        self.bars[np.argmax(predictions)].set_color("orange")
        self.canvas.figure.canvas.draw()

class InputImage(tk.Frame):
    def __init__(self, master=None, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self.master = master

        figure = plt.Figure(figsize=(1,1))
        ax = figure.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(figure, self)
        self.canvas.get_tk_widget().pack(fill="both", expand=1)

        ax.imshow(np.ones(784).reshape((28, 28, 1)), cmap="gray", vmin=0, vmax=1)
        ax.set_title("Input image 28x28")
        ax.set_xticks([])
        ax.set_yticks([])

    def plot(self, img):
        ax = self.canvas.figure.gca()
        ax.imshow(img, cmap="gray", vmin=0, vmax=1)
        self.canvas.figure.canvas.draw()

class Toolbar(tk.Frame):
    def __init__(self, master=None, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self.master = master

        self.fg_button = tk.Button(self, padx=8, pady=1, bg=self.master.paint_component.foreground, relief="sunken", cursor="hand2")
        self.bg_button = tk.Button(self, padx=8, pady=1, bg=self.master.paint_component.background, relief="sunken", cursor="hand2")
        self.width_button = tk.Button(self, image=self.master.img_width, cursor="hand2", bg="white", activebackground="white", border=0)
        self.brush_button = tk.Button(self, image=self.master.img_brush, cursor="hand2", bg="white", activebackground="white", border=0)
        self.eraser_button = tk.Button(self, image=self.master.img_eraser, cursor="hand2", bg="white", activebackground="white", border=0)
        self.clear_button = tk.Button(self, image=self.master.img_delete, cursor="hand2", bg="white", activebackground="white", border=0)
        self.select_button = tk.Button(self, image=self.master.img_select, cursor="hand2", bg="white", activebackground="white", border=0, state="disabled")
        
        self.fg_button.pack(side="top", padx=10, pady=10)
        self.bg_button.pack(side="top", padx=10, pady=10)
        self.width_button.pack(side="top", padx=10, pady=10)
        self.brush_button.pack(side="top", padx=10, pady=10)
        self.eraser_button.pack(side="top", padx=10, pady=10)
        self.clear_button.pack(side="top", padx=10, pady=10)
        self.select_button.pack(side="top", padx=10, pady=10)

        self.fg_button.bind("<Button-1>", self.change_foreground)
        self.bg_button.bind("<Button-1>", self.change_background)
        self.brush_button.bind("<Button-1>", self.switch_tool)
        self.eraser_button.bind("<Button-1>", self.switch_tool)
        self.select_button.bind("<Button-1>", self.switch_tool)
        self.clear_button.bind("<Button-1>", self.clear_canvas)
        self.width_button.bind("<Button-1>", self.master.toggle_width_scale)

    def change_foreground(self, e):
        color = askcolor(color=self.master.paint_component.foreground)[1]
        self.fg_button.configure(bg=color, activebackground=color)
        self.master.paint_component.foreground = color

    def change_background(self, e):
        color = askcolor(color=self.master.paint_component.background)[1]
        self.bg_button.configure(bg=color, activebackground=color)
        self.master.paint_component.background = color

    def switch_tool(self, e):
        self.master.paint_component.mode = {
            self.brush_button:  Paint.BRUSH,
            self.eraser_button: Paint.ERASER,
            self.select_button: Paint.SELECTOR,
        }[e.widget]

    def unlock_select_button(self):
        self.select_button["state"] = "normal"

    def lock_select_button(self):
        self.select_button["state"] = "disabled"

    def clear_canvas(self, e):
        self.master.paint_component.delete("all")

class Paint(tk.Canvas):
    BRUSH = 1
    ERASER = 2
    SELECTOR = 3

    def __init__(self, master=None, *args, **kwargs):
        tk.Canvas.__init__(self, master, *args, **kwargs)
        self.master = master

        self.width = self.winfo_reqwidth()
        self.height = self.winfo_reqheight()

        self.mode = 0
        self.x = None
        self.y = None
        self.line_width = 5
        self.foreground = "black"
        self._background = "white"

        self.bind("<Configure>", self.handle_on_resize)
        self.bind("<Motion>", self.handle_on_cursor_motion)
        self.bind("<Leave>", self.handle_on_cursor_leave)
        self.bind("<Button-1>", self.handle_on_click)
        self.bind("<B1-Motion>", self.handle_on_motion)
        self.bind("<ButtonRelease-1>", self.handle_on_release)

    @property
    def background(self):
        return self._background

    @background.setter
    def background(self, color):
        self.configure(bg=color)
        self.itemconfig("eraser", fill=color)
        self._background = color

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
            self.master.guess(img)
            self.delete("selector", "selector-size")

class WidthScale(tk.Frame):
    def __init__(self, master=None, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self.master = master
        self.scale_component = tk.Scale(self, bg="white", bd=0, highlightthickness=0, orient="horizontal", from_=5, to=20)
        self.scale_component.pack(padx=(0,10), pady=(5,10))
        self.scale_component.bind("<ButtonRelease-1>", self.handle_on_button_release)

    def handle_on_button_release(self, e):
        self.master.paint_component.line_width = self.scale_component.get()

class ModelLoader(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.master= master

        self.name_label = tk.Label(self, text="Name: -", anchor="w", width=15, font="12", bg="white")
        self.acc_label = tk.Label(self, text="Model acc: 0.00%", font="12", bg="white")
        self.state_label = tk.Label(self, text="Not loaded", font="12", bg="white")
        self.load_button = tk.Button(self, image=self.master.img_open, cursor="hand2", bg="white", activebackground="white", border=0)
        self.progressbar = ttk.Progressbar(self)

        self.rowconfigure([0,1], weight=1)
        self.columnconfigure(1, weight=1)

        self.name_label.grid(row=0, column=0, sticky="nws", padx=10, pady=10)
        self.progressbar.grid(row=0, column=1, sticky="nwse", pady=10)
        self.load_button.grid(row=0, column=2, sticky="nwse", padx=10, pady=10)
        self.acc_label.grid(row=1, column=0, sticky="nws", padx=10, pady=(0,10))
        self.state_label.grid(row=1, column=1, sticky="nes", pady=(0,10))

        self.load_button.bind("<Button-1>", self.load)
        
    def load(self, e):
        filepath = tk.filedialog.askopenfilename(initialdir="./", title="Select file", filetypes=(("h5 files","*.h5"),))
        if filepath:
            self.progressbar["value"] = 30
            self.state_label["text"] = "Loading - 30%"
            self.update_idletasks()
            self.update()

            model = tf.keras.models.load_model(filepath)

            self.progressbar["value"] = 60
            self.state_label["text"] = "Testing - 60%"
            self.update_idletasks()
            self.update()

            acc = self.test(model)

            self.progressbar["value"] = 100
            self.state_label["text"] = "Completed - 100%"

            self.name_label["text"] = f"Name: {model._name}"
            self.acc_label["text"] = f"Model acc: {acc * 100:5.2f}%"
            self.load_button["relief"] = "raised"
            self.master.model = model
            
    def test(self, model):
        (_,_), (X_test, y_test) = tf.keras.datasets.mnist.load_data()
        y_test = tf.keras.utils.to_categorical(y_test, 10)
        X_test = X_test.reshape(*X_test.shape, 1)
        X_test = X_test / 255
        _, acc = model.evaluate(X_test, y_test, verbose=0)
        return acc

class Guesser(tk.Tk):
    def __init__(self, width, height, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self._model = None

        self.minsize(width=width, height=height)
        self.configure(bg="white")
        
        self.load_assets()

        self.rowconfigure([1,2], weight=1)
        self.columnconfigure(1, weight=3)
        self.columnconfigure(2, weight=1)

        self.paint_component = Paint(self, bg="white", bd=2, relief="raised", highlightthickness=0)
        self.toolbar_component = Toolbar(self, bg="white", bd=2, relief="raised")
        self.model_loader_component = ModelLoader(self, bg="white", bd=2, relief="raised")
        self.input_img_component = InputImage(self, bg="white", bd=2, relief="raised")
        self.bar_chart_component = BarChart(self, bg="white", bd=2, relief="raised")
        self.width_scale_component = WidthScale(self, bg="white", bd=2, relief="raised")
        
        self.paint_component.grid(row=0, column=1, rowspan=3, sticky="nwse", padx=(0,10), pady=10)
        self.toolbar_component.grid(row=0, column=0, rowspan=3, sticky="nwse", padx=(10,0), pady=10)
        self.model_loader_component.grid(row=0, column=2, sticky="nwse", padx=(0,10), pady=(10,0))
        self.input_img_component.grid(row=1, column=2, sticky="nwse", padx=(0,10), pady=(10,0))
        self.bar_chart_component.grid(row=2, column=2, sticky="nwse", padx=(0,10), pady=10)
        self.width_scale_component.grid(row=1, column=1, sticky="nw")
        self.width_scale_component.grid_remove()

        self.iconphoto(False, self.img_icon)
        self.title("Number quesser")
        self.mainloop()

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, new):
        if new:
            self.title(f"Number quesser - {new._name}")
            self.toolbar_component.unlock_select_button()
        else:
            self.title(f"Number quesser")
            self.toolbar_component.lock_select_button()
        self._model = new

    def load_assets(self):
        self.img_icon = tk.PhotoImage(file=os.path.join("assets", "icon.png"))
        self.img_open = tk.PhotoImage(file=os.path.join("assets", "open.png"))
        self.img_width = tk.PhotoImage(file=os.path.join("assets", "width.png"))
        self.img_brush = tk.PhotoImage(file=os.path.join("assets", "brush.png"))
        self.img_eraser = tk.PhotoImage(file=os.path.join("assets", "eraser.png"))
        self.img_delete = tk.PhotoImage(file=os.path.join("assets", "delete.png"))
        self.img_select = tk.PhotoImage(file=os.path.join("assets", "select.png"))

    def toggle_width_scale(self, e):
        if self.width_scale_component.winfo_ismapped():
            self.width_scale_component.grid_remove()
        else:
            self.width_scale_component.grid()

    def guess(self, src):
        img = src.resize((28, 28))
        img = img.convert("L")
        img = np.array(img)
        img = img.reshape(*img.shape, 1)
        img = img / 255
        self.input_img_component.plot(img)

        img = img.reshape(1, *img.shape)
        [prediction] = self.model.predict(img)
        self.bar_chart_component.plot(prediction)

if __name__ == "__main__": 
    Guesser(1000, 600)