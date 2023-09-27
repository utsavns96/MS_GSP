#MS_GSP

import re

def readdata():
    #print("Data:")
    data = [] #holds our formatted data
    lines = [] #holds lines of the input file
    temp = [] #temp list #1 - holds items in one record <>
    temp1 = [] #temp list #2 - holds items in one set of {}
    f = open("data.txt", "r")
    for line in f:
        line = line.replace('<','')
        line = line.replace('>','')
        lines.append(line.rstrip('\n'))
    for t in lines:
        t = t.strip()[1:-1]
        for s in re.split(r'}{',t):
            #print("new itemset")
            for i in re.split(', ',s):
                temp1.append(int(i))
                #print(i)
                #print("temp1 = ",temp1)
            temp.append(temp1)
            #print("temp = ",temp)
            temp1 = []
        data.append(temp)
        temp = []
        #print("new line")
    #print(data)
    f.close()
    return data
    
def readparam():
    mis = [] #holds our minsups
    temp = [] #temp list #1
    sdc = 0
    #print("\nParameters:")
    f = open("para1-1.txt", "r")
    for line in f:
        #print(line.find("MIS"))
        if(line.find("MIS")==0):
            #print(line)
            temp = line.split('=')
            item = temp[0][temp[0].find("(")+1:temp[0].find(")")]
            #item = re.findall(r'\(.*?\)', temp[0])
            value = float(temp[1].rstrip("\n"))
            mis.append([item,value])
            #print(item,"-",value)
        #print(line)
        else:
            sdc = float(line.split('=')[1])
            
    f.close()
    return mis,sdc


data = readdata()
print("Data:\n",data)
print("\n************\n")
mis, sdc = readparam()
print("MIS:\n",mis)
print("\n************\n")
print("SDC = ",sdc)