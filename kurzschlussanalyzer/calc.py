# calc.py

import numpy as np
import pandas as pd

def calculate(df):
    
    # suchen I_max
    colcurrent = df["I Strom [A]"]
    I_max = colcurrent.max()
    df_size = len(df)
    
    # abfragen der Zeit in Zeile 50 (Start Ereigniss)
    start_time = df.iloc[50]["Time [s]"]
    print(start_time)
    # spannung vor der Belastung abfragen
    u_0 = df.iloc[25]["U Spannung [V]"]      
    
    # spannung bei I_max abfragen
    index_i_max = df["I Strom [A]"].idxmax()
    print(index_i_max)
    print(df)
    u_l = df.iloc[index_i_max]["U Spannung [V]"]
    print(u_l)
    
    # abfrage um alte Messmethode zu erkennen und Spannung im endzustand zu nehmen
    if u_0 <= 1:
        voltage = u_l
    else: 
        voltage = (u_0 - u_l)# Spannungsabfall über der FL und Gleis berechnen wenn neue Messmethode verwendet wird
    
        
    # Berechne r_fl
    r_fl = (voltage / I_max)

    # Findet die Zeit, wenn der Strom 63% von I_max erreicht (1 Tau)
    target_current = 0.63 * I_max
    for _, row in df.iterrows():
        current_value = row["I Strom [A]"]
        if current_value >= target_current:
            tau = row["Time [s]"] - start_time
            break  # Beende die Schleife, sobald 63% von I_max erreicht ist

    # Berechne l_fl
    i_tau = colcurrent.max() * 0.63
    l_fl = (-r_fl * tau) / np.log(1 - (i_tau / I_max))
    
    data = {"Timer [s]": np.arange(0, df_size * 0.00005, 0.00005)}
    #Dataframe zum realen kurzschluss erstellen
    df_real = pd.DataFrame(data, columns=["Time [s]", "I Strom [A]", "U Spannung [V]"])

    print(df_real)

    # rückgabewerte
    return r_fl, l_fl, tau
