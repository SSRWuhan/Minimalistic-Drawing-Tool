import math
import threading
import numpy as np
from PIL import Image
import tkinter as tk
from tkinter import ttk
from tkinter import colorchooser
from tkinter import filedialog
from tkinter import messagebox

class mdt(tk.Tk):
    def __init__(self, title="minimalistic drawing tool", screen_dim=(500, 500)):
        self.__COLOR = "white"
        self.__BACKGROUND = "black"
        self.__WIDTH = 500
        self.__HEIGHT = 500
        self.__COLOR_CHANNELS = 3
        self.__CELL_SIZE = 50
        self.__GRID_X = 10
        self.__GRID_Y = 10

        self.__rgb_color = (255, 255, 255)
        self.__bg_color = (0, 0, 0)

        self.window_buffer = np.zeros((self.__GRID_Y, self.__GRID_X, self.__COLOR_CHANNELS), dtype=np.uint8)

    def __draw(self, event):
        cursor_x, cursor_y  = event.x, event.y
        drawn_cell_x = math.ceil(cursor_x / self.__CELL_SIZE)
        drawn_cell_y = math.ceil(cursor_y / self.__CELL_SIZE)
        self.window_buffer[drawn_cell_y -1][drawn_cell_x -1] = self.__rgb_color
        drawn_cell_x *= self.__CELL_SIZE
        drawn_cell_y *= self.__CELL_SIZE
        self.__canvas.create_rectangle(drawn_cell_x - self.__CELL_SIZE, drawn_cell_y - self.__CELL_SIZE, drawn_cell_x, drawn_cell_y, fill=self.__COLOR)

    def __erase(self, event):
        cursor_x, cursor_y  = event.x, event.y
        drawn_cell_x = math.ceil(cursor_x / self.__CELL_SIZE)
        drawn_cell_y = math.ceil(cursor_y / self.__CELL_SIZE)
        self.window_buffer[drawn_cell_y -1][drawn_cell_x -1] = self.__bg_color
        drawn_cell_x *= self.__CELL_SIZE
        drawn_cell_y *= self.__CELL_SIZE
        self.__canvas.create_rectangle(drawn_cell_x - self.__CELL_SIZE, drawn_cell_y - self.__CELL_SIZE, drawn_cell_x, drawn_cell_y, fill=self.__BACKGROUND)

    def __change_color(self):
        color = colorchooser.askcolor()
        if(color[1] == None):
            pass
        else:
            self.__COLOR = color[1]
            self.__rgb_color = color[0]

    def __save(self):
        save_image = Image.fromarray(self.window_buffer, "RGB")
        filepath = filedialog.asksaveasfilename(defaultextension="*.png", filetypes=[("PNG files", "*.png"), ("all files", "*.*")])
        if filepath is None:
            return
        save_image.save(filepath)


    def __change_resolution(self, resolution, cell_size, screen_dim):

        resolution = resolution.split(",")
        screen_dim = screen_dim.split(",")

        if(self.__WIDTH == self.__GRID_Y * self.__CELL_SIZE and self.__HEIGHT == self.__GRID_X * self.__CELL_SIZE):
            self.__WIDTH = int(resolution[0])
            self.__HEIGHT = int(resolution[1])
            self.__CELL_SIZE = int(cell_size)
            self.__GRID_Y = int(screen_dim[0])
            self.__GRID_X = int(screen_dim[1])
            self.__window.geometry(f"{self.__WIDTH}x{self.__HEIGHT}")
            self.window_buffer = np.zeros((self.__GRID_Y, self.__GRID_X, self.__COLOR_CHANNELS))
            self.__canvas.delete("all")
            self.__querry_window.destroy()
        else:
            messagebox.showerror(title="ERROR", message="Incompatiable dimensions")

    def __create_querry_window(self):
        self.__querry_window = tk.Toplevel()
        self.__querry_window.geometry("500x150")
        frame = ttk.Frame(self.__querry_window)
        l1 = ttk.Label(frame, text="enter resolution: (width, height)").grid(row=0,column=0, padx=10, pady=5)
        resolution_var = tk.StringVar(value=f"{self.__WIDTH}, {self.__HEIGHT}")
        resolution = ttk.Entry(frame, textvariable=resolution_var).grid(row=0,column=1, padx=10, pady=5)
        l2 = ttk.Label(frame, text="enter each cell/pixel size: " ).grid(row=1,column=0, padx=10, pady=5)
        cell_size_var = tk.StringVar(value=self.__CELL_SIZE)
        cell_size = ttk.Entry(frame, textvariable=cell_size_var).grid(row=1,column=1, padx=10, pady=5)
        l3 = ttk.Label(frame, text="enter screen dimensions: (width, height)" ).grid(row=2,column=0, padx=10, pady=5)
        screen_dim_var = tk.StringVar(value=f"{self.__GRID_Y}, {self.__GRID_X}")
        screen_dim = ttk.Entry(frame, textvariable=screen_dim_var).grid(row=2,column=1, padx=10, pady=5)
        button = ttk.Button(frame, text="apply changes", command=lambda: self.__change_resolution(resolution_var.get(), cell_size_var.get(), screen_dim_var.get())).grid(row=3,column=2, padx=10, pady=5)
        frame.pack(anchor="center")

    def __exit(self):
        self.__window.destroy()

    def __grayscale(self):
        self.__editmenu.entryconfig("Change color", state="disabled")
        self.__canvas.delete("all")
        self.__COLOR = "white"
        self.__rgb_color = (1)
        self.__COLOR_CHANNELS = 1
        self.window_buffer = np.zeros((self.__GRID_Y, self.__GRID_X, self.__COLOR_CHANNELS))

    def __rgb(self):
        self.__editmenu.entryconfig("Change color", state="normal")
        self.__canvas.delete("all")
        self.__COLOR = "white"
        self.__rgb_color = (255, 255, 255)
        self.__COLOR_CHANNELS = 3
        self.window_buffer = np.zeros((self.__GRID_Y, self.__GRID_X, self.__COLOR_CHANNELS))

    def __run(self):
        self.__window = tk.Tk()

        self.__window.title("minimalistic drawing tool")

        self.__window.geometry(f"{self.__WIDTH}x{self.__HEIGHT}")

        self.__menubar = tk.Menu(self.__window)
        self.__window.config(menu=self.__menubar)

        self.__filemenu = tk.Menu(self.__window, tearoff=0, font = ("Courier New", 9))
        self.__menubar.add_cascade(label="File", menu=self.__filemenu)
        self.__filemenu.add_command(label="Save", command=self.__save)
        self.__filemenu.add_separator()
        self.__filemenu.add_command(label="Exit", command=self.__exit)

        self.__editmenu = tk.Menu(self.__window, tearoff=0, font = ("Courier New", 9))
        self.__menubar.add_cascade(label="Edit", menu=self.__editmenu)
        self.__editmenu.add_command(label="Change color", command=self.__change_color)


        self.__settings = tk.Menu(self.__window, tearoff=0, font = ("Courier New", 9))
        self.__menubar.add_cascade(label="Settings", menu=self.__settings)
        self.__settings.add_command(label="Change resolution / grid size", command=self.__create_querry_window)
        self.__settings.add_separator()
        self.__settings.add_radiobutton(label="Grayscale", command=self.__grayscale)
        self.__settings.add_radiobutton(label="RGB", command=self.__rgb)


        self.__canvas= tk.Canvas(self.__window, bg=self.__BACKGROUND)
        self.__canvas.pack(fill= "both", expand= True)
        self.__canvas.event_add("<<left_motion>>", "<B1-Motion>", "<Button-1>")
        self.__canvas.event_add("<<right_motion>>", "<B3-Motion>", "<Button-3>")
        self.__canvas.bind("<<left_motion>>", self.__draw)
        self.__canvas.bind("<<right_motion>>", self.__erase)
        self.__window.bind("<space>", lambda x: self.__canvas.delete("all"))
        tk.mainloop()
    
    def initialize(self, daemon):
        threading.Thread(target=self.__run, daemon=daemon).start()


app = mdt()
app.initialize(False)