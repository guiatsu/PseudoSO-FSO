from src.File import *
from src.Disk import *
from src.Memory import *
from src.ResourceManager import * 
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
        self.ResourceManager = ResourceManager()
        self.time = 0

    def Run(self):
        while(True):
            processesToRemove = []
            text = ""
            if(time.time()-self.second >= 1):
                for i in self.processes:
                    text = ""
                    # print(i)
                    if(int(i[0]) == self.time):
                        if(int(i[1]) == 0):
                            self.memory,text,self.ResourceManager = self.ProcessManager.AddProcess(i,'RT',self.memory,self.ResourceManager)
                            processesToRemove.append(i)
                        else:
                            self.memory,text,self.ResourceManager = self.ProcessManager.AddProcess(i,'User',self.memory,self.ResourceManager)
                            processesToRemove.append(i)
                    if(text != ""):
                        print(text)
                print(self.time)
                for i in processesToRemove:
                    self.processes.remove(i)
                self.memory,self.ResourceManager = self.ProcessManager.Update(self.memory,self.ResourceManager)
                self.ProcessManager.UpdatePriorities()
                self.second = time.time()
                self.time += 1
                if(len(self.processes) == 0 and self.ProcessManager.qttProcessInQueue == 0):
                    break
        text = ""
        for i in range(2,2+int(self.archives[1][0])):
            line = self.archives[i]
            text = ""
            text = self.disk.CreateFile(-1,0, line[0], int(line[1]), int(line[2]))
            if(text != ""):
                print(text)
        for i in range(2+int(self.archives[1][0]),len(self.archives)):
            processes = self.ProcessManager.processes
            line = self.archives[i]
            text = ""
            if(line[1] == "0"):
                offset = self.disk.FindValidSegment(int(line[3]))
                text = self.disk.CreateFile(int(line[0]),processes.get(int(line[0])),line[2],offset,int(line[3]))
            if(line[1] == "1"):
                text = self.disk.DeleteFile(int(line[0]),processes.get(int(line[0])),line[2])
            print(text)

        print("todos processos foram finalizados, fim!")