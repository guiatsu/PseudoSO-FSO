class Process:

    def __init__(self, PID,memOffset,process):
        self.PID = int(PID)
        self.memOffset = int(memOffset)
        self.initTime = int(process[0])
        self.priority = int(process[1])
        self.execTime = int(process[2])
        self.size = int(process[3])
        self.printNumber = int(process[4])
        self.scanNumber = int(process[5])
        self.modemNumber = int(process[6])
        self.diskNumber = int(process[7])
        self.instruction = self.execTime + 1

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
