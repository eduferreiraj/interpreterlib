

import builtins
from .assertions import Assertions
from .syntaxTree import SyntaxTree
from .config import configuration
from .token import *
import sys

class Interpreter():
    def __init__(self, parameters):
        configuration["shadowing"] = "-s" in parameters
        try:
            parameters.remove("-s")
        except:
            pass
        Assertions.assertParameters(parameters)
        self.filename = parameters[1]

    def lexicalAnalysis(self):
        try:
            fs = open(self.filename)
            content = fs.read()
            fs.close()
        except Exception as e:
            Assertions.assertIO()
        return tokenize(content)

    def syntaxAnalysis(self, tkStream):
        return SyntaxTree(tkStream).generate()

    def semanticAnalysis(self, syntaxTree):
        sys.stdout.write("\n> {}\n".format(syntaxTree.evaluate()))

    def execute(self):
        tkStream = self.lexicalAnalysis()
        syntaxTree = self.syntaxAnalysis(tkStream)
        self.semanticAnalysis(syntaxTree)
