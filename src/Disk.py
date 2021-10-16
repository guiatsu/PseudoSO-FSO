class Disk:
    def __init__(self, max_size):
        self.max_size = max_size
        self.memory = [""]*max_size
        self.qttOcuppied = 0
    def FindValidSegment(self,size):
        cont = 0
        for i in range(len(self.memory)):
            if (i+size <= len(self.memory)):
                if(self.memory[i] == ""):
                    for j in range(i,i+size):
                        if(self.memory[j] == ""):
                            cont += 1
                        if(cont == size):
                            return i
                else:
                    i += cont
            else:
                break
            cont = 0
        return -1
    def CreateFile(self, name, initial_block, size):
        if(self.max_size-self.qttOcuppied < size):
            return "Nao pode criar o arquivo "+name+" (falta de espaco) ."
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
                    if(self.memory[i] != ""):
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
                        self.memory[int(i)] = name
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
                
    def DeleteFile(self, name):
        nameFound = False
        for i in range(len(self.memory)):
            if(self.memory[i] == name):
                self.memory[i] = ""
                nameFound = True
        if(not nameFound):
            return "Nao pode deletar o arquivo "+name+" porque ele nao existe."
        return "Deletou o arquivo "+name