"""
TEST FILE TO TRY USING TREEVIEW. NOT A WORKING FILE
"""

import pandas as pd
from tkinter import *
import tkinter as tk
import tkinter.font as tkFont
from tkinter import filedialog, messagebox, ttk
from datetime import datetime
from datetime import timedelta


root = tk.Tk()

#to do: find way to detect screen length & width and display acoordingly
root.geometry("1200x600") # set the root dimensions
root.pack_propagate(False) # tells the root to not let the widgets inside it determine its size.
root.resizable(0, 0) # makes the root window fixed in size.

# Frame for TreeView
frame1 = tk.LabelFrame(root, text="Excel Data")
frame1.place(height=250, width=1200)

# Frame for open file dialog
file_frame = tk.LabelFrame(root, text="Open File")
file_frame.place(height=100, width=400, rely=0.65, relx=0)

# Buttons
button1 = tk.Button(file_frame, text="Browse A File", command=lambda: File_dialog())
button1.place(rely=0.65, relx=0.50)

button2 = tk.Button(file_frame, text="Load File", command=lambda: Load_excel_data())
button2.place(rely=0.65, relx=0.30)

# The file/file path text
label_file = ttk.Label(file_frame, text="No File Selected")
label_file.place(rely=0, relx=0)


## Treeview Widget
tv1 = ttk.Treeview(frame1)
tv1.place(relheight=1, relwidth=1) # set the height and width of the widget to 100% of its container (frame1).

treescrolly = tk.Scrollbar(frame1, orient="vertical", command=tv1.yview) # command means update the yaxis view of the widget
treescrollx = tk.Scrollbar(frame1, orient="horizontal", command=tv1.xview) # command means update the xaxis view of the widget
tv1.configure(xscrollcommand=treescrollx.set, yscrollcommand=treescrolly.set) # assign the scrollbars to the Treeview Widget
treescrollx.pack(side="bottom", fill="x") # make the scrollbar fill the x axis of the Treeview widget
treescrolly.pack(side="right", fill="y") # make the scrollbar fill the y axis of the Treeview widget



####################################   HOME PAGE   #########################################################
#add/edit machines  -------------ADMIN
#update jobs   (this uses CSV as source, but going forward could be direct from SQL)  ----------MANAGER
#view schedule -----------ANYONE
#REPORTS  -----------ANYONE
#settings --------------ADMIN





##############################   ADD / EDIT MACHINES   #####################################################
###TEST DATA:    searh for machine position with: EG : lathes.index(search)), returns zero-based index position
mills = ["VMC-2", "VMC-1", "VM-10", "VM10-2", "VMX-30", "VMX-30-4"]
lathes = ["XYZ", "TM8-2", "TM8-1", "TM-6", "TM-10"]

#Machine name
#Process (mill / turn / router)




##############################    ADD WEEK             ###########################################################
#define hours available for each day
#add week to list






##############################   DRAW SCHEDULE    ##############################################################
#use WHATEVER method to render schedule to the screen! 
#could be tkinter labels or treeview
#should be able to click on slots and edit / insert / delete items







##############################   IMPORT / UPDATE JOBS LIST   ############################################

###INPUTS: active_ops.csv
#take jobs list from active_ops.csv
filename = 'active_ops.csv'


###OUTPUT: create jobs list
def createJobsList(filename):
    df = pd.read_csv(filename)
    #put df in order of required date, then wo #, then op #
    df["REQ'D DATE"] = df["REQ'D DATE"].apply(lambda x: datetime.strptime(x, '%d/%m/%Y'))
    df = df.sort_values(by=["REQ'D DATE", "WO ref", "OP #"])
    df = df.reset_index(drop=True)

    return df






##################################   SCHEDULE JOBS   ############################################################

def scheduleJobs(jobs_df):
    pass
    #click on machine / day on schedule
    #display list of jobs not scheduled
    #user selects job from Treeview
    #new window suggests start time (editable), asks if all ops to be scheduled, and suggests end time (editable)
    #on ok, subsequent processes pop up for scheduling
    #add machine / slots info to jobs df
    #draw updated schedule




#EDIT SCHEDULE
#move jobs around (insert job / push job back / delete)
#mark machines or days unavailable
#flush week





#REPORTS
#capacity report
#late job report
#start date for each machine



def Load_excel_data(df):
    clear_data()
    tv1["column"] = list(df.columns)
    tv1["show"] = "headings"
    for column in tv1["columns"]:
        tv1.heading(column, text=column) # let the column heading = column name

    df_rows = df.to_numpy().tolist() # turns the dataframe into a list of lists
    for row in df_rows:
        tv1.insert("", "end", values=row) # inserts each list into the treeview. For parameters see https://docs.python.org/3/library/tkinter.ttk.html#tkinter.ttk.Treeview.insert
    return None


def clear_data():
    tv1.delete(*tv1.get_children())
    return None


df = createJobsList(filename)
Load_excel_data(df)
root.mainloop()