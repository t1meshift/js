from antlr4.error.ErrorListener import ErrorListener
import logging


class LogErrorListener(ErrorListener):
    def __init__(self):
        super().__init__()

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        logging.debug(
            "{}\n{}\n{}\n{}\n{}".format(offendingSymbol, line, column, msg, e)
        )

    def reportAmbiguity(
        self, recognizer, dfa, startIndex, stopIndex, exact, ambigAlts, configs
    ):
        logging.debug(
            "{}\n{}\n{}\n{}\n{}\n{}".format(
                dfa, startIndex, stopIndex, exact, ambigAlts, configs
            )
        )

    def reportAttemptingFullContext(
        self, recognizer, dfa, startIndex, stopIndex, conflictingAlts, configs
    ):
        logging.debug(
            "{}; {}; {}; {}; {}".format(
                dfa, startIndex, stopIndex, conflictingAlts, configs
            )
        )

    def reportContextSensitivity(
        self, recognizer, dfa, startIndex, stopIndex, prediction, configs
    ):
        logging.debug(
            "{}; {}; {}; {}; {}".format(dfa, startIndex, stopIndex, prediction, configs)
        )
