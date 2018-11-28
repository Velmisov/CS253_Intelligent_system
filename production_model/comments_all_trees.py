import numpy as np


def read_comments():
    d = {}
    with open("teachers_comments_fids.txt", "rt", encoding='utf-8') as f:
        for l in f.readlines():
            ls = l.split()
            comm_id = ls.index("//")
            # name = ' '.join(ls[1:comm_id])
            name = ls[0]
            comm_id = l.find('//')
            comms = [x.split(', ')[1].strip('()\n') for x in l[comm_id + 2:].split(')(')]

            d[name] = comms
    return d


def get_features(d):
    f = set()
    for n in d:
        for x in d[n]:
            f.add(x)
    return list(f)


def divide(d, x):
    d1 = {}
    d2 = {}
    for n in d:
        if x in d[n]:
            d1[n] = d[n]
        else:
            d2[n] = d[n]
    return d1, d2


class NodeD:
    def __init__(self, left, right, d, feature):
        self.left = left
        self.right = right
        self.d = d
        self.feature = feature


class NodeT:
    def __init__(self, divs):
        self.divs = divs


tree_depth = 0
checked = set()


def build_trees(d, root: NodeT, path=frozenset()):
    global tree_depth, checked

    tree_depth += 1
    f = get_features(d)
    divs = []
    for x in f:
        d1, d2 = divide(d, x)
        if len(d) == max(len(d1), len(d2)) and len(d) != 1:
            continue

        node = NodeD(
            feature=x.replace(' ', '_').replace('.', '_'),
            left=NodeT(
                None
            ),
            right=NodeT(
                None
            ),
            d=d
        )

        pth = path.union(frozenset([x]))
        if pth in checked:
            continue
        checked.add(pth)

        if len(d) != 1:
            build_trees(d1, node.left, pth)
            build_trees(d2, node.right, pth)

        divs.append(node)

        if len(d) == 1:
            break

    root.divs = divs


def gen_all_rules(fn, root: NodeT):
    cnt_cons = 1
    cnt_rule = 1

    def rec_print(f, node, ncons):
        nonlocal cnt_cons, cnt_rule
        if node.divs is None:
            return

        for chld in node.divs:
            if len(chld.d) == 1:
                f.write("r{} c{}, {} -> {}\n".format(
                    cnt_rule, ncons, chld.feature, list(chld.d.keys())[0].replace(' ', '_').replace('.', '_')
                ))
                cnt_rule += 1
            else:
                chld_cons = cnt_cons
                f.write("r{} c{} -> c{}\n".format(cnt_rule, ncons, chld_cons))
                cnt_cons += 1
                cnt_rule += 1
                f.write("r{} c{}, {} -> c{}\n".format(cnt_rule, chld_cons, chld.feature, cnt_cons))
                cnt_cons += 1
                cnt_rule += 1
                rec_print(f, chld.left, cnt_cons - 1)
                f.write("r{} c{}, n{} -> c{}\n".format(cnt_rule, chld_cons, chld.feature, cnt_cons))
                cnt_cons += 1
                cnt_rule += 1
                rec_print(f, chld.right, cnt_cons - 1)

    with open(fn, 'wt', encoding='utf-8') as f:
        rec_print(f, root, 0)


d = read_comments()
# print(d)
root = NodeT([])
build_trees(d, root)
print(tree_depth)
gen_all_rules("new_rules2.txt", root)
