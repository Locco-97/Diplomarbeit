import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import pandas as pd
from kurzschlussanalyzer.calc import calculate 
from kurzschlussanalyzer.calc import real_current
from kurzschlussanalyzer.calc import safety_function


class App():    #Hauptanwendung mit Absprung in Unterprogromme

    def __del__(self):
        pass

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Diplomarbeit M-Thoma - FL-Rechner")
        self.root.iconphoto(False, tk.PhotoImage(file="kurzschlussanalyzer/images/blt_icon.png"))

        img = Image.open("kurzschlussanalyzer/images/blt_long.png")
        img_width, img_height = img.size
        resized_img = img.resize((int(img_width/4), int(img_height/4)))
        blt_label = ImageTk.PhotoImage(resized_img)

        # Menu Gesaltung
        left_menu_width = 150
        self.menu_left = tk.Frame(self.root, width=left_menu_width , bg="#ababab") #setzt die Hintergrundfarbe auf grau (ababab)
        self.menu_left_upper = tk.Frame(self.menu_left, width=left_menu_width)
        self.menu_left_lower = tk.Frame(self.menu_left, width=left_menu_width)
        # Fenster gestaltung
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

        # Text und Eingabefelder erstellen
        self.test = tk.Label(self.menu_left_upper, text="GR-Lastspannung: ", font=('Segoe UI', 10, 'normal'))
        self.test.grid(row=5, column=0, sticky=tk.W)
        self.entry_lastspannung = tk.Entry(self.menu_left_upper, width=10)
        self.entry_lastspannung.grid(row=5, column=1)
        self.entry_lastspannung.insert(0, "630")

        self.test = tk.Label(self.menu_left_upper, text="Leitungseinduktivität: ", font=('Segoe UI', 10, 'normal'))
        self.test.grid(row=6, column=0, sticky=tk.W)
        self.entry_induktivitaet = tk.Entry(self.menu_left_upper, width=10)
        self.entry_induktivitaet.grid(row=6, column=1)
        self.entry_induktivitaet.insert(0,"0.005")

        self.test = tk.Label(self.menu_left_upper, text="Leitungswiderstand: ", font=('Segoe UI', 10, 'normal'))
        self.test.grid(row=7, column=0, sticky=tk.W)
        self.entry_widerstand = tk.Entry(self.menu_left_upper, width=10)
        self.entry_widerstand.grid(row=7, column=1)
        self.entry_widerstand.insert(0,"0.25")

        self.sep = ttk.Separator(self.menu_left_upper, orient="horizontal")
        self.sep.grid(row=8, column=0,ipadx=70, pady=10, columnspan=2)

        self.test = tk.Label(self.menu_left_upper, text="SA, E: [A/ms]", font=('Segoe UI', 10, 'normal'))
        self.test.grid(row=9, column=0, sticky=tk.W)
        self.entry_sae = tk.Entry(self.menu_left_upper, width=10)
        self.entry_sae.grid(row=9, column=1)
        self.entry_sae.insert(0,"20")

        self.test = tk.Label(self.menu_left_upper, text="SA, F: [A/ms]", font=('Segoe UI', 10, 'normal'))
        self.test.grid(row=10, column=0, sticky=tk.W)
        self.entry_saf = tk.Entry(self.menu_left_upper, width=10)
        self.entry_saf.grid(row=10, column=1)
        self.entry_saf.insert(0,"15")

        self.test = tk.Label(self.menu_left_upper, text="SA, delta Imax: [A]", font=('Segoe UI', 10, 'normal'))
        self.test.grid(row=11, column=0, sticky=tk.W)
        self.entry_deltaimax = tk.Entry(self.menu_left_upper, width=10)
        self.entry_deltaimax.grid(row=11, column=1)
        self.entry_deltaimax.insert(0,"1997")

        self.test = tk.Label(self.menu_left_upper, text="SA, t Delta Imax: [s]", font=('Segoe UI', 10, 'normal'))
        self.test.grid(row=12, column=0, sticky=tk.W)
        self.entry_tdeltaimax = tk.Entry(self.menu_left_upper, width=10)
        self.entry_tdeltaimax.grid(row=12, column=1)
        self.entry_tdeltaimax.insert(0,"0.01997")

        self.test = tk.Label(self.menu_left_upper, text="SA, Tmax: [ms]", font=('Segoe UI', 10, 'normal'))
        self.test.grid(row=13, column=0, sticky=tk.W)
        self.entry_satmax = tk.Entry(self.menu_left_upper, width=10)
        self.entry_satmax.grid(row=13, column=1)
        self.entry_satmax.insert(0,"25")
        
        self.test = tk.Label(self.menu_left_upper, text="SA, Delta Imin: [A]", font=('Segoe UI', 10, 'normal'))
        self.test.grid(row=14, column=0, sticky=tk.W)
        self.entry_sadeltaimin = tk.Entry(self.menu_left_upper, width=10)
        self.entry_sadeltaimin.grid(row=14, column=1)
        self.entry_sadeltaimin.insert(0,"900")

        self.sep = ttk.Separator(self.menu_left_upper, orient="horizontal")
        self.sep.grid(row=15, column=0,ipadx=70, pady=10, columnspan=2)
        
        self.menu_left_upper.pack(side="top", fill="both", expand=True)
        self.menu_left_lower.pack(side="top", fill="both", expand=True)
        
        self.button_update = tk.Button(self.menu_left_upper, text="Update", command=self.__update_calc)
        self.button_update.grid(row=16, column=0, columnspan=2)

        self.sep = ttk.Separator(self.menu_left_upper, orient="horizontal")
        self.sep.grid(row=17, column=0,ipadx=70, pady=10, columnspan=2)
        
        # status bar 
        self.status_frame = tk.Frame(self.root)
        self.status = tk.Label(self.status_frame, text="Programmstatus Anzeige")
        self.status.pack(fill="both", expand=True)

        self.menu_left.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.status_frame.grid(row=4, column=0, columnspan=2, sticky="ew")

        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        # mainloop
        self.root.mainloop()

    def run(self) -> None:
        self.root.mainloop()
    def __browse_files(self) -> None:
        self.__filename = filedialog.askopenfilename(
            title="Select a File",
            filetypes=(("CSV-files", ".csv"), ("all files", ".")),
        )

        sa_e = float(self.entry_sae.get())
        sa_f = float(self.entry_saf.get())
        sa_delta_imax = float(self.entry_deltaimax.get())
        sa_t_delta_imax = float(self.entry_tdeltaimax.get())
        sa_delta_imin = float(self.entry_sadeltaimin.get())
        sa_tmax = float(self.entry_satmax.get().replace(',', '.'))
        self.__get_measurement_data() #funktionsaufruf daten einlesen, df generieren
        r_fl, l_fl, tau, size_df = calculate(self.df_measure) # funktionsaufruf berechnungen
        df_real = real_current(size_df, l_fl, r_fl, self.df_measure) # funktionsaufruf realer kurzschluss berechnen
        print(df_real)
        # funktionsaufruf schutzfunktionsanalyse
        ddl_start, ddl_stop, ddl_ausloesung = safety_function(df_real, sa_e, sa_f, sa_delta_imax, sa_t_delta_imax, sa_tmax, sa_delta_imin)
        print(f"Widerstand (r_fl): {r_fl} Ohm, Induktivität (l_fl): {l_fl} H, Tau: {tau} s")
        
        # Anzeigelinien in Plot
        points = {"Start": ddl_start, "Stop": ddl_stop, "Auslösung": ddl_ausloesung}
        self.__create_plot(df_measure=self.df_measure, df_real=df_real, points=points)

       
     

    def __get_measurement_data(self) -> None:
        # Initialisieren von Variablen und Flags
        voltageindex = 0  # Index für Spannung
        currentindex = 0  # Index für Strom
        endindex = 0      # Index für das Ende
        endflag = False   # Flag, um das Ende zu markieren
        startflag = False # Flag, um den Start zu markieren

        #ausgewählte CSV-Datei in DataFrame einlesen
        df = pd.read_csv(self.__filename, sep=",")

        #Dataframe reduzieren auf relevante Spalten und überschrift vergeben
        df = df.iloc[:, [0, 5, 10]]
        df.columns = ["Time [s]", "I Strom [A]", "U Spannung [V]"]
   
         # Überprüfen, ob das Verfahren 50V oder 600V basiert auf den ersten Zeilen
        avg_voltage_first_rows = df["U Spannung [V]"].head(50).mean()
        if avg_voltage_first_rows < 100:  # Mittelwert ersten 50 Messungen <100VDC
            Messverfahren = 1  # Merker Messverfahren = 1
        else:
            Messverfahren = 0  # Merker Messverfahren 2

        # Die Strom-Spalte in einer separaten Variable speichern
        colcurrent = df["I Strom [A]"]

        #<50 VDC Ereignissanalyse
        if Messverfahren == 1:
            # Schleife über die Zeilen des DataFrames
            for i, row in df.iterrows():
                voltage_value = row.iloc[2]  # Spannungswert für die aktuelle Zeile
                next_voltage_value = (df.iloc[i + 1]).iloc[2]  # Spannungswert für die nächste Zeile
                current_value = row.iloc[1]  # Stromwert für die aktuelle Zeile
                next_current_value = (df.iloc[i + 1]).iloc[1]  # Stromwert für die nächste Zeile

                # Bedingungen überprüfen, um den Start zu markieren von der Messung
                if (voltage_value + 1) <= next_voltage_value or (voltage_value - 1) >= next_voltage_value:
                    voltageindex = i
                    startflag = True
                if (current_value + 1) <= next_current_value or (current_value - 1) >= next_current_value:
                    currentindex = i
                    startflag = True

                # Bedingungen überprüfen, um das Ende zu markieren
                if current_value >= colcurrent.max() * 0.995 and startflag:
                    endindex = i
                    endflag = True

                # Wenn sowohl Start als auch Ende markiert wurden, die Schleife beenden
                if endflag and startflag:
                    break

            # Überprüfen, ob der Abstand zwischen Start und Ende klein genug ist
            if (currentindex - voltageindex) < 100:
                # Einen neuen DataFrame erstellen, der die relevanten Daten enthält
                    self.df_measure = df.iloc[currentindex - 50 : endindex + 50]
                    self.df_measure = self.df_measure.reset_index()
       
        #>50VDC Ereignissanalyse
        if Messverfahren != 1:
            # Schleife über die Zeilen des DataFrames
            for i, row in df.iterrows():
                current_value = row.iloc[1]  # Stromwert für die aktuelle Zeile
                next_current_value = (df.iloc[i + 1]).iloc[1]  # Stromwert für die nächste Zeile
                voltage_value = row.iloc[2]  # Spannungswert für die aktuelle Zeile
                next_voltage_value = (df.iloc[i + 1]).iloc[2]  # Spannungswert für die nächste Zeile

                # Bedingungen überprüfen, um den Start zu markieren von der Messung
                if (current_value + 2.5) <= next_current_value or (voltage_value - 2.5) >= next_voltage_value:
                    currentindex = i
                    startflag = True

                # Bedingungen überprüfen, um das Ende zu markieren
                if current_value >= colcurrent.max() * 0.995 and startflag:
                    endindex = i
                    endflag = True
                    
                # Wenn sowohl Start als auch Ende markiert wurden, die Schleife beenden
                if endflag and startflag:
                   # Einen neuen DataFrame erstellen, der die relevanten Daten enthält
                    self.df_measure = df.iloc[currentindex - 50 : endindex + 50]
                    self.df_measure = self.df_measure.reset_index() 
                    break

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
        # plot style einstellungen
        plot1.grid()
        plot1.set_title("Diagramm Kurzschluss")
        plot1.set_xlabel("Zeit [s]")
        plot1.set_ylabel("Strom [A]", color="g")
        secay = plot1.secondary_yaxis("right")
        secay.set_ylabel("Spannung [U]", color="r")

        # plot Data Messung
        plot1.plot(df_measure["Time [s]"], df_measure["U Spannung [V]"], color="r", label="Kurzschlussspanung")
        plot1.plot(df_measure["Time [s]"], df_measure["I Strom [A]"], color="g", label="Kurzschlusstrom")

        # --- Plot 2 ---
        # plot style einstellungen
        plot2.grid()
        plot2.set_title("Diagramm Berechung Kurzschluss")
        plot2.set_xlabel("Time [s]")
        plot2.set_ylabel("Strom [A]", color="g")
 

        # Minimale und maximale Zeitwerte aus df_real abrufen
        x_min = df_real["Time [s]"].min()
        x_max = df_real["Time [s]"].max()

        # Grenzen der x-Achse für plot2 festlegen
        plot2.set_xlim(x_min, x_max)

        # plot data Dataframe df_real
        plot2.plot(df_real["Time [s]"], df_real["I Strom [A]"], color="g", label="Kurzschlusstrom")

        # Linienbeschriftung
        yMin, yMax = plot2.get_ylim()
        yMean = (yMax - yMin) * 0.75 #Beschriftungsposition festlegen auf 75% höhe

        for text, pos in points.items():
            plot2.axvline(x=pos, linestyle="--")
            plot2.text(pos, yMean, text, ha='center', va='center',rotation='vertical', bbox={'facecolor':'white', 'pad':4})

        # platzieren der Ausgabefenster
        canvas1.get_tk_widget().grid(column=1, row=3, columnspan=5, pady=5)
        canvas.get_tk_widget().grid(column=1, row=1, columnspan=5, pady=5)
        
    def __update_calc(self) -> None:
        # Updaten der Schutzanalyse
        sa_e = float(self.entry_sae.get())
        sa_f = float(self.entry_saf.get())
        sa_delta_imax = float(self.entry_deltaimax.get())
        sa_t_delta_imax = float(self.entry_tdeltaimax.get())
        sa_delta_imin = float(self.entry_sadeltaimin.get())
        sa_tmax = float(self.entry_satmax.get().replace(',', '.'))

        # neuaufruf 
        self.__get_measurement_data()  # Funktionsaufruf daten einlesen, df generieren
        r_fl, l_fl, tau, size_df = calculate(self.df_measure) # Funktionsaufruf berechnungen
        df_real = real_current(size_df, l_fl, r_fl, self.df_measure) # Funktionsaufruf realer kurzschluss berechnen
        
        # Funktionsaufruf schutzfunktionsanalyse
        ddl_start, ddl_stop, ddl_ausloesung = safety_function(df_real, sa_e, sa_f, sa_delta_imax, sa_t_delta_imax, sa_tmax, sa_delta_imin)

        # Update plot
        points = {"Start": ddl_start, "Stop": ddl_stop, "Auslösung": ddl_ausloesung}
        self.__create_plot(df_measure=self.df_measure, df_real=df_real, points=points)
