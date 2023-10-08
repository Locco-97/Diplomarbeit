# calc.py

import numpy as np
import pandas as pd


def calculate(df):

    # eigene Datenreihe mit den Stromwerten erstellen
    colcurrent = df["I Strom [A]"]
    #groesster Stromwert im df suchen und in die variable kopieren
    i_max = df["I Strom [A]"].max()
    #groesse vom df auslesen und in variable schreiben
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
    # Trigger standardmäßig auf keine Ausloesung setzen
    trigger_type = 0
    
    # F und E werden angepasst an die Messaufloesung von 20kHz, Eingabe sa_E & sa_F erfolgt in A/ms (*1000 --> pro Sekunde/ 20000 --> 20kHz im df)
    sa_E = ((sa_E*1000) / 20000)
    sa_F = ((sa_F*1000) / 20000)

    # Finden des Startzeitpunkts der Analyse, wo der Anstieg steiler als E ist
    start_time_indices = df_real[df_real['Delta_I'] >= sa_E].index

    # Überprüfen, ob ein Startzeitpunkt existiert
    if not start_time_indices.empty:
        ddl_start_index = start_time_indices[0]
        ddl_start_time = df_real.loc[ddl_start_index, 'Time [s]']
    else:
        trigger_type = 0
        ddl_start_time = None

    # Ausloesezeit
    t_trigger = None  # Setze den Standardwert auf None, falls keine Ausloesung erfolgt

    delta_I = df_real['I Strom [A]'].diff().abs() #erstellt datenreihe mit differenz zum jeweils vorgängigen wert
    sum_delta_I = delta_I.cumsum()  # erstellt datenreihe mit summe zum jeweils fortlaufenden wert im df
    trigger_index = sum_delta_I[sum_delta_I > sa_Delta_Imax].index #gibt die zeilennummer zurück in welcher zeile die summe groesser als das delta_imax ist
    
    # Überprüft, ob es zur Ausloesung kommt, und speichert die Zeit (durch den trigger_index) in die t_trigger-Variable
    trigger_index = sum_delta_I[sum_delta_I > sa_Delta_Imax].index
    if not trigger_index.empty:
        # Überprüfen, ob der Anstieg immer noch steiler als sa_F ist
        if delta_I.loc[trigger_index[0]] >= sa_F:
            t_trigger = df_real.loc[trigger_index[0], 'Time [s]']
            trigger_type = 1 #status setzten auf delta i max ausloesung
        else:
            # Der Anstieg ist nicht steil genug delta_imax loest nicht aus! status setzten
            trigger_type = 0

    #Teil 2 (DDL+ Delta T) und Sperrschwelle (Delta Imin)
    if ddl_start_time is not None:
        t_max = ddl_start_time + sa_Tmax
        trigger_index = df_real[df_real['Time [s]'] == t_max].index
        # Überprüfung, ob die Steigung nach t_max immer noch größer oder gleich sa_F ist
        if delta_I.loc[trigger_index[0]] >= sa_F:
            if df_real.loc[trigger_index[0], 'Time [s]'] < trigger_time: #überprüfen ob dieser schutz zuerst ausloest
                t_trigger = df_real.loc[trigger_index[0], 'Time [s]']
                trigger_type = 2 #status setzten auf Tmax ausloesung
        else:
            # es kommt zu keiner ausloesung
            trigger_type = 0  # Setz den status auf keine ausloesung


        if trigger_time is not None:
        # Finden des Index für die trigger_time
            trigger_index = df_real[df_real['Time [s]'] == trigger_time].index
    
        # Überprüfen, ob der Stromwert zum Zeitpunkt der trigger_time größer als sa_Delta_imin ist
        if not df_real.loc[trigger_index[0], 'I Strom [A]'] > sa_Delta_imin:
        # Stromwert nicht ist größer als sa_Delta_imin, es passiert nichts
            trigger_type = 0
            trigger_time = None
        

    # Berechnung der Stopzeit, falls die Analyse gestoppt wird
    for idx, row in df_real.iterrows():
        if row['Time [s]'] >= ddl_start_time:
            if row['Delta_I'] < sa_F:
                ddl_stop_time = row['Time [s]']
                trigger_type = 0
                break

    return ddl_start_time, ddl_stop_time, t_trigger, trigger_type





