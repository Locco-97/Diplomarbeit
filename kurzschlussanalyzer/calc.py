# calc.py

import numpy as np
import pandas as pd




def calculate(df):

    # suchen I_max
    colcurrent = df["I Strom [A]"]
    #global i_max
    i_max = colcurrent.max()
    #global size_df 
    size_df = len(df)
    
    # abfragen der Zeit in Zeile 50 (Start Ereigniss)
    start_time = df.iloc[50]["Time [s]"]
    print(start_time)
    # spannung vor der Belastung abfragen
    u_0 = df.iloc[25]["U Spannung [V]"]      
    
    # spannung bei I_max abfragen
    index_i_max = df["I Strom [A]"].idxmax()
    u_l = df.iloc[index_i_max]["U Spannung [V]"]
    
    # abfrage um alte Messmethode zu erkennen und Spannung im endzustand zu nehmen
    if u_0 <= 1:
        voltage = u_l
    else: 
        voltage = (u_0 - u_l)# Spannungsabfall über der FL und Gleis berechnen wenn neue Messmethode verwendet wird
    
        
    # Berechne r_fl
    r_fl = (voltage / i_max)

    # Findet die Zeit, wenn der Strom 63% von I_max erreicht (1 Tau)
    target_current = 0.63 * i_max
    for _, row in df.iterrows():
        current_value = row["I Strom [A]"]
        if current_value >= target_current:
            tau = row["Time [s]"] - start_time
            break  # Beende die Schleife, sobald 63% von I_max erreicht ist

    # Berechne l_fl
    i_tau = colcurrent.max() * 0.63
    l_fl = (-r_fl * tau) / np.log(1 - (i_tau / i_max))

    
    # rückgabewerte
    return r_fl, l_fl, tau, size_df

def real_current(size_df, l_fl, r_fl,df):
    """"
    u_max = df["U Spannung [V]"].max()
    i_real = u_max/r_fl
    data = {"Time [s]": np.arange(0, size_df * 0.00005, 0.00005)}
    #Dataframe zum realen kurzschluss erstellen
    df_real = pd.DataFrame(data, columns=["Time [s]", "I Strom [A]", "U Spannung [V]"])
    df_real["I Strom [A]"] = df_real["Time [s]"].apply(lambda t: i_real * (1 - np.exp((-r_fl / l_fl) * t)))
    """
    data = {"Time [s]": np.arange(0, len(df) * 0.00005, 0.00005)}

    # Dataframe zum realen kurzschluss erstellen
    df_real = pd.DataFrame(data, columns=["Time [s]", "I Strom [A]", "U Spannung [V]"])

    # Füge die Werte von "U Spannung [V]" aus dem ursprünglichen df hinzu
    df_real["U Spannung [V]"] = df["U Spannung [V]"].values

    # Berechne "I Strom [A]" für jeden Zeitpunkt unter Verwendung der aktuellen Spannung
    df_real["I Strom [A]"] = df_real.apply(lambda row: (row["U Spannung [V]"]/r_fl) * (1 - np.exp((-r_fl / l_fl) * row["Time [s]"])), axis=1)

    print("test df 1")
    print(df_real)
    return df_real
    
""" 
def safety_function(df_real):
    ddl_start =0
    ddl_stop = 0
    
    df_real['Delta_I'] = df_real['I Strom [A]'].diff()
    # Den ersten Zeitpunkt finden, an dem der Unterschied größer als 0.25A ist
    ddl_start_row = df_real[df_real['Delta_I'] > 20].iloc[0]

    ddl_start = ddl_start_row['Time [s]']
    return ddl_start, ddl_stop """

""""
def safety_function(df_real, E, F, Delta_Imax, t_Delta_Imax):
    # Berechnung des Stromanstiegs
    df_real['di/dt'] = df_real['I Strom [A]'].diff() / (df_real['Time [s]'].diff())

    # Finden des Startzeitpunkts der Analyse (wo di/dt > E)
    start_time = df_real[df_real['di/dt'] > E]['Time [s]'].iloc[0]

    # Finden des Endzeitpunkts der Analyse (wo di/dt < F nach start_time)
    #end_time = df_real[(df_real['di/dt'] < F) & (df_real['Time [s]'] > start_time)]['Time [s]'].iloc[0]

    # Überprüfen, ob Delta I den Wert Delta_Imax während der Analysezeit übersteigt
    max_delta_I = df_real[(df_real['Time [s]'] >= start_time) & (df_real['Time [s]'] <= end_time)]['I Strom [A]'].diff().max()

    if max_delta_I > Delta_Imax:
        trigger_time = df_real[df_real['I Strom [A]'].diff() == max_delta_I]['Time [s]'].iloc[0]

        # Überprüfen, ob der Stromwert nach der Verzögerung t_Delta_Imax immer noch über Delta_Imax liegt
        time_after_delay = trigger_time + (t_Delta_Imax / 1000)  # Konvertierung von ms in s
        current_after_delay = df_real[df_real['Time [s]'] == time_after_delay]['I Strom [A]'].iloc[0]

        if current_after_delay - df_real[df_real['Time [s]'] == trigger_time]['I Strom [A]'].iloc[0] > Delta_Imax:
            return trigger_time
        else:
            return None
    else:
        return None


    # Analyse des df_real DataFrames
    result = safety_function(df_real, 1e3, 1e3, 1, 5)
    if result:
        print(f"Auslösung aktiviert bei {result} s")
    else:
        print("Keine Auslösung aktiviert.")

"""