"""
THIS FILE HAS A TREE VIEW OF THE JOBS LIST DATAFRAME.
NOT HAPPY WITH THE VIEW AS IT IS STUCK ON HALF PAGE!! CAN'T SEEM TO SORT THIS. 
"""


import pandas as pd
from tkinter import *
from tkinter import ttk
from datetime import datetime
from datetime import timedelta


root = Tk()
root.title = ('Tree Demo')
#root.geometry("1200x600")


filename = 'active_ops.csv'







###OUTPUT: create jobs list
def createJobsList(filename):
    df = pd.read_csv(filename)
    #put df in order of required date, then wo #, then op #
    df["REQ'D DATE"] = df["REQ'D DATE"].apply(lambda x: datetime.strptime(x, '%d/%m/%Y'))
    df = df.sort_values(by=["REQ'D DATE", "WO ref", "OP #"])
    df = df.reset_index(drop=True)

    return df



df = createJobsList(filename)




######################   TREE CODE   #########################################


# Frame for TreeView
frame1 = LabelFrame(root, text="Jobs list")
frame1.pack()
my_tree =ttk.Treeview(frame1) 

#define our columns
my_tree['columns'] = ("CUSTOMER", "REQ'D DATE", "WO ref", "OP #", "PROCESS")

#format our columns
#my_tree.column("#0", width=0)
my_tree.column("CUSTOMER", width=350, anchor=W, minwidth=25)
my_tree.column("REQ'D DATE", width=150, anchor=CENTER, minwidth=25)
my_tree.column("WO ref", width=150, anchor=CENTER, minwidth=25)
my_tree.column("OP #", width=150, anchor=CENTER, minwidth=25)
my_tree.column("PROCESS", width=200, anchor=W, minwidth=25)

#create headings
#my_tree.heading("#0", text="index", anchor=W)
my_tree.heading("CUSTOMER", text="Customer", anchor=W)
my_tree.heading("REQ'D DATE", text="Required", anchor=CENTER)
my_tree.heading("WO ref", text="WO", anchor=CENTER)
my_tree.heading("OP #", text="Op #", anchor=CENTER)
my_tree.heading("PROCESS", text="Department", anchor=W)


treescrolly = Scrollbar(frame1, orient="vertical", command=my_tree.yview) # command means update the yaxis view of the widget
treescrollx = Scrollbar(frame1, orient="horizontal", command=my_tree.xview) # command means update the xaxis view of the widget
my_tree.configure(xscrollcommand=treescrollx.set, yscrollcommand=treescrolly.set) # assign the scrollbars to the Treeview Widget
treescrollx.pack(side="bottom", fill="x") # make the scrollbar fill the x axis of the Treeview widget
treescrolly.pack(side="right", fill="y") # make the scrollbar fill the y axis of the Treeview widget


#add data
df = df[["CUSTOMER", "REQ'D DATE", "WO ref", "OP #", "PROCESS"]]
df_rows = df.to_numpy().tolist()
for row in df_rows:
	my_tree.insert("", "end", values=row)


#pack tree
my_tree.pack(fill=X)

 
root.mainloop()