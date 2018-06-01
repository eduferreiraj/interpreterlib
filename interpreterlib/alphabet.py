# Eduardo Ferreira José, 2018.
#
# - Arquivo Alphabet.py
# Arquivo que contém a classe estática Alphabet, que fornece as informações
# necessárias para a classificação dos Tokens, junto com os tipos de Tokens


class Alphabet:
    def getUnitaryOperators():
        return "-"
    def getEnd():
        return ";"
    def getBinaryOperators():
        return "+-*/^"
    def getOpenParentesis():
        return "("
    def getAssignment():
        return "="
    def getCloseParentesis():
        return ")"
    def getDecimalPoint():
        return "."
    def getVariableAccess():
        return "@"
    def getSymbols():
        return "".join([Alphabet.getBinaryOperators(), Alphabet.getUnitaryOperators(),
                        Alphabet.getDecimalPoint(), Alphabet.getEnd(),
                        Alphabet.getOpenParentesis(), Alphabet.getCloseParentesis(),
                        Alphabet.getAssignment(), Alphabet.getVariableAccess()])
    def getLetters():
        return "abcdefghijklmnopqrstuvwxyz"
    def getConstants():
        return "0123456789"
    def getAlphabet():
        return "".join([Alphabet.getConstants(), Alphabet.getSymbols(), Alphabet.getLetters()])
    def getRules():
        return (
            (Alphabet.getUnitaryOperators(), "TkUnOp"),
            (Alphabet.getBinaryOperators(), "TkBinOp"),
            (Alphabet.getAssignment(), "TkEqual"),
            (Alphabet.getConstants(), "TkNum"),
            (Alphabet.getLetters(), "TkVar"),
            (Alphabet.getOpenParentesis(), "TkLParen"),
            (Alphabet.getCloseParentesis(), "TkRParen"),
            (Alphabet.getVariableAccess(),"TkVarAccess"),
            (Alphabet.getDecimalPoint(),"TkPoint"),
            (Alphabet.getEnd(), "TkEnd")
        )
