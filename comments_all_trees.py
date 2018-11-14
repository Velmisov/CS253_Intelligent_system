import numpy as np


def read_comments():
    d = {}
    with open("teachers_comments.txt", "rt") as f:
        for l in f.readlines():
            ls = l.split()
            comm_id = ls.index("//")
            name = ' '.join(ls[1:comm_id])
            comm_id = l.find('//')
            comms = [x.strip() for x in l[comm_id + 2:].split(', ')]

            d[name] = comms
    return d


def get_features(d):
    f = set()
    for n in d:
        for x in d[n]:
            f.add(x)
    return list(f)


# def feature_entropy(d, f):
#     def count_f(x, d):
#         c = 0
#         for n in d:
#             if x in d[n]:
#                 c += 1
#         return c
#
#     res = []
#     for x in f:
#         c = count_f(x, d)
#         p = c / len(d)
#         if p == 0 or p == 1:
#             res.append(-1)
#         else:
#             res.append(-p * np.log2(p) - (1 - p) * np.log2(1 - p))
#     res = np.array(res)
#     return f[res.argmax()]


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
checked = []


def build_trees(d, root: NodeT, path=[]):
    global tree_depth, checked


    tree_depth += 1
    # print('\n\nbuild', d)
    # print('\n')
    f = get_features(d)
    # x = feature_entropy(d, f)
    divs = []
    for x in f:
        d1, d2 = divide(d, x)
        if len(d) == max(len(d1), len(d2)):
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

        pth = path + [x]
        b = False
        for p in checked:
            if len(p) == len(pth):
                b = True
                for q in pth:
                    if not q in p:
                        b = False
                        break
                if b:
                    break
        if b:
            continue
        checked.append(set(pth))

        build_trees(d1, node.left, pth)
        build_trees(d2, node.right, pth)


        divs.append(node)
    root.divs = divs


# def print_trees(root, fn):
#     cnt = 0
#
#     def print_node(n, f):
#         nonlocal cnt
#         tmp = cnt
#
#         f.write("{}{}->".format(n.feature, cnt))
#         if n.left.feature == None:
#             f.write("Leaf{}_{};\n".format(cnt, len(n.left.d)))
#             cnt += 1
#         else:
#             f.write("{}{};\n".format(n.left.feature, cnt))
#             print_node(n.left, f)
#             cnt += 1
#
#         f.write("{}{}->".format(n.feature, tmp))
#         if n.right.feature == None:
#             f.write("Leaf{}_{};\n".format(cnt, len(n.right.d)))
#             cnt += 1
#         else:
#             f.write("{}{};\n".format(n.right.feature, cnt))
#             print_node(n.right, f)
#             cnt += 1
#
#     with open(fn, "wt") as f:
#         f.write("digraph g{\n")
#         print_node(root, f)
#         f.write("}\n")

def gen_all_rules(fn, root: NodeT):
    cnt_cons = 1
    cnt_rule = 1

    def rec_print(f, node, ncons):
        nonlocal cnt_cons, cnt_rule
        for chld in node.divs:
            chld_cons = cnt_cons
            f.write("r{} c{} -> c{}\n".format(cnt_rule, ncons, chld_cons))
            cnt_cons += 1
            cnt_rule += 1
            # TODO: do this shit right
            f.write("r{} c{}, f{} -> c{}\n".format(cnt_rule, chld_cons, chld.feature, cnt_cons))
            cnt_cons += 1
            cnt_rule += 1
            rec_print(f, chld.left, cnt_cons - 1)
            f.write("r{} c{}, nf{} -> c{}\n".format(cnt_rule, chld_cons, chld.feature, cnt_cons))
            cnt_cons += 1
            cnt_rule += 1
            rec_print(f, chld.right, cnt_cons - 1)

    with open(fn, 'wt') as f:
        rec_print(f, root, 0)


d = read_comments()
root = NodeT([])
build_trees(d, root)
print(tree_depth)
# print_trees(root, "trees.dot")
gen_all_rules("new_rules.txt", root)
