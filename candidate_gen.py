from MS_GSP import readdata, readparam, init_pass, sortdata

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
            for h in keys[index + 1:]:  # "for each item h in L that is after l, do:"
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
            for h in keys[index + 1:]:  # "for each item h in L that is after l, do:"
                if L[h] / num_sequences >= mis_l and abs(sup(h, data) - sup(l, data)) <= phi:
                    # join step: merge sequences containing l and h
                    for sequence in data:
                        for sub_sequence in sequence:
                            if l in sub_sequence and h in sub_sequence:
                                l_index = sub_sequence.index(l)
                                h_index = sub_sequence.index(h)
                                if l_index < h_index:
                                    new_sequence = [l,h]
                                    C2.add(tuple(new_sequence))
                                else:
                                    new_sequence = [h,l]
                                    C2.add(tuple(new_sequence))
                                C2.add(((l,),(h,)))
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
    if flatten_subsequence(s1[1:]) == flatten_subsequence(s2[:-1]):
        # the candidate sequence is the sequence s1 extended with the last item in s2
        if isinstance(s2[-1], tuple):
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
        else:
            if isinstance(s1[-1], tuple):
                new_sequence = s1[-1] + (s2[-1], )
                new_tup = s1[:-1] + (tuple(new_sequence),)
                #Ck.add(new_tup)
            else: # it's an integer,
                new_sequence = list(s1)
                new_sequence.append(s2[-1])
                new_tup = tuple(new_sequence)
                #Ck.add(new_tup)
        # if new_tup == ():
        #     print("new_tup is empty\ns1:", s1, "\ns2: " , s2)
    return new_tup

def Size(s):
    size = 0
    if isinstance(s[0], tuple):
        for _ in s:
            size += 1
    else:
        size = 1
    return size

def mscandidate_gen_SPM(Fk_1, mis):
    Ck = set()
    #Ck = join_step(Fk_1)  # 1. Join Step
    # Fk_test = set()
    # # Fk_test.add(((20,), (30,)))
    # # Fk_test.add((30,80))
    # Fk_test.add((20, 30))
    # Fk_test.add((30, 80))
    # Ck = join_step(Fk_test)
    for s1 in Fk_1:
        s1_first_mis = mis[flatten_subsequence(s1)[0]] if isinstance(s1[0], tuple) else mis[s1[0]]
        s1_first_smallest = None
        # check for condition 1
        for index,i in enumerate(s1[1:]):
            mis_i = mis[flatten_subsequence(s1)[0]] if isinstance(i, tuple) else mis[i]
            if index < len(s1[1:]) -1 and mis_i<s1_first_mis:
                s1_first_smallest = False
            elif index == len(s1[1:]) -1 and mis_i<s1_first_mis:
                s1_first_smallest = True

        for s2 in Fk_1:
            s2_last_smallest = None
            s2_last_mis = mis[flatten_subsequence(s2)[-1]] if isinstance(s2[-1:], tuple) else mis[s2[-1:]]
            
            # check for condition 2
            if (not s1_first_smallest):
                for index, i in enumerate(s2[:-1]):
                    mis_i = mis[flatten_subsequence(s2)[-1]] if isinstance(i, tuple) else mis[i]
                    if index < len(s2[:-1]) -1 and mis_i<s2_last_mis:
                        s2_last_smallest = False
                    elif index == len(s2[:-1]) -1 and mis_i<s2_last_mis:
                        s2_last_smallest = True

            # condition 1: if the MIS value of the first item in a sequence (denoted by s1) is < the MIS value of every other item in s1
            if(s1_first_smallest):
                t1 = list(s1)
                t1.pop(1)
                if(t1 == list(s2)[:-1] and s2_last_mis>s1_first_mis):
                    if isinstance(s2[-1], tuple):
                        c1 = list(s1)
                        c1.append(s2[-1])
                        #Ck.add(tuple(new_sequence))
                        #print("Ck: {}".format(Ck))
                        s1_last_item = flatten_subsequence(s1[-1:]) if isinstance(s1[-1:], tuple) else s1[-1:]
                        s2_last_item = flatten_subsequence(s2[-1:]) if isinstance(s2[-1:], tuple) else s2[-1:]
                        if Size(s1) == 2 and len(s1)==2 and s2_last_item > s1_last_item: 
                            c2 = list(s1)
                            c2.append(flatten_subsequence(s2[-1]))
                    elif (Size(s1) == 1 and len(s1)==2 and s2_last_item > s1_last_item) or (len(s1)>2):
                        c2 = list(s1)
                        c2.append(flatten_subsequence(s2[-1]))
                    
            # condition 2: if the MIS value of the last item in a sequence (denoted by s2) is < the MIS value of every other item in s2
            elif (s2_last_smallest):
                print("s2_last_smallest")
                break

            # condtition 3: default case
            else:
                c1 = join_step(s1, s2) # need to update this to take s1 and s2 only instead of Fk_1 - iteration of sequences happens here
                Ck.add(c1) if c1 != () else None
         
    for c in Ck:
        print(c,"\n")
    return Ck

if __name__ == "__main__":
    for i in range(10, 100, 10):
        print("{}: {}".format(i, sup(i, data)))

    L = init_pass(data, m, mis)
