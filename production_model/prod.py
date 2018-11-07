

class ProductionModel:
    def __init__(self, frame):
        self.frame = frame

        self.features = []
        self.facts = {}
        self.teachers_photos = {}

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
        pass

    def show_answer(self):
        self.frame.put_answer(self.teachers_photos[next(iter(self.teachers_photos.keys()))])
