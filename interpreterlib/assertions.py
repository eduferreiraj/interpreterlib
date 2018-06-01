# Eduardo Ferreira José, 2018
#
# - Arquivo Assertions.py
# Nesse arquivo vão estar as funções que irão detectar os possiveis erros que
# irão ocorrer durante a execução, através do assert.

from .alphabet import Alphabet

class Assertions:
    def assertParameters(parameters):
        assert len(parameters) == 2, "stdin: Quantidade incorreta de parâmetros. Provavelmente você esqueceu de colocar o caminho para o arquivo."

    def assertSymbol(lexeme, position):
        assert lexeme in Alphabet.getAlphabet(), "stdin: (Linha {1}, Coluna {2}) Simbolo {0} é desconhecido da linguagem.".format(lexeme, position[0], position[1])

    def assertToken(tk):
        assert tk.lexeme[-1] != ".", "stdin: (Linha {0}, Coluna {1}) Faltando número após o ponto no '{2}'.".format(tk.position[0], tk.position[1], tk.lexeme)
