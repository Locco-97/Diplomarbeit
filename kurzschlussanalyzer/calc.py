voltage = 600 #Testwert

import numpy
from numpy import log

def calculate(self,voltage):
    df = self.__dataframefinal #Dataframefinal wird in df(dataframe) kopiert für private Methode
    
    colcurrent = df["I Strom [A]"]
    for i, row in df.iterrows():
        current_value = row.iloc[1]
        current_value >= colcurrent.max()
        shortcurrent = current_value
        r_fl = (voltage/shortcurrent)
        
    colcurrent = df["I Strom [A]"]
    for i, row in df.iterrows():
        current_value = row.iloc[1]
        current_value >= colcurrent.max() * 0.63
        current_half = row.iloc[1]
        l_fl = (-(r_fl*tau)/log(1-(current_half/shortcurrent)))
    



  