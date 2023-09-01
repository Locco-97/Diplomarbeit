from tkinter import *
import tkinter.ttk
from tkinter import filedialog
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import pandas as pd


class App:
    """simple App for user interaction"""

    __window = Tk()
    __x = 600
    __y = 600
    __filename = ""

    def __init__(self) -> None:
        pass

    def create(self) -> None:
        self.__window.title("Diplomarbeit M-Thoma - FL-Rechner")
        self.__window.geometry(f"{self.__x}x{self.__y}")
        self.__window.minsize(self.__x, self.__y)
        self.__window.maxsize(self.__x, self.__y)

        self.label_file_explorer = Label(
            self.__window,
            text="File Explorer using Tkinter",
            width=100,
            height=4,
            fg="blue",
        )
        button = Button(
            self.__window, text="explorer", width=15, command=self.__browse_files
        )
        button.grid(column=0, row=0)

        t1 = Label(
            self.__window, text="R\u1D65 Eingabe:"
        )  # u1D65 UNICODE für tiefgestelltes V
        t1.grid(column=0, row=1, sticky=W)
        e1 = Entry(self.__window)
        e1.grid(column=0, row=2, sticky=W)

        t2 = Label(
            self.__window, text="L\u1D65 Eingabe:"
        )  # u1D65 UNICODE für tiefgestelltes V
        t2.grid(column=0, row=3, sticky=W)
        e3 = Entry(self.__window)
        e3.grid(column=0, row=4, sticky=W)

        t4 = Label(
            self.__window, text="U\u2080 GR Eingabe:"
        )# u1D65 UNICODE für tiefgestelltes 0
        t4.grid(column=0, row=5, sticky=W)
        e4 = Entry(self.__window)
        e4.grid(column=0, row=6, sticky=W)

        t5 = Label(self.__window, text="Leitungswiderstand:")
        t5.grid(column=0, row=7, sticky=W)

        t6 = Label(self.__window, text="Leitungsinduktivität:")
        t6.grid(column=0, row=8, sticky=W)

        t7 = Label(
            self.__window,
            text="IK0:",
        )
        t7.grid(column=0, row=9, sticky=W)

        t8 = Label(
            self.__window,
            text="Zeit für 3T",
        )
        t8.grid(column=0, row=10, sticky=W)

        t9 = Label(
            self.__window,
            text="max Steigung A/ms:",
        )
        t9.grid(column=0, row=11, sticky=W)

        tkinter.ttk.Separator(self.__window, orient=VERTICAL).grid(
            column=1, row=0, rowspan=13, sticky="ns", padx=5
        )

    def __browse_files(self) -> str:
        self.__filename = filedialog.askopenfilename(
            title="Select a File",
            filetypes=(("CSV-files", ".csv"), ("all files", ".")),
        )
        # Change label contents
        self.label_file_explorer.configure(text="File Opened: " + self.__filename)

        self.__create_plot()

    def __get_measurement_data(self) -> pd.DataFrame:
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

            if (voltage_value + 1) <= next_voltage_value or (voltage_value - 1) >= next_voltage_value:
                voltageindex = i
                startflag = True
            if (current_value + 1) <= next_current_value or (current_value - 1) >= next_current_value:
                currentindex = i
                startflag = True

            if current_value >= colcurrent.max() * 0.99 and startflag:
                endindex = i
                endflag = True

            if endflag and startflag:
                break

        if (currentindex - voltageindex) < 10:
            df = df.iloc[currentindex - 50 : endindex + 50]
            return df
        return None

    def __create_plot(self) -> None:
        df = self.__get_measurement_data()

        # the figure that will contain the plot
        fig = Figure(figsize=(4, 2), dpi=100)
        fig1 = Figure(figsize=(4, 2), dpi=100)

        plot1 = fig.add_subplot(111)
        plot2 = fig1.add_subplot(111)

        # plotting the graph
        plot1.plot(df["Time [s]"],df["U Spannung [V]"])
        plot2.plot(df["Time [s]"],df["I Strom [A]"])
        canvas = FigureCanvasTkAgg(fig, master=self.__window)
        canvas.draw()
        canvas1 = FigureCanvasTkAgg(fig1, master=self.__window)
        canvas1.draw()

        # placing the canvas on the Tkinter self.__window
        canvas.get_tk_widget().grid(column=2, row=0, rowspan=6, columnspan=3, pady=5)
        canvas1.get_tk_widget().grid(column=2, row=7, rowspan=6, columnspan=3, pady=5)
    def run(self) -> None:
        self.__window.mainloop()  # In der Ereignisschleife auf Eingabe des Benutzers warten.
