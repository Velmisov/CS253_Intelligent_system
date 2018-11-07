

class ProductionModel:
    def __init__(self, frame):
        self.frame = frame

        self.facts = {}
        self.teachers_photos = {}
        self.rules = {}

        self.used_facts = []
        self.consequences = []
        self.last_cons = ''

        self.parse_facts()
        self.parse_teachers()

    def parse_facts(self, fname='facts.txt'):
        with open(fname, 'r') as f:
            for line in f.readlines():
                id, *fact = line.split(' ')
                fact = ' '.join(fact)
                self.facts[id] = fact

    def parse_teachers(self, fname='teachers.txt'):
        with open(fname, 'r') as f:
            for line in f.readlines():
                id, url = line.split(' : ')
                self.teachers_photos[id] = url

    def parse_rules(self, fname='rules.txt'):
        with open(fname, 'r') as f:
            for line in f.readlines():
                id, *others = line.split(' ')
                others = ' '.join(others)
                facts, consequence = others.split(' => ')
                facts = facts.split(', ')
                self.rules[id] = (facts, consequence)

    def next_step(self):
        ask = 'r1'
        best = 0
        fact = ''
        for rule_id in self.rules:
            needed_facts = self.rules[rule_id][0]
            current_cons = self.rules[rule_id][1]

            all = True
            now = 0
            for con in needed_facts:
                if con.startswith('c'):
                    if con not in self.consequences:
                        all = False
                        break
                    else:
                        now += 1

            if all and best < now:
                for f in self.rules[rule_id]:
                    if f.startswith('f') and f not in self.used_facts:
                        fact = f
                        break
                ask = rule_id
                best = now

        self.frame.ask_question(fact)
        self.used_facts.append(fact)
        self.last_cons = self.rules[ask][1]

    def set_answer(self, ans):
        if ans == 'Yes':
            self.consequences.append(self.last_cons)

    def show_answer(self):
        self.frame.put_answer(self.teachers_photos[next(iter(self.teachers_photos.keys()))])
