# Eduardo Ferreira José, 2018
#
# - Arquivo Token.py
# Arquivo contendo a definição do objeto Token, de maneira bem simplória, para
# armazenamento em estrutura do objeto.


from .alphabet import Alphabet

tkRules = Alphabet.getRules()


class Token:
    def __init__(self, position, type, lexeme):
        self.position = position
        self.type = type
        self.lexeme = lexeme

    def __repr__(self):
        return self.__str__()
    def __str__(self):
        return "'{0}' on {1} [{2}]".format(str(self.lexeme), self.position, self.type)


# Classifica um token entre os tipos mais primários (incluindo TkPoint)
def tokenClassifier(lexeme, lastToken):
    global tkRules
    for (tkAlphabet, tkType) in tkRules:
        if lexeme in tkAlphabet:
            if tkType == "TkUnOp" and (lastToken.type == "TkNum" or lastToken.type == "TkVar"):
                continue
            else:
                return tkType

# Monta o Token e deixa em yield
def basicTokenize(content):
    lastToken = Token((0,0), "TkStart", "")
    for i, line in enumerate(content.split("\n")):
        for j, lexeme in enumerate(line):
            if lexeme == " ":
                continue
            if line[j:j+2] == "//":
                break
            position = (i + 1, j + 1)
            Assertions.assertSymbol(lexeme,position)
            lastToken = Token(position, tokenClassifier(lexeme,lastToken), lexeme)
            yield lastToken

# Faz o append do próximo Token em yield do gerador tkGenerator na tkList
def appendNextToken(tkGenerator, tkList):
    try:
        tkList.append(next(tkGenerator))
    except StopIteration:
        pass

# Monta os Tokens finais, juntando os TkNum com TkNum, TkVar com TkVar e TkPoint junto dos TkNum
def tokenize(content):
    basicTk = basicTokenize(content)
    tkCached = []
    while len(tkCached) < 5:
        appendNextToken(basicTk, tkCached)
    while len(tkCached) > 0:
        mainTk = tkCached.pop(0)
        appendNextToken(basicTk, tkCached)
        if mainTk.type == "TkPoint":
            mainTk.lexeme = "0."
            mainTk.type = "TkNum"
        if mainTk.type == "TkNum":
            while tkCached[0].type == "TkNum" or tkCached[0].type == "TkPoint":
                mainTk.lexeme += tkCached.pop(0).lexeme
                appendNextToken(basicTk, tkCached)
        elif mainTk.type == "TkVar":
            while tkCached[0].type == "TkVar":
                mainTk.lexeme += tkCached.pop(0).lexeme
                appendNextToken(basicTk, tkCached)

        Assertions.assertToken(mainTk)
        yield mainTk
