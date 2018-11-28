

class ProductionModel:
    def __init__(self, frame):
        self.frame = frame

        self.facts = {}
        self.teachers_photos = {}
        self.teachers_names = {}
        self.rules = {}

        self.used_facts = []
        self.consequences = []
        self.last_cons = ''
        self.last_fact = ''

        self.parse_facts()
        self.parse_teachers()
        self.parse_rules()

    def clear(self):

        self.used_facts = []
        self.consequences = []
        self.last_cons = ''
        self.last_fact = ''

    def parse_facts(self, fname='facts.txt'):
        with open(fname, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                id, *fact = line.split(' ')
                fact = ' '.join(fact)
                self.facts[id] = fact

    def parse_teachers(self, fname='teachers.txt'):
        with open(fname, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                id, url = line.split(' : ')
                id, *name = id.split(' ')
                name = ' '.join(name)
                self.teachers_names[id] = name
                self.teachers_photos[id] = url

    def parse_rules(self, fname='rules.txt'):
        with open(fname, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                id, *others = line.split(' ')
                others = ' '.join(others)
                facts, consequence = others.split(' => ')
                facts = facts.split(', ')
                consequence = consequence.strip()
                self.rules[id] = (facts, consequence)

    def next_step(self):
        ask = 'r1'
        best = 0
        fact = ''
        for rule_id in self.rules:
            needed_facts = self.rules[rule_id][0]
            print(needed_facts)
            current_cons = self.rules[rule_id][1]

            all = True
            now = 0
            for con in needed_facts:
                if not con.startswith('f'):
                    if con not in self.consequences:
                        all = False
                        print(con)
                        break
                else:
                    now += 1

            if all:
                for fl in self.rules[rule_id]:
                    for f in fl:
                        if f.startswith('f') and f not in self.used_facts:
                            fact = f
                            break
                ask = rule_id
                best = now

        if fact == '':
            # print(self.teachers_photos)
            # self.frame.put_answer(self.teachers_photos[self.rules[ask][1]])
            self.frame.put_answer(self.rules[ask][1])
            return

        # print('fact=', fact)
        # print(self.consequences)
        self.frame.ask_question(self.facts[fact][:-1] + '?')
        self.last_fact = fact
        self.used_facts.append(fact)
        self.last_cons = self.rules[ask][1]

        if self.last_cons.startswith('t'):
            self.frame.put_answer(self.last_cons)

    def set_answer(self, ans):
        if ans == 'Yes':
            self.consequences.append(self.last_cons)
        else:
            self.consequences.append('n' + self.last_fact)

    def show_answer(self):
        self.frame.put_answer(self.teachers_photos[next(iter(self.teachers_photos.keys()))])
