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
                                C2.add((l,))
                                C2.add((h,))
    return C2


if __name__ == "__main__":
    for i in range(10, 100, 10):
        print("{}: {}".format(i, sup(i, data)))

    L = init_pass(data, m, mis)

