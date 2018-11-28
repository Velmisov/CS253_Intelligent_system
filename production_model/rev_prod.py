import re
import networkx as nx


class ReverseProductionModel:
    def __init__(self):
        self.read_facts()
        self.read_teachers()
        self.read_rules()

    def read_facts(self):
        reg = re.compile(r'(f\d+) (.*)$')
        res = {}
        with open('facts.txt', 'rt', encoding='utf8') as f:
            for line in f.readlines():
                m = reg.match(line)
                fnum, fdesc = m.groups()
                res[fnum] = fdesc
        self.facts = res

    def read_teachers(self):
        reg = re.compile(r'(t\d+) (.*?):.*$')
        res = {}
        with open('teachers.txt', 'rt', encoding='utf8') as f:
            for line in f.readlines():
                m = reg.match(line)
                tnum, tdesc = m.groups()
                res[tnum] = tdesc
        self.teachers = res

    def read_rules(self):
        G = nx.DiGraph()
        reg = re.compile(r'(r\d+) ((?:(?:\w{1,2}\d+)(?:, )?)*) -> ([ct]\d+)')
        with open('new_rules_filtered.txt', 'rt', encoding='utf8') as f:
            for line in f.readlines():
                m = reg.match(line)
                rule, premise, cons = m.groups()
                for p in premise.split(', '):
                    G.add_edge(p, cons, rule=rule)
        self.G = G

    def try_produce(self, t, premises):
        def dfs(v):
            rules = {}
            for u in self.G.pred[v]:
                if u in premises:
                    return True
                res = dfs(u)
                rule = self.G[u][v]['rule']
                if rule in rules:
                    rules[rule] = rules[rule] and res
                else:
                    rules[rule] = res
            return len(rules) != 0 and any(rules.values())
        return dfs(t)


if __name__ == "__main__":
    m = ReverseProductionModel()
    print(m.facts)
    print(m.teachers)
    print(m.try_produce('t1', {'f19'}))
