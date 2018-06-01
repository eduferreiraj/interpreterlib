

from .assertions import Assertions
from .syntaxTree import SyntaxTree
from .token import *


class Interpreter():
    def __init__(filename):
        self.filename = filename

    def lexicalAnalysis(self):
        try:
            fs = open(filename)
            content = fs.read()
            fs.close()
        except Exception as e:
            raise Exception("Houve um problema ao abrir o arquivo.")
        return tokenize(content)

    def syntaxAnalysis(self, tkStream):
        for tk in tkStream:
            print(tk)
        # syntaxTree = SyntaxTree(tkGenerator

    def semanticAnalysis(self, syntaxTree):
        return True

    def execute(self):
        tkStream = self.lexicalAnalysis()
        syntaxTree = self.syntaxAnalysis(tkStream)
        semanticAnalysis(syntaxTree)
