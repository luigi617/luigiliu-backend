import numpy as np
from itertools import combinations
from time import time


def group(n, iterable, l): 
    return [c for c in set(combinations(iterable, l)) if sum(c) == n and (0 not in c[1:len(c)-1])]

# def group_1(n, iterable, l): 
#     comb = np.array(list(set(combinations(iterable, l))))
#     comb = comb[comb.sum(axis=1) == n]
#     mask = np.apply_along_axis(lambda row: 0 not in row[1:len(row) - 1], axis=1, arr=comb)
#     comb = comb[mask]
#     return comb
def group_1(n, iterable, l): 
    iterable = [iterable if i == 0 or i == l-1 else iterable[1:] for i in range(l)]
    comb = np.array(np.meshgrid(*iterable)).T.reshape(-1,l)
    comb = comb[comb.sum(axis=1) == n]
    # mask = np.apply_along_axis(lambda row: 0 not in row[1:len(row) - 1], axis=1, arr=comb)
    # comb = comb[mask]
    return comb


def nonogram_solver(row, column):
    shape = (len(row), len(column))
    table = np.zeros((len(row), len(column)), dtype=np.int8)

    r_trials = [None for _ in range(len(row))]
    c_trials = [None for _ in range(len(column))]
    for c_i, c in enumerate(column):
        # comb = [x for x in range(shape[0] - sum(c) - (len(c) - 3))]
        # comb *= (len(c)+1)
        # all_space_combs = group(shape[0] - sum(c), comb, len(c)+1)

        comb = [x for x in range(shape[0] - sum(c) - (len(c) - 3))]
        all_space_combs = group_1(shape[0] - sum(c), comb, len(c)+1)

        all_trials = np.zeros((len(all_space_combs), shape[0]), dtype=np.int8)
        for i in range(len(all_space_combs)):
            j = 0
            t_i = 0
            for sp in all_space_combs[i]:
                t_i += sp
                if t_i >= shape[0]:
                    break
                all_trials[i][t_i:t_i + c[j]] = 1
                t_i += c[j]
                j += 1
        c_trials[c_i] = all_trials

    for r_i, r in enumerate(row):

        comb = [x for x in range(shape[0] - sum(r) - (len(r) - 3))]
        all_space_combs = group_1(shape[0] - sum(r), comb, len(r)+1)
        
        all_trials = np.zeros((len(all_space_combs), shape[1]), dtype=np.int8)
        for i in range(len(all_space_combs)):
            j = 0
            t_i = 0
            for sp in all_space_combs[i]:
                t_i += sp
                if t_i >= shape[1]:
                    break
                all_trials[i][t_i:t_i + r[j]] = 1
                t_i += r[j]
                j += 1
        r_trials[r_i] = all_trials


    sorted_row_index = sorted(range(len(row)), key=lambda k: (sum(row[k]), 1/len(row[k])))
    sorted_col_index = sorted(range(len(column)), key=lambda k: (sum(column[k]), 1/len(column[k])))
    while (0 in table):
        for r_i in sorted_row_index:
            r = row[r_i]
            if r[0] != shape[1]:
                m = np.tile(table[:,r_i], r_trials[r_i].shape[0]).reshape(r_trials[r_i].shape[0], len(table[:,r_i]))
                all_trials_mask = np.where(m == 1, r_trials[r_i], 1).all(axis=1)
                all_error_trials_mask = (np.where(m == -1, r_trials[r_i], 0).any(axis=1) != 1)
                all_total_mask = all_trials_mask * all_error_trials_mask
                all_trials = r_trials[r_i][all_total_mask]
                

            mask = all_trials.sum(axis=0) == all_trials.shape[0]
            error_mask = all_trials.sum(axis=0) == 0
            table[:,r_i][mask] = 1
            table[:,r_i][error_mask] = -1

        for c_i in sorted_col_index:
            c = column[c_i]
            if c[0] != shape[0]:
                m = np.tile(table[c_i], c_trials[c_i].shape[0]).reshape(c_trials[c_i].shape[0], len(table[c_i]))
                all_trials_mask = np.where(m == 1, c_trials[c_i], 1).all(axis=1)
                all_error_trials_mask = (np.where(m == -1, c_trials[c_i], 0).any(axis=1) != 1)
                all_total_mask = all_trials_mask * all_error_trials_mask
                all_trials = c_trials[c_i][all_total_mask]
                
                
            mask = all_trials.sum(axis=0) == all_trials.shape[0]
            error_mask = all_trials.sum(axis=0) == 0
            table[c_i][mask] = 1
            table[c_i][error_mask] = -1
    return table



    
    

