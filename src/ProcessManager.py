from src.Process import *
from queue import Queue

class ProcessManager:

    def __init__(self):
        self.nextPID = 0

        self.RTQueue = Queue()
        self.UserQueue = [Queue(),Queue(),Queue()]
        self.processes = {}
        self.qttProcessInQueue = 0
        self.runningProcess = (0,"")


    def AddProcess(self,process, processType,memory,ResourceManager):
        if(self.qttProcessInQueue >= 1000):
            self.nextPID += 1
            return memory, "processo "+str(self.nextPID-1)+", nao sera executado, pois excedeu o limite da fila",ResourceManager
        else:
            if(processType == 'RT'):
                memOffset = memory.FindValidSegment(int(process[3]),processType)
                if(memOffset < 0):
                    self.nextPID += 1
                    return memory, "processo "+str(self.nextPID-1)+", nao sera executado, pois excedeu o limite de memoria",ResourceManager
                else:
                    memory.MemAlloc(self.nextPID,memOffset,processType,int(process[3]))
                    self.RTQueue.put(Process(self.nextPID,memOffset,process))
                    self.nextPID += 1
                    self.qttProcessInQueue += 1
            elif(processType == 'User'):
                text = ResourceManager.CanAlloc(int(process[4]),int(process[5]),int(process[6]),int(process[7]))
                if(text == ""):
                    memOffset = memory.FindValidSegment(int(process[3]),processType)
                    if(memOffset < 0):
                        self.nextPID += 1
                        return memory, "processo "+str(self.nextPID-1)+", nao sera executado, pois excedeu o limite de memoria",ResourceManager
                    else:
                        memory.MemAlloc(self.nextPID,memOffset,processType,int(process[3]))
                        self.UserQueue[int(process[1])-1].put(Process(self.nextPID,memOffset,process))
                        self.nextPID += 1
                        self.qttProcessInQueue += 1

                else:
                    return memory, text, ResourceManager

            self.processes[self.nextPID-1] = {
                        "PID" : int(self.nextPID-1),
                        "memOffset" : int(memOffset),
                        "initTime" : int(process[0]),
                        "priority" : int(process[1]),
                        "execTime" : int(process[2]),
                        "size" : int(process[3]),
                        "printNumber" : int(process[4]),
                        "scanNumber" : int(process[5]),
                        "modemNumber" : int(process[6]),
                        "sataNumber" : int(process[7]),
            }
            
            return memory, "",ResourceManager

    def Update(self,memory,ResourceManager):

        if((self.RTQueue.qsize() > 0) or self.runningProcess[1] == "RT"):
            if(self.runningProcess[1] == "User"):

                    self.UserQueue[self.runningProcess[0].priority-1] = self.PlaceInFrontOfQueue(
                                                                            self.UserQueue[self.runningProcess[0].priority-1],
                                                                            self.runningProcess[0]
                                                                        )
                    self.runningProcess[0].Print("STOPPING")

                    process = self.runningProcess[0]
                    ResourceManager.FreeResources(process.printNumber,process.scanNumber,process.modemNumber,process.sataNumber)
                    self.RTQueue,ResourceManager = self.PrepareToRun(self.RTQueue,"RT",ResourceManager)
                    memory,ResourceManager = self.RunProcess(memory,ResourceManager)
            elif(self.runningProcess[1] == "RT"):
                memory,ResourceManager = self.RunProcess(memory,ResourceManager)
            else:
                self.RTQueue,ResourceManager = self.PrepareToRun(self.RTQueue,"RT",ResourceManager)
                memory,ResourceManager = self.RunProcess(memory,ResourceManager)
        else:
            queueToGet = 0
            queueHasMember = False
            if(self.UserQueue[0].qsize() > 0):
                queueToGet = 0
                queueHasMember = True
            elif(self.UserQueue[1].qsize() > 0):
                queueToGet = 1
                queueHasMember = True
            elif(self.UserQueue[2].qsize() > 0):
                queueToGet = 2
                queueHasMember = True
            if(queueHasMember or self.runningProcess[1] == "User"):
                if(self.runningProcess[1] == "User"):
                    if((queueHasMember) and (queueToGet+1 < self.runningProcess[0].priority)):
                        self.runningProcess[0].Print("STOPPING")
    
                        process = self.runningProcess[0]
                        ResourceManager.FreeResources(process.printNumber,process.scanNumber,process.modemNumber,process.sataNumber)
                        aux = self.runningProcess
                        self.PlaceInFrontOfQueue(self.UserQueue[aux[0].priority-1],aux[0])
                        self.UserQueue[queueToGet],ResourceManager = self.PrepareToRun(self.UserQueue[queueToGet],"User",ResourceManager)
                        memory,ResourceManager = self.RunProcess(memory,ResourceManager)
                    else:
                        memory,ResourceManager = self.RunProcess(memory,ResourceManager)
                else:
                    self.UserQueue[queueToGet],ResourceManager = self.PrepareToRun(self.UserQueue[queueToGet],"User",ResourceManager)
                    memory,ResourceManager = self.RunProcess(memory,ResourceManager)
                

        return memory,ResourceManager
            
          
    def RunProcess(self,memory,ResourceManager):
        if(self.runningProcess[1] == "RT"):
            if(self.runningProcess[0].execTime-1 == 0):
                memory.FreeMem(self.runningProcess[0].PID)
                self.runningProcess[0].Print("RUNNING")
                self.runningProcess[0].Print("END")
                self.runningProcess = (0,"")
                self.qttProcessInQueue -= 1
            else:
                self.runningProcess[0].Print("RUNNING")
                self.runningProcess[0].execTime -= 1
                
                #roda processo de tempo real
        elif(self.runningProcess[1] == "User"):
            if(self.runningProcess[0].execTime-1 == 0):
                process = self.runningProcess[0]
                ResourceManager.FreeResources(process.printNumber,process.scanNumber,process.modemNumber,process.sataNumber)
                memory.FreeMem(self.runningProcess[0].PID)
                self.runningProcess[0].Print("RUNNING")
                self.runningProcess[0].Print("END")
                self.runningProcess = (0,"")
                self.qttProcessInQueue -= 1
            else:
                self.runningProcess[0].Print("RUNNING")
                self.runningProcess[0].execTime -= 1
               
                #roda processo de usuario
                if(self.runningProcess[0].priority > 1):
                    self.runningProcess[0].priority -= 1
        return memory,ResourceManager
    def PrepareToRun(self,queue,processType,ResourceManager):
        self.runningProcess = (queue.get(),processType)
        if(processType == "User"):
            process = self.runningProcess[0]
            text = ResourceManager.AllocResources(process.printNumber,process.scanNumber,process.modemNumber,process.sataNumber)
            if(text != ""):
                print(text)
        self.PrintDispatcher(self.runningProcess[0])
        self.runningProcess[0].Print("BEGIN")
        return queue,ResourceManager

    def PlaceInFrontOfQueue(self,queue,item):
        queue.put(item)
        for i in range(queue.qsize()-1):
            queue.put(queue.get())

        return queue
    def UpdatePriorities(self):
        for i in range(1,len(self.UserQueue)):
            for j in range(self.UserQueue[i].qsize()):
                aux = self.UserQueue[i].get()
                if(aux.priority > 1):
                    aux.priority -= 1
                    self.UserQueue[i].put(aux)
                else:
                    self.UserQueue[i].put(aux)
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
                             process.sataNumber))
