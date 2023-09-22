# calc.py

import numpy as np
import pandas as pd


def calculate(df):

    # suchen I_max
    colcurrent = df["I Strom [A]"]
    #global i_max
    i_max = df["I Strom [A]"].max()
    #global size_df 
    size_df = len(df)
    
    # abfragen der Zeit in Zeile 50 (Start Ereigniss)
    start_time = df.iloc[50]["Time [s]"]
    # spannung vor der Belastung abfragen
    u_0 = df.iloc[25]["U Spannung [V]"]      
    
    # spannung bei I_max abfragen
    index_i_max = df["I Strom [A]"].idxmax()
    u_l = df.iloc[index_i_max]["U Spannung [V]"]
    
    # abfrage um alte Messmethode zu erkennen und Spannung im endzustand zu nehmen
    if u_0 <= 1:
        voltage = u_l
    else: 
        u_max = df["U Spannung [V]"].max()
        voltage = (u_max - u_l)# Spannungsabfall über der FL und Gleis berechnen wenn neue Messmethode verwendet wird
        print(voltage)
        
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
    i_1tau = colcurrent.max() * 0.63
    l_fl = (-r_fl * tau) / np.log(1 - (i_1tau / i_max))

    
    # rückgabewerte
    return r_fl, l_fl, tau, size_df

def real_current(size_df, l_fl, r_fl,df):
    
    u_max = df["U Spannung [V]"].max()
    i_real = u_max/r_fl
    data = {"Time [s]": np.arange(0, size_df * 0.00005, 0.00005)}
    #Dataframe zum realen kurzschluss erstellen
    df_real = pd.DataFrame(data, columns=["Time [s]", "I Strom [A]", "U Spannung [V]"])
    df_real["I Strom [A]"] = df_real["Time [s]"].apply(lambda t: i_real * (1 - np.exp((-r_fl / l_fl) * t)))
    return df_real
    
""""
def safety_function(df_real):
    ddl_start =0
    ddl_stop = 0
    
    df_real['Delta_I'] = df_real['I Strom [A]'].diff()
    # Den ersten Zeitpunkt finden, an dem der Unterschied größer als 0.20A ist
    ddl_start_row = df_real[df_real['Delta_I'] > 5].iloc[0]

    ddl_start = ddl_start_row['Time [s]']
    return ddl_start, ddl_stop 
"""

def safety_function(df_real, E, F, Delta_Imax, t_Delta_Imax):
    # Berechnung des Stromanstiegs
    df_real['di/dt'] = df_real['I Strom [A]'].diff() / (df_real['Time [s]'].diff())

    # Finden des Startzeitpunkts der Analyse (wo di/dt > E)
    start_time = df_real[df_real['di/dt'] > E]['Time [s]'].iloc[0]

    # Überwachungszeitraum festlegen
    end_time = start_time + t_Delta_Imax
    relevant_df = df_real[(df_real['Time [s]'] >= start_time) & (df_real['Time [s]'] <= end_time)]
    
    # Überprüfen, ob Delta I den Wert Delta_Imax während der Analysezeit übersteigt
    max_delta_I = relevant_df['I Strom [A]'].diff().max()

    if max_delta_I > Delta_Imax:
        trigger_time = relevant_df[relevant_df['I Strom [A]'].diff() == max_delta_I]['Time [s]'].iloc[0]
        
        # 2. Überprüfen, ob die Steigung innerhalb des Zeitraums flacher wird als F
        stop_time = relevant_df[relevant_df['di/dt'] < F]['Time [s]'].iloc[0] if any(relevant_df['di/dt'] < F) else None

        if stop_time:
            print("Analyse gestoppt bei Zeit:", stop_time)
        else:
            print("Auslösezeit (da die Steigung nicht flacher als F wurde):", end_time)
    else:
        # 3. Überprüfen, ob die Steigung innerhalb dieses Zeitraums flacher wird
        stop_time = relevant_df[relevant_df['di/dt'] < E]['Time [s]'].iloc[0] if any(relevant_df['di/dt'] < E) else None

        # 4. Überprüfen, ob der Stromanstieg länger dauert als t_Delta_Imax
        activation_time_index = relevant_df[relevant_df['I Strom [A]'].diff() > Delta_Imax]['Time [s]'].index
        if not activation_time_index.empty:
            activation_time = relevant_df.loc[activation_time_index[0], 'Time [s]']
            time_difference = activation_time - start_time

            if time_difference > t_Delta_Imax:
                print("Der Anstieg dauert länger als t_Delta_Imax!")
        else:
            activation_time = None

        print("Start Time:", start_time)
        print("Stop Time (falls flacher wird):", stop_time)
        print("Auslösungszeit (falls stärkerer Anstieg):", activation_time)
    
    # Überprüfen, ob ddl_stop None ist und entsprechend den letzten Zeitwert von df_real setzen
    ddl_stop = stop_time if stop_time != None else df_real['Time [s]'].iloc[-1]
    
    ddl_start = start_time
           
    return ddl_start, ddl_stop 


"""

        # Analyse des df_real DataFrames
        result = safety_function(df_real, 1e3, 1e3, 1, 5)
        if result:
            print(f"Auslösung aktiviert bei {result} s")
        else:
            print("Keine Auslösung aktiviert.")

"""