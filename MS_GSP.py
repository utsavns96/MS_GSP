#MS_GSP

import re
from candidate_gen import *

rest = -998
count_c = {}  # to keep track of "count" of each candidate

def readdata():
    '''
    Read input data file and format it as a list of lists
    '''
    #print("Data:")
    data = [] #holds our formatted data
    lines = [] #holds lines of the input file
    temp = [] #temp list #1 - holds items in one record <>
    temp1 = [] #temp list #2 - holds items in one set of {}
    f = open("test-data/small-data-1/data-1.txt", "r")
    #f = open("test-data/large-data-2/data2.txt", "r")
    #f = open("data.txt", "r")
    for line in f:
        line = line.replace('<','')
        line = line.replace('>','')
        lines.append(line.rstrip('\n'))
    for t in lines:
        if not t:
            continue
        else:
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
    #f = open("test-data/small-data-1/para1-1.txt", "r")
    f = open("test-data/small-data-1/para1-2.txt", "r")
    #f = open("test-data/large-data-2/para2-1.txt", "r")
    #f = open("test-data/large-data-2/para2-2.txt", "r")
    for line in f:
        #print(line.find("MIS"))
        if(line.find("MIS")==0):
            #print(line)
            temp = line.split('=')
            item = temp[0][temp[0].find("(")+1:temp[0].find(")")]
            #item = re.findall(r'\(.*?\)', temp[0])
            value = float(temp[1].rstrip("\n"))
            if item == 'rest':
                item = rest
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
                    if item in mis:
                        temp.append(mis[item])
                    else:
                        mis[item] = mis[rest]
                        temp.append(mis[rest])
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
    for i in m:
        for transaction in S:
            for sequence in transaction:
                if i in sequence:
                    if i in supportcounts:
                        supportcounts[i] += 1
                    else:
                        supportcounts[i] = 1
                    break
    #Step 2: follow sorted order to find the first item i in m that meets i.count/n >= MIS(i).
    mis_i = 0
    #find the first item i in M that meets MIS(i)
    for i in m:
        if(len(L)==0):
            if i in mis:
                if(supportcounts[i]/len(data) >= mis[i]):
                    #L.append(i)
                    mis_i = mis[i]
                    L[i]=supportcounts[i]
            else:
                if(supportcounts[i]/len(data) >= mis[rest]):
                    #L.append(i)
                    mis_i = mis[rest]
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
    ret = []
    for candidate in L:
        #val = supportcounts[candidate]/num_sequences # f.count / n
        if candidate in mis:
            if L[candidate]/num_sequences >= mis[candidate]:
                ret.append((candidate, ))
        else:
            if L[candidate]/num_sequences >= mis[rest]:
                ret.append((candidate, ))
    return ret

def is_orderedsubset(s1, s2):
    first_index = -1
    for idx, item in enumerate(s2):
        if item == s1[0]:
            first_index = idx
            break
    if first_index == -1:
        return False

    idx_2 = first_index

    for idx, item in enumerate(s1):
        if idx_2 >= len(s2):
            return False
        if item == s2[idx_2]:
            idx_2 += 1
        else:
            return False
    return True

def is_subset(s1, s2):
    return all(item in s2 for item in s1)

def sumtaken(taken):
    count = 0
    for i in taken:
        if i == 1:
            count += 1
    return count

def is_contained(c, s):
    c_taken = []
    taken = []
    for subseq in s:
        taken.append(0)
    for subseq in c:
        c_taken.append(0)
    if not isinstance(c[0], tuple): # C is a 2-tuple of ints
        for subseq in s:
            if is_subset(c, subseq):
                return True
    else:
       for i, item in enumerate(c):
            for j, subseq in enumerate(s):
                if is_subset(item, subseq):
                    if taken[j] != 1:
                        taken[j]= 1
                        c_taken[i] = 1
                        break
                else:
                    taken[j] = 1
    if sumtaken(c_taken) == len(c):
        return True
    return False

def minMIS(c,mis):
    if isinstance(c[0], tuple):
        min_mis = mis[c[0][0]]
    else:
        min_mis = mis[c[0]]
    for tup in c:
        if isinstance(tup, tuple):
            for item in tup:
                if item in mis:
                    if mis[item] < min_mis:
                        min_mis = mis[item]
                else:
                    if mis[rest] < min_mis:
                        min_mis = mis[rest]
        else:
            if tup in mis:
                if mis[tup] < min_mis:
                    min_mis = mis[tup]
            else:
                if mis[rest] < min_mis:
                    min_mis = mis[rest]
    return min_mis


def remove_mis(c, min_mis, mis):
    removed = False
    c2 = []
    for tup in c:
        if isinstance(tup, tuple):
            new_tup = []
            for item in tup:
                if not removed and mis[item] == min_mis:
                    removed = True
                else:
                    new_tup.append(item)
            if len(new_tup) > 0:
                c2.append(tuple(new_tup))
        else:
            if not removed and mis[tup] == min_mis:
                removed = True
            else:
                c2.append(tup)
    return tuple(c2, )


def print_k_sequence(Fk, k, output):
    output.write("**************************************\n{}-sequences:\n\n".format(k))
    print_sequences = ""
    for f in Fk:
        sequence = ""
        if isinstance(f, tuple):
            is_nested_tuple = True
            for i in f:
                if not isinstance(i, tuple):
                    is_nested_tuple = False
                    break
            if is_nested_tuple:
                for item in f:
                    sequence += '{' + ','.join(map(str, item)) + '}'
            else:
                sequence = '{' + ','.join(map(str, f)) + '}'
        else:
            sequence = '{' + str(f) + '}'
        print_sequences += "<" + sequence + ">\n"
    output.write(print_sequences + "\n")
    output.write("The count is: {}\n".format(len(Fk)))


# GSP algorithm:
def GSP(S,m,mis, sdc):
    L = init_pass(S,m,mis)
    print("L: ",L)
    print("\n************\n")
    F = [] # frequent itemsets
    F.append(filter(L, mis, len(S))) # F1
    # writing to file
    output = open("output.txt", "w")
    print_k_sequence(F[0], 1, output)
    print("F: ", F)
    print("\n************\n")
    k = 2
    while len(F[k-2]) != 0: # for (k=2; Fk-1 not empty; k++), F[k-2] is Fk-1
        if k == 2:
            Ck = level2_candidate_gen_SPM(L, sdc, mis, len(S))
        else:
            Ck = mscandidate_gen_SPM(F[k-2], mis) # F[k-2] is Fk-1
        for s in S:
            for c in Ck:
                if is_contained(c, s):
                    count_c[c] = count_c.get(c, 0) + 1
                    # if c’ is contained in s, where c’ is c after an occurrence of c.minMISItem is removed from c
                mis_c = minMIS(c,mis)
                c2 = remove_mis(c, mis_c, mis)
                if is_contained(c2, s):
                    count_c[c2] = count_c.get(c2, 0) + 1
        Fk = set()
        for c in Ck:
            if c in count_c and count_c[c]/len(S) >= minMIS(c, mis):
                Fk.add(c)
        if(len(Fk) > 0):
            print_k_sequence(Fk, k, output)
        F.append(Fk)
        k += 1 # k++
    return F

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
    F = GSP(data,m, mis, sdc)
    print(F)