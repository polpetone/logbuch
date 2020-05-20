from typing import List

from logbuch.service.TermService import Term


class AnalysisView(object):

    def __init__(self, terms: List[Term]):
        self.terms = terms

    def view(self):
        template = "{0:<30}{1:<80}\n"
        out = ""
        for term in self.terms:
            out += template.format(term.count, term.value)
        return out
