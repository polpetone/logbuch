from unittest import TestCase

from logbuch.domain.Task import Task

from logbuch.service.TermService import TermService


class TestTermService(TestCase):
    def test_get_most_used_terms(self):
        # given
        l = [Task("foobar blub"), Task("jup jeah"), Task("foobar")]

        # when
        term_service = TermService(l)
        result = term_service.get_most_used_terms()

        # then
        found_terms = [term for term in result if term.value == "foobar"]
        assert len(result) == 4
        assert found_terms[0].count == 2
