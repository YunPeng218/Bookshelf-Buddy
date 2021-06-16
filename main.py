import tkinter as tk
from login import *
from tkinter.messagebox import *

status=0
def disable_event():
    global status
    ask = askyesno ('Confirmation','Are you sure you want to exit?')
    if ask:
        status=1
        start.destroy()
            
while status==0:
    start = tk.Tk()
    start.geometry('1000x740')
    start.title('Bookshop System')
    start.resizable(False, False)
    start.protocol("WM_DELETE_WINDOW", disable_event)
    login_panel(start)
    start.mainloop()