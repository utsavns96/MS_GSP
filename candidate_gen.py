from MS_GSP import readdata, readparam, init_pass, sortdata, minMIS
from copy import deepcopy

data = readdata()
mis, sdc = readparam()
m = sortdata(data, mis)
rest = -998

def sup(item, data):
    ret = 0
    for t in data:
        x = t[0]
        y = t[1]
        if item in x or item in y:
            ret += 1
    return ret


def level2_candidate_gen(L, phi, mis, num_sequences):
    C2 = set()
    keys = list(L.keys())
    for index, l in enumerate(L):
        if L[l] / num_sequences >= mis[l]:
            for h in keys[index:]:  # "for each item h in L that is after l, do:"
                if L[h] / num_sequences >= mis[l] and abs(sup(h, data) - sup(l, data)) <= phi:
                    C2.add((l, h))  # insert the candidate {l,h} into C2
    return C2


def level2_candidate_gen_SPM(L, phi, mis, num_sequences):
    C2 = set()
    keys = list(L.keys())
    mis_l = 0.0
    for index, l in enumerate(L):
        if l in mis:
            mis_l = mis[l]
        else:
            mis_l = mis[rest]
        if L[l] / num_sequences >= mis_l:
            for h in keys[index:]:  # "for each item h in L that is after l, do:"
                if L[h] / num_sequences >= mis_l and abs(L[h] / num_sequences - L[l] / num_sequences) <= phi:
                    # join step: merge sequences containing l and h
                    if l < h:
                        new_sequence = [l, h]
                        C2.add(tuple(new_sequence))
                    elif h > l:
                        new_sequence = [h, l]
                        C2.add(tuple(new_sequence))
                    C2.add(((l,), (h,)))
                    C2.add(((h,),(l,)))
    return C2


def flatten_subsequence(t):
    l = []
    for i in t:
        if isinstance(i, tuple):
            l = l + flatten_subsequence(i)
        else:
            l.append(i)
    return l

def join_step(s1, s2):
    new_tup = ()
    # if the subsequence obtained by dropping the first item of s1
    # is the same as the subsequence obtained by dropping the last item of s2,
    if flatten_subsequence(s1)[1:] == flatten_subsequence(s2)[:-1]:
        # the candidate sequence is the sequence s1 extended with the last item in s2
        if isinstance(s2[-1], tuple) and Length(s2[-1]) == 1: # last item of s2 is a tuple {20}
            #new_sequence = list(s1)
            #new_sequence.append(s2[-1])
            #new_tup = tuple(new_sequence)
            if isinstance(s1[0], tuple):
                new_seq = list(s1)
                new_seq.append(s2[-1])
                new_tup = tuple(new_seq,)
            else:
                new_tup = tuple([s1,s2[-1]])
                #new_tup=(tuple(list(s1)),s2[-1])
            #Ck.add(tuple(new_sequence))
        elif isinstance(s2[-1], tuple) and Size(s1) > 1: # last item of s2 is a tuple of size >1 i.e. {20,30}
            new_seq = list(s1[-1])
            new_item = s2[-1][-1]
            new_seq.append(new_item)
            new_seq = tuple(new_seq)
            new_tup = (list(s1[:1]))
            new_tup.append(new_seq)
            new_tup = tuple(new_tup)
        else: # S2 is not a tuple
            if isinstance(s1[-1], tuple):
                new_sequence = s1[-1] + (s2[-1], )
                new_tup = s1[:-1] + (tuple(new_sequence),)
                #Ck.add(new_tup)
            else: # it's an integer,
                new_sequence = list(s1)
                if isinstance(s2[-1], int):
                    new_sequence.append(s2[-1])
                else: #{20,30}
                    new_sequence.append(s2[-1][-1])
                new_tup = tuple(new_sequence)
                #Ck.add(new_tup)
        # if new_tup == ():
        #     print("new_tup is empty\ns1:", s1, "\ns2: " , s2)
    return new_tup

def Size(s):
    if isinstance(s[0], int):
        return 1
    else:
        return len(s)

def Length(s):
    return len(flatten_subsequence(s))

def prune_step(Fk_1,Ck, mis):
    final_Ck = set()
    for index_c, c in enumerate(Ck):
        c_list = []
        temp_list = []
        if isinstance(c[0], tuple):
            for i in c:
                c_list.append(i)
        else:
            t = []
            for i in c:
                t.append(i)
            c_list.append(t)

        for index_seq, seq_t in enumerate(c_list):
            seq = []
            if(isinstance(c_list[0], tuple)):
                for s in seq_t:
                    seq.append(s)
            else:
                seq = seq_t
            #1. find minMIS and item with minMIS
            min_mis_seq_item = seq[0]
            print(c)
            for item in seq:
                if(mis[item]<mis[min_mis_seq_item]):
                    min_mis_seq_item = item
            #print("min_mis_seq_item: ", min_mis_seq_item)
            #2. find all k-1 sequences and store them in a list
            for index_i, i in enumerate(seq):
                temp_c = []
                if(isinstance(c_list[0], tuple)):
                    for a in c_list:
                        temp_c.append(list(a))
                else:
                    temp_c = c_list
                # for a in c_list:
                #     temp_c.append(list(a))
                if(temp_c[index_seq][index_i] == min_mis_seq_item):
                    del temp_c[index_seq][index_i]
                    temp_c = list(filter(None, temp_c))
                    temp_list.append(list(temp_c))
        # print(temp_list)
        temp = 0
        #3. iterate through them and compare with Fk_1
        #first convert Fk_1 to list of lists
        f_list = []
        for f_k in Fk_1:
            temp_f = []
            if(isinstance(f_k[0], tuple)):
                for f in f_k:
                    temp_f.append(list(f))
            else:
                temp_f = list(f_k)
            f_list.append(list(temp_f))
        #print(f_list)
        for temp_l in temp_list:
            if (not any(temp_l == f_items for f_items in f_list)):
                temp += 1
            if temp == 0:
                final_Ck.add(c)
    return final_Ck


def mscandidate_gen_SPM(Fk_1, mis):
    Ck = set()
    for s1 in Fk_1:
        s1_first_mis = mis[flatten_subsequence(s1)[0]] if isinstance(s1[0], tuple) else mis[s1[0]]
        s1_first_smallest = True
        # check for condition 1
        for index,i in enumerate(s1[1:]):
            mis_i = mis[flatten_subsequence(s1)[0]] if isinstance(i, tuple) else mis[i]
            if s1_first_mis >= mis_i:
                s1_first_smallest = False
        for s2 in Fk_1:
            s2_last_smallest = False
            s2_last_mis = mis[flatten_subsequence(s2)[-1]] if isinstance(s2[-1:], tuple) else mis[s2[-1:]]
            
            # check for condition 2
            if not s1_first_smallest:
                s2_last_smallest = True
                for index, i in enumerate(s2[:-1]):
                    mis_i = mis[flatten_subsequence(s2)[-1]] if isinstance(i, tuple) else mis[i]
                    if s2_last_mis >= mis_i:
                        s2_last_smallest = False
            # condition 1: if the MIS value of the first item in a sequence (denoted by s1) is < the MIS value of every other item in s1
            if(s1_first_smallest):
                t1 = list(s1)
                t1.pop(1)
                if(t1 == list(s2)[:-1] and s2_last_mis>s1_first_mis):
                    if isinstance(s2[-1], tuple):
                        c1 = list(s1)
                        c1.append(s2[-1])
                        s1_last_item = flatten_subsequence(s1[-1:]) if isinstance(s1[-1:], tuple) else s1[-1:]
                        s2_last_item = flatten_subsequence(s2[-1:]) if isinstance(s2[-1:], tuple) else s2[-1:]
                        if Length(s1) == 2 and Size(s1) == 2 and s2_last_item > s1_last_item:
                            c2 = list(s1)
                            c2.append(flatten_subsequence(s2[-1]))
                            Ck.add(c2)
                        elif (Length(s1) == 2 and Size(s1) == 1 and s2_last_item > s1_last_item) or (Length(s1)>2):
                            c2 = list(s1)
                            c2.append(flatten_subsequence(s2[-1]))
                            Ck.add(c2)
                        Ck.add(c1)
                    
            # condition 2: if the MIS value of the last item in a sequence (denoted by s2) is < the MIS value of every other item in s2
            elif (s2_last_smallest):
                t2 = list(s2)
                t2.pop(1)
                if t2 == list(s1)[:-1] and s1_first_mis>s2_last_mis:
                    if isinstance(s1[-1], tuple):
                        c2 = list(s2)
                        c2.append(s2[-1])
                        s1_last_item = flatten_subsequence(s1[-1:]) if isinstance(s1[-1:], tuple) else s1[-1:]
                        s2_last_item = flatten_subsequence(s2[-1:]) if isinstance(s2[-1:], tuple) else s2[-1:]
                        if Length(s2) == 2 and Size(s2) == 2 and s1_last_item > s2_last_item:
                            c1 = list(s2)
                            c1.append(flatten_subsequence(s1[-1]))
                            Ck.add(c1)
                        elif Length(s2) == 2 and Size(s2) == 1 and s1_last_item > s2_last_item or Length(s2) > 2:
                            c1 = list(s2)
                            c1.append(flatten_subsequence(s1[-1]))
                            Ck.add(c1)
                        Ck.add(c2)

            # condtition 3: default case
            else:
                c1 = join_step(s1, s2) # need to update this to take s1 and s2 only instead of Fk_1 - iteration of sequences happens here
                Ck.add(c1) if c1 != () else None
         
    for c in Ck:
        print(c,"\n")
    prune_step(Fk_1,Ck, mis) # 2. Prune Step
    return Ck

if __name__ == "__main__":
    for i in range(10, 100, 10):
        print("{}: {}".format(i, sup(i, data)))

    L = init_pass(data, m, mis)
