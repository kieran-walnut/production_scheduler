from tkinter import *
import tkinter as tk
import tkinter.font as tkFont
from schedule_utils import *
from default_machines_days import *



WIDTH = 1600
HEIGHT = 600


class DrawGrid(object):
    
    def __init__(self, parent, schedule_df, jobs_list):  
        self.schedule_df = schedule_df  # jobs programmed in
        self.jobs_list = jobs_list
        self.df_rows_list = list(self.schedule_df.index.values)
        self.columns = list(self.schedule_df)  # list of column headings in dataframe
        self.labels = []  # full list
        self.widget_rel_height = 1 / (len(self.df_rows_list)+2)
        self.widget_piece_length = 0.9 / 7 #0.1 reserved for row labels, remainder of 0.9 divided by week days
        self.day_font = tkFont.Font(family="Calibri", size=16, weight="bold", slant="italic")
        self.op_font = tkFont.Font(family="Calibri", size=10)
        self.machine_font = tkFont.Font(family="Arial", size=25, weight="bold", slant="italic")
        self.week_no = 0


        #frames etc
        self.parent = parent
        self.navigation_frame = Frame(self.parent)
        self.canvas = Canvas(self.parent, bg='white', width=WIDTH, height=HEIGHT)
        self.mainFrame = Frame(self.canvas)
        self.navigation_frame.pack()
        self.show_details_frame = Frame(self.mainFrame)
        
        #buttons
        self.week_back_button = Button(self.canvas, text=" < PREVIOUS WEEK", command=self.selectPrevWeek).place(relx=0/7, rely=0, relwidth=1/7, relheight=self.widget_rel_height)
        self.week_fwd_button = Button(self.canvas, text="NEXT WEEK >", command=self.selectNextWeek).place(relx=1/7, rely=0,relwidth=1/7, relheight=self.widget_rel_height)
        self.add_job_button = Button(self.canvas, text="ADD JOB", command=self.addJob).place(relx=2/7, rely=0,relwidth=1/7, relheight=self.widget_rel_height)
        self.new_week_button = Button(self.canvas, text="ADD WEEK").place(relx=3/7, rely=0,relwidth=1/7, relheight=self.widget_rel_height)
        self.search_button = Button(self.canvas, text="SEARCH").place(relx=4/7, rely=0,relwidth=1/7, relheight=self.widget_rel_height)
        self.reports_button = Button(self.canvas, text="REPORTS").place(relx=5/7, rely=0, relwidth=1/7, relheight=self.widget_rel_height)
        self.settings_button = Button(self.canvas, text="SETTINGS").place(relx=6/7, rely=0, relwidth=1/7, relheight=self.widget_rel_height)
        self.week_label = None
     

    def selectNextWeek(self):
        if self.week_no + 7 < len(self.schedule_df.columns):
            self.week_no += 7
            jobs_df = exportDataframeProperty(self.schedule_df, "label")
            self.draw_schedule(jobs_df)
        pass
    
    def selectPrevWeek(self):
        if self.week_no - 7 >= 0:
            self.week_no -= 7
            jobs_df = exportDataframeProperty(self.schedule_df, "label")
            self.draw_schedule(jobs_df)
        pass

    def addJob(self):
        self.schedule_df = testSchedFunc(self.schedule_df, self.jobs_list, numberOfTests=5)
        jobs_df = exportDataframeProperty(self.schedule_df, "label")
        self.draw_schedule(jobs_df)

        
    def draw_schedule(self, jobs_df):
        #iretate through DF row by row using label length loop and create labels
        week_start_date = jobs_df.columns[self.week_no]
        self.week_label = Label(self.canvas, text="WEEK COMMENCING: {}".format(week_start_date)).place(x=0, rely=self.widget_rel_height, 
        relheight=self.widget_rel_height, relwidth=1)
        
        machine_row_posn = 2

        for row in self.df_rows_list: ###TO DO: ADD LEAD TIME / FIRST START DATE
            machine_label = Label(self.canvas, text=row, relief=RAISED).place(x=0, rely=machine_row_posn*self.widget_rel_height, relheight=self.widget_rel_height, relwidth=0.1)
            machine_row_posn += 1

        label_y_posn = 2  #3rd COL - SITS TO RIGHT OF MACHINE NAMES
        df_col_name_ref = 0
        for row in self.df_rows_list:
            df_list = jobs_df.loc[row].values.tolist()
            df_list = df_list[self.week_no:self.week_no+7]
            df_list_length = len(df_list)
            item_ref = 0  #for iterating through row items
            label_length = 1 #initial length of label
            label_x_posn = 0.1  #to sit to right of machine labels

            while item_ref < df_list_length:
                current_item = df_list[item_ref]
                self.op_font = self.setFont(current_item)

                try:
                    if current_item == df_list[item_ref+1]:   #make label continuous if job runs over more than one slot
                        label_length += 1
                        item_ref += 1
                    else:
                        widgetName = ("{},{}".format(df_col_name_ref-1, item_ref + self.week_no))
                        job_label = Label(self.canvas, text=str(current_item), borderwidth=2, relief="groove", font=self.op_font, name=widgetName)
                        job_label.place(relx=label_x_posn, 
                        rely=label_y_posn*self.widget_rel_height, relwidth=self.widget_piece_length*label_length, relheight=self.widget_rel_height)
                        job_label.bind('<Button-1>', lambda event: self.showSlotContents(event))
                        self.labels.append(job_label)
                        item_ref += 1
                        label_x_posn += label_length*self.widget_piece_length
                        label_length = 1
                except IndexError:
                    widgetName = ("{},{}".format(df_col_name_ref-1, item_ref + self.week_no))
                    job_label = Label(self.canvas, text=str(current_item), borderwidth=2, relief="groove", font=self.op_font, name=widgetName)
                    job_label.place(relx=label_x_posn, 
                    rely=label_y_posn*self.widget_rel_height, relwidth=self.widget_piece_length*label_length, relheight=self.widget_rel_height)
                    job_label.bind('<Button-1>', lambda event: self.showSlotContents(event))
                    self.labels.append(job_label)
                    break
            label_y_posn += 1
            label_x_posn = 0.1
            df_col_name_ref += 1
            

        self.scroll = Scrollbar(self.parent, orient = HORIZONTAL, command=self.canvas.xview)
        self.canvas.configure(xscrollcommand=self.scroll.set)
        self.scroll.pack(side='bottom', fill='x')
        self.canvas.pack(side='left', fill='both')
        self.canvas.create_window((4,4), window=self.mainFrame, anchor="nw", tags="frame")

        self.canvas.configure(xscrollcommand = self.scroll.set)
        self.mainFrame.bind("<Configure>", self.update)

        
    def update(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def setFont(self, current_item):     
        self.op_font = tkFont.Font(family="Calibri", size=10)
        font_size = 10
        if len(current_item) > 65:
            self.op_font = tkFont.Font(family="Calibri", size=5)
            font_size = 5
        elif 64 < len(current_item) < 50:
            self.op_font = tkFont.Font(family="Calibri", size=6)
            font_size = 6
        elif 49 < len(current_item) < 20:
            self.op_font = tkFont.Font(family="Calibri", size=7) 
            font_size = 7

        return self.op_font

    def showSlotContents(self, event):
            #print("widget name:", str(event.widget).split(".")[-1])
            widgetRefObject = str(event.widget).split(".")[-1]
            chosenCellPosn = str(widgetRefObject).split(",")
            row = int(chosenCellPosn[0]) + 1
            column = int(chosenCellPosn[1])
            wo_list = self.schedule_df.iloc[row][column].job

            for wo in wo_list:
                print("WO No: {}".format(wo.wo))
                print("WO Customer: {}".format(wo.cust))
                print("PROCESS: {}".format(wo.process))
                print("WO Part: {}".format(wo.part_no))
                print("WO Hours: {}".format(wo.hours))
                print("\n")
    
    def show_job_detail(self, event):  #SHOW A WINDOW WITH JOB DETAILS   ###NOT FINISHED!!
        widgetRefObject = str(event.widget).split(".")[-1]
        chosenCellPosn = str(widgetRefObject).split(",")
        row = int(chosenCellPosn[0]) + 1
        column = int(chosenCellPosn[1])
        wo_list = self.schedule_df.iloc[row][column].job
        

        for widget in self.canvas.winfo_children(): #clear the window
                widget.destroy()
        wo_label = Label(self.canvas, text ="WO ref: {}".format(job.wo))  #add details of the found job to the window
        wo_label.grid(row=0, column=0)
        cust_label = Label(self.canvas, text ="Customer: {}".format(job.cust))
        cust_label.grid(row=1, column=0)
        descr_label = Label(self.canvas, text ="Item: {}".format(job.descript))
        descr_label.grid(row=2, column=0)
        process_label = Label(self.canvas, text="Department: {}".format(job.process))
        process_label.grid(row=3, column=0)
        day_label = Label(self.canvas, text ="Start Day: {}".format(job.day))
        day_label.grid(row=4, column=0)
        machine_label = Label(self.canvas, text ="Machine: {}".format(job.machine))
        machine_label.grid(row=5, column=0)
         

        

