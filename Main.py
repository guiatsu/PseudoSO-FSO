from src.OperationalSystem import *
import sys
if(len(sys.argv) < 3):
    print("quantidade de argumentos invalida!")
else:
    OS = OperationalSystem(sys.argv[1],sys.argv[2])
    OS.Run()

