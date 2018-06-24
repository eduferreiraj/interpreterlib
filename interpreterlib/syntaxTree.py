# Eduardo Ferreira José, 2018
#
# - Arquivo SyntaxTree.py
# Arquivo contendo a definição do objeto SyntaxTree, que vai gerar as arvores
# de sintaxe através do método getTree.

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
#         | {TkVar} {TkEqual} Expression {TkEnd}
#         | ''
# Expression = Expression [+-] Term
#         | Term
# Term = Term [*/%] Factor
#         | Factor
# Factor = Element
#         | '-' Element
#         | 'sqrt' Element
# Element = Terminal
#         | Terminal '^' Factor
# Terminal = {TkNum}
#         | {TkVarAccess} {TkVar}
#         | {TkLParen} Expression {TkRParen}

from .node import Node
from .assertions import Assertions

class SyntaxTree:
    def __init__(self, tkStream):
        self.tkList = list(tkStream)
        self.nodes = []

    def find(tkQueue, symbolType, position = 0):
        parentesisRate = 0
        for tk in tkQueue:
            if str(tk) is "(":
                parentesisRate = parentesisRate + 1
            if str(tk) is ")":
                parentesisRate = parentesisRate - 1
            if tk.type is symbolType:
                return position
            position = position + 1
        return None


    def rfind(tkQueue, symbols, position = -1, parentesisRate = 0):
        if len(tkQueue) is 0:
            return None
        elif position is -1:
            position = len(tkQueue) - 1
        if str(tkQueue[-1]) == "(":
            parentesisRate = parentesisRate + 1
        elif str(tkQueue[-1]) == ")":
            parentesisRate = parentesisRate - 1
        elif str(tkQueue[-1]) in symbols and parentesisRate is 0:
            return position
        return SyntaxTree.rfind(tkQueue[:-1], symbols, position = position - 1, parentesisRate = parentesisRate)

    def parentesisFinder(tkQueue):
        actualParentesis = 0
        tkQueue = tkQueue[1:]
        for index, tk in enumerate(tkQueue):
            if tk.type == "TkRParen":
                actualParentesis = actualParentesis - 1
            if tk.type == "TkLParen":
                actualParentesis = actualParentesis + 1
            if actualParentesis == -1:
                return index + 1


    def safeSee(self, listTarget, index=0):
        try:
            listTarget[index]
        except:
            return None
        return listTarget[index]


    def generate(self):
        try:
            return self.ruleStart(self.tkList).stabilizeSpaces()
        except:
            print("\nstdin: Houve algum erro, abortando.")
            exit(-1)

    # Terminal = {TkNum}
    #         | {TkVarAccess} {TkVar}
    #         | {TkLParen} Expression {TkRParen}
    def ruleTerminal(self, tkQueue):
        if tkQueue[0].type is "TkNum":
            numberNode = Node(tkQueue[0])
            terminalNode = Node("Terminal")
            terminalNode.addChild(numberNode)
            Assertions.assertIsEmpty(tkQueue[1:], tkQueue[0])
            return terminalNode
        elif tkQueue[0].type is "TkVarAccess" and tkQueue[1].type is "TkVar":
            return Node("Terminal").addChild(Node(tkQueue[0])).addChild(Node(tkQueue[1]))
        elif tkQueue[0].type is "TkLParen":
            closePosition = SyntaxTree.parentesisFinder(tkQueue)
            nodeExpression = self.ruleExpression(tkQueue[1:closePosition])
            return Node("Terminal").addChild(Node(tkQueue[0])).addChild(nodeExpression).addChild(Node(tkQueue[closePosition]))
        else:
            Assertions.assertIsEmpty([None], tkQueue[0])

    # Element = Terminal
    #         | Terminal '^' Factor
    def ruleElement(self, tkQueue):
        valuePosition = SyntaxTree.rfind(tkQueue, "^")
        if valuePosition:
            terminalTk, factorTk = tkQueue[:valuePosition], tkQueue[valuePosition + 1:]
            nodeFactor = self.ruleFactor(factorTk)
            nodeTerminal = self.ruleTerm(terminalTk)
            return Node("Element").addChild(nodeTerminal).addChild(Node(tkQueue[valuePosition])).addChild(nodeFactor)
        else:
            return Node("Element").addChild(self.ruleTerminal(tkQueue))

    # Factor = Element
    #         | '-' Element
    def ruleFactor(self, tkQueue):
        if tkQueue[0].lexeme in ["-", "sqrt", "ceil", "floor", "cos", "sin"]:
            Assertions.assertSyntax(tkQueue[1:], tkQueue[0])
            return Node("Factor").addChild(Node(tkQueue[0])).addChild(self.ruleElement(tkQueue[1:]))
        return Node("Factor").addChild(self.ruleElement(tkQueue))

    # Term = Term [*/] Factor
    #         | Factor
    def ruleTerm(self, tkQueue):
        valuePosition = SyntaxTree.rfind(tkQueue, "/*%")
        if valuePosition:
            termTk, factorTk = tkQueue[:valuePosition], tkQueue[valuePosition + 1:]
            nodeFactor = self.ruleFactor(factorTk)
            nodeTerm = self.ruleTerm(termTk)
            Assertions.assertSyntax(factorTk, tkQueue[0])
            Assertions.assertSyntax(termTk, tkQueue[0])
            return Node("Term").addChild(nodeTerm).addChild(Node(tkQueue[valuePosition])).addChild(nodeFactor)
        else:
            nodeFactor = self.ruleFactor(tkQueue)
            return Node("Term").addChild(nodeFactor)


    # Expression = Expression [+-] Term
    #         | Term
    def ruleExpression(self, tkQueue):
        valuePosition = SyntaxTree.rfind(tkQueue, "+-")
        if valuePosition:
            expressionTk, termTk = tkQueue[:valuePosition], tkQueue[valuePosition + 1:]
            Assertions.assertSyntax(termTk, tkQueue[valuePosition])
            Assertions.assertSyntax(expressionTk, tkQueue[valuePosition])
            nodeTerm = self.ruleTerm(termTk)
            nodeExpression = self.ruleExpression(expressionTk)
            return Node("Expression").addChild(nodeExpression).addChild(Node(tkQueue[valuePosition])).addChild(nodeTerm)
        else:
            nodeTerm = self.ruleTerm(tkQueue)
            return Node("Expression").addChild(nodeTerm)


    # Declaration = Declaration Declaration
    #         | {TkVar} {TkEqual} Expression {TkEnd}
    #         | ''
    def ruleDeclaration(self, tkQueue):
        nodeDeclaration = None
        if tkQueue[0].type is "TkVar" and tkQueue[1].type is "TkEqual":
            tkEndPos = SyntaxTree.find(tkQueue, "TkEnd")
            Assertions.assertSemicolon(tkEndPos, tkQueue[0])
            Assertions.assertSyntax(tkQueue[2:tkEndPos], tkQueue[1])
            Assertions.assertKeyword(tkQueue[0])
            nodeExpression = self.ruleExpression(tkQueue[2:tkEndPos])
            nodeDeclaration = Node("Declaration").addChild(Node(tkQueue[0])).addChild(Node(tkQueue[1])).addChild(nodeExpression).addChild(Node(tkQueue[tkEndPos]))
            otherDeclaration, newTkQueue = self.ruleDeclaration(tkQueue[tkEndPos + 1:])
            if len(newTkQueue) is not len(tkQueue[tkEndPos + 1:]):
                nodeDeclaration = Node("Declaration").addChild(nodeDeclaration).addChild(otherDeclaration)
            return nodeDeclaration, newTkQueue
        return Node("Declaration").addChild(Node("")), tkQueue


    # Start = Declaration Expression {TkEnd}
    def ruleStart(self, tkQueue):
        Assertions.assertParentesis(self.checkForParentesis(tkQueue))
        if tkQueue[-1].type is "TkEnd":
            nodeDeclaration, newTkQueue = self.ruleDeclaration(tkQueue)
            nodeExpression = self.ruleExpression(newTkQueue[:-1])
            return Node("Start").addChild(nodeDeclaration).addChild(nodeExpression).addChild(Node(tkQueue[-1]))
        else:
            Assertions.assertSemicolon(None, tkQueue[-1])

    def checkForParentesis(self, tkQueue):
        parentesisRate = 0
        parentesisQueue = []
        for tk in tkQueue:
            if tk.type == "TkLParen":
                parentesisQueue.append(tk)
                parentesisRate = parentesisRate + 1
            if tk.type == "TkRParen":
                if len(parentesisQueue) == 0:
                    return tk, False
                parentesisQueue.pop()
                parentesisRate = parentesisRate - 1
        if parentesisRate == 0:
            return None, False
        return parentesisQueue.pop(), True
