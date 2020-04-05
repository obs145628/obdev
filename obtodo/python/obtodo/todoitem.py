TAGS_LEVELS = {'bug': 0, 'issue': 0, 'main': 0,
               'todo': 1, 'task': 1,
               'extra': 2, 'optional': 2,
               'feature': 3,
               'idea': 4,
               'info': 5, 'tip': 5}
TAGS = list(TAGS_LEVELS.keys())

TAGS_SYM = ['@' + t for t in TAGS]

class TodoItem:

    def __init__(self, full_path, rel_path, prefix_path, lnum, text):
        self.ty = None
        self.full_path = full_path
        self.rel_path = rel_path
        self.lnum = lnum
        self.text = text
        self.extra  = None

        if prefix_path is None or len(prefix_path) == 0:         
            self.print_path = self.rel_path
        else:
            self.print_path = '{}:{}'.format(prefix_path, self.rel_path)

        for (t, sym) in zip(TAGS, TAGS_SYM):
            if sym in text.lower():
                self.ty = TAGS_LEVELS[t]
                pos_end = text.lower().index(sym) + len(sym)
                if len(text) > pos_end + 2 and text[pos_end] == ':' and text[pos_end+1] != ' ':
                    self.extra = text[pos_end+1:].split()[0]
                break

    

    def __str__(self):
        return '{}:{}: {}'.format(self.print_path, self.lnum, self.text)
