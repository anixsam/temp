import os 

path ="./image_data"
dir_list = os.listdir(path)

def initializeImageData():
    file = open("names.txt","w")
    for i in range(0,len(dir_list)):
        dir = str(dir_list[i])
        file.write(dir[0:len(dir_list[i])-4]+"\n")
    file.close()