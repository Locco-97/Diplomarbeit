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


def real_current(size_df, l_fl, r_fl, df, u_last):
    # Maximale Spannung ermitteln
    u_max = df["U Spannung [V]"].max()
    
    # Wenn die maximale Spannung unter 100 ist, setzen wir u_last auf den manuell eingegebenen Wert (für Messmethode Variante 1)
    if u_max < 100:
        u_max = u_last
    
    # Realen Strom berechnen
    i_real = u_max / r_fl
    
    # df erweitern für den Fall, dass die manuelle Eingabe verwendet wird... Wenn keine Messung existiert
    size_df = size_df * 1.5
    
    
    # Erstellen eines DataFrames für den realen Kurzschluss,
    # bei dem die ersten 50 Zeitschritte negative Werte haben
    data = {"Time [s]": np.arange(-0.0025, (size_df * 0.00005) - 0.0025, 0.00005)}
    df_real = pd.DataFrame(data, columns=["Time [s]", "I Strom [A]"])
    
    # Werte für die ersten 50 Zeilen explizit auf 0 setzen
    df_real.loc[:49, ["I Strom [A]"]] = 0
    
    # Berechnen und Zuweisen der tatsächlichen Werte ab dem Index 50
    df_real.loc[50:, "I Strom [A]"] = df_real.loc[50:, "Time [s]"].apply(lambda t: i_real * (1 - np.exp((-r_fl / l_fl) * t)))

    # Finden Sie den Index, an dem "I Strom [A]" 99% erreicht
    idx_99_percent = (df_real["I Strom [A]"] >= 0.9999 * df_real["I Strom [A]"].max()).idxmax()
    # Kürzen Sie das DataFrame ab diesem Index
    df_real = df_real.loc[:idx_99_percent].copy()
    
    return df_real


def safety_function(df_real, sa_E, sa_F, sa_Delta_Imax, sa_t_Delta_Imax, sa_Tmax, sa_Delta_imin):
    # Trigger standardmässig auf keine Auslösung setzen
    trigger_type = 0
    ddl_start_time = None
    t_trigger = None
    trigger_time = None

    
    # F und E werden angepasst an die Messaufloesung von 20kHz, Eingabe sa_E & sa_F erfolgt in A/ms (*1000 --> pro Sekunde/ 20000 --> 20kHz im df)
    sa_E = ((sa_E*1000) / 20000)
    sa_F = ((sa_F*1000) / 20000)

    
    df_real["delta I"] = df_real["I Strom [A]"].diff()  # Erstellt Datenreihe mit Differenz zum jeweils vorherigen Wert
   
    ddl_start_time = None
    start_flag = False

    for index, row in df_real.iterrows():
        if row["delta I"] >= sa_E:
            ddl_start_time = row["Time [s]"]
            start_flag = True
            print("analyse gestartet")
            break
    
    if not start_flag:
        trigger_type = 0
        ddl_start_time = None
        ddl_stop_time = None
        t_trigger = None
        print("analyse nicht gestartet")
        return ddl_start_time, ddl_stop_time, t_trigger, trigger_type
    
    if sa_Tmax >= sa_t_Delta_Imax:
        ddl_max_time = ddl_start_time + sa_Tmax
    else:
        ddl_max_time = ddl_start_time + sa_t_Delta_Imax 
    
    print(df_real)
    
    # Erstellt eine leere Spalte "sum delta I"
    df_real["sum delta I"] = 0.0
    
    # Beginnt ab dem Startwert und kumuliert die Summe der Differenzen
    cum_sum_started = False
    cum_sum = 0
    for index, row in df_real.iterrows():
        if not cum_sum_started and row["delta I"] >= sa_E:
            cum_sum_started = True
        if cum_sum_started:
            cum_sum = cum_sum + row["delta I"]
        df_real.at[index, "sum delta I"] = cum_sum
    print(df_real)
    
    if df_real["sum delta I"].gt(sa_Delta_Imax).any():
        trigger_time = df_real.loc[df_real["sum delta I"] >= sa_Delta_Imax, "Time [s]"].min()

    else:
        trigger_type = 6
    
    #trigger_time = df_real.loc[df_real["sum delta I"] > sa_Delta_Imax, "Time [s]"].min()
    print("start df real neu",df_real[df_real["Time [s]"] == trigger_time])

    
    
    #wenn ein wert gefunden wurde
    if trigger_time is not None:
        print("trigger_time != None", trigger_time)
        #verzoegerung zeit bilden
        trigger_time = trigger_time + sa_t_Delta_Imax 
        print("trigger_time 2", trigger_time)    
        #gibt den am nächsten liegenden wert nach der verzoegerung der delta I summe zurück
        nearest_sum_delta_I = df_real.loc[df_real["Time [s]"].sub(trigger_time).abs().idxmin(), "sum delta I"]
        
        print(nearest_sum_delta_I, "trigger 1!!!!!!!!") 
        if nearest_sum_delta_I is not None:
            #ueberpruefen ob delta I noch immer groesser delta I max ist
            if nearest_sum_delta_I >= sa_Delta_Imax:
                # Die Bedingung ist nach der Verzögerung immer noch erfüllt
                t_trigger = trigger_time  # Zeitpunkt nach der Verzögerung
                trigger_type = 1  # Setze trigger_type auf 1
                print("trigger type 1", trigger_type)
        else: 
            t_trigger = None
            trigger_type = 0

    # Teil 2 (DDL+ Delta T) und Sperrschwelle (Delta Imin)
    if ddl_start_time is not None:
        #Live Strom nach verzögerung Tmax abfragen
        t_max = ddl_start_time + sa_Tmax
        #nächstliegender Stromwert nach der Verzögerung suchen
        trigger_time = df_real.loc[df_real["Time [s]"].sub(t_max).abs().idxmin(), "Time [s]"]
        print(trigger_time, "2!!!!!!!!!")
        delta_I_delayed  = df_real.loc[df_real["Time [s]"] == trigger_time, "delta I"].values[0]
        print("Triggertime Analyse 2")

        # Überprüfung, ob die Steigung nach t_max immer noch grösser oder gleich sa_F ist
        if delta_I_delayed >= sa_F:
            if t_trigger is not None:
                if trigger_time < t_trigger:  # Überprüfen ob dieser Schutz zuerst auslöst
                    t_trigger = trigger_time
                    trigger_type = 2  # Status setzen auf Delta T Auslösung
            else:
                t_trigger = trigger_time
                trigger_type = 2  # Status setzen auf Delta T Auslösung
        if delta_I_delayed < sa_F and t_trigger is None:
            trigger_type = 7

    # Berechnung der Stopzeit, falls die Analyse gestoppt wird
    if ddl_start_time is not None:
        for idx, row in df_real.iterrows():
            if row['Time [s]'] >= ddl_start_time and row['Time [s]'] <= ddl_max_time:
                if row['delta I'] < sa_F:
                    ddl_stop_time = row['Time [s]']
                    trigger_type = 4
                    t_trigger = None
                    break
            else:
                ddl_stop_time = None
                
    #Stromwert zum Zeitpunkt der ausloesung abfragen, falls zeit in t_trigger geschrieben wurde und anschliessend Imin überprüfen
    if t_trigger is not None:
        live_current = df_real.loc[df_real["Time [s]"].sub(t_trigger).abs().idxmin(), "I Strom [A]"]
        if not live_current > sa_Delta_imin:
            trigger_type = 5
            t_trigger = None


    return ddl_start_time, ddl_stop_time, t_trigger, trigger_type






