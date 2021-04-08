from job import Job

class Slot(Job):
    """
    Creates slot object to be placed into dataframe cells.
    These slots are used to track job and available hours in each cell.
    """

    def __init__(self, avail_hours):
        self.avail_hours = avail_hours
        self.job = []
        self.label = ""
