from src.Process import *
from queue import PriorityQueue

class ProcessManager:

    def __init__(self):
        self.nextPID = 0
        self.RTQueue = PriorityQueue()
        self.UserQueue = PriorityQueue()
    def AddProcess(self,process, type,memory):
        if(self.RTQueue.qsize()+self.UserQueue.qsize() >= 1000):
            return "Falha ao criar o processo, limite de processos atingido"
        else:
            if(type == 'RT'):
                memOffset = memory.FindValidSegment(int(process[3]),'RT')
                if(memOffset < 0):
                    print("Nao foi possivel criar o processo, falta de espaco na memoria")
                else:
                    memory.MemAlloc(self.nextPID,memOffset,'RT',int(process[3]))
                    self.RTQueue.put((int(process[1]),Process(self.nextPID,memOffset,process)))
                    self.nextPID += 1
            elif(type == 'User'):
                memOffset = memory.FindValidSegment(int(process[3]),'User')
                if(memOffset < 0):
                    print("Nao foi possivel criar o processo, falta de espaco na memoria")
                else:
                    memory.MemAlloc(self.nextPID,memOffset,'User',int(process[3]))
                    self.UserQueue.put((int(process[1]),Process(self.nextPID,memOffset,process)))
                    self.nextPID += 1
            return memory
    def Update(self):
        if(self.RTQueue.qsize()>0):
            process = self.RTQueue.get()
            #executa ele
            if(process[1].execTime-1 == 0):
                #nao coloca de novo na fila
                pass
            else:
                process[1].execTime -= 1
                self.RTQueue.put(process)
                for i in range(self.RTQueue.qsize()-1):
                    process = self.RTQueue.get()
                    self.RTQueue.put(process)
        else:
            process = self.UserQueue.get()
            #executo o processo
            if(process[1].execTime-1 == 0):
                #acabou nao recoloco na fila
                pass
            else:
                process[1].execTime -= 1
                if(process[0] > 0):
                    process[0] -= 1
                    process[1].priority -= 1
                self.UserQueue.put(process)
                for i in range(self.UserQueue.qsize()-1):
                    if(process[0] > 0):
                        process[1].priority -= 1
                        process[0] -= 1
                        self.UserQueue.put(process)
                    else:
                        self.UserQueue.put(process)
        


