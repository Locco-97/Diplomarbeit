# calc.py

import numpy as np

def calculate(df):
    
    # suchen I_max
    colcurrent = df["I Strom [A]"]
    I_max = colcurrent.max()

    
    # abfragen der Zeit in Zeile 50 (Start Ereigniss)
    start_time = df.iloc[50]["Time [s]"]
    # spannung vor der Belastung abfragen
    u_0 = df.iloc[25]["U Spannung [V]"]
    # spannung bei I_max abfragen
    u_l = df.iloc[colcurrent.max()]["U Spannung [V]"]
    # Spannungsabfall über der FL und Gleis berechnen
    voltage = (u_0 - u_l)
        
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
    
    print(f"R_FL: {r_fl}")
    print(f"L_FL: {l_fl}")
    print(f"Tau: {tau}")
    # rückgabewerte
    return r_fl, l_fl, tau
