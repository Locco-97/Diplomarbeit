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

def real_current(size_df, l_fl, r_fl):
    i_real = 600/r_fl
    data = {"Time [s]": np.arange(0, size_df * 0.00005, 0.00005)}
    #Dataframe zum realen kurzschluss erstellen
    df_real = pd.DataFrame(data, columns=["Time [s]", "I Strom [A]", "U Spannung [V]"])
    df_real["I Strom [A]"] = df_real["Time [s]"].apply(lambda t: i_real * (1 - np.exp((-r_fl / l_fl) * t)))
    print("test df 1")
    print(df_real)
    return df_real
