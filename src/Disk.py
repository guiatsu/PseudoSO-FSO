class Disk:

    def __init__(self, max_size):

        self.max_size = max_size
        self.memory = [("0",None)]*max_size
        self.qttOcuppied = 0

    def FindValidSegment(self,size):
        cont = 0
        for i in range(len(self.memory)):
            if (i+size <= len(self.memory)):
                if(self.memory[i][0] == "0"):
                    for j in range(i,i+size):
                        if(self.memory[j][0] == "0"):
                            cont += 1
                        if(cont == size):
                            return i
                else:
                    i += cont+1
            else:
                break
            cont = 0
        return -1


    def CreateFile(self,PID,process, name, initial_block, size):

        if(self.max_size-self.qttOcuppied < size):
            return "Nao pode criar o arquivo "+name+" (falta de espaco) ."
        elif(process == None):
            return "Nao pode criar o arquivo "+name+" (processo "+str(PID)+" nao existe)"
        else:
            if(initial_block >= self.max_size):
                return "Nao pode criar o arquivo "+name+" (bloco inicial ocupado) ."
            elif(initial_block + size >= self.max_size):
                return "Nao pode criar o arquivo "+name+" (quantidade de blocos insuficientes no disco) ."
            elif(size < 0):
                return "Nao pode criar o arquivo "+name+" (quantidade de blocos invalida, numero negativo) ."
            elif(initial_block < 0):
                return "Nao pode criar o arquivo "+name+" (falta de espaco) ."
            else:
                invalid = []
                valid = []
                for i in range(initial_block,initial_block+size):
                    if(self.memory[i][0] != "0"):
                        invalid.append(str(i))
                    else:
                        valid.append(str(i))   
                if(invalid):
                    if(len(invalid) == 1):
                        return "Nao pode criar o arquivo "+name+" (bloco "+invalid[0]+" ocupado) ."
                    
                    else:
                        ret = ""
                        if(invalid):
                            ret+= invalid[0]
                            for i in range(1,len(invalid)-1):
                                ret+= ", "+invalid[i]
                            
                            ret +=  " e " + invalid[len(invalid)-1]
                            return "Nao pode criar o arquivo "+name+" (blocos "+ret+" ocupados) ."
                    
                else:
                    for i in valid:
                        self.memory[int(i)] = (name,int(PID))
                        self.qttOcuppied += 1
                    if(len(valid) == 1):
                        return "Criou o arquivo "+name+" (bloco "+valid[0]+") ."
                    else:
                        ret = ""
                        ret+= valid[0]
                        for i in range(1,len(valid)-1):
                            ret+= ", "+valid[i]
                        ret +=  " e " + valid[len(valid)-1]
                        return "Criou o arquivo "+name+" (blocos "+ret+") ."
                
    def DeleteFile(self,PID,process, name):
        nameFound = False
        invalidProcess = False
        if(process == None):
            return "O processo "+str(PID)+" nao existe"
        
        for i in range(len(self.memory)):
            if(self.memory[i][0] == name):
                nameFound = True
                if(process["priority"] == 0 or self.memory[i][1] == process["PID"]):
                    self.memory[i] = "0"
                else:
                    invalidProcess = True
        msg = ""
        if(invalidProcess):
            msg = "O processo "+str(process["PID"])+" nao pode deletar o arquivo, pois ele nao tem permissao"
        if(not nameFound):
            if(msg != ""):
                msg += " "
            msg += "O processo "+str(process["PID"])+" nao pode deletar o arquivo "+name+" porque ele nao existe."
        if(invalidProcess or not nameFound):
            return msg        
        return "Deletou o arquivo "+name