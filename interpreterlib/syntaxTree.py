# Eduardo Ferreira José, 2018
#
# - Arquivo SyntaxTree.py
# Arquivo contendo a definição do objeto SyntaxTree, que vai gerar as arvores
# de sintaxe através do método getNextTree.

# Original Grammar
#
#  Start ::= {Dec} Exp
#  Dec  ::= Var '=' Exp
#  Exp  ::= Exp BinOp Exp
# 		| UnOp Exp
# 		| Num
# 		| '@' Var|
# 	    | '(' Exp ')'
#  BinOp::= '+' | '-' | '/' | '*' | '^'
#  Var  ::= 'x' | 'y' | 'z'
#  Num	::= [0-9]+[(.)[0-9]]+

# Implemented Grammar
#
# Start = Declaration Expression {TkEnd}
# Declaration = Declaration Declaration
#       | {TkVar} {TkEqual} Expression {TkEnd}
#       | ''
# Expression = Term [+-] Expression
#       | Term
# Term = Factor [*/^] Term
#       | Factor
# Factor = Element
#       | '-' Element
# Element = Terminal
#       | Terminal '^' Factor
# Terminal = {TkNum}
#       | {TkVarAccess} {TkVar}
#       | {TkOpenParentesis} Expression {TkCloseParentesis}

import treelib

class SyntaxTree:
    def __init__(self, tkStream):
        self.tkStream = tkStream
        self.tkList = []
    def getToken(self):
        try:
            self.tkList.append(next(self.tkGenerator))
        except StopIteration:
            pass
    def generate(self):
        return self.start()
    def start(self):
        print("a")
