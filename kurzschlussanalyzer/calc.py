# calc.py

import numpy as np

def calculate(df, voltage=600):
    # Finde die Zeit in Zeile 50
    start_time = df.iloc[50]["Time [s]"]
    
    # Berechne I_max
    colcurrent = df["I Strom [A]"]
    I_max = colcurrent.max()
    r_fl = (voltage / I_max)
    
    # Berechne r_fl
    for _, row in df.iterrows():
        current_value = row["I Strom [A]"]
        if current_value >= I_max:
            shortcurrent = current_value
            r_fl = (voltage / shortcurrent)
            break  # Beende die Schleife, sobald I_max erreicht ist

    # Finde die Zeit, wenn der Strom 63% von I_max erreicht
    target_current = 0.63 * I_max
    for _, row in df.iterrows():
        current_value = row["I Strom [A]"]
        if current_value >= target_current:
            tau = row["Time [s]"] - start_time
            break  # Beende die Schleife, sobald 63% von I_max erreicht ist

    # Berechne l_fl
    i_tau = colcurrent.max() * 0.63
    l_fl = (-r_fl * tau) / np.log(1 - (i_tau / shortcurrent))
    
    # rückgabe
    return r_fl, l_fl, tau
