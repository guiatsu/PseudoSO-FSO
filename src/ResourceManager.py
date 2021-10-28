class ResourceManager:
    def __init__(self):
        self.scanAvail = ["Avail"]
        self.printAvail = ["Avail"]*2
        self.modemAvail = ["Avail"]
        self.sataAvail = ["Avail"]*2
        self.scanMaxQtt = 1
        self.printMaxQtt = 2
        self.modemMaxQtt = 1
        self.sataMaxQtt = 2

    def CanAlloc(self,printNumber,scanNumber,modemNumber,sataNumber):
        if(scanNumber >= self.scanMaxQtt or scanNumber < 0):
            return "scan de codigo "+str(scanNumber)+" nao existe"
        if(printNumber >= self.printMaxQtt or printNumber < 0):
            return "impressora de codigo "+str(printNumber)+" nao existe"
        if(modemNumber >= self.modemMaxQtt or modemNumber < 0):
            return "modem de codigo "+str(modemNumber)+" nao existe"
        if(sataNumber >= self.sataMaxQtt or sataNumber < 0):
            return "disco de codigo "+str(sataNumber)+" nao existe"
        return ""

    def AllocResources(self,printNumber,scanNumber,modemNumber,sataNumber):
        msg = ""

        if(self.scanAvail[scanNumber] == "UnAvail"):
            msg += "Scanner de codigo "+str(scanNumber)+" esta indisponivel"
        if(self.printAvail[printNumber] == "UnAvail"):
            if(msg != ""):
                msg+= ", "
            msg += "Impressora de codigo "+str(printNumber)+" esta indisponivel"
        if(self.modemAvail[modemNumber] == "UnAvail"):
            if(msg != ""):
                msg+= ", "
            msg += "Modem de codigo "+str(modemNumber)+" esta indisponivel"
        if(self.sataAvail[sataNumber] == "UnAvail"):
            if(msg != ""):
                msg+= ", "
            msg += "Dispositivo Sata de codigo "+str(sataNumber)+" esta indisponivel"
        msg+= "."

        if(msg == "."):
            self.scanAvail[scanNumber] = "UnAvail"
            self.printAvail[printNumber] = "UnAvail"
            self.modemAvail[modemNumber] = "UnAvail"
            self.sataAvail[sataNumber] = "UnAvail"
            return ""
        else:
            return msg
    def FreeResources(self,printNumber,scanNumber,modemNumber,sataNumber):
        self.scanAvail[scanNumber] = "Avail"
        self.printAvail[printNumber] = "Avail"
        self.modemAvail[modemNumber] = "Avail"
        self.sataAvail[sataNumber] = "Avail"
