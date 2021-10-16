class Process:

    def __init__(self, PID,memOffset,process):
        self.PID = PID
        self.memOffset = memOffset
        self.initTime = process[0]
        self.priority = process[1]
        self.execTime = process[2]
        self.size = process[3]
        self.printNumber = process[4]
        self.scanNumber = process[5]
        self.modemNumber = process[6]
        self.diskNumber = process[7]

    def __gt__(self,other):
        return self.priority > other.priority

    def __lt__(self,other):
        return self.priority < other.priority

    def __le__(self,other):
        return self.priority <= other.priority

    def __ge__(self,other):
        return self.priority >= other.priority

    def __eq__(self,other):
        return self.priority == other.priority

    def __ne__(self,other):
        return self.priority != other.priority
