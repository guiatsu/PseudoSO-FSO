class Memory:
    
    def __init__(self):
        self.RTMSize = 64
        self.UsrMSize = 960
        self.memory = [None]*(self.RTMSize+self.UsrMSize)
        self.qttOccupiedUsrM = 0
        self.qttOccupiedRTM = 0

    def FindValidSegment(self,size,processType):
        cont = 0
        begin = 0
        end = 0
        memsize = 0
        if(processType == 'RT'):
            end = self.RTMSize
            memsize = self.RTMSize
        if(processType == 'User'):
            begin = self.RTMSize
            end = self.RTMSize+self.UsrMSize
            memsize = self.UsrMSize
        for i in range(begin,end):
            if (i+size <= memsize):
                if(self.memory[i] == None):
                    for j in range(i,i+size):
                        if(self.memory[j] == None):
                            cont += 1
                        if(cont == size):
                            return i
                else:
                    i += cont+1
            else:
                break
            cont = 0
        return -1
    def FreeMem(self,PID):
        PIDFound = False
        for i in range(len(self.memory)):
            if(self.memory[i] == PID):
                self.memory[i] = None
                PIDFound = True
        if(not PIDFound):
            return "Nao pode liberar o processo "+str(PID)+" da memoria porque ele nao existe."
        return "Liberou o processo "+str(PID)+" da memoria"

    def MemAlloc(self,PID,initial_block,processType,size):
        cont = 0
        end = 0
        memsize = 0
        qttOcuppied = 0
        if(processType == 'RT'):
            end = self.RTMSize
            memsize = self.RTMSize
            qttOcuppied = self.qttOccupiedRTM

        if(processType == 'User'):
            end = self.RTMSize+self.UsrMSize
            memsize = self.UsrMSize
            qttOcuppied = self.qttOccupiedUsrM

        if(memsize-qttOcuppied < size):
            return "Nao pode alocar memoria para o processo "+str(PID)+" (falta de espaco) ."
        else:
            if(initial_block >= end):
                return "Nao pode alocar memoria para o processo "+str(PID)+" (bloco inicial ocupado) ."
            elif(initial_block + size > end+1):
                return "Nao pode alocar memoria para o processo "+str(PID)+" (quantidade de blocos insuficientes na memoria) ."
            elif(size < 0):
                return "Nao pode alocar memoria para o processo "+str(PID)+" (quantidade de blocos invalida, numero negativo) ."
            elif(initial_block < 0):
                return "Nao pode alocar memoria para o processo "+str(PID)+" (falta de espaco) ."
            else:
                invalid = []
                valid = []
                for i in range(initial_block,initial_block+size):
                    if(self.memory[i] != None):
                        invalid.append(str(i))
                    else:
                        valid.append(str(i))   
                if(invalid):
                    if(len(invalid) == 1):
                        return "Nao pode alocar memoria para o processo "+str(PID)+" (bloco "+invalid[0]+" ocupado) ."
                    
                    else:
                        ret = ""
                        if(invalid):
                            ret+= invalid[0]
                            for i in range(1,len(invalid)-1):
                                ret+= ", "+invalid[i]
                            
                            ret +=  " e " + invalid[len(invalid)-1]
                            return "Nao pode alocar memoria para o processo "+str(PID)+" (blocos "+ret+" ocupados) ."
                    
                else:
                    for i in valid:
                        self.memory[int(i)] = PID
                        if(processType == 'RT'):
                            self.qttOccupiedRTM += 1
                        elif(processType == 'User'):
                            self.qttOccupiedUsrM += 1
                    if(len(valid) == 1):
                        return "Criou o processo "+str(PID)+" (bloco "+valid[0]+") ."
                    else:
                        ret = ""
                        ret+= valid[0]
                        for i in range(1,len(valid)-1):
                            ret+= ", "+valid[i]
                        ret +=  " e " + valid[len(valid)-1]
                        return "Criou o processo "+str(PID)+" (blocos "+ret+") ."