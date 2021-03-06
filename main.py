from tkinter import *
import tkinter as tk
from schedule_utils import *
from draw import DrawGrid




####################################   HOME PAGE   #########################################################
#add/edit machines  -------------ADMIN
#update jobs   (this uses CSV as source, but going forward could be direct from SQL)  ----------MANAGER
#view schedule -----------ANYONE
#REPORTS  -----------ANYONE
#settings --------------ADMIN





##############################   ADD / EDIT MACHINES   #####################################################
#Machine name
#Process (mill / turn / router)
#INFO WILL BE SAVED TO default_machines_days.py




##############################    ADD WEEK             ###########################################################
#define hours available for each day
#add week to list
start_date = datetime.today() + timedelta(days=2)    #THIS CAN BE SET VIA GUI AT FIRST INSTANCE. 




##############################   DRAW SCHEDULE    ##############################################################
#use WHATEVER method to render schedule to the screen! 
#could be tkinter labels or treeview
#should be able to click on slots and edit / insert / delete items




##############################   IMPORT / UPDATE JOBS LIST   ############################################

###INPUTS: active_ops.csv
#take jobs list from active_ops.csv    #GOING FORWARD THIS CAN BE VIA ACCESS TO DATABASE
filename = 'active_ops.csv'
###OUTPUT: create jobs list
jobs_list = create_jobs_list(filename)   ##TO DO: round hours up to nearest 0.25 hr





##################################   SCHEDULE JOBS   ############################################################

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


#SETTINGS
#screen size (can this be detected?)





schedule_df = createWeek(machines_list, days_list, start_date)    #CREATE INITIAL WEEK 
#schedule_df = testSchedFunc(schedule_df, jobs_list, 50)  #TEST JOB INSERTIONS

root = Tk()

app = DrawGrid(root, schedule_df, jobs_list)

job_df = exportDataframeProperty(schedule_df, "label")
app.draw_schedule(job_df)

#schedule_df.to_csv("sched_job_df.csv")
#job_df.to_csv("test_job_df.csv")
root.mainloop()


"""

#TEST VALUES

scheduleWO(schedule_df, jobs_list, jobs_list[5])
scheduleWO(schedule_df, jobs_list, jobs_list[3])
scheduleWO(schedule_df, jobs_list, jobs_list[77])
scheduleWO(schedule_df, jobs_list, jobs_list[99])
scheduleWO(schedule_df, jobs_list, jobs_list[199])


print("Job status: {}".format(jobs_list[5].slots))
print("Job status: {}".format(jobs_list[3].slots))
print("Job status: {}".format(jobs_list[77].slots))
print("Job status: {}".format(jobs_list[99].slots))
print("Job status: {}".format(jobs_list[199].slots))

print("Schedule DF id{}:\n{}".format(id(schedule_df), schedule_df))
#new_df = exportDataframeProperty(schedule_df, 'job')
#new_df_hrs = exportDataframeProperty(schedule_df, 'avail_hours')

#PRINT JOBS AND HOURS LISTS
#pd.set_option("display.max_rows", None, "display.max_columns", None)
#print("\n\n")
#print("New DF job id: {}: \n{}".format(id(new_df), new_df))
#new_df.to_csv('jobs_export.csv')
#print("\n\n")
#print("New DF hours id: {}: \n{}".format(id(new_df_hrs), new_df_hrs))
#new_df_hrs.to_csv('hours_export.csv')


schedule_df.at['TM-6', '05 Apr 21'].job = "50352.1"
schedule_df.at['TM-6', '06 Apr 21'].job = "50352.1"
schedule_df.at['TM-6', '08 Apr 21'].job = "10"
schedule_df.at['TM-6', '11 Apr 21'].job = "50677.1.02"

"""