import sys
from .token import Token
from .assertions import Assertions
from .config import configuration

class Node:
    def __init__(self):
        self.nodeName = None
        self.nodeChildren = []
        self.spaceNumbers = 0

    def __init__(self, nodeName):
        self.nodeName = nodeName
        self.nodeChildren = []
        self.spaceNumbers = 0

    def addChild(self, node):
        self.nodeChildren.append(node)
        return self

    def stabilizeSpaces(self, initial = 0):
        self.spaceNumbers = initial
        for child in self.nodeChildren:
            child.stabilizeSpaces(initial = initial + 1)
        return self

    def show(self, last=False):
        sys.stdout.write("\n")
        if self.spaceNumbers is 0:
            sys.stdout.write(str(self.nodeName))
        else:
            for i in range(self.spaceNumbers - 1):
                sys.stdout.write("  ")
            if last:
                sys.stdout.write("└")
            else:
                sys.stdout.write("├")
            sys.stdout.write("── ")
            sys.stdout.write(str(self.nodeName))
        for child in self.nodeChildren:
            child.show(last = child is self.nodeChildren[-1])
        return self
    def getTk(self):
        if len(self.nodeChildren) is 0:
            return self.nodeName
        return self.nodeChildren[0].getTk()

    def evaluate(self, variables = {}):
        if self.nodeName == "":
            return None


        if len(self.nodeChildren) is 0:
            return self.nodeName.lexeme

        childResult = []
        for child in self.nodeChildren:
            childResult.append(child.evaluate(variables = variables))
        try:
            childResult.remove(None)
        except:
            pass

        results = []
        for result in childResult:
            try:
                results.append(float(result))
            except:
                results.append(result)
                pass

        if len(results) is 1:
            return results[0]

        if len(results) is 2 and results[1] == ";":
            return results[0]

        if not childResult:
            return None

        # Operações Unárias
        if childResult[0] == '-':
            return childResult[1] * -1

        if childResult[0] == "(" and childResult[2] == ")":
            return childResult[1]

        # Operações Binárias
        if childResult[1] == "+":
            return childResult[0] + childResult[2]

        if childResult[1] == "-":
            return childResult[0] - childResult[2]

        if childResult[1] == "*":
            return childResult[0] * childResult[2]

        if childResult[1] == "/":
            Assertions.assertZeroDivision(childResult[2], self.nodeChildren[2].getTk())
            return float(childResult[0]) / childResult[2]

        if childResult[1] == "^":
            return childResult[0] ** childResult[2]

        if childResult[0] == "@":
            Assertions.assertUndeclaredVariable(variables, childResult[1])
            return variables[childResult[1]]

        if childResult[1] == "=":
            if not configuration["shadowing"]:
                Assertions.assertDeclaredVariable(variables, childResult[0])
            variables[childResult[0]] = childResult[2]


    def __str__(self):
        return self.nodeName
