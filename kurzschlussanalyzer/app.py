import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import pandas as pd

class App():
    """simple App for user interaction"""

    def __del__(self):
        pass
        #self.root.destroy()

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Diplomarbeit M-Thoma - FL-Rechner")
        self.root.iconphoto(False, tk.PhotoImage(file="kurzschlussanalyzer/images/blt_icon.png"))

        img = Image.open("kurzschlussanalyzer/images/blt_long.png")
        img_width, img_height = img.size
        resized_img = img.resize((int(img_width/4), int(img_height/4)))
        blt_label = ImageTk.PhotoImage(resized_img)

        # --- menu left ---
        left_menu_width = 150
        self.menu_left = tk.Frame(self.root, width=left_menu_width , bg="#ababab")
        self.menu_left_upper = tk.Frame(self.menu_left, width=left_menu_width)
        self.menu_left_lower = tk.Frame(self.menu_left, width=left_menu_width)

        self.company_label = tk.Label(self.menu_left_upper, image=blt_label)
        self.company_label.grid(row=0, column=0, columnspan=2)
        self.test = tk.Label(self.menu_left_upper, text="Kurzschlussanalyzer", font=('Segoe UI', 14, 'bold'))
        self.test.grid(row=1, column=0, columnspan=2)
        self.sep = ttk.Separator(self.menu_left_upper, orient="horizontal")
        self.sep.grid(row=2, column=0,ipadx=70, pady=10, columnspan=2)
        self.button_file_select = tk.Button(self.menu_left_upper, text="Explorer", command=self.__browse_files)
        self.button_file_select.grid(row=3, column=0, columnspan=2)
        self.sep = ttk.Separator(self.menu_left_upper, orient="horizontal")
        self.sep.grid(row=4, column=0,ipadx=70, pady=10, columnspan=2)

        self.test = tk.Label(self.menu_left_upper, text="R\u1D65:", font=('Segoe UI', 10, 'normal'))
        self.test.grid(row=5, column=0, sticky=tk.W)
        self.entry_resistance = tk.Entry(self.menu_left_upper, width=10)
        self.entry_resistance.grid(row=5, column=1)
        self.test = tk.Label(self.menu_left_upper, text="L\u1D65:", font=('Segoe UI', 10, 'normal'))
        self.test.grid(row=6, column=0, sticky=tk.W)
        self.entry_indutance = tk.Entry(self.menu_left_upper, width=10)
        self.entry_indutance.grid(row=6, column=1)
        self.test = tk.Label(self.menu_left_upper, text="U\u2080:", font=('Segoe UI', 10, 'normal'))
        self.test.grid(row=7, column=0, sticky=tk.W)
        self.entry_voltage = tk.Entry(self.menu_left_upper, width=10)
        self.entry_voltage.grid(row=7, column=1)

        self.sep = ttk.Separator(self.menu_left_upper, orient="horizontal")
        self.sep.grid(row=8, column=0,ipadx=70, pady=10, columnspan=2)
        
        self.menu_left_upper.pack(side="top", fill="both", expand=True)
        self.menu_left_lower.pack(side="top", fill="both", expand=True)

        # --- right area ---
        # is created in __create_plot()

        # --- status bar ---
        self.status_frame = tk.Frame(self.root)
        self.status = tk.Label(self.status_frame, text="this is the status bar")
        self.status.pack(fill="both", expand=True)

        self.menu_left.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.status_frame.grid(row=4, column=0, columnspan=2, sticky="ew")

        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        # --- mainloop ---
        self.root.mainloop()

    def run(self) -> None:
        self.root.mainloop()
    def __browse_files(self) -> None:
        self.__filename = filedialog.askopenfilename(
            title="Select a File",
            filetypes=(("CSV-files", ".csv"), ("all files", ".")),
        )

        self.__get_measurement_data()

        # TESTING
        points = {"Start": 4.035, "Stop": 4.036, "xyz": 4.05}
        self.__create_plot(df_measure=self.__dataframefinal, points=points)

    def __get_measurement_data(self) -> None:
        voltageindex = 0
        currentindex = 0
        endindex = 0
        endflag = False
        startflag = False

        df = pd.read_csv(self.__filename, sep=",")
        df = df[["Time [s]", "I Strom [A]", "U Spannung [V]"]]

        colcurrent = df["I Strom [A]"]

        for i, row in df.iterrows():
            voltage_value = row.iloc[2]
            next_voltage_value = (df.iloc[i + 1]).iloc[2]
            current_value = row.iloc[1]
            next_current_value = (df.iloc[i + 1]).iloc[1]

            if (voltage_value + 1) <= next_voltage_value or (
                voltage_value - 1
            ) >= next_voltage_value:
                voltageindex = i
                startflag = True
            if (current_value + 1) <= next_current_value or (
                current_value - 1
            ) >= next_current_value:
                currentindex = i
                startflag = True

            if current_value >= colcurrent.max() * 0.99 and startflag:
                endindex = i
                endflag = True

            if endflag and startflag:
                break

        if (currentindex - voltageindex) < 10:
            self.__dataframefinal = df.iloc[currentindex - 50 : endindex + 50]

    def __create_plot(self, points, df_measure, df_real=pd.DataFrame) -> None:
        figure_size = (10, 5)
        dpi_scale = 100

        fig1 = Figure(figsize=figure_size, dpi=dpi_scale)
        canvas = FigureCanvasTkAgg(fig1, master=self.root)
        plot1 = fig1.add_subplot(111)
        fig2 = Figure(figsize=figure_size, dpi=dpi_scale)
        canvas1 = FigureCanvasTkAgg(fig2, master=self.root)
        plot2 = fig2.add_subplot(111)
        
        # --- Plot 1 ---
        # plot style settings
        plot1.grid()
        plot1.set_title("Diagramm Kurzschluss")
        plot1.set_xlabel("Time [s]")
        plot1.set_ylabel("Strom [A]", color="g")
        secay = plot1.secondary_yaxis("right")
        secay.set_ylabel("Spannung [U]", color="r")

        # plot data input
        plot1.plot(df_measure["Time [s]"], df_measure["U Spannung [V]"], color="r", label="Kurzschlussspanung")
        plot1.plot(df_measure["Time [s]"], df_measure["I Strom [A]"], color="g", label="Kurzschlusstrom")

        # --- Plot 2 ---
        # plot style settings
        plot2.grid()
        plot2.set_title("Diagramm Berechung Kurzschluss")
        plot2.set_xlabel("Time [s]")
        plot2.set_ylabel("Strom [A]", color="g")

        # plot data input
        plot2.plot(df_measure["Time [s]"], df_measure["I Strom [A]"], color="g", label="Kurzschlusstrom")

        # plot line input
        yMin, yMax = plot2.get_ylim()
        yMean = (yMax - yMin) * 0.75 # set text in the upper half of the line

        for text, pos in points.items():
            plot2.axvline(x=pos, linestyle="--")
            plot2.text(pos, yMean, text, ha='center', va='center',rotation='vertical', bbox={'facecolor':'white', 'pad':4})

        # placing the canvas on the Tkinter self.__window
        canvas1.get_tk_widget().grid(column=1, row=3, columnspan=5, pady=5)
        canvas.get_tk_widget().grid(column=1, row=1, columnspan=5, pady=5)