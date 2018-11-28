import re
import networkx as nx


class ReverseProductionModel:
    def __init__(self):
        self.facts = self.read_facts()
        self.teachers = self.read_teachers()
        self.G = self.read_rules()

    def read_facts(self):
        reg = re.compile(r'(f\d+) (.*)$')
        res = {}
        with open('facts.txt', 'rt', encoding='utf8') as f:
            for line in f.readlines():
                m = reg.match(line)
                fnum, fdesc = m.groups()
                res[fnum] = fdesc
        return res

    def read_teachers(self):
        reg = re.compile(r'(t\d+) (.*?):.*$')
        res = {}
        with open('teachers.txt', 'rt', encoding='utf8') as f:
            for line in f.readlines():
                m = reg.match(line)
                tnum, tdesc = m.groups()
                res[tnum] = tdesc
        return res

    def read_rules(self):
        G = nx.DiGraph()
        reg = re.compile(r'(r\d+) ((?:(?:\w{1,2}\d+)(?:, )?)*) -> ([ct]\d+)')
        with open('new_rules_filtered.txt', 'rt', encoding='utf8') as f:
            for line in f.readlines():
                m = reg.match(line)
                rule, premise, cons = m.groups()
                for p in premise.split(', '):
                    G.add_edge(p, cons, rule=rule)
        return G

    def try_produce_dfs(self, t, premises):
        def dfs(v):
            if v in premises or v == 'c0':
                return True
            rules = {}
            for u in self.G.pred[v]:
                rule = self.G[u][v]['rule']
                if rule in rules and not rules[rule]:
                    continue
                res = dfs(u)
                if rule in rules:
                    rules[rule] = rules[rule] and res
                else:
                    rules[rule] = res
            res = len(rules) != 0 and any(rules.values())
            # if res:
            #     print(v)
            return res
        return dfs(t)


if __name__ == "__main__":
    # from matplotlib import pyplot as plt
    m = ReverseProductionModel()
    print(m.facts)
    print(m.teachers)

    print(m.try_produce('t1', {'f6', 'f1'}))
    # l = nx.kamada_kawai_layout(m.G)
    # nx.draw(m.G, pos=l)
    # nx.draw_networkx_labels(m.G, pos=l)
    # plt.show()
