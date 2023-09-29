#MS_GSP

import re

def readdata():
    '''
    Read input data file and format it as a list of lists
    '''
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
    '''
    Read input parameters file and store

    Returns
    -------
    mis : dictionary
        dict with mis values stored at index values corresponding to item values.
    sdc : float
        sdc value.

    '''
    mis = {} #holds our minsups
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
            mis[int(item)] = value
            #print(item,"-",value)
        #print(line)
        else:
            sdc = float(line.split('=')[1])
            
    f.close()
    return mis,sdc

def sortdata(data,mis):
    '''
    Go through the itemsets and sort the items based on their MIS values
    :param data: list of raw data read from file
    :param mis: mis values
    :return: List of lists of sorted itemsets
    '''
    temp = [] #temp variable to hold the MIS values that we need
    m=[] #final sorted items
    for itemset in data:
        for sequence in itemset:
            for item in sequence:
                if(item not in m):
                    m.append(item)
                    temp.append(mis[item])
    m = [x for _,x in sorted(zip(temp,m))]
    return m


def init_pass(S,m,mis):
    '''
    Go through dataset "S" once to calculate support count of individual items.
    :param S:
    :param m:
    :return: A dictionary with key being the item, value being count.
    '''
    supportcounts = {}
    #L=[]
    L={}
    #Step 1: Scan through data and record support count
    for itemset in S:
        for sequence in itemset:
            for item in sequence:
                if item in supportcounts:
                    supportcounts[item] += 1
                else:
                    supportcounts[item] = 1
    #Step 2: follow sorted order to find the first item i in m that meets i.count/n >= MIS(i).
    mis_i = 0
    #find the first item i in M that meets MIS(i)
    for i in m:
        if(len(L)==0):
            if(supportcounts[i]/len(data) >= mis[i]):
                #L.append(i)
                mis_i = mis[i]
                L[i]=supportcounts[i]
        # For each subsequent item j in M after i, if j.count/n >= MIS(i), then j is also inserted into L
        else:
            if(supportcounts[i]/len(data) >= mis_i):
                #L.append(i)
                L[i]=supportcounts[i]
    #return L,supportcounts
    return L

def filter(L, mis, num_sequences):
    '''
    Go through candidates "C", filter out those that fall below minsup for that item.
    F <- {<F> | for f in C, f.count >= minsup}
    :param L: Candidates from init_pass
    :param mis: list of minsups
    :num_sequences: number of sequences in S (len(S))
    :return: A dictionary with key being the item, value being count.
    '''
    ret = {}
    for candidate in L:
        #val = supportcounts[candidate]/num_sequences # f.count / n
        if L[candidate]/num_sequences >= mis[candidate]:
            ret[candidate] = L[candidate]
    return ret

# GSP algorithm:
def GSP(S,m,mis):
    L= init_pass(S,m,mis)
    print("L: ",L)
    print("\n************\n")
    F = filter(L, mis, len(S))
    print("F: ", F)
    print("\n************\n")

if __name__ == "__main__":
    data = readdata()
    print("Data:\n",data)
    print("\n************\n")
    mis, sdc = readparam()
    print("MIS:\n",mis)
    print("\n************\n")
    print("SDC = ",sdc)
    print("\n************\n")
    m = sortdata(data,mis)
    print("Sorted Data:\n",m)
    print("\n************\n")
    GSP(data,m, mis)