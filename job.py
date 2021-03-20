
class Job():
    """
    Creates Job object which stores all op attributes. 
    The input object is "job" which is a line in active ops. 
    Going forward this could be taken direct from the database.
    """
    
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

