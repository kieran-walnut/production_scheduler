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

        self.canvas.pack(side='left', fill='both')
        self.canvas.create_window((4,4), window=self.mainFrame, anchor="nw") #, tags="frame"
        #self.canvas.configure(xscrollcommand = self.scroll.set)
        #self.scroll = Scrollbar(self.parent, orient = HORIZONTAL, command=self.canvas.xview)
        #self.canvas.configure(xscrollcommand=self.scroll.set)
        #self.scroll.pack(side='bottom', fill='x')
        self.mainFrame.bind("<Configure>", self.update)

        self.drawButtonsAndScroll()

    def drawButtonsAndScroll(self):    
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
                        job_label.bind('<Button-1>', lambda event: self.showJobDetail(event))
                        self.labels.append(job_label)
                        item_ref += 1
                        label_x_posn += label_length*self.widget_piece_length
                        label_length = 1
                except IndexError:
                    widgetName = ("{},{}".format(df_col_name_ref-1, item_ref + self.week_no))
                    job_label = Label(self.canvas, text=str(current_item), borderwidth=2, relief="groove", font=self.op_font, name=widgetName)
                    job_label.place(relx=label_x_posn, 
                    rely=label_y_posn*self.widget_rel_height, relwidth=self.widget_piece_length*label_length, relheight=self.widget_rel_height)
                    job_label.bind('<Button-1>', lambda event: self.showJobDetail(event))
                    self.labels.append(job_label)
                    break
            label_y_posn += 1
            label_x_posn = 0.1
            df_col_name_ref += 1
                
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

    
    def showJobDetail(self, event):  #SHOW A WINDOW WITH JOB DETAILS
        #TAKE CLICKED WIDGET DETAILS FROM THE EVENT AND FIND SPECIFIC CELL IN schedule_df
        widgetRefObject = str(event.widget).split(".")[-1]
        chosenCellPosn = str(widgetRefObject).split(",")
        row = int(chosenCellPosn[0]) + 1
        column = int(chosenCellPosn[1])
        avail_hours = round(self.schedule_df.iloc[row][column].avail_hours, 2)
        wo_list = self.schedule_df.iloc[row][column].job
        for widget in self.canvas.winfo_children(): #clear the window
                widget.destroy()
        
        showJobHeading = Label(self.canvas, text="JOB DETAILS: ", borderwidth=4, relief="sunken", font=self.day_font)
        showJobHeading.place(x=0, rely=0, 
        relheight=self.widget_rel_height, relwidth=1)
        
        label_row_posn = 2
        for wo in wo_list:        
            label_text = "WO: {},  Customer: {},  Process: {},  Part: {},  Hours: {}\n".format(wo.wo, 
            wo.cust, wo.process, wo.part_no, wo.hours)
            wo_label = Label(self.canvas, text = label_text, borderwidth=2, relief="groove", font=self.op_font)
            wo_label.place(x=0, rely=label_row_posn*self.widget_rel_height, relheight=self.widget_rel_height, relwidth=1)
            label_row_posn += 1
        
        if len(wo_list) > 0:
            label_row_posn += 1
            hours_label_text = "Hours available in day: {}".format(avail_hours)
            hours_label = Label(self.canvas, text = hours_label_text, borderwidth=2, relief="groove", font=self.op_font)
            hours_label.place(x=0, rely=label_row_posn*self.widget_rel_height, relheight=self.widget_rel_height, relwidth=1)
        
        edit_add_button = Button(self.canvas, text="Edit / Add contents", borderwidth=3, relief="raised", font=self.op_font, command=self.butpressed)
        edit_add_button.place(relx=0.35, anchor=CENTER, rely=6/7, relheight=self.widget_rel_height, relwidth=0.15)

        back_button = Button(self.canvas, text="Back to schedule...", borderwidth=3, relief="raised", font=self.op_font, command=self.backToSchedule)
        back_button.place(relx=0.7, anchor=CENTER, rely=6/7, relheight=self.widget_rel_height, relwidth=0.15)        
        

    def butpressed(self):
        print("Button Pressed!")

    def backToSchedule(self):
        jobs_df = exportDataframeProperty(self.schedule_df, "label")
        self.draw_schedule(jobs_df)
        self.drawButtonsAndScroll()


         