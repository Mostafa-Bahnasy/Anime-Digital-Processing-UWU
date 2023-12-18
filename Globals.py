import tkinter as tk
from tkinter import PhotoImage
from collections import OrderedDict
from tkinter import filedialog

from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np


class FileOp:
    def __init__(self):
        self.data = []

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, "r") as file:
                for line in file:
                    self.data.append(line)


class Signal:
    def __init__(self):
        self.x = []
        self.y = []
        self.phase = 0
        self.amp = 0
        self.freq = 0
        self.freq_s = 0
        self.my_file = FileOp()

    def get_data(self):
        self.my_file.open_file()

    def get_phase(self, pos):
        self.phase = int(self.my_file.data[pos])

    def get_amp(self, pos):
        self.amp = int(self.my_file.data[pos])

    def get_points(self, start):
        for index in range(start, len(self.my_file.data) - 1):
            temp = self.my_file.data[index].split()
            self.x.append(temp[0])
            self.y.append(temp[1])

    def set_phase(self, phase):
        self.phase = phase

    def set_amp(self, amp):
        self.amp = amp

    def set_analog(self, freq):
        self.freq = freq

    def set_sample(self, freq_s):
        self.freq_s = freq_s


class Buttons:
    def __init__(self):
        self.button = None
        self.button_img = None

    def make_button(self, window, title, x, y, action):
        self.button = tk.Button(window, text=title, command=action)
        self.button.place(x=x, y=y)

    def make_img_button(self, window, path, x, y, action):
        self.button_img = PhotoImage(file=path)
        self.button = tk.Button(window, image=self.button_img, command=action)
        self.button.place(x=x, y=y)

    def toggle(self):
        if self.button.cget("state") == "normal":
            self.button.config(state="disabled")
        else:
            self.button.config(state="normal")

    def set_state(self, flag):
        if flag == 1:
            self.button.config(state="normal")
        else:
            self.button.config(state="disabled")

    def set_position(self, x, y):
        self.button.place(x=x, y=y)

    def set_action(self, action):
        self.button.config(command=action)


class Drop_List:
    def __init__(self):
        self.selected_option = tk.StringVar()
        self.drop = None
        self.label = None
        self.options = []

    def on_dropdown_select(self):
        self.label.config(text=f"Selected Option: {self.selected_option}")

    def make_drop(self, window, options, x, y):
        self.options = options
        self.selected_option.set(self.options[0])
        print(self.selected_option.get())
        self.drop = tk.OptionMenu(window, self.selected_option, *self.options)
        self.drop.place(x=x, y=y)


class Main_Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.bg_label = None
        self.title("Anime Digital Processing uwu")
        self.geometry("1920x1080")
        self.bg_image = None
        self.task_button = []
        self.show_main_screen()

    def show_main_screen(self):
        pass

    def set_back_image(self, path):
        # Load the image
        self.bg_image = PhotoImage(file=path)  # Replace with the path to your image

        # Create a Label with the image
        self.bg_label = tk.Label(self, image=self.bg_image)
        self.bg_label.place(relwidth=1, relheight=1)

    def set_buttons(self):
        for index in range(0, 4):
            self.task_button.append(Buttons())
            self.task_button[index].make_img_button(self,
                                                    "E:\\other\\Anime\\backgrounds\\task" + str(index + 1) + ".png", 0,
                                                    0, lambda: (print("clicked")))

        self.task_button[0].set_position(100, 100)
        self.task_button[1].set_position(150, 500)
        self.task_button[2].set_position(1200, 100)
        self.task_button[3].set_position(1150, 500)

    def edit_button_action(self, title, action):
        self.task_button[int(title)].set_action(action)


class subWindow(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.bg_label = None
        self.title("Anime Digital Processing uwu")
        self.geometry("1920x1080")
        self.bg_image = None
        self.buttons = OrderedDict()
        self.radio = RadioBlock()
        self.radio_selected = ""

    def set_back_image(self, path):
        # Load the image
        self.bg_image = PhotoImage(file=path)  # Replace with the path to your image

        # Create a Label with the image
        self.bg_label = tk.Label(self, image=self.bg_image)
        self.bg_label.place(relwidth=1, relheight=1)

    def add_button_img(self, title, path, x, y, action):
        self.buttons[title] = Buttons()
        self.buttons[title].make_img_button(self, path, x, y, action)

    def add_button(self, title, x, y, action):
        self.buttons[title] = Buttons()
        self.buttons[title].make_button(self, title, x, y, action)

    def edit_button_action(self, title, action):
        self.buttons[title].set_action(action)

    def add_textbox(self, title, x, y, label):
        self.buttons[title] = TextBox()
        self.buttons[title].create_box(self, x, y, label)

    def add_radiobutton(self, x, y, title):
        self.radio.init(x, y)
        self.radio.add_to_block(self, title, lambda: (print("radio: " + title + "selected")))

    def toggle_radio(self):
        self.radio.rotate()

    def hide_wid(self, wid):
        wid.lower(self.bg_label)

    def show_wid(self, wid):
        wid.lift(self.bg_label)


class TextBox:
    def __init__(self):
        self.box = None
        self.label = None
        self.x = 0
        self.y = 0
        self.width = 20
        self.height = 1
        self.label_size = 0

    def create_box(self, frame, x, y, label):
        self.box = tk.Text(frame,
                           height=self.height,
                           width=self.width)
        self.set_position(x, y)
        self.x = int(x)
        self.y = int(y)
        self.label_size = len(label)
        self.label = tk.Label(frame, text=label)
        self.align()

    def set_position(self, x, y):
        self.box.place(x=x, y=y)
        self.x = int(x)
        self.y = int(y)

    def get_value(self):
        return self.box.get(1.0, "end-1c")

    def align(self):
        moves = (self.width - self.label_size) * 5
        self.label.place(x=self.x + moves, y=self.y - 23)


class RadioBlock:
    def __init__(self):
        self.shared = tk.StringVar()
        self.buttons = OrderedDict()
        self.direction = [0, 1]  # Horizontal - Vertical
        self.start_x = 0
        self.start_y = 0

    def init(self, x, y):
        self.start_x = int(x)
        self.start_y = int(y)

    def add_to_block(self, frame, title, action):
        self.buttons[title] = tk.Radiobutton(frame, text=title, variable=self.shared, value=title, command=action)
        nw_x = self.start_x + (self.direction[0] * ((len(self.buttons) - 1) * 80))
        nw_y = self.start_y + (self.direction[1] * ((len(self.buttons) - 1) * 40))
        self.buttons[title].place(x=nw_x, y=nw_y)

    def rotate(self):
        self.direction[0] = 0 if self.direction[0] == 1 else 1
        self.direction[1] = 0 if self.direction[1] == 1 else 1

        idx = 0
        for title, button in self.buttons.items():
            nw_x = self.start_x + (self.direction[0] * (idx * 80))
            nw_y = self.start_y + (self.direction[1] * (idx * 40))
            button.place(x=nw_x, y=nw_y)
            idx = idx + 1


