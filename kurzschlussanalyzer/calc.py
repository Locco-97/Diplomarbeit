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


def real_current(size_df, l_fl, r_fl, df):
    
    # Maximale Spannung ermitteln
    u_max = df["U Spannung [V]"].max()
    
    # Wenn die maximale Spannung unter 500 ist, setzen wir u_max auf 600V (bei älterer Messmethode)
    if u_max < 500:
        u_max = 600
    
    # Realen Strom berechnen
    i_real = u_max/r_fl
    
    # Erstellen eines DataFrames für den realen Kurzschluss,
    # bei dem die ersten 50 Zeitschritte negative Werte haben
    data = {"Time [s]": np.arange(-0.0025, (size_df * 0.00005) - 0.0025, 0.00005)}
    df_real = pd.DataFrame(data, columns=["Time [s]", "I Strom [A]", "U Spannung [V]"])
    
    # Werte für die ersten 50 Zeilen explizit auf 0 setzen
    df_real.loc[:49, ["I Strom [A]", "U Spannung [V]"]] = 0
    
    # Berechnen und Zuweisen der tatsächlichen Werte ab dem Index 50
    df_real.loc[50:, "I Strom [A]"] = df_real.loc[50:, "Time [s]"].apply(lambda t: i_real * (1 - np.exp((-r_fl / l_fl) * t)))
    
    # Berechnen der Zeitableitung des Stroms
    df_real['Delta_I'] = df_real['I Strom [A]'].diff().fillna(0)
    
    return df_real


def safety_function(df_real, sa_E, sa_F, sa_Delta_Imax, sa_t_Delta_Imax, sa_Tmax, sa_Delta_imin):

    extracted_rows = df_real.iloc[45:61]
    # Gib die ausgewählten Zeilen im Terminal aus (Start Kurzschluss)
    print(extracted_rows)
    
    # F und E werden angepasst an die Messauflösung von 20kHz
    sa_E = (sa_E / 20)
    sa_F = (sa_F / 20)


    # Finden des Startzeitpunkts der Analyse
    start_time_indices = df_real[df_real['Delta_I'] >= sa_E].index

    # Überprüfen, ob ein Startzeitpunkt existiert
    if not start_time_indices.empty:
        ddl_start_index = start_time_indices[0]
        ddl_start_time = df_real.loc[ddl_start_index, 'Time [s]']
    else:
        print("Kein Startzeitpunkt gefunden.")
        return None, None, None

    # Relevanter Datenbereich
    relevant_df = df_real[(df_real['Time [s]'] >= ddl_start_time) &
                          (df_real['Time [s]'] <= ddl_start_time + sa_t_Delta_Imax)]

    # Auslösezeit
    t_Ausloesen = ddl_start_time + sa_t_Delta_Imax  # Setze Standardwert für den Fall, dass die if-Bedingung nicht erfüllt ist
    if not relevant_df.empty:
        delta_I = relevant_df['I Strom [A]'].diff().abs()
        sum_delta_I = delta_I.cumsum()
        trigger_index = sum_delta_I[sum_delta_I > sa_Delta_Imax].index

        if not trigger_index.empty:
            t_Ausloesen = relevant_df.loc[trigger_index[0], 'Time [s]']

    # Ausgabe der Ergebnisse
    print("Start Time:", ddl_start_time)
    print("Stop Time (falls flacher wird):", ddl_start_time + sa_t_Delta_Imax)
    print("Auslösungszeit (falls stärkerer Anstieg):", t_Ausloesen)

    # Tmax-Schutz
    if ddl_start_time is not None:
        t_max = ddl_start_time + sa_Tmax
        if t_max < relevant_df['Time [s]'].max():
            print("Tmax-Schutz ausgelöst.")

    return ddl_start_time, ddl_start_time + sa_t_Delta_Imax, t_Ausloesen









 
    


"""

        # Analyse des df_real DataFrames
        result = safety_function(df_real, 1e3, 1e3, 1, 5)
        if result:
            print(f"Auslösung aktiviert bei {result} s")
        else:
            print("Keine Auslösung aktiviert.")

"""