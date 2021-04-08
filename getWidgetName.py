from tkinter import *

def getWidgetName(event):
    print("widget name:", str(event.widget).split(".")[-1])

root = Tk()

label = Label(root, text="Label text", name="widgetNameHere!")
label.bind("<Button>", lambda event: getWidgetName(event))
label.pack()

root.mainloop()

#should be able to add name during drawGrid function. name could be mix of column and date or day. 
#when clicked, the view / edit window can be auto-populated with the currently scheduled jobs and the machine and day. 
#need to look at the Slot class inheriting the Job class to see if the label and other properties can be used...
#...to improve the control over the schedule labels. 
