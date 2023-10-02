from MS_GSP import readdata, readparam, init_pass, sortdata

data = readdata()
mis, sdc = readparam()
m = sortdata(data, mis)


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
    for index, l in enumerate(L):
        if L[l] / num_sequences >= mis[l]:
            for h in keys[index + 1:]:  # "for each item h in L that is after l, do:"
                if L[h] / num_sequences >= mis[l] and abs(sup(h, data) - sup(l, data)) <= phi:
                    # join step: merge sequences containing l and h
                    for sequence in data:
                        for sub_sequence in sequence:
                            if l in sub_sequence and h in sub_sequence:
                                l_index = sub_sequence.index(l)
                                h_index = sub_sequence.index(h)
                                if l_index < h_index:
                                    new_sequence = [l,h]
                                    C2.add(tuple(new_sequence))
                                    C2.add(((l,),(h,)))
    return C2


def flatten_subsequence(t):
    for i in t:
        if isinstance(i, tuple):
            return flatten_subsequence(i)
        else:
            return i


def join_step(Fk_1):
    Ck = set()
    for s1 in Fk_1:
        for s2 in Fk_1:
            # if the subsequence obtained by dropping the first item of s1
            # is the same as the subsequence obtained by dropping the last item of s2,
            if flatten_subsequence(s1[1:]) == flatten_subsequence(s2[:-1]):
                # the candidate sequence is the sequence s1 extended with the last item in s2
                if isinstance(s2[-1], tuple):
                    new_sequence = list(s1)
                    new_sequence.append(s2[-1])
                    Ck.add(tuple(new_sequence))
                else:
                    if isinstance(s1[-1], tuple):
                        new_sequence = s1[-1] + (s2[-1], )
                        new_tup = s1[:-1] + (tuple(new_sequence),)
                        Ck.add(new_tup)
                    else: # it's an integer,
                        new_sequence = list(s1)
                        new_sequence.append(s2[-1])
                        new_tup = tuple(new_sequence)
                        Ck.add(new_tup)
    return Ck


def mscandidate_gen_SPM(Fk_1, mis):
    Ck = join_step(Fk_1)  # 1. Join Step
    # Fk_test = set()
    # # Fk_test.add(((20,), (30,)))
    # # Fk_test.add((30,80))
    # Fk_test.add((20, 30))
    # Fk_test.add((30, 80))
    # Ck = join_step(Fk_test)
    print(Ck)

if __name__ == "__main__":
    for i in range(10, 100, 10):
        print("{}: {}".format(i, sup(i, data)))

    L = init_pass(data, m, mis)
