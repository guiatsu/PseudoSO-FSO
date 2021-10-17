from src.Process import *
from queue import PriorityQueue

class ProcessManager:

    def __init__(self):
        self.nextPID = 0
        self.RTQueue = PriorityQueue()
        self.UserQueue = PriorityQueue()
        self.runningProcess = (0,"")
        self.dispatcher = 0


    def AddProcess(self,process, type,memory):
        if(self.RTQueue.qsize()+self.UserQueue.qsize() >= 999):
            return memory,"Falha ao criar o processo, limite de processos atingido"
        else:
            if(type == 'RT'):
                memOffset = memory.FindValidSegment(int(process[3]),'RT')
                if(memOffset < 0):
                    return memory,"Nao foi possivel criar o processo, falta de espaco na memoria"
                else:
                    memory.MemAlloc(self.nextPID,memOffset,'RT',int(process[3]))
                    self.RTQueue.put((int(process[1]),Process(self.nextPID,memOffset,process)))
                    self.nextPID += 1
            elif(type == 'User'):
                memOffset = memory.FindValidSegment(int(process[3]),'User')
                if(memOffset < 0):
                    return memory,"Nao foi possivel criar o processo, falta de espaco na memoria"
                else:
                    memory.MemAlloc(self.nextPID,memOffset,'User',int(process[3]))
                    self.UserQueue.put((int(process[1]),Process(self.nextPID,memOffset,process)))
                    self.nextPID += 1
            return memory, ""
    def Update(self,memory):
        if(self.RTQueue.qsize()>0 or self.runningProcess[1] == "RT"):
            if(self.runningProcess[1] == "User"):
                if(self.runningProcess[0][1].execTime-1 == 0):
                    self.runningProcess = (self.RTQueue.get(),"RT")
                    self.PrintDispatcher(self.runningProcess[0][1])
                    self.PrintProcess(self.runningProcess[0][1],"BEGIN")
                    memory = self.RunProcess(memory)
                else:
                    self.UserQueue = self.PlaceInFrontOfQueue(self.UserQueue,self.runningProcess[0])
                    self.PrintProcess(self.runningProcess[0][1],"STOPPING")
                    #desalocar recursos aqui
                    self.runningProcess = (self.RTQueue.get(),"RT")
                    self.PrintDispatcher(self.runningProcess[0][1])
                    self.PrintProcess(self.runningProcess[0][1],"BEGIN")
                    memory = self.RunProcess(memory)
            elif(self.runningProcess[1] == "RT"):
                memory = self.RunProcess(memory)
            else:
                self.runningProcess = (self.RTQueue.get(),"RT")
                self.PrintDispatcher(self.runningProcess[0][1])
                self.PrintProcess(self.runningProcess[0][1],"BEGIN")
                memory = self.RunProcess(memory)

        elif(self.UserQueue.qsize()>0 or self.runningProcess[1] == "User"):
            if(self.runningProcess[1] == "User"):
                if((self.UserQueue.qsize() > 0) and (self.UserQueue.queue[0][0] < self.runningProcess[0][0])):
                    self.PrintProcess(self.runningProcess[0][1],"STOPPING")
                    #desalocar recursos aqui
                    aux = self.runningProcess
                    self.runningProcess = (self.UserQueue.get(),"User")
                    self.PrintDispatcher(self.runningProcess[0][1])
                    self.PrintProcess(self.runningProcess[0][1],"BEGIN")
                    self.PlaceInFrontOfQueue(self.UserQueue,aux)
                    memory = self.RunProcess(memory)
                else:
                    memory = self.RunProcess(memory)
            else:
                self.runningProcess = (self.UserQueue.get(),"User")
                self.PrintDispatcher(self.runningProcess[0][1])
                self.PrintProcess(self.runningProcess[0][1],"BEGIN")
                memory = self.RunProcess(memory)
        return memory
            
          
    def RunProcess(self,memory):
        if(self.runningProcess[1] == "RT"):
            if(self.runningProcess[0][1].execTime-1 == 0):
                #desalocar recursos aqui
                memory.FreeMem(self.runningProcess[0][1].PID)
                self.PrintProcess(self.runningProcess[0][1],"RUNNING")
                self.PrintProcess(self.runningProcess[0][1],"END")
                self.runningProcess = (0,"")
            else:
                self.PrintProcess(self.runningProcess[0][1],"RUNNING")
                self.runningProcess[0][1].execTime -= 1
                
                #roda processo de tempo real
        elif(self.runningProcess[1] == "User"):
            if(self.runningProcess[0][1].execTime-1 == 0):
                #desalocar recursos aqui
                memory.FreeMem(self.runningProcess[0][1].PID)
                self.PrintProcess(self.runningProcess[0][1],"RUNNING")
                self.PrintProcess(self.runningProcess[0][1],"END")
                self.runningProcess = (0,"")
            else:
                self.PrintProcess(self.runningProcess[0][1],"RUNNING")
                self.runningProcess[0][1].execTime -= 1
               
                #roda processo de usuario
                if(self.runningProcess[0][0] > 0):
                    self.runningProcess[0][0] -= 1
                    self.runningProcess[0][1].priority -= 1
                for i in range(self.UserQueue.qsize()):
                    aux = self.UserQueue.get()
                    if(aux[0] > 0):
                        aux[1].priority -= 1
                        aux[0] -= 1
                        self.UserQueue.put(aux[0])
                    else:
                        self.UserQueue.put(aux[0])
        return memory
    def PlaceInFrontOfQueue(self,queue,item):
        queue.put(item)
        for i in range(queue.qsize()-1):
                queue.put(queue.get())
        return queue
    def PrintDispatcher(self,process):
        print("dispatcher =>\n\
        \tPID: {}\n\
        \toffset: {}\n\
        \tblocks: {}\n\
        \tpriority: {}\n\
        \ttime: {}\n\
        \tprinters: {}\n\
        \tscanners: {}\n\
        \tmodems: {}\n\
        \tdrives: {}".format(process.PID,
                             process.memOffset,
                             process.size,
                             process.priority,
                             process.execTime,
                             process.printNumber,
                             process.scanNumber,
                             process.modemNumber,
                             process.diskNumber))
    def PrintProcess(self,process,state):
        if(state == "BEGIN"):
            print("P{} STARTED".format(process.PID))
        elif(state == "RUNNING"):
            print("P{} instruction {}".format(process.PID,process.instruction-process.execTime))
        elif(state == "END"):
            print("P{} return SIGINT".format(process.PID))
        else:
            print("P{} Stopping...".format(process.PID))
