from src.File import *
from src.Disk import *
from src.Memory import *
from src.ProcessManager import *
import time

class OperationalSystem:

    def __init__(self):
        self.archives = read_file("assets/files.txt")
        self.processes = read_file("assets/processes.txt")
        self.disk = Disk(int(self.archives[0][0]))
        self.memory = Memory()
        self.second = time.time()
        self.ProcessManager = ProcessManager()
        self.time = 0

    def Run(self):
        while(True):
            if(time.time()-self.second >= 1):
                for i in self.processes:
                    if(int(i[0]) == self.time):
                        self.memory,text = self.ProcessManager.AddProcess(i,'RT',self.memory)
                        self.processes.remove(i)
                
                print(self.time)
                self.memory = self.ProcessManager.Update(self.memory)
                self.second = time.time()
                self.time += 1