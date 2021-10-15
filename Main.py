from src.File import *
from src.Disk import *

file = read_file("assets/files.txt")
disk = Disk(int(file[0][0]))
for i in range(2,2+int(file[1][0])):
    print(disk.CreateFile(file[i][0],int(file[i][1]),int(file[i][2])))
print(disk.memory)
for i in range(2+int(file[1][0]),len(file)):
    if(int(file[i][1]) == 1):
        print(disk.DeleteFile(file[i][2]))
    else:
        print(disk.CreateFile(file[i][2],disk.FindValidSegment(int(file[i][3])),int(file[i][3])))