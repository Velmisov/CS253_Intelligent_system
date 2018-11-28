import jellyfish as jf
import numpy as np


def read_facts(fn):
    facts = set()
    with open(fn, 'rt', encoding='utf8') as f:
        for line in f.readlines():
            sep_i = line.index('// ')
            lst = line[sep_i+3:].split(', ')
            for f in lst:
                facts.add(f.strip())
    return facts


def read_fids(fn):
    fids = {}
    with open(fn, 'rt', encoding='utf8') as f:
        for line in f.readlines():
            fid, *desc = line.split()
            fids[' '.join(desc)] = fid
    return fids


def give_ids_to_facts(facts, fids):
    res = {}
    for f in facts:
        dists = [(x, (0 if f in x.lower() else jf.levenshtein_distance(f, x))) for x in fids]
        min_dist = np.argmin([x[1] for x in dists])
        res[f] = fids[dists[min_dist][0]]
    return res


def save_with_fids(fn_ref, fn_to, res):
    with open(fn_ref, 'rt', encoding='utf8') as ref:
        with open(fn_to, 'wt', encoding='utf8') as wr:
            for line in ref.readlines():
                sep_i = line.index('// ')
                lst = line[sep_i + 3:].split(', ')
                wr.write(line[:sep_i+3])
                for f in lst:
                    wr.write("({}, {})".format(
                        f.strip(),
                        res[f.strip()]
                    ))
                wr.write('\n')


facts = read_facts('teachers_comments.txt')
fids = read_fids('facts.txt')
res = give_ids_to_facts(facts, fids)
res['нейросети'] = 'f19'
res['сисадмин'] = 'f18'
res['машинка'] = 'f16'
res['книга'] = 'f8'

save_with_fids('teachers_comments.txt', 'teachers_comments_fids.txt', res)
