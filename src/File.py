def read_file(path):
    file = open(path,'r')
    text = []
    for line in file:
        line = line.strip().split(", ")
        text.append(line)
    return text