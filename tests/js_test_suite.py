from typing import List, Optional
import os
from pathlib import Path
import difflib
from jasminesnake.js_stream import JSStringStream
import jasminesnake.ast as js_ast


class JSTest:
    _test_name: str
    _test_file: str
    _result_file: Optional[str]

    @property
    def name(self):
        return self._test_name

    def __init__(self, name: str, test_file: str, result_file: Optional[str]):
        self._test_name = name
        self._test_file = test_file
        self._result_file = result_file

    def run(self, must_fail: bool = False):
        payload = Path(self._test_file).read_text()
        jst = JSStringStream(payload)
        tree = jst.parse()
        ast_tree = None
        try:
            ast_tree = js_ast.from_parse_tree(tree)
        except NotImplementedError as e:
            print("Seems like some nodes are not implemented :^)")
            print("Error message: ")
            if hasattr(e, "message"):
                print(e.message)
            else:
                print(e)

            return must_fail

        expected = None
        if self._result_file is not None:
            expected = Path(self._result_file).read_text()

        got = js_ast.to_ascii_tree(ast_tree, ast_format="short")

        del jst
        del tree
        del ast_tree

        if expected is not None:
            if expected == got:
                print("Test {} OK...".format(self._test_name))
            else:
                print(
                    "Error in test `{}':\nExpected:\n```{}```\nGot:\n```{}```".format(
                        self._test_name, expected, got
                    )
                )
                # for i, s in enumerate(difflib.ndiff(expected, got)):
                #     if s[0] != " ":
                #         print(s[0], ord(s[-1]), "at", i)

                return False
        else:
            print("Test {} has no result file!\nGot:\n{}".format(self._test_name, got))
            return False

        return True


class JSTestCollection:
    tests: List[JSTest]

    def __init__(self, module_path: str):
        self.tests = []
        basedir = os.path.abspath(module_path)
        tests_dir = os.path.join(basedir, "t")
        results_dir = os.path.join(basedir, "r")

        # Collect tests
        test_files = [
            os.path.join(tests_dir, f)
            for f in os.listdir(tests_dir)
            if os.path.isfile(os.path.join(tests_dir, f))
        ]
        test_names = [
            os.path.splitext(os.path.basename(path))[0] for path in test_files
        ]

        for (test_name, test_file) in zip(test_names, test_files):
            result_file = os.path.join(results_dir, test_name) + ".ast"
            print(test_name, test_file, result_file)
            if not os.path.isfile(result_file):
                result_file = None

            test_case = JSTest(test_name, test_file, result_file)
            self.tests.append(test_case)

    def run_all(self, must_fail: bool = False):
        for test in self.tests:
            if not test.run(must_fail):
                return False
        return True
