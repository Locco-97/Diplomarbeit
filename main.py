from tkinter import*
import tkinter.ttk
from tkinter import filedialog
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import pandas as pd



# Ein Fenster erstellen
window = Tk()
x_window=600
y_window=600

window.geometry(f'{x_window}x{y_window}')
window.minsize(x_window,y_window)
window.maxsize(x_window,y_window)
#window.columnconfigure(0, weight=4)
#window.rowconfigure(0, weight=12)


def browseFiles():
    filename = filedialog.askopenfilename(
        #initialdir="/",
        title="Select a File",
        filetypes=(("CSV-files", ".csv"), ("all files", ".")),
    )

    df = pd.read_csv (filename, sep=",")

    voltageindex = 50
    df = df[["Time [s]","I Strom [A]", "U Spannung [V]"]]

    colvoltage = df ["U Spannung [V]"]
    colcurrent = df ["I Strom [A]"]
    currentindex = 0
    voltageindex = 0
    endindex = 0
    endflag = False
    startflag = False
    
 
    for i, row in df.iterrows():
        nextvoltagevalue = df.iloc[i+1][2]
        nextcurrentvalue = df.iloc[i+1][1]
        if  (row[2]+1) <= nextvoltagevalue or (row[2]-1) >= nextvoltagevalue:
            voltageindex = i
            startflag = True
        if  (row[1]+1) <= nextcurrentvalue or (row[1]-1) >= nextcurrentvalue:
            currentindex = i
            startflag = True
            
        if row[1] >= colcurrent.max()*0.99 and startflag:
            endindex = i
            endflag = True
        
        
        if i %1 == 0:
            print(f"index: {i}\nmeanvoltagevalue: {nextvoltagevalue} - rowvoltage{row[2]}\nmeancurrentvalue: {nextcurrentvalue} - rowcurrent{row[1]}")   
        if endflag and startflag:
            break
         
    if (currentindex - voltageindex) < 10:
        df = df.iloc[currentindex-50:endindex+50]

    
    # Change label contents
    label_file_explorer.configure(text="File Opened: " + filename)

# Explorer Taste erstellen
label_file_explorer = Label(
    window, text="File Explorer using Tkinter", width=100, height=4, fg="blue"
)




# Den Fenstertitle erstellen
window.title("Diplomarbeit M-Thoma - FL-Rechner")
button =Button(window, text='explorer', width=15, command=browseFiles)
button.grid(column=0, row=0)

t1 = Label(window,text ='R\u1D65 Eingabe:') #u1D65 UNICODE für tiefgestelltes V
t1.grid(column=0, row=1, sticky=W)
e1 = Entry(window)
e1.grid(column=0, row=2, sticky=W)

t2 = Label(window,text = 'L\u1D65 Eingabe:' ) #u1D65 UNICODE für tiefgestelltes V
t2.grid(column=0, row=3, sticky=W)
e3 = Entry(window)
e3.grid(column=0, row=4, sticky=W)

t4 = Label(window,text = 'U\u2080 GR Eingabe:')
t4.grid(column=0, row=5, sticky=W)
e4 = Entry(window)
e4.grid(column=0, row=6, sticky=W)


t5 = Label(window,text = 'Leitungswiderstand:')
t5.grid(column=0, row=7, sticky=W)

t6 = Label(window,text = 'Leitungsinduktivität:')
t6.grid(column=0, row=8, sticky=W)

t7 = Label(window,text = 'IK0:',)
t7.grid(column=0, row=9, sticky=W)

t8 = Label(window,text = 'Zeit für 3T',)
t8.grid(column=0, row=10, sticky=W)

t9 = Label(window,text = 'max Steigung A/ms:',)
t9.grid(column=0, row=11, sticky=W)

# the figure that will contain the plot
fig = Figure(figsize = (4, 2),
                dpi = 100)

# list of squares
y = [i**2 for i in range(101)]

# adding the subplot
plot1 = fig.add_subplot(111)

# plotting the graph
#plot1.plot(df[0],df[1])

canvas = FigureCanvasTkAgg(fig, master = window)  
canvas.draw()
canvas1 = FigureCanvasTkAgg(fig, master = window)  
canvas1.draw()  
  
# placing the canvas on the Tkinter window
canvas.get_tk_widget().grid(column=2,row=0,rowspan=6,columnspan=3,pady=5)
canvas1.get_tk_widget().grid(column=2,row=7,rowspan=6,columnspan=3,pady=5)

tkinter.ttk.Separator(window, orient=VERTICAL).grid(column=1, row=0, rowspan=13, sticky='ns',padx=5)

window.mainloop()# In der Ereignisschleife auf Eingabe des Benutzers warten.