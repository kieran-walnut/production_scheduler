import pandas as pd
from datetime import timedelta, datetime
import copy
import random
from job import Job
from slots import Slot
from default_machines_days import *


def create_jobs_list(filename):
    """
    Cycles through all ops in active ops file and adds the ops to the jobs_list
    """
    ops_df = pd.read_csv(filename)
    ops_list = ops_df.values.tolist()
    jobs_list = []  # create job list

    for op in ops_list:   # loop through ops, create job objects, add to jobs_list
        job = Job(op)
        jobs_list.append(job)

    return jobs_list


def createWeek(machines_list, days_list, start_date):
    """
    Create blank dataframe from days_list * slot numbers
    """
    day_headers_list = []
    for day in days_list:
        day_headers_list.append(day[0])
    
    date_headers = []
    date = start_date
    for day in days_list:
        date_headers.append(date.strftime("%d %b %y"))
        date = date + timedelta(days=1)
   
    df_slots = pd.DataFrame(columns=date_headers)  # CREATE DATAFRAME AND ADD HEADERS
    df_slots.loc[0] = day_headers_list

    for row in range(0, len(machines_list)):  # FOR EVERY MACHINE ROW...
        rows = []
        for day in days_list:
            #for col in range(0, len(day_headers_list)):   # FOR EVERY COLUMN ADD A "0"
            slot = Slot(day[1])
            rows.append(slot)
        df_length = len(df_slots)  # STORE LENGTH OF DATAFRAME IN df_length
        df_slots.loc[df_length] = rows  # ADD rows LIST CONTENTS TO EACH NEW DATAFRAME ROW

    machines_list.insert(0, "Day")
    #print("Machine list after insert: {}".format(df_cols_list))

    df_slots['Machines'] = machines_list  # ADD COLUMN WITH MACHINE NAMES
    df_slots = df_slots.set_index('Machines')
    # MAKE THE MACHINES COLUMN THE INDEX ROW
    # (TO ALLOW CALLING SPECIFIC ROW VIA MACHINE NAME)

    machines_list.pop(0)   #Remove the Days item from the list
    
    return df_slots


def exportDataframeProperty(df, property):
    """
    Returns a given property of objects in the schedule_df
    Can use this to create dataframs with job names, or with available hours.
    """
    new_df = copy.copy(df)  #CREATES NEW DATAFRAME OBJECT AND LEAVES THE schedule_df UNCHANGED

    jobs_list= []
    for machine in machines_list:
        day_jobs_list = []
        for col in new_df.columns:
            #print("FOUND: {}".format(getattr(df[col][machine], property)))
            day_jobs_list.append( getattr(df[col][machine], property) )
        jobs_list.append(day_jobs_list)

    list_row_ref = 0
    for machine in machines_list:
        day_jobs_list = []
        list_col_ref=0
        for col in new_df.columns:
            new_df.at[machine, col] = jobs_list[list_row_ref][list_col_ref]
            list_col_ref += 1
        list_row_ref += 1

    return new_df


def returnNewStartDate(schedule_df):
    """
    Finds last date in the schedule and returns next week start date
    """
    last_date_posn = len(schedule_df.columns) - 1
    lastCurrentDate = schedule_df.columns[-1]
    date_time_obj = datetime.strptime(lastCurrentDate, '%d %b %y')

    new_week_start_date = date_time_obj + timedelta(days=1)
    return new_week_start_date


def addWeek(schedule_df):
    """
    Adds a blank week to the schedule_df. 
    Currently uses default days list. 
    TO DO: Can use GUI to confirm day hours going forward
    """
    #find new week start date

    new_date = returnNewStartDate(schedule_df)

    #create new week with above date + 1
    new_df = createWeek(machines_list, days_list, new_date)

    #append new DF to the existing schedule df
    extended_df = pd.concat([schedule_df, new_df], axis=1)

    return extended_df


def scheduleWO(schedule_df, jobs_list, wo, target_machine):
    """
    Places a WO into the schedule dataframe. Looks for all ops
    for a WO. Need to add GUI to allow which ops to be scheduled. 
    Need to add GUI to choose which machine to target to
    """

    ##check WO not allocated
    #print("Scheduling WO {} {} {}".format(wo.wo, wo.label, wo.process))
    #list ops on wo and ask which ops are being allocated

    wo_ops_list = []
    for job in jobs_list:
        if job.wo == wo.wo:
            wo_ops_list.append(job)
    def sort_ops(e):   ##SORT OPS LIST BY OP No
        return getattr(e, 'op_no')
    wo_ops_list.sort(key=sort_ops)
    
    """
    print("WO ops to be allocated: \n") 
    for wo_op in wo_ops_list:
        print("{}, {} {}, Hours: {}".format(wo_op.label, wo_op.op_no, wo_op.process, wo_op.hours))
    print("\n\n")
    """

    #assume all ops are being added in this test. 
    ##TO DO: confirm ops which are being scheduled via GUI
    #get user input on machine to which op/ops are being allocated
    target_machine = target_machine
    #cycle through cells in schedule_df row for machine
    #wo_last_label = 0
    ###FOR op in wo_ops_list:
    for wo in wo_ops_list:
        while wo.hours_tba > 0.25:   #while there are still hours to be allocated
            for x in range(0, schedule_df.shape[1]): #for each cell in chosen row
                slot_hours = schedule_df.loc[target_machine][(schedule_df.columns[x])].avail_hours #get avail hours from each cell in machine row
                if wo.hours_tba > 0.25 and slot_hours > 0.24: #if the slot has available hours...
                    if wo.hours_tba > slot_hours:   #if the job is longer than the avail hours
                        schedule_df.at[target_machine, (schedule_df.columns[x])].avail_hours = 0   #make avail_hours in the cell = 0
                        #if wo_last_label == 0:
                        schedule_df.at[target_machine, (schedule_df.columns[x])].job += wo.label   #add the WO label to the cell  ##TO DO: ADD LENGTH OF SLOT TO LABEL
                        wo.hours_tba -= slot_hours  #remove the slot hours from the wo.tba value
                        wo.slots += [target_machine, (schedule_df.columns[x])]  #add the slot to the wo slots list
                        #wo_last_label += 1
                    else:  #if there is room to spare in the cell
                        #print("target machine: {}, column: {},  {}".format(target_machine, x, schedule_df.at[target_machine, (schedule_df.columns[x])].avail_hours ))
                        schedule_df.at[target_machine, (schedule_df.columns[x])].avail_hours -= wo.hours_tba
                        #if wo_last_label == 0:
                        schedule_df.at[target_machine, (schedule_df.columns[x])].job += wo.label  #add label 
                        wo.slots += [target_machine, (schedule_df.columns[x])] 
                        wo.hours_tba = 0
                        #wo_last_label += 1
            if wo.hours_tba > 0.25:
                schedule_df = addWeek(schedule_df)
        wo.allocated = True

    return schedule_df


def testSchedFunc(schedule_df, jobs_list, numberOfTests=1):
    """
    Insert random job into random machine. 
    """
    for x in range(numberOfTests):
        #select random machine from list
        randomMachine = random.choice(machines_list)
        #select random work order from job list
        randomWO = random.choice(jobs_list)
        #call scheduleWO function
        schedule_df = scheduleWO(schedule_df, jobs_list, randomWO, randomMachine)
    return schedule_df
