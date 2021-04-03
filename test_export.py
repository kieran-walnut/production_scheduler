import pandas as pd
from datetime import timedelta, datetime
import copy
from job import Job
from slots import Slot
from default_machines_days import *

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

    df = createWeek(machines_list, days_list, start_date)

    
def exportDataframeProperty(df, property):
    """
    Returns a given property of objects in the schedule_df
    Can use this to create dataframs with job names, or with available hours.
    """
    new_df = copy.copy(df)  #CREATES NEW DATAFRAME OBJECT AND LEAVES THE schedule_df UNCHANGED
    cols, rows = new_df.shape
    print(("x:{}, y:{}".format(rows, cols)))

    return new_df

    