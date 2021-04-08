    def show_job_detail(self, win, job):  #SHOW A WINDOW WITH JOB DETAILS
        for widget in win.winfo_children(): #clear the window
                widget.destroy()
        wo_label = Label(win, text ="WO ref: {}".format(job.wo))  #add details of the found job to the window
        wo_label.grid(row=0, column=0)
        cust_label = Label(win, text ="Customer: {}".format(job.cust))
        cust_label.grid(row=1, column=0)
        descr_label = Label(win, text ="Item: {}".format(job.descript))
        descr_label.grid(row=2, column=0)
        process_label = Label(win, text="Department: {}".format(job.process))
        process_label.grid(row=3, column=0)
        day_label = Label(win, text ="Start Day: {}".format(job.day))
        day_label.grid(row=4, column=0)
        machine_label = Label(win, text ="Machine: {}".format(job.machine))
        machine_label.grid(row=5, column=0)


    #NEED TO ADD FUNCTIONALITY TO CHOOSE PARTICULAR OP OR ALL OPS OF A SPECIFIC TYPE
    def addJob(self):
        for widget in self.win.winfo_children():
            widget.destroy()
        text_label = "No jobs allocated to {} on {}. \nClick below to add\n\n".format(self.machine_search.upper(), self.day_search.upper())
        label = Label(self.win, text=text_label)
        label.config(font=self.day_font)
        label.grid(row=0, column=0)        
        print("In add job")
        label = Label(self.win, text="Add WO: ")
        label.grid(row=1, column=0)
        self.wo = StringVar()
        enterWO = Entry(self.win, textvariable=self.wo)
        enterWO.grid(row=2, column=0)
        submit = Button(self.win, text="Submit", command=self.getWO)
        submit.grid(row=4, column=0)