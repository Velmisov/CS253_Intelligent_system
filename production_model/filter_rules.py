import networkx as nx
import re


def read_graph(fn):
    G = nx.DiGraph()
    reg = re.compile(r'(r\d+) ((?:(?:\w{1,2}\d+)(?:, )?)*) -> ([ct]\d+)')
    with open(fn, 'rt', encoding='utf8') as f:
        n_rules = 0
        for line in f.readlines():
            n_rules += 1
            m = reg.match(line)
            rule, premise, consequence = m.groups()
            for p in premise.split(', '):
                G.add_edge(p, consequence, rule=rule)
    return G, n_rules


def mark_unused(G, n_rules):
    for u, v, label in nx.dfs_labeled_edges(G, 'c0'):
        if label == 'reverse' and u != v:
            if v[0] == 't' or 'productive' in G.node[v]:
                G.node[u]['productive'] = True
                G.node[v]['productive'] = True
                # print(u, v)
                G[u][v]['productive'] = True
    used = [True]*n_rules
    for u, v in G.edges:
        if 'productive' not in G[u][v]:
            used[int(G[u][v]['rule'][1:]) - 1] = False
    return used


def filter(fn_ref, fn_to, used):
    with open(fn_ref, 'rt', encoding='utf8') as ref:
        with open(fn_to, 'wt', encoding='utf8') as wr:
            n = 0
            for line in ref.readlines():
                if used[n]:
                    wr.write(line)
                    # wr.write('\n')
            n += 1


G, n_rules = read_graph('new_rules2.txt')
used = mark_unused(G, n_rules)
print(used)
filter('new_rules2.txt', 'new_rules_filtered.txt', used)
