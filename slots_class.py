"""
THIS FILE HAS METHODS TO CREATE BLANK DATAFRAME FOR WEEK.
THE DATAFRAME IS POPULATED BY Slots CLASS OBJECTS.
THE exportDataframeProperty FUNCTION ALLOWS SPECIFIC Slot PROPERTIES TO BE EXPORTED TO A NEW DATAFRAME
"""


import pandas as pd
from tkinter import *
import tkinter as tk
import tkinter.font as tkFont
from tkinter import filedialog, messagebox, ttk
from datetime import timedelta, datetime
import copy

jobs_test = [["Job 1-4", 4], ["Job 2-2", 2], ["Job 3-2", 2],["Job 4-8", 8], ["Job 5-2", 2]]

machines_list = ["TM-6", "TM8-2", "TM8-1", "VMX-30", "VMX-30-4", "VM-10", "VM10-2", "VMC-2", "VMC-1", "XYZ"]
days_list = [["Monday", 8], ["Tuesday", 8], ["Wednesday", 8], ["Thursday", 8],
                 ["Friday", 5], ["Saturday", 5], ["Sunday", 5]]

start_date = datetime.today() + timedelta(days=2)

filename = 'active_ops.csv'


class Job():
    def __init__(self, job):
        # columns = [0 WO ref, 1 PROCESS, 2 PART #, 3 PART DESCRIPT
        # 4 CUSTOMER, 5 HOURS O/S, 6 OP #, 7 OP DESCRIPT, 8 REQ'D DATE]
        self.wo = job[0]
        self.process = job[1]
        self.part_no = job[2]
        self.descript = job[3]
        self.cust = job[4]
        self.hours = job[5]   ##TO DO: round hours up to nearest 0.25 hr
        self.hours_tba = self.hours
        self.op_no = job[6]
        self.op_desc = job[7]
        self.req_date = job[8]
        self.label = str(job[4])[:10] + "\n" + str(job[2])[8:] + "\n" # label is mix of cust + part no
        self.slots = []
        self.allocated = False
        self.isLate = False
        self.shortName = None



class Slot():
    def __init__(self, avail_hours):
        self.avail_hours = avail_hours
        self.job = ""



def create_jobs_list(filename):
    ops_df = pd.read_csv(filename)
    ops_list = ops_df.values.tolist()
    jobs_list = []  # create job list

    for op in ops_list:   # loop through ops, create job objects, add to jobs_list
        job = Job(op)
        jobs_list.append(job)

    return jobs_list




def create_week(machines_list, days_list, start_date):
    # create blank dataframe from days_list * slot numbers
    day_headers_list = []
    for day in days_list:
        day_headers_list.append(day[0])
    
    date_headers = []
    date = start_date
    for day in days_list:
        date_headers.append(date.strftime("%d %b %y"))
        date = date + timedelta(days=1)
   
    df_slots = pd.DataFrame(columns=day_headers_list)  # CREATE DATAFRAME AND ADD HEADERS
    df_slots.loc[0] = day_headers_list
    df_slots.loc[1] = date_headers

    for row in range(0, len(machines_list)):  # FOR EVERY MACHINE ROW...
        rows = []
        for day in days_list:
            #for col in range(0, len(day_headers_list)):   # FOR EVERY COLUMN ADD A "0"
            slot = Slot(day[1])
            rows.append(slot)
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



def exportDataframeProperty(df, property):
    
    """
    RETURNS PROPERTY OF OBJECTS IN DATAFRAME.
    CAN USE TO CREATE DATAFRAME WITH JOB NAMES ONLY, OR AVAILABLE HOURS
    """

    new_df = copy.copy(df)  #CREATES NEW DATAFRAME OBJECT AND LEAVES THE schedule_df UNCHANGED

    jobs_list= []
    for machine in machines_list[2:]:
        day_jobs_list = []
        for day in days_list:
            day_jobs_list.append( getattr(schedule_df[day[0]][machine], property) )
        jobs_list.append(day_jobs_list)


    list_row_ref = 0
    for machine in machines_list[2:]:
        day_jobs_list = []
        list_col_ref=0
        for day in days_list:
            new_df.at[machine, day[0]] = jobs_list[list_row_ref][list_col_ref]
            list_col_ref += 1
        list_row_ref += 1

    return new_df

def addWeek(schedule_df):
    pass
    #initially use day_list to repeat week
    #append another week to days list
    #use createWeek function to create newWeekDF
    #append newWeekDF to schedule_df
    #return schdedule_df


def scheduleWO(schedule_df, wo):
    ##check WO not allocated
    print("Scheduling WO {} {} {}".format(wo.wo, wo.label, wo.process))
    #list ops on wo and ask which ops are being allocated

    wo_ops_list = []
    for job in jobs_list:
        if job.wo == wo.wo:
            wo_ops_list.append(job)
    def sort_ops(e):   ##SORT OPS LIST BY OP No
        return getattr(e, 'op_no')
    wo_ops_list.sort(key=sort_ops)
    print("WO ops to be allocated: \n")
    for wo_op in wo_ops_list:
        print("{} {}, Hours: {}".format(wo_op.op_no, wo_op.process, wo_op.hours))
    print("\n\n")
    
    #assume all ops are being added in this test. 
    ##TO DO: confirm ops which are being scheduled via GUI

    #get user input on machine to which op/ops are being allocated
    #target_machine = input("Enter machine name: ") ##WILL BE DONE VIA GUI
    target_machine = 'XYZ'
    #cycle through cells in schedule_df row for machine

    ###FOR op in wo_ops_list:
    for wo in wo_ops_list:
        #print("Scheduling {}, op {}".format(wo.label, wo.op_no))
        while wo.hours_tba > 0.25:   #while there are still hours to be allocated
            for x in range(0, schedule_df.shape[1]): #for each cell in chosen row
                slot_hours = schedule_df.loc[target_machine][(schedule_df.columns[x])].avail_hours #get avail hours from each cell in machine row
                if wo.hours_tba > 0.25 and slot_hours > 0: #if the slot has available hours...
                    if wo.hours_tba > slot_hours:   #if the job is longer than the avail hours
                        schedule_df.at[target_machine, (schedule_df.columns[x])].avail_hours = 0   #make avail_hours in the cell = 0
                        schedule_df.at[target_machine, (schedule_df.columns[x])].job += wo.label   #add the WO label to the cell  ##TO DO: ADD LENGTH OF SLOT TO LABEL
                        wo.hours_tba -= slot_hours  #remove the slot hours from the wo tba valie
                        wo.slots += [target_machine, (schedule_df.columns[x])]  #add the slot to the wo slots list
                    else:  #if there is room to spare in the cell
                        #print("target machine: {}, column: {},  {}".format(target_machine, x, schedule_df.at[target_machine, (schedule_df.columns[x])].avail_hours ))
                        schedule_df.at[target_machine, (schedule_df.columns[x])].avail_hours -= wo.hours_tba
                        schedule_df.at[target_machine, (schedule_df.columns[x])].job += wo.label  #add label 
                        wo.slots += [target_machine, (schedule_df.columns[x])] 
                        wo.hours_tba = 0
        wo.allocated = True
    
    for x in range(schedule_df.shape[1]): 
        print((schedule_df.columns[x]))
        slot_hours = schedule_df.loc[target_machine][(schedule_df.columns[x])].job
        print("Slot hours: {}".format(slot_hours))
    

    ####else cell.avail_hours -= wo.hours, cell.job = wo.label
    #####once wo.hours_tba < 0.25 wo.allocated = True
    

    #check if available slots are greater than required hours
    #if yes, slot.job = wo
    
    #if no - ADD WEEK
    #CAN WE CREATE NEW WEEK USING EXISTING create_week FUNCTION? 
    #Get start date at last date in schedule + 1
    #Create separate dataframe from create_week funtion
    #Place the dataframe side by side with existing schedule  - pd.concat([first_df, new_df], axis=1)    ##AXIS = 1 MEANS ADD AT R.H.S. OF EXISTING DF
    


schedule_df = create_week(machines_list, days_list, start_date)

jobs_list = create_jobs_list(filename)   ##TO DO: round hours up to nearest 0.25 hr

#print(jobs_list[1].wo, jobs_list[1].process, jobs_list[1].allocated)


#TEST VALUES
scheduleWO(schedule_df, jobs_list[5])
scheduleWO(schedule_df, jobs_list[3])
scheduleWO(schedule_df, jobs_list[77])
#scheduleWO(schedule_df, jobs_list[99])

print("Job status: {}".format(jobs_list[5].slots))
print("Job status: {}".format(jobs_list[3].slots))
print("Job status: {}".format(jobs_list[77].slots))
print("Job status: {}".format(jobs_list[99].slots))
print("Job status: {}".format(jobs_list[199].slots))

print("Schedule DF id{}:\n{}".format(id(schedule_df), schedule_df))
new_df = exportDataframeProperty(schedule_df, 'job')
new_df_hrs = exportDataframeProperty(schedule_df, 'avail_hours')

#PRINT JOBS AND HOURS LISTS
print("\n\n")
print("New DF job id: {}: \n{}".format(id(new_df), new_df))
#new_df.to_csv('jobs_export.csv')
print("\n\n")
#print("New DF hours id: {}: \n{}".format(id(new_df_hrs), new_df_hrs))
new_df_hrs.to_csv('hours_export.csv')

