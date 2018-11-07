import numpy as np

def read_comments():
    d = {}
    with open("teachers.txt", "rt") as f:
        for l in f.readlines():
            ls = l.split()
            comm_id = ls.index("//")
            name = ' '.join(ls[1:comm_id])
            comm_id = l.find('//')
            comms = [x.strip() for x in l[comm_id+2:].split(', ')]

            d[name] = comms
    return d

def get_features(d):
    f = set()
    for n in d:
        for x in d[n]:
            f.add(x)
    return list(f)

def feature_entropy(d, f):
    def count_f(x, d):
        c = 0
        for n in d:
            if x in d[n]:
                c += 1
        return c

    res = []
    for x in f:
        c = count_f(x, d)
        p = c/len(d)
        if p == 0 or p == 1:
            res.append(-1)
        else:
            res.append(-p * np.log2(p) - (1 - p) * np.log2(1 - p))
    res = np.array(res)
    return f[res.argmax()]

def divide(d, x):
    d1 = {}
    d2 = {}
    for n in d:
        if x in d[n]:
            d1[n] = d[n]
        else:
            d2[n] = d[n]
    return d1, d2

class Node:
    def __init__(self, left, right, d, feature):
        self.left = left
        self.right = right
        self.d = d
        self.feature = feature

def build_tree(d, root):
    # print('\n\nbuild', d)
    # print('\n')
    f = get_features(d)
    x = feature_entropy(d, f)
    d1, d2 = divide(d, x)
    if len(d) == max(len(d1), len(d2)):
        return

    root.feature = x.replace(' ', '_').replace('.', '_')
    root.left = Node(
        None, None, d1, None
    )
    root.right = Node(
        None, None, d2, None
    )

    build_tree(d1, root.left)
    build_tree(d2, root.right)

def print_tree(root, fn):
    cnt = 0
    def print_node(n, f):
        nonlocal cnt
        tmp = cnt

        f.write("{}{}->".format(n.feature, cnt))
        if n.left.feature == None:
            f.write("Leaf{}_{};\n".format(cnt, len(n.left.d)))
            cnt += 1
        else:
            f.write("{}{};\n".format(n.left.feature, cnt))
            print_node(n.left, f)
            cnt += 1

        f.write("{}{}->".format(n.feature, tmp))
        if n.right.feature == None:
            f.write("Leaf{}_{};\n".format(cnt, len(n.right.d)))
            cnt += 1
        else:
            f.write("{}{};\n".format(n.right.feature, cnt))
            print_node(n.right, f)
            cnt += 1

    with open(fn, "wt") as f:
        f.write("digraph g{\n")
        print_node(root, f)
        f.write("}\n")

d = read_comments()
root = Node(None, None, d, None)
build_tree(d, root)
print_tree(root, "tree.dot")
