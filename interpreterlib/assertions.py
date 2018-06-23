# Eduardo Ferreira José, 2018
#
# - Arquivo Assertions.py
# Nesse arquivo vão estar as funções que irão detectar os possiveis erros que
# irão ocorrer durante a execução, através do assert.

from .alphabet import Alphabet

class Assertions:
    def assertParameters(parameters):
        try:
            assert len(parameters) == 2
        except AssertionError:
            print("\nstdin: Quantidade incorreta de parâmetros. Provavelmente você esqueceu de colocar o caminho para o arquivo ou colocou parâmetros além do necessário.")
            exit(-1)
    def assertSymbol(lexeme, position):
        try:
            assert lexeme in Alphabet.getAlphabet()
        except AssertionError:
            print("\nstdin: (Linha {1}, Coluna {2}) Simbolo {0} é desconhecido da linguagem.".format(lexeme, position[0], position[1]))
            exit(-1)

    def assertToken(tk):
        try:
            assert tk.lexeme[-1] != "."
        except AssertionError:
            print("\nstdin: (Linha {0}, Coluna {1}) Faltando número após o ponto no '{2}'.".format(tk.position[0], tk.position[1], tk.lexeme))
            exit(-1)

    def assertIO():
        print("\nstdin: Houve um problema ao abrir o arquivo.")
        exit(-1)

    def assertParentesis(parentesisPosition, tk):
        try:
            assert parentesisPosition is not None
        except AssertionError:
            print("\nstdin: (Linha {0}, Coluna {1}) O parentesis dessa posição não está sendo fechado.".format(tk.position[0], tk.position[1]))
            exit(-1)

    def assertSyntax(tokenList, tk):
        try:
            assert len(tokenList) > 0
        except AssertionError:
            print("\nstdin: (Linha {0}, Coluna {1}) Sintaxe inválida.".format(tk.position[0], tk.position[1]))
            exit(-1)

    def assertIsEmpty(tokenList, tk):
        try:
            assert len(tokenList) is 0
        except AssertionError:
            print("\nstdin: (Linha {0}, Coluna {1}) Sintaxe inválida.".format(tk.position[0], tk.position[1]))
            exit(-1)


    def assertSemicolon(semicolonPosition, tk):
        try:
            assert semicolonPosition is not None
        except AssertionError:
            print("\nstdin: (Linha {0}, Coluna {1}) Faltando ponto-e-vírgula no final do comando.".format(tk.position[0], tk.position[1]))
            exit(-1)

    def assertZeroDivision(number, tk):
        try:
            assert number is not 0
        except AssertionError:
            print("\nstdin: (Linha {0}, Coluna {1}) Tentativa de divisão por zero detectada.".format(tk.position[0], tk.position[1]))
            exit(-1)

    def assertUndeclaredVariable(variables, variable):
        try:
            variables[variable]
        except KeyError:
            print("\nstdin: Variavel {} sendo referenciada antes da sua declaração.".format(variable))
            exit(-1)

    def assertDeclaredVariable(variables, variable):
        try:
            variables[variable]
            print("\nstdin: Variavel {} com declaração duplicada.".format(variable))
            exit(-1)
        except KeyError:
            pass

    def assertKeyword(tk):
        try:
            assert tk.lexeme not in  ["-", "sqrt", "ceil", "floor", "cos", "sin"]
        except AssertionError:
            print("\nstdin: (Linha {0}, Coluna {1}) Uso da palavra-chave {2} para variável.".format(tk.position[0], tk.position[1], tk.lexeme))
            exit(-1)
            pass

    def assertConstant(variable):
        try:
            assert variable not in ["pi"]
        except AssertionError:
            print("\nstdin: Tentativa de mudança do valor de uma constante: {0}.".format(variable))
            exit(-1)
            pass
