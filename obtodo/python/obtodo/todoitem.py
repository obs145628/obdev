TAGS_LEVELS = {'bug': 0, 'issue': 0, 'main': 0,
               'todo': 1, 'task': 1,
               'extra': 2, 'optional': 2,
               'feature': 3,
               'idea': 4,
               'info': 5, 'tip': 5}
TAGS = list(TAGS_LEVELS.keys())

TAGS_SYM = ['@' + t for t in TAGS]

class TodoItem:

    def __init__(self, full_path, rel_path, lnum, text):
        self.ty = None
        self.full_path = full_path
        self.rel_path = rel_path
        self.lnum = lnum
        self.text = text

        for (t, sym) in zip(TAGS, TAGS_SYM):
            if sym in text.lower():
                self.ty = TAGS_LEVELS[t]
                break

    

    def __str__(self):
        return '{}:{}: {}'.format(self.rel_path, self.lnum, self.text)
