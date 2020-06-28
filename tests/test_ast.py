import os
import pytest
from js_test_suite import *

BASE_PATH = os.path.dirname(os.path.abspath(__file__))


class TestAST:
    def test_literals(self):
        tcl = JSTestCollection(os.path.join(BASE_PATH, "literals"))
        assert tcl.run_all()

    def test_statements(self):
        tcs = JSTestCollection(os.path.join(BASE_PATH, "statements"))
        assert tcs.run_all()

    # @pytest.mark.skip(reason="Not yet implemented")
    def test_expressions(self):
        tce = JSTestCollection(os.path.join(BASE_PATH, "expressions"))
        assert tce.run_all()

    # @pytest.mark.xfail(reason="Not yet implemented features.")
    def test_todos(self):
        tcb = JSTestCollection(os.path.join(BASE_PATH, "todos"))
        assert tcb.run_all(must_fail=True)

    @pytest.mark.xfail(reason="Bugs.")
    def test_bugs(self):
        tcb = JSTestCollection(os.path.join(BASE_PATH, "bugs"))
        assert tcb.run_all(must_fail=True)
