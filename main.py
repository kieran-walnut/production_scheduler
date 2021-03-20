import pandas as pd
from tkinter import *
import tkinter as tk
import tkinter.font as tkFont
from tkinter import filedialog, messagebox, ttk

from datetime import timedelta, datetime



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

machines_list = ["XYZ", "TM-6", "TM8-2", "TM8-1", "VMX-30", "VMX-30-4", "VM-10", "VM10-2", "VMC-2", "VMC-1"]
days_list = [["Monday", 8], ["Tuesday", 8], ["Wednesday", 8], ["Thursday", 8],
                 ["Friday", 5], ["Saturday", 5], ["Sunday", 5]]

start_date = datetime.today() + timedelta(days=2)
print("Today: {}, startdate {}".format(datetime.today(), start_date))


def create_week(machines_list, days_list, start_date):
    # create blank dataframe from days_list * slot numbers
    day_headers_list = []
    for day in days_list:
        day_headers_list.append(day[0])
    print("Created day header list: {}".format(day_headers_list))
    
    date_headers = []
    date = start_date
    for day in days_list:
        date_headers.append(date.strftime("%d %b %y"))
        date = date + timedelta(days=1)
    print("Created date header list: {}".format(date_headers))
   
    df_slots = pd.DataFrame(columns=day_headers_list)  # CREATE DATAFRAME AND ADD HEADERS
    df_slots.loc[0] = day_headers_list
    df_slots.loc[1] = date_headers

    for row in range(0, len(machines_list)):  # FOR EVERY MACHINE ROW...
        rows = []
        for col in range(0, len(day_headers_list)):   # FOR EVERY COLUMN ADD A "0"
            rows.append(['', 8])
        df_length = len(df_slots)  # STORE LENGTH OF DATAFRAME IN df_length
        df_slots.loc[df_length] = rows  # ADD rows LIST CONTENTS TO EACH NEW DATAFRAME ROW

    machines_list.insert(0, "Date")
    machines_list.insert(0, "Day")
    #print("Machine list after insert: {}".format(df_cols_list))

    df_slots['Machines'] = machines_list  # ADD COLUMN WITH MACHINE NAMES
    df_slots = df_slots.set_index('Machines')
    # MAKE THE MACHINES COLUMN THE INDEX ROW
    # (TO ALLOW CALLING SPECIFIC ROW VIA MACHINE NAME

    # slots_final_list = df_slots.values.tolist()
    
    return df_slots






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
    ##CHOICE OF:
    #    display list of jobs not scheduled      #user selects job from Treeview
    #    ENTER WO NUMBER (BARCODE?)
    
    #new window suggests start time (editable), asks if all ops to be scheduled, and suggests end time (editable)
    #suggests shorthand name for job (part no), this is editable. 
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





df = createJobsList(filename)
schedule_df = create_week(machines_list, days_list, start_date)
print(schedule_df)

pd.set_option("display.max_rows", None, "display.max_columns", None)

#print(df[["REQ'D DATE", "WO ref", "OP #", "PROCESS"]])