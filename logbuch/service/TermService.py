class TermService:

    def __init__(self, tasks):
        self.tasks = tasks

    def get_most_used_terms(self):
        result = []
        for task in self.tasks:
            words = task.text.split(' ')
            for word in words:
                f = [term for term in result if term.value == word]
                if len(f) == 1:
                    f[0].count += 1
                else:
                    result.append(Term(word))
        return result


class Term:
    def __init__(self, value):
        self.value = value
        self.count = 1
